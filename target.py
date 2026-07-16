"""Inspects a target host's OS/kernel and resolves it to a release-server distro directory name.

Matching strategy: try the explicit mapping table (distro_map.toml) first, since release-server
distro directory names are not consistently formatted (CentOS_7.3 vs OracleLinux7.5-Kern4.1 vs
UOS-Desktop-v20-Pro-Kern4.19). Only fall back to a heuristic substring match when no explicit
mapping exists, and never silently guess when the heuristic match is ambiguous.
"""

import argparse
import getpass
import logging
import os
import re
import shlex
import sys
from dataclasses import dataclass, field
from typing import Callable, Optional

import paramiko

import config
from csp import CSP_CUSTOMER_UNITNAME, CSPSAMGR
from release import ReleaseServer
from remote import RemoteHost, reboot_and_wait

logger = logging.getLogger(__name__)


@dataclass
class SystemInfo:
    os_name: str
    os_version: str
    kernel: str
    arch: str


@dataclass
class DistroMatch:
    distro: Optional[str]
    confidence: str  # "kernel" | "exact" | "heuristic" | "ambiguous" | "none"
    candidates: list = field(default_factory=list)  # other plausible matches, for "ambiguous"
    matched: Optional[object] = None  # the original candidate (str or dict) resolve_distro picked


class TargetInspector:
    """Collects OS/kernel/arch info from a target host over SSH."""

    def __init__(self, remote: RemoteHost):
        self.remote = remote

    def get_package_manager(self) -> Optional[str]:
        """Returns 'rpm' or 'dpkg' if qdocse is owned by either, or None if not installed.

        The dpkg status letters for every broken-but-present state are uppercase (U unpacked,
        F half-installed, H half-configured, W triggers-awaited; t triggers-pending is the one
        lowercase straggler) and all of them must count as installed: a package stranded
        half-configured by a failed prerm/postinst still has its files on disk, and reporting
        it "not installed" makes uninstall() skip the cleanup and install() stack a fresh
        dpkg -i on top of the wreckage. Only n (not-installed) and c (config-files-only,
        i.e. already removed) mean there is nothing to manage.
        """
        result = self.remote.run("rpm -q qdocse 2>&1 | grep -E '^qdocse-'")
        if result.ok and result.stdout.strip():
            return "rpm"
        result = self.remote.run(
            "dpkg-query -W -f='${db:Status-Abbrev}' qdocse 2>/dev/null"
            " | awk 'substr($0,2,1) ~ /[iUFHWt]/{print \"dpkg\"}'"
        )
        if result.ok and result.stdout.strip() == "dpkg":
            return "dpkg"
        return None

    def check_installed(self) -> tuple:
        """Returns (installed: bool, version: str|None, package_manager: 'rpm'|'dpkg'|None).

        version is just the version-release string (e.g. '3.2.0-1') for either package
        manager -- rpm's default `-q` output is the full NEVRA (name-version-release.arch,
        e.g. 'qdocse-3.2.0-1.x86_64'), so query just the fields that match dpkg's
        `${Version}` instead of the package name/arch too.
        """
        pm = self.get_package_manager()
        if pm is None:
            return False, None, None
        if pm == "rpm":
            result = self.remote.run("rpm -q qdocse --qf '%{VERSION}-%{RELEASE}' 2>/dev/null")
        else:
            result = self.remote.run("dpkg-query -W -f='${Version}' qdocse 2>/dev/null")
        return True, result.stdout.strip() or None, pm

    def verify_uninstalled(self) -> bool:
        """True if QDocSE is gone from both package managers and its service is not active."""
        installed, _, _ = self.check_installed()
        if installed:
            return False
        result = self.remote.run("systemctl is-active QDocSEService 2>&1")
        return result.stdout.strip() != "active"

    def get_qid(self) -> int:
        """Reads the installed QDocSE instance's unique ID from /qdoc/conf/qid.txt."""
        result = self.remote.run("cat /qdoc/conf/qid.txt")
        if not result.ok or not result.stdout.strip():
            raise RuntimeError(f"Could not read QID from {self.remote.host}: is QDocSE installed?")
        try:
            return int(result.stdout.strip())
        except ValueError:
            raise RuntimeError(
                f"Unexpected QID content on {self.remote.host}: {result.stdout.strip()!r}"
            )

    def get_system_info(self) -> SystemInfo:
        os_release = self.remote.run("cat /etc/os-release").stdout
        kernel = self.remote.run("uname -r").stdout.strip()
        arch = self.remote.run("uname -m").stdout.strip()

        fields = {}
        for line in os_release.splitlines():
            if "=" in line:
                key, _, value = line.partition("=")
                fields[key.strip()] = value.strip().strip('"')

        os_name = fields.get("NAME", "").strip()
        os_version = fields.get("VERSION_ID", "").strip()

        # RHEL-family distros report only the major version in VERSION_ID (e.g. "7");
        # /etc/redhat-release has the full minor version (e.g. "7.6.1810").
        if fields.get("ID_LIKE", "").find("rhel") != -1 or fields.get("ID", "") in ("centos", "rhel", "rocky"):
            redhat_release = self.remote.run("cat /etc/redhat-release").stdout.strip()
            match = re.search(r"release\s+(\d+\.\d+)", redhat_release)  # major.minor only, matches dir naming
            if match:
                os_version = match.group(1)

        return SystemInfo(os_name=os_name, os_version=os_version, kernel=kernel, arch=arch)


def apply_package(
    remote: RemoteHost,
    local_path: str,
    fresh_install: bool,
    on_progress: Optional[Callable[[str], None]] = None,
) -> bool:
    """Upload local_path to /tmp on remote and install or upgrade it.

    Detects installer type by magic bytes: '#!' → sh script, '!<arch>' → deb, else → rpm.
    Kept in var/downloads/ after install (not deleted) so the file is available for diagnostics.
    """
    with open(local_path, "rb") as _f:
        magic = _f.read(7)
    is_script = magic[:2] == b"#!"
    is_deb = not is_script and (local_path.endswith(".deb") or magic == b"!<arch>")
    remote_path = "/tmp/" + os.path.basename(local_path)
    remote.upload(local_path, remote_path)
    if is_script:
        install_cmd = f"sh {remote_path}"
    elif is_deb:
        install_cmd = f"dpkg -i {remote_path}"
    else:
        install_cmd = f"rpm -i {remote_path}" if fresh_install else f"rpm -U {remote_path}"
    result = remote.run(f"bash -lc {shlex.quote(install_cmd)}", timeout=2 * remote.command_timeout)
    if on_progress:
        for line in (result.stdout + result.stderr).strip().splitlines():
            on_progress(f"    {line}")
    return result.ok


def remove_package(
    remote: RemoteHost,
    package_manager: str,
    on_progress: Optional[Callable[[str], None]] = None,
) -> bool:
    """Stop QDocSEService then remove the qdocse package via rpm or dpkg.

    The service stop runs as its own SSH command -- finished and gone before the package
    manager starts. The rpm %preun/%postun scriptlets kill -9 every process whose command
    *line* matches 'QDocSEService' (a ps|egrep text match, not a process-name match), so a
    combined "systemctl stop QDocSEService ...; rpm -e qdocse" shell is itself a target:
    the scriptlet kills our own session mid-removal and the exit status reads SIGKILL
    instead of rpm's real result. `rpm -e qdocse` alone never matches -- the pattern is
    case-sensitive CamelCase. (The deb prerm uses `killall QDocSEService`, which matches by
    process name and never saw our shell; split all the same, for symmetry and defense.)
    """
    if package_manager not in ("rpm", "dpkg"):
        return False
    # Heavy operations (service stop, package scriptlets) get 2x the idle cap: a wedged
    # service alone can stall silently for systemd's default 90s stop timeout.
    remote.run("systemctl stop QDocSEService 2>/dev/null", timeout=2 * remote.command_timeout)
    if package_manager == "rpm":
        result = remote.run("rpm -e qdocse", timeout=2 * remote.command_timeout)
    else:
        result = remote.run("bash -lc 'dpkg -r qdocse'", timeout=2 * remote.command_timeout)
    if on_progress:
        for line in (result.stdout + result.stderr).strip().splitlines():
            on_progress(f"    {line}")
    return result.ok


def remove_package_skip_prerm(
    remote: RemoteHost,
    package_manager: str,
    on_progress: Optional[Callable[[str], None]] = None,
) -> bool:
    """Remove qdocse with its pre-removal script bypassed, for when that script itself is
    what refuses -- e.g. a panic-corrupted DB makes its license-mode check fail everything.
    The post-removal script, which does the actual cleanup, still runs.

    Only safe once nothing of QDocSE's is loaded or mounted (force_uninstall()'s post-reboot
    verification): the prerm's real duties (umounts, mode checks) are no-ops at that point.

    rpm keeps scriptlets in the rpmdb, so it takes the native --nopreun flag; dpkg has no
    such flag, but its maintainer scripts are plain files, so the prerm is backed up to
    /root/ and replaced with an exit-0 stub.
    """
    if package_manager == "rpm":
        result = remote.run("rpm -e --nopreun qdocse", timeout=2 * remote.command_timeout)
    elif package_manager == "dpkg":
        prerm = "/var/lib/dpkg/info/qdocse.prerm"
        remote.run(
            f"test -f /root/qdocse.prerm.orig || cp {prerm} /root/qdocse.prerm.orig; "
            f"printf '#!/bin/sh\\nexit 0\\n' > {prerm}"
        )
        result = remote.run("bash -lc 'dpkg -r qdocse'", timeout=2 * remote.command_timeout)
    else:
        return False
    if on_progress:
        for line in (result.stdout + result.stderr).strip().splitlines():
            on_progress(f"    {line}")
    return result.ok


# What the maintainer scripts would have cleaned up but remove_package_no_scripts() skips:
# postinst-copied units/modules and runtime-generated state, all outside the package's own
# file manifest. Deliberately a short fixed list -- if qdocse's install layout changes,
# update it here.
QDOCSE_RUNTIME_ARTIFACTS = [
    "/qdoc",
    "/lib/modules/*/qdocse",
    "/lib/systemd/system/QDocSEService.service",
    "/lib/systemd/system/qdocsesubagent.service",
    "/etc/modules-load.d/qdocse_modules.conf",
    "/etc/modules-load.d/qdocse_modules.conf.disabled-by-force-uninstall",
    "/usr/bin/QDocSEConsole",
]


def remove_package_no_scripts(
    remote: RemoteHost,
    package_manager: str,
    on_progress: Optional[Callable[[str], None]] = None,
) -> bool:
    """LAST RESORT removal that trusts nothing inside the package: every maintainer script
    is skipped and the package manager deletes the packaged files by its own manifest
    (rpm -e --noscripts / dpkg --purge with both scripts stubbed), then the runtime
    artifacts those scripts would have cleaned up (QDOCSE_RUNTIME_ARTIFACTS) are deleted
    by fixed path. Same precondition as remove_package_skip_prerm(): nothing loaded or
    mounted.
    """
    if package_manager == "rpm":
        result = remote.run("rpm -e --noscripts qdocse", timeout=2 * remote.command_timeout)
    elif package_manager == "dpkg":
        info = "/var/lib/dpkg/info/qdocse"
        remote.run(
            "for s in prerm postrm; do "
            f"if test -f {info}.$s; then "
            f"test -f /root/qdocse.$s.orig || cp {info}.$s /root/qdocse.$s.orig; "
            f"printf '#!/bin/sh\\nexit 0\\n' > {info}.$s; "
            "fi; done"
        )
        result = remote.run("bash -lc 'dpkg --purge qdocse'", timeout=2 * remote.command_timeout)
    else:
        return False
    if on_progress:
        for line in (result.stdout + result.stderr).strip().splitlines():
            on_progress(f"    {line}")
    if not result.ok:
        return False
    remote.run(f"rm -rf {' '.join(QDOCSE_RUNTIME_ARTIFACTS)}; systemctl daemon-reload", timeout=2 * remote.command_timeout)
    return True


def _normalize(s: str) -> str:
    return re.sub(r"[^a-z0-9.]", "", s.lower())


def _candidate_recency(candidate) -> int:
    if isinstance(candidate, dict):
        return candidate.get("updateTime", 0)
    return 0


def _candidate_text(candidate) -> str:
    """Returns the searchable text for a candidate: a release-server folder name (str) as-is,
    or a synthesized string from a CSP package record's osName/osVersion/osKernel fields."""
    if isinstance(candidate, str):
        return candidate
    return f"{candidate.get('osName', '')}{candidate.get('osVersion', '')}-Kern{candidate.get('osKernel', '')}"


def resolve_distro_by_kernel(kernel: str, kernel_map: dict) -> DistroMatch:
    """Resolve a target's exact `uname -r` against each candidate package's own compiled-for
    kernel version (see ReleaseServer.build_kernel_map()). This is authoritative rather than
    a guess -- it's the same uname -r check the package's own installer enforces -- so it
    sidesteps /etc/os-release naming-convention mismatches entirely (e.g. RHEL's NAME field
    is "Red Hat Enterprise Linux", which doesn't textually match a "RHEL8.3-..." folder name).
    Packages with no embedded kernel check (e.g. Windows .zip/.msi) have kernel_map[distro] is
    None and never match here.
    """
    matches = [distro for distro, pkg_kernel in kernel_map.items() if pkg_kernel is not None and pkg_kernel == kernel]
    if len(matches) == 1:
        return DistroMatch(distro=matches[0], confidence="kernel", matched=matches[0])
    if len(matches) > 1:
        logger.warning(f"Multiple distros' packages claim kernel '{kernel}': {sorted(matches)}")
        return DistroMatch(distro=None, confidence="ambiguous", candidates=matches)
    return DistroMatch(distro=None, confidence="none")


def resolve_package_from_csp(kernel: str, packages: list, pk_version: Optional[str] = None) -> DistroMatch:
    """Resolves a target directly against CSP's published package list by exact osKernel
    match, optionally narrowed to one pkVersion (a specific version/build).

    This is the production-facing counterpart to resolve_distro_by_kernel(): CSP is what
    targets actually install from (the release server is the internal build archive), and as
    of csp.py's upload_tagged_packages() tagging osKernel from the package's own install-script
    check (see release.extract_local_kernel_version()) rather than guessing it from the
    distro folder name, CSP's osKernel field is just as authoritative as probing the release
    server directly -- but reading it is one fast query instead of one SSH probe per distro.
    matched is the winning CSP package record (dict), for callers that need its "id".
    """
    candidates = [p for p in packages if p.get("osKernel") == kernel]
    if pk_version is not None:
        candidates = [p for p in candidates if p.get("pkVersion") == pk_version]

    if not candidates:
        return DistroMatch(distro=None, confidence="none")

    distinct_ids = {p["id"] for p in candidates}
    if len(distinct_ids) > 1:
        # info, not warning: find_package_from_csp usually resolves this by os-release name
        # (distros legitimately share upstream kernels); a real dead end surfaces to the
        # caller as confidence "ambiguous"/"none" anyway.
        logger.info(f"Multiple CSP packages claim kernel '{kernel}': {sorted(distinct_ids)}")
        return DistroMatch(distro=None, confidence="ambiguous", candidates=candidates)

    best = max(candidates, key=_candidate_recency)
    return DistroMatch(distro=best.get("osName"), confidence="kernel", matched=best)


def find_package_from_csp(
    target: RemoteHost,
    csp,
    version: str,
    build: str,
    distro_map: dict,
    build_packages: Optional[list] = None,
    info: Optional[SystemInfo] = None,
) -> tuple:
    """CSP-based counterpart to find_package_for_target(): resolves a target's package from
    CSP's published package list (scoped to this version/build) instead of probing the release
    server. Tries the exact kernel match first (resolve_package_from_csp); if several distros
    legitimately share one upstream kernel build (e.g. NeoKylin vs. CentOS on the same
    kernel-3.10.0-957.el7), disambiguates among those kernel-matched candidates by the host's
    os-release name; only a host whose kernel no package claims falls back to the full
    /etc/os-release naming heuristic (resolve_distro).

    build_packages, if given, is reused as-is (pre-filtered to this version/build and fetched
    once with csp.query_packages()) -- pass it in when resolving many targets against the same
    version/build, rather than re-querying CSP's full package list once per target. info, if
    given, likewise skips the SystemInfo probe.

    Returns (matched_package_dict_or_None, DistroMatch).
    """
    if info is None:
        info = TargetInspector(target).get_system_info()
    if build_packages is None:
        pk_version = f"{version}-{build}"
        build_packages = [p for p in csp.query_packages() if p.get("pkVersion") == pk_version]

    match = resolve_package_from_csp(info.kernel, build_packages)
    if match.confidence == "ambiguous":
        # Several distros claim this exact kernel: narrow those candidates by the host's
        # os-release name alone. Deliberately no version-string test -- version spelling is
        # exactly what differs across vendors (NeoKylin reports "V7Update6", the package
        # says "7.6") and the kernel match has already done the version's job.
        norm_name = _normalize(info.os_name.split()[0])
        narrowed = [c for c in match.candidates if norm_name in _normalize(_candidate_text(c))]
        if narrowed and len({_candidate_text(c) for c in narrowed}) == 1:
            best = max(narrowed, key=_candidate_recency)
            match = DistroMatch(distro=best.get("osName"), confidence="kernel", matched=best)
    if match.distro is None:
        # Name-heuristic fallback, minus any candidate compiled for a different kernel: these
        # are kernel modules, so a near-miss on the name must never install a package built
        # for another kernel. Prefix comparison (not equality) because some CSP records carry
        # a truncated tag ("3.10.0-957" for kernel 3.10.0-957.el7.x86_64); packages with no
        # osKernel tag at all stay eligible -- untagged records are who this fallback is for.
        compatible = [
            p for p in build_packages
            if not p.get("osKernel") or info.kernel.startswith(p["osKernel"])
        ]
        match = resolve_distro(info, compatible, distro_map)
    if match.matched is None:
        return None, match
    return match.matched, match


def resolve_distro(info: SystemInfo, available: list, distro_map: dict) -> DistroMatch:
    """Resolve a SystemInfo to one entry in available.

    available is either a list of release-server distro folder names (str), or a list of CSP
    package records (dict with osName/osVersion/osKernel). distro_map is keyed by
    "{os_name}|{os_version}" -> exact distro directory name (see config.load_distro_map());
    it only applies to the folder-name case. Falls back to a heuristic substring match,
    narrowed by kernel version, only when no explicit mapping exists.
    """
    map_key = f"{info.os_name}|{info.os_version}"
    if map_key in distro_map:
        target = distro_map[map_key]
        if target in available:
            return DistroMatch(distro=target, confidence="exact", matched=target)
        logger.error(f"Mapped distro '{target}' for '{map_key}' not found among available distros.")
        return DistroMatch(distro=None, confidence="none")

    # Use only the first word of os_name (e.g. "CentOS Linux" -> "CentOS"): release-server
    # directory names use the vendor's short name, not the full pretty name.
    norm_name = _normalize(info.os_name.split()[0])
    norm_version = _normalize(info.os_version)
    norm_kernel = _normalize(info.kernel.split("-")[0])  # major.minor.patch only

    candidates = [c for c in available if norm_name in _normalize(_candidate_text(c)) and norm_version in _normalize(_candidate_text(c))]

    if len(candidates) == 1:
        return DistroMatch(distro=_candidate_text(candidates[0]), confidence="heuristic", matched=candidates[0])

    if len(candidates) > 1:
        # Candidates that all share the same (osName, osVersion, osKernel) identity aren't really
        # ambiguous -- they're repeated uploads of the same distro (e.g. CSP's package list keeps
        # every historical upload). Pick the most recently updated one rather than bailing out.
        distinct = {_candidate_text(c) for c in candidates}
        if len(distinct) == 1:
            best = max(candidates, key=_candidate_recency)
            return DistroMatch(distro=_candidate_text(best), confidence="heuristic", matched=best)

        kernel_filtered = [c for c in candidates if norm_kernel and norm_kernel in _normalize(_candidate_text(c))]
        distinct_kernel = {_candidate_text(c) for c in kernel_filtered}
        if len(distinct_kernel) == 1 and kernel_filtered:
            best = max(kernel_filtered, key=_candidate_recency)
            return DistroMatch(distro=_candidate_text(best), confidence="heuristic", matched=best)

        logger.warning(f"Ambiguous distro match for '{map_key}': {sorted(distinct)}")
        return DistroMatch(distro=None, confidence="ambiguous", candidates=candidates)

    return DistroMatch(distro=None, confidence="none")


def find_package_for_target(
    target: RemoteHost,
    release: ReleaseServer,
    version: str,
    build: str,
    distro_map: dict,
    kernel_map: Optional[dict] = None,
    info: Optional[SystemInfo] = None,
) -> tuple:
    """Detects a target's OS and returns (remote_package_path, DistroMatch).

    Tries an exact kernel-version match first (see resolve_distro_by_kernel) and only falls
    back to the /etc/os-release naming heuristic if no package's compiled-for kernel matches.
    kernel_map, if given, is reused as-is (build it once with release.build_kernel_map()
    and pass it to every target sharing the same version/build, rather than re-probing every
    package's install script once per target). info, if given, skips the SystemInfo probe --
    pass it when the caller has already inspected the target (e.g. to print it).

    remote_package_path is None if no confident distro match was found; inspect the
    returned DistroMatch for "ambiguous"/"none" candidates to add an entry to distro_map.toml.
    """
    if info is None:
        info = TargetInspector(target).get_system_info()
    available = release.list_distros(version, build)
    if kernel_map is None:
        kernel_map = release.build_kernel_map(version, build, available)

    match = resolve_distro_by_kernel(info.kernel, kernel_map)
    if match.distro is None:
        match = resolve_distro(info, available, distro_map)
    if match.distro is None:
        return None, match
    return release.find_package(version, build, match.distro), match


def _target_defaults(host: str) -> dict:
    for target in config.load_targets():
        if target.get("host") == host:
            return target
    return {}


def _connect_kwargs(args: argparse.Namespace, defaults: dict, prefix: str) -> dict:
    """prefix is "" for commands that only ever connect to one host (dest/flag names
    unprefixed: --host/--port/...), or a real prefix (e.g. "target"/"rs") for commands that
    need to disambiguate two different hosts (dest names "{prefix}_host" etc., flags
    "--{prefix}-host" etc.).
    """
    dest = f"{prefix}_" if prefix else ""
    flag = f"{prefix}-" if prefix else ""
    host = getattr(args, f"{dest}host") or defaults.get("host")
    port = getattr(args, f"{dest}port") or defaults.get("port", 22)
    user = getattr(args, f"{dest}user") or defaults.get("user")
    key_file = getattr(args, f"{dest}key_file")
    password = getattr(args, f"{dest}password")
    if not host or not user:
        raise SystemExit(f"Missing --{flag}host/--{flag}user and no matching entry in targets.toml.")
    if password is None and key_file is None:
        password = defaults.get("password") or getpass.getpass(f"Password for {user}@{host}: ")
    return {"host": host, "port": port, "username": user, "password": password, "key_filename": key_file,
            "command_timeout": defaults.get("command_timeout")}


def _cmd_list(args: argparse.Namespace) -> int:
    for target in config.load_targets():
        print(f"{target['host']}: user={target.get('user')} port={target.get('port', 22)}")
    return 0


def _cmd_add(args: argparse.Namespace) -> int:
    try:
        config.add_target(args.host, port=args.port, user=args.user, password=args.password)
    except ValueError as e:
        logger.error(str(e))
        return 1
    return 0


def _cmd_remove(args: argparse.Namespace) -> int:
    try:
        config.remove_target(args.host)
    except ValueError as e:
        logger.error(str(e))
        return 1
    return 0



def _cmd_info(args: argparse.Namespace) -> int:
    target_kwargs = _connect_kwargs(args, _target_defaults(args.host), "")
    with RemoteHost(**target_kwargs) as target:
        info = TargetInspector(target).get_system_info()
    print(info)
    return 0


def _cmd_reboot(args: argparse.Namespace) -> int:
    target_kwargs = _connect_kwargs(args, _target_defaults(args.host), "")
    host = target_kwargs["host"]
    print(f"Rebooting {host}...")
    if reboot_and_wait(target_kwargs, on_progress=print):
        print(f"{host}: back online.")
        return 0
    print(f"{host}: did not come back online within the polling window.")
    return 1


def _cmd_match(args: argparse.Namespace) -> int:
    rs_defaults = config.load_release_server()
    target_kwargs = _connect_kwargs(args, _target_defaults(args.target_host), "target")
    rs_kwargs = _connect_kwargs(args, rs_defaults, "rs")
    base_path = args.rs_base_path or rs_defaults.get("base_path")
    if not base_path:
        raise SystemExit("Missing --rs-base-path and no base_path in release_server.toml.")

    distro_map = config.load_distro_map()
    with RemoteHost(**rs_kwargs) as rs_remote, RemoteHost(**target_kwargs) as target:
        rs = ReleaseServer(rs_remote, base_path=base_path)
        path, match = find_package_for_target(target, rs, args.version, args.build, distro_map)

    print(f"distro: {match.distro} (confidence: {match.confidence})")
    if match.candidates:
        print(f"candidates: {match.candidates}")
    if path is None:
        return 1
    print(f"package: {path}")
    return 0


def _cmd_download(args: argparse.Namespace) -> int:
    rs_defaults = config.load_release_server()
    rs_kwargs = _connect_kwargs(args, rs_defaults, "rs")
    base_path = args.rs_base_path or rs_defaults.get("base_path")
    if not base_path:
        raise SystemExit("Missing --rs-base-path and no base_path in release_server.toml.")
    distro_map = config.load_distro_map()

    if args.all:
        exit_code = 0
        with RemoteHost(**rs_kwargs) as rs_remote:
            rs = ReleaseServer(rs_remote, base_path=base_path)
            kernel_map = rs.build_kernel_map(args.version, args.build)
            for target_cfg in config.load_targets():
                host = target_cfg["host"]
                try:
                    with RemoteHost(
                        host=host,
                        port=target_cfg.get("port", 22),
                        username=target_cfg.get("user"),
                        password=target_cfg.get("password"),
                    ) as target:
                        _, match = find_package_for_target(
                            target, rs, args.version, args.build, distro_map, kernel_map=kernel_map
                        )
                        if match.distro is None:
                            print(f"{host}: no confident match (confidence={match.confidence})")
                            exit_code = 1
                            continue
                        local_path = rs.download_package(args.version, args.build, match.distro, args.local_dir)
                except (paramiko.SSHException, OSError) as e:
                    print(f"{host}: SSH connection failed: {e}")
                    exit_code = 1
                    continue
                print(f"{host}: {local_path}")
        return exit_code

    target_kwargs = _connect_kwargs(args, _target_defaults(args.target_host), "target")
    with RemoteHost(**rs_kwargs) as rs_remote, RemoteHost(**target_kwargs) as target:
        rs = ReleaseServer(rs_remote, base_path=base_path)
        _, match = find_package_for_target(target, rs, args.version, args.build, distro_map)
        if match.distro is None:
            logger.error(f"No confident distro match (confidence={match.confidence}, candidates={match.candidates})")
            return 1
        local_path = rs.download_package(args.version, args.build, match.distro, args.local_dir)

    print(local_path)
    return 0


def _cmd_csp_match(args: argparse.Namespace) -> int:
    target_kwargs = _connect_kwargs(args, _target_defaults(args.host), "")
    csp = CSPSAMGR()
    if not csp.login():
        return 1

    distro_map = config.load_distro_map()
    with RemoteHost(**target_kwargs) as target:
        pkg, match = find_package_from_csp(target, csp, args.version, args.build, distro_map)

    print(f"distro: {match.distro} (confidence: {match.confidence})")
    if match.candidates:
        print(f"candidates: {match.candidates}")
    if pkg is None:
        return 1
    print(f"package: id={pkg['id']} pkName={pkg['pkName']} pkVersion={pkg['pkVersion']}")
    return 0


def _cmd_csp_download(args: argparse.Namespace) -> int:
    csp = CSPSAMGR()
    if not csp.login():
        return 1
    distro_map = config.load_distro_map()

    owner = args.owner
    if owner is None:
        owner = csp.get_owner_id(args.domain or CSP_CUSTOMER_UNITNAME)
        if owner is None:
            return 1

    if args.all:
        pk_version = f"{args.version}-{args.build}"
        build_packages = [p for p in csp.query_packages() if p.get("pkVersion") == pk_version]

        exit_code = 0
        for target_cfg in config.load_targets():
            host = target_cfg["host"]
            try:
                with RemoteHost(
                    host=host,
                    port=target_cfg.get("port", 22),
                    username=target_cfg.get("user"),
                    password=target_cfg.get("password"),
                ) as target:
                    pkg, match = find_package_from_csp(
                        target, csp, args.version, args.build, distro_map, build_packages=build_packages
                    )
                    if pkg is None:
                        print(f"{host}: no confident CSP package match (confidence={match.confidence})")
                        exit_code = 1
                        continue
                    local_path = csp.download_package(
                        pkg["id"], os.path.join(args.local_dir, args.version, args.build), owner=owner
                    )
                    if args.stage:
                        remote_path = args.remote_dir.rstrip("/") + "/" + os.path.basename(local_path)
                        target.upload(local_path, remote_path)
                        local_path = remote_path
            except (paramiko.SSHException, OSError) as e:
                print(f"{host}: SSH connection failed: {e}")
                exit_code = 1
                continue
            print(f"{host}: {local_path}")
        return exit_code

    target_kwargs = _connect_kwargs(args, _target_defaults(args.host), "")
    with RemoteHost(**target_kwargs) as target:
        pkg, match = find_package_from_csp(target, csp, args.version, args.build, distro_map)
        if pkg is None:
            logger.error(f"No confident CSP package match (confidence={match.confidence}, candidates={match.candidates})")
            return 1

        local_path = csp.download_package(
            pkg["id"], os.path.join(args.local_dir, args.version, args.build), owner=owner
        )
        if local_path is None:
            return 1

        if not args.stage:
            print(local_path)
            return 0

        # --stage reuses the same connection find_package_from_csp() already opened to
        # inspect the target, instead of reconnecting -- stops short of installing (that's
        # lifecycle.py's job); just uploads the file so it's ready for a manual install.
        remote_path = args.remote_dir.rstrip("/") + "/" + os.path.basename(local_path)
        target.upload(local_path, remote_path)
        print(remote_path)
    return 0


def _add_connection_args(parser: argparse.ArgumentParser, prefix: str, label: str) -> None:
    """prefix is "" for commands that only ever connect to one host -- plain --host/--port/...
    -- or a real prefix (e.g. "target"/"rs") for commands needing to disambiguate two
    different hosts (--target-host/--rs-host etc; see match/download, which take both).
    """
    dest = f"{prefix}_" if prefix else ""
    flag = f"{prefix}-" if prefix else ""
    parser.add_argument(f"--{flag}host", dest=f"{dest}host", help=f"{label} hostname or IP.")
    parser.add_argument(f"--{flag}port", dest=f"{dest}port", type=int, help=f"{label} SSH port (default: 22).")
    parser.add_argument(f"--{flag}user", dest=f"{dest}user", help=f"{label} SSH username.")
    auth = parser.add_mutually_exclusive_group()
    auth.add_argument(f"--{flag}password", dest=f"{dest}password", help=f"{label} SSH password.")
    auth.add_argument(f"--{flag}key-file", dest=f"{dest}key_file", help=f"{label} SSH private key file.")


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Detect a target's OS/distro and resolve it to a release-server package."
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Show full SSH/SFTP debug output (quiet by default)."
    )
    subparsers = parser.add_subparsers(dest="command")
    parser.set_defaults(func=lambda args: (parser.print_help(), 1)[1])

    subparsers.add_parser("list", help="List all targets in targets.toml.").set_defaults(func=_cmd_list)

    add = subparsers.add_parser("add", help="Add a target to targets.toml.")
    add.add_argument("--host", required=True, help="Target hostname or IP.")
    add.add_argument("--port", type=int, help="SSH port (default: inherited from [defaults]).")
    add.add_argument("--user", help="SSH username (default: inherited from [defaults]).")
    add.add_argument("--password", help="SSH password, stored in secrets.toml under a new secret_ref.")
    add.set_defaults(func=_cmd_add)

    remove = subparsers.add_parser("remove", help="Remove a target from targets.toml.")
    remove.add_argument("--host", required=True, help="Target hostname or IP to remove.")
    remove.set_defaults(func=_cmd_remove)

    info = subparsers.add_parser("info", help="Print the target's detected OS/kernel info.")
    _add_connection_args(info, "", "Target host")
    info.set_defaults(func=_cmd_info)

    reboot = subparsers.add_parser("reboot", help="Reboot the target and wait until SSH comes back.")
    _add_connection_args(reboot, "", "Target host")
    reboot.set_defaults(func=_cmd_reboot)

    match = subparsers.add_parser("match", help="Resolve the target's distro and find its release package.")
    _add_connection_args(match, "target", "Target host")
    _add_connection_args(match, "rs", "Release server")
    match.add_argument("--rs-base-path", help="Release archive base path (default: from release_server.toml).")
    match.add_argument("--version", required=True, help="Release version (e.g. 3.2.0).")
    match.add_argument("--build", required=True, help="Build number.")
    match.set_defaults(func=_cmd_match)

    download = subparsers.add_parser(
        "download",
        help="Resolve and download the package matching the target (--all: every target in targets.toml).",
    )
    _add_connection_args(download, "target", "Target host")
    _add_connection_args(download, "rs", "Release server")
    download.add_argument("--rs-base-path", help="Release archive base path (default: from release_server.toml).")
    download.add_argument("--version", required=True, help="Release version (e.g. 3.2.0).")
    download.add_argument("--build", required=True, help="Build number.")
    download.add_argument(
        "--local-dir", default=config.DEFAULT_DOWNLOAD_DIR,
        help="Local directory to download into (default: var/downloads/release).",
    )
    download.add_argument(
        "--all", action="store_true", help="Every target in targets.toml instead of one (--target-host is ignored)."
    )
    download.set_defaults(func=_cmd_download)

    csp = subparsers.add_parser("csp", help="Resolve/download the target's matching package from CSP (not the release server).")
    csp_sub = csp.add_subparsers(dest="csp_command")
    csp.set_defaults(func=lambda args: (csp.print_help(), 1)[1])

    csp_match = csp_sub.add_parser(
        "match", help="Resolve the target's package directly against CSP's published package list."
    )
    _add_connection_args(csp_match, "", "Target host")
    csp_match.add_argument("--version", required=True, help="Release version (e.g. 3.2.0).")
    csp_match.add_argument("--build", required=True, help="Build number.")
    csp_match.set_defaults(func=_cmd_csp_match)

    csp_download = csp_sub.add_parser(
        "download",
        help="Resolve and download the target's matching package from CSP "
        "(--all: every target in targets.toml).",
    )
    _add_connection_args(csp_download, "", "Target host")
    csp_download.add_argument("--version", required=True, help="Release version (e.g. 3.2.0).")
    csp_download.add_argument("--build", required=True, help="Build number.")
    csp_download.add_argument(
        "--local-dir", default=config.CSP_DOWNLOAD_DIR,
        help="Local directory to download into (default: var/downloads/csp).",
    )
    csp_download.add_argument("--owner", type=int, help="Owner id (default: resolved from --domain).")
    csp_download.add_argument(
        "--domain", help="Customer unitname to resolve the owner id from (default: csp.toml's customer.unitname)."
    )
    csp_download.add_argument(
        "--all", action="store_true", help="Every target in targets.toml instead of one (--host is ignored)."
    )
    csp_download.add_argument(
        "--stage", action="store_true",
        help="Also upload the downloaded file to the target (--remote-dir) -- stages it for a "
        "manual install; does not install it (that's lifecycle.py's job). Works with --all too.",
    )
    csp_download.add_argument(
        "--remote-dir", default="/tmp", help="With --stage: remote directory to upload into (default: /tmp)."
    )
    csp_download.set_defaults(func=_cmd_csp_download)

    return parser


def main(argv: Optional[list] = None) -> int:
    args = build_arg_parser().parse_args(argv)
    config.configure_logging(args.verbose)
    try:
        return args.func(args)
    except (paramiko.SSHException, OSError) as e:
        logger.error(f"SSH connection failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
