"""Lifecycle orchestrator: install / uninstall / upgrade / reinstall / activate QDocSE.

Each public function composes calls to the modules that own the details:
  target.py  — OS inspection, package-manager detection, apply/remove packages
  console.py — QDocSEConsole commands (mode, install_prep, finalize, elevate)
  csp.py     — CSP customer portal (activation) and SAMGR (package download)
  remote.py  — SSH connections, reboot_and_wait

Per-host state persistence (survives a target reboot) and license .dat generation are this
module's own concern, not a separate module's -- lifecycle.py is their only caller, so there
was no reason for them to live anywhere else (see DESIGN.md SS10.1).

No rpm/dpkg/QDocSEConsole command strings live here. See DESIGN.md SS5.1.
"""

import argparse
import getpass
import json
import logging
import os
import sys
import tempfile
import threading
import time
from typing import Callable, Optional

import paramiko

import config
import console
from csp import CSP_CUSTOMER_UNITNAME, CSPCustomer, CSPSAMGR
from helpers.codec import LicInfo, LicKind, encode, encode_to_file
from release import ReleaseServer
from remote import RemoteHost, reboot_and_wait
from target import (
    TargetInspector,
    apply_package,
    find_package_for_target,
    find_package_from_csp,
    remove_package,
    remove_package_no_scripts,
    remove_package_skip_prerm,
)

logger = logging.getLogger(__name__)

STATE_DIR = os.path.join(config.VAR_DIR, "state")


def _state_path(host: str) -> str:
    return os.path.join(STATE_DIR, f"{host}.json")


def _save_state(host: str, data: dict) -> None:
    os.makedirs(STATE_DIR, exist_ok=True)
    with open(_state_path(host), "w") as f:
        json.dump(data, f)


def _load_state(host: str) -> Optional[dict]:
    path = _state_path(host)
    if not os.path.isfile(path):
        return None
    with open(path) as f:
        return json.load(f)


def _clear_state(host: str) -> None:
    path = _state_path(host)
    if os.path.isfile(path):
        os.remove(path)


def _build_lic_info(kind: LicKind, qid: int, duration: int, mode: int, foot_print: Optional[str]) -> LicInfo:
    return LicInfo(
        kind=kind, qid=qid,
        foot_print=foot_print or str(int(time.time() * 1000)),
        duration=duration, mode=mode,
    )


def _generate_license_bytes(
    kind: LicKind, qid: int, duration: int = 2_678_400, mode: int = 5, foot_print: Optional[str] = None,
) -> bytes:
    """Encodes a license .dat in memory -- for callers that take raw bytes directly (e.g.
    CSP's activate_device()), no file/upload involved."""
    return encode(_build_lic_info(kind, qid, duration, mode, foot_print))


def _generate_license_file(
    kind: LicKind, qid: int, duration: int = 2_678_400, mode: int = 5, foot_print: Optional[str] = None,
) -> str:
    """Encodes a license .dat to a local temp file and returns its path. Caller is
    responsible for uploading it (via remote.RemoteHost) and deleting the local temp file
    afterward."""
    tmp = tempfile.NamedTemporaryFile(suffix=".dat", delete=False)
    tmp.close()
    encode_to_file(_build_lic_info(kind, qid, duration, mode, foot_print), tmp.name)
    return tmp.name


def _log(msg: str, on_progress: Optional[Callable[[str], None]] = None) -> None:
    logger.info(msg)
    if on_progress:
        on_progress(msg)


def _local_elevate(remote: RemoteHost, duration: str, mode: int = 5) -> dict:
    """Generates an elevation file locally (qid = the device's real qid, same as
    activate() -- unlike renew(), elevation has no separate challenge/request step)
    and applies it. Returns console.elevate()'s result dict."""
    qid = TargetInspector(remote).get_qid()
    local_path = _generate_license_file(LicKind.ELEVATION, qid, mode=mode)
    try:
        remote_path = f"/tmp/qdocse_elevate_{qid}.dat"
        remote.upload(local_path, remote_path)
    finally:
        os.unlink(local_path)
    return console.elevate(remote, remote_path, duration)


def _elevate_if_needed(
    host: str,
    remote: RemoteHost,
    mode: str,
    elevation_file: Optional[str],
    elevation_duration: str,
    operation: str,
    on_progress: Optional[Callable[[str], None]] = None,
) -> None:
    """Moves De-elevated -> Elevated before operation; no-op otherwise.
    Uses elevation_file if given (an externally-supplied elevation file), otherwise
    generates one locally (see elevate()/_local_elevate()).
    """
    if mode != "de-elevated":
        return
    if elevation_file:
        _log(f"{host}: De-elevated — uploading and applying elevation file...", on_progress)
        remote_elev = f"/tmp/qdocse_elev_{os.path.basename(elevation_file)}"
        remote.upload(elevation_file, remote_elev)
        data = console.elevate(remote, remote_elev, elevation_duration)
    else:
        _log(f"{host}: De-elevated — generating elevation file locally...", on_progress)
        data = _local_elevate(remote, elevation_duration)
    if not data["elevated"]:
        raise RuntimeError(f"Elevation failed on {host}: {data.get('error')}")
    _log(f"{host}: now Elevated.", on_progress)


def resolve_build(
    version: str,
    build: str,
    source: str = "csp",
    on_progress: Optional[Callable[[str], None]] = None,
) -> str:
    """Resolve a --build value to a concrete build number: 'latest' queries the given
    source (CSP's pkVersion tags, or the release server's build listing) for the newest
    build of version; anything else passes through unchanged. Raises RuntimeError if
    'latest' finds no build at all. Also used by fleet.py, which resolves once up front
    so every host in one run gets the same build.
    """
    if build != "latest":
        return build

    if source == "csp":
        csp = CSPSAMGR()
        if not csp.login():
            raise RuntimeError("CSP SAMGR login failed.")
        resolved = csp.latest_build(version)
    elif source == "release":
        rs_cfg = config.load_release_server()
        with RemoteHost(
            host=rs_cfg["host"],
            port=rs_cfg.get("port", 22),
            username=rs_cfg["user"],
            password=rs_cfg.get("password"),
        ) as rs_remote:
            builds = ReleaseServer(rs_remote, base_path=rs_cfg["base_path"]).list_builds(version)
            resolved = builds[-1] if builds else None
    else:
        raise ValueError(f"Unknown source '{source}', expected 'csp' or 'release'.")

    if resolved is None:
        raise RuntimeError(f"--build latest: no builds found on {source} for version {version}.")
    _log(f"--build latest -> {resolved} (newest build on {source} for version {version})", on_progress)
    return resolved


# Parallel fleet runs (fleet.py -j/--jobs) hit the shared local download cache from
# several threads at once, and neither downloader is re-entrant: csp.download_package()
# truncate-writes its destination and release's download_package() rmtree's the whole
# dest dir -- either one corrupts a file another host is still SFTP-uploading from.
# _download_once() makes each distinct package download exactly once per process (keyed
# per package, so different packages still download in parallel) and hands every later
# requester the already-downloaded path.
_download_cache: dict = {}
_download_locks: dict = {}
_download_guard = threading.Lock()


def _download_once(key: tuple, fetch: Callable[[], str]) -> str:
    with _download_guard:
        lock = _download_locks.setdefault(key, threading.Lock())
    with lock:
        path = _download_cache.get(key)
        if path and os.path.exists(path):
            return path
        path = fetch()
        _download_cache[key] = path
        return path


def _resolve_and_download(
    remote: RemoteHost,
    version: str,
    build: str,
    source: str,
    local_dir: Optional[str],
    domain: Optional[str],
    on_progress: Optional[Callable[[str], None]] = None,
) -> str:
    """Resolve the package matching remote's platform and download it locally.
    Returns the local file path. Shared by install() and upgrade().

    local_dir=None picks the per-source default: the release cache tree for
    source="release", the separate CSP re-download tree for source="csp" (CSP filenames
    are pk_names, not cache-layout entries -- see config.CSP_DOWNLOAD_DIR).
    """
    _log(f"    Resolving package (source={source})...", on_progress)
    # The Target/Matched pair lets the operator eyeball host-vs-package consistency
    # (distro and compiled-for kernel) right where the install decision is made.
    info = TargetInspector(remote).get_system_info()
    _log(f"    Target:  {info.os_name} {info.os_version}, kernel {info.kernel} ({info.arch})", on_progress)

    if source == "csp":
        csp = CSPSAMGR()
        if not csp.login():
            raise RuntimeError("CSP SAMGR login failed.")
        distro_map = config.load_distro_map()
        pkg, match = find_package_from_csp(remote, csp, version, build, distro_map, info=info)
        if pkg is None:
            raise RuntimeError(f"No confident CSP package match (confidence={match.confidence}).")
        _log(
            f"    Matched: {pkg.get('osVersion')} (kernel {pkg.get('osKernel') or 'untagged'}, "
            f"confidence: {match.confidence})",
            on_progress,
        )
        owner = csp.get_owner_id(domain or CSP_CUSTOMER_UNITNAME)
        if owner is None:
            raise RuntimeError("Failed to resolve CSP owner id.")
        # Per-package-id subdir: CSP packages for different distros can share a filename
        # (only arch varies), so a flat {version}/{build}/ would collide when a parallel
        # run downloads packages for two distros at once.
        dest_dir = os.path.join(local_dir or config.CSP_DOWNLOAD_DIR, version, build, str(pkg["id"]))

        def fetch() -> str:
            local_path = csp.download_package(pkg["id"], dest_dir, owner=owner)
            if local_path is None:
                raise RuntimeError(f"Failed to download package id={pkg['id']} from CSP.")
            return local_path

        return _download_once(("csp", pkg["id"], dest_dir), fetch)

    if source == "release":
        rs_cfg = config.load_release_server()
        with RemoteHost(
            host=rs_cfg["host"],
            port=rs_cfg.get("port", 22),
            username=rs_cfg["user"],
            password=rs_cfg.get("password"),
        ) as rs_remote:
            rs = ReleaseServer(rs_remote, base_path=rs_cfg["base_path"])
            distro_map = config.load_distro_map()
            _, match = find_package_for_target(remote, rs, version, build, distro_map, info=info)
            if match.distro is None:
                raise RuntimeError(
                    f"No confident release-server distro match (confidence={match.confidence})."
                )
            _log(f"    Matched: {match.distro} (confidence: {match.confidence})", on_progress)
            base_dir = local_dir or config.DEFAULT_DOWNLOAD_DIR
            return _download_once(
                ("release", version, build, match.distro, base_dir),
                lambda: rs.download_package(version, build, match.distro, base_dir),
            )

    raise ValueError(f"Unknown source '{source}', expected 'csp' or 'release'.")


def install(
    connect_kwargs: dict,
    version: str,
    build: str,
    source: str = "csp",
    local_dir: Optional[str] = None,
    domain: Optional[str] = None,
    on_progress: Optional[Callable[[str], None]] = None,
) -> bool:
    """Install QDocSE on a target with nothing currently installed."""
    with RemoteHost(**connect_kwargs) as remote:
        ti = TargetInspector(remote)
        installed, existing_version, _ = ti.check_installed()
        if installed:
            _log(f"QDocSE already installed: {existing_version}", on_progress)
            return True

        local_path = _resolve_and_download(remote, version, build, source, local_dir, domain, on_progress)
        _log(f"Installing {os.path.basename(local_path)}...", on_progress)
        if not apply_package(remote, local_path, fresh_install=True, on_progress=on_progress):
            raise RuntimeError(f"Install failed on {connect_kwargs['host']}.")

        installed, _, _ = ti.check_installed()
        if not installed:
            # A bare False here surfaces as an unexplained FAILED in fleet output; say what
            # actually happened: the installer exited 0, yet the package manager doesn't
            # report qdocse installed afterwards.
            raise RuntimeError(
                f"{connect_kwargs['host']}: installer reported success but qdocse is not "
                "registered as installed afterwards -- check the package state on the target."
            )
        return True


def _deregister_from_csp(host: str, qid: Optional[int], on_progress: Optional[Callable[[str], None]] = None) -> None:
    """Best-effort cleanup: delete this device's CSP customer record so a future
    reinstall (which mints a new qid) doesn't leave today's qid orphaned in CSP.
    Never raises -- a CSP lookup failure shouldn't turn a successful uninstall into
    a reported failure.
    """
    if qid is None:
        return
    try:
        csp = CSPCustomer()
        if not csp.login():
            return
        devices = csp.get_device_list()
        device = next((d for d in devices if str(d.get("qid")) == str(qid)), None)
        if device is None:
            return
        if csp.delete_device(device["id"]):
            _log(f"{host}: removed stale CSP device record (qid={qid}, id={device['id']}).", on_progress)
    except Exception as e:
        logger.warning(f"{host}: could not clean up CSP device record for qid={qid}: {e}")


def uninstall(
    connect_kwargs: dict,
    elevation_file: Optional[str] = None,
    elevation_duration: str = "1h",
    on_progress: Optional[Callable[[str], None]] = None,
) -> bool:
    """Mode-aware uninstall:
        unlicensed         → remove directly, no reboot needed.
        de-elevated        → elevate first, then install_prep → reboot → remove.
        elevated/learning  → install_prep → reboot → remove.

    On success, also deletes the device's CSP customer record (best-effort) so a
    later reinstall's new qid doesn't leave this one behind as an orphaned duplicate.
    """
    host = connect_kwargs["host"]

    state = _load_state(host)
    if state and state.get("operation") == "uninstall" and state.get("phase") == "post_reboot":
        _log(f"[resume] {host}: finishing uninstall after reboot...", on_progress)
        with RemoteHost(**connect_kwargs) as remote:
            ti = TargetInspector(remote)
            try:
                qid = ti.get_qid()
            except RuntimeError:
                qid = None
            ok = remove_package(remote, state["package_manager"], on_progress=on_progress)
            verified = ok and ti.verify_uninstalled()
        _clear_state(host)
        if verified:
            _deregister_from_csp(host, qid, on_progress)
        return verified

    with RemoteHost(**connect_kwargs) as remote:
        ti = TargetInspector(remote)
        installed, _, package_manager = ti.check_installed()
        if not installed:
            _log(f"{host}: QDocSE is not installed.", on_progress)
            return True

        try:
            qid = ti.get_qid()
        except RuntimeError:
            qid = None

        mode = console.show_mode(remote)
        _log(f"{host}: current mode is '{mode}'.", on_progress)

        if mode == "unlicensed":
            _log(f"{host}: Unlicensed — removing directly, no reboot needed.", on_progress)
            ok = remove_package(remote, package_manager, on_progress=on_progress)
            verified = ok and ti.verify_uninstalled()
            if verified:
                _deregister_from_csp(host, qid, on_progress)
            return verified

        if mode not in ("elevated", "learning", "de-elevated"):
            raise RuntimeError(
                f"Cannot determine how to uninstall: {host} reported mode '{mode}'. "
                "Check that QDocSEConsole is accessible on the target."
            )

        _elevate_if_needed(host, remote, mode, elevation_file, elevation_duration, "uninstall", on_progress)

        _log(f"{host}: running install_prep (marks system for uninstall)...", on_progress)
        data = console.install_prep(remote, "on")
        if not data["ok"]:
            raise RuntimeError(f"install_prep failed on {host}: {data.get('error')}")

        _save_state(host, {"operation": "uninstall", "phase": "post_reboot", "package_manager": package_manager})

    _log(f"{host}: rebooting...", on_progress)
    try:
        if not reboot_and_wait(connect_kwargs, on_progress=on_progress):
            raise RuntimeError(f"{host} did not come back online after reboot.")
        _log(f"{host}: back online.", on_progress)
        with RemoteHost(**connect_kwargs) as remote:
            _log(f"{host}: removing package ({package_manager})...", on_progress)
            ok = remove_package(remote, package_manager, on_progress=on_progress)
            verified = ok and TargetInspector(remote).verify_uninstalled()
    finally:
        _clear_state(host)
    if verified:
        _deregister_from_csp(host, qid, on_progress)
    return verified


def upgrade(
    connect_kwargs: dict,
    version: str,
    build: str,
    source: str = "csp",
    local_dir: Optional[str] = None,
    domain: Optional[str] = None,
    elevation_file: Optional[str] = None,
    elevation_duration: str = "1d",
    on_progress: Optional[Callable[[str], None]] = None,
) -> bool:
    """Mode-aware upgrade.

    unlicensed:        remove then fresh install (preinst blocks in-place upgrade when unlicensed).
    de-elevated:       elevate first, then install_prep → reboot → rpm -U/dpkg -i → finalize.
    elevated/learning: install_prep → reboot → rpm -U/dpkg -i → finalize.
    """
    host = connect_kwargs["host"]

    state = _load_state(host)
    if state and state.get("operation") == "upgrade" and state.get("phase") == "post_reboot":
        _log(f"[resume] {host}: finishing upgrade after reboot...", on_progress)
        local_path = state["local_path"]
        try:
            with RemoteHost(**connect_kwargs) as remote:
                ok = apply_package(remote, local_path, fresh_install=False, on_progress=on_progress)
                if ok:
                    result = console.finalize(remote)
                    if not result.get("ok"):
                        raise RuntimeError(f"finalize failed on {host}: {result.get('error')}")
        finally:
            _clear_state(host)
        return ok

    with RemoteHost(**connect_kwargs) as remote:
        ti = TargetInspector(remote)
        installed, _, package_manager = ti.check_installed()
        if not installed:
            raise RuntimeError(f"QDocSE is not installed on {host}; use install(), not upgrade().")

        mode = console.show_mode(remote)
        _log(f"{host}: current mode is '{mode}'.", on_progress)

        if mode == "unlicensed":
            local_path = _resolve_and_download(remote, version, build, source, local_dir, domain, on_progress)
            _log(f"{host}: Unlicensed — removing current package before fresh install...", on_progress)
            if not remove_package(remote, package_manager, on_progress=on_progress):
                raise RuntimeError(f"Failed to remove existing package on {host} before upgrade.")
            _log(f"{host}: Installing new package...", on_progress)
            return apply_package(remote, local_path, fresh_install=True, on_progress=on_progress)

        if mode not in ("elevated", "learning", "de-elevated"):
            raise RuntimeError(
                f"Cannot upgrade: {host} reported mode '{mode}'. "
                "Expected unlicensed, de-elevated (with --elevation-file), elevated, or learning."
            )

        _elevate_if_needed(host, remote, mode, elevation_file, elevation_duration, "upgrade", on_progress)

        local_path = _resolve_and_download(remote, version, build, source, local_dir, domain, on_progress)

        _log(f"{host}: running install_prep (marks system for upgrade)...", on_progress)
        data = console.install_prep(remote, "on")
        if not data["ok"]:
            raise RuntimeError(f"install_prep failed on {host}: {data.get('error')}")

        _save_state(host, {"operation": "upgrade", "phase": "post_reboot", "local_path": local_path})

    _log(f"{host}: rebooting...", on_progress)
    try:
        if not reboot_and_wait(connect_kwargs, on_progress=on_progress):
            raise RuntimeError(f"{host} did not come back online after reboot.")
        _log(f"{host}: back online.", on_progress)
        with RemoteHost(**connect_kwargs) as remote:
            _log(f"{host}: applying upgrade...", on_progress)
            ok = apply_package(remote, local_path, fresh_install=False, on_progress=on_progress)
            if ok:
                result = console.finalize(remote)
                if not result.get("ok"):
                    raise RuntimeError(f"finalize failed on {host}: {result.get('error')}")
    finally:
        _clear_state(host)
    return ok


def activate(
    connect_kwargs: dict,
    duration: int = 2_678_400,
    mode: int = 5,
    on_progress: Optional[Callable[[str], None]] = None,
) -> bool:
    """Read QID from target, find its device on CSP customer, generate and send activation.

    Skips if the device is already activated and the license has not yet expired.
    """
    host = connect_kwargs["host"]

    _log(f"[1] Reading QID from {host}...", on_progress)
    with RemoteHost(**connect_kwargs) as remote:
        qid = TargetInspector(remote).get_qid()
    _log(f"    qid={qid}", on_progress)

    _log("[2] Looking up device on CSP customer portal...", on_progress)
    csp = CSPCustomer()
    if not csp.login():
        raise RuntimeError("CSP customer login failed.")
    devices = csp.get_device_list()
    device = next((d for d in devices if str(d.get("qid")) == str(qid)), None)
    if device is None:
        raise RuntimeError(f"No CSP device found with qid={qid}. Has the target checked in yet?")
    device_id = device["id"]
    _log(
        f"    device id={device_id}, type={device.get('type')}, expireTime={device.get('expireTime')}",
        on_progress,
    )

    now_ms = int(time.time() * 1000)
    if device.get("expireTime", 0) > now_ms:
        _log("    Already activated and not yet expired — skipping.", on_progress)
        return True

    _log("[3] Generating activation file...", on_progress)
    dat = _generate_license_bytes(LicKind.ACTIVATION, qid, duration=duration, mode=mode)

    _log(f"[4] Activating device id={device_id} on CSP...", on_progress)
    ok = csp.activate_device(dat, device_id)

    if not ok:
        raise RuntimeError(f"CSP activation failed for device id={device_id}.")
    _log("    Done.", on_progress)
    return True


def renew(
    connect_kwargs: dict,
    duration: int = 2_678_400,
    mode: int = 5,
    on_progress: Optional[Callable[[str], None]] = None,
) -> bool:
    """Renew an expired/expiring license entirely locally -- no CSP involved.

    QDocSEConsole -c renewrequest -> local .dat (encoded with the pending REQUEST NUMBER
    as qid, NOT the device's real qid -- confirmed against a real QDocSEConsole; see
    helpers/codec.py's LicKind.RENEWAL docstring) -> QDocSEConsole -c renewcommit.

    Use this instead of activate() when a device already has license history (activate()
    is only for a device's first-ever license) and isn't CSP-managed, or CSP hasn't
    picked up its renewal yet.
    """
    host = connect_kwargs["host"]

    with RemoteHost(**connect_kwargs) as remote:
        _log(f"[1] Requesting a renewal challenge from {host}...", on_progress)
        req = console.renewrequest(remote)
        if not req["ok"]:
            raise RuntimeError(f"renewrequest failed on {host}: {req.get('error')}")
        request_number = req["request_number"]
        _log(f"    request_number={request_number}", on_progress)

        _log("[2] Generating renewal file locally...", on_progress)
        local_path = _generate_license_file(LicKind.RENEWAL, request_number, duration=duration, mode=mode)
        try:
            remote_path = f"/tmp/qdocse_renew_{request_number}.dat"
            remote.upload(local_path, remote_path)
        finally:
            os.unlink(local_path)

        _log("[3] Applying renewal...", on_progress)
        result = console.renewcommit(remote, remote_path)
        if not result["ok"]:
            raise RuntimeError(f"renewcommit failed on {host}: {result.get('error')}")

        mode_after = console.show_mode(remote)
        _log(f"    mode now: {mode_after}", on_progress)

    return mode_after != "unlicensed"


def elevate(
    connect_kwargs: dict,
    duration: str = "1h",
    mode: int = 5,
    on_progress: Optional[Callable[[str], None]] = None,
) -> bool:
    """Move a De-elevated device to Elevated, generating the elevation file locally
    (see _local_elevate()). No CSP involved. No-op (returns True) if already Elevated
    or Learning.
    """
    host = connect_kwargs["host"]

    with RemoteHost(**connect_kwargs) as remote:
        current_mode = console.show_mode(remote)
        if current_mode in ("elevated", "learning"):
            _log(f"{host}: already {current_mode} — skipping.", on_progress)
            return True
        if current_mode != "de-elevated":
            raise RuntimeError(
                f"Cannot elevate {host}: current mode is '{current_mode}' (expected de-elevated)."
            )

        _log(f"[1] Generating and applying elevation file locally on {host}...", on_progress)
        data = _local_elevate(remote, duration, mode)
        if not data["elevated"]:
            raise RuntimeError(f"Elevation failed on {host}: {data.get('error')}")

        mode_after = console.show_mode(remote)
        _log(f"    mode now: {mode_after}", on_progress)

    return mode_after == "elevated"


def reinstall(
    connect_kwargs: dict,
    version: str,
    build: str,
    source: str = "csp",
    local_dir: Optional[str] = None,
    domain: Optional[str] = None,
    elevation_file: Optional[str] = None,
    elevation_duration: str = "1h",
    do_activate: bool = False,
    on_progress: Optional[Callable[[str], None]] = None,
) -> bool:
    """Full cycle: inspect target, uninstall if already installed, install fresh, optionally activate."""
    host = connect_kwargs["host"]

    _log(f"[1] Gathering system info from {host}...", on_progress)
    with RemoteHost(**connect_kwargs) as remote:
        ti = TargetInspector(remote)
        info = ti.get_system_info()
        installed, version_str, package_manager = ti.check_installed()
        current_mode = console.show_mode(remote) if installed else "not_installed"

    _log(f"    os:      {info.os_name} {info.os_version}", on_progress)
    _log(f"    kernel:  {info.kernel}", on_progress)
    _log(f"    arch:    {info.arch}", on_progress)
    _log(
        f"    qdocse:  {'installed (' + version_str + ', ' + package_manager + ')' if installed else 'not installed'}",
        on_progress,
    )
    _log(f"    mode:    {current_mode}", on_progress)

    if installed:
        _log(f"[2] QDocSE already installed — running uninstall first...", on_progress)
        if not uninstall(connect_kwargs, elevation_file=elevation_file, elevation_duration=elevation_duration, on_progress=on_progress):
            raise RuntimeError(f"Uninstall failed on {host}; aborting reinstall.")
        _log(f"    Uninstall complete.", on_progress)
    else:
        _log(f"[2] QDocSE not installed — skipping uninstall.", on_progress)

    _log(f"[3] Installing QDocSE {version}-{build} from {source}...", on_progress)
    if not install(connect_kwargs, version, build, source=source, local_dir=local_dir,
                   domain=domain, on_progress=on_progress):
        return False

    if do_activate:
        _log("[4] Activating via CSP customer portal...", on_progress)
        activate(connect_kwargs, on_progress=on_progress)

    return True


def force_uninstall(
    connect_kwargs: dict,
    on_progress: Optional[Callable[[str], None]] = None,
) -> bool:
    """LAST RESORT: disable QDocSE's own module-loading paths, reboot, and only then
    run the package removal -- so nothing is mounted or loaded left for the package's
    own %preun/prerm scriptlet to fight. Removal itself escalates automatically: the
    ordinary remove_package() first, then remove_package_skip_prerm() if the package's
    pre-removal script refuses anyway (e.g. a panic-corrupted DB fails its mode check),
    then remove_package_no_scripts() if even the cleanup script is unusable. The
    escalation lives here, inside the already --force-gated path, because past the
    post-reboot "nothing loaded" verification the skipped script checks are all no-ops.

    This entirely bypasses QDocSE's license-gated uninstall dance (install_prep +
    reboot). Use only when a device is genuinely stuck and cannot be unblocked
    through install()/activate()/renew()/elevate() -- e.g. an expired license with no
    way to renew or elevate it. Nothing else in this module calls this automatically;
    it must be invoked explicitly (CLI: `lifecycle.py force-uninstall --force`).

    Steps: disable+stop QDocSEService/qdocsesubagent (this is what actually performs
    the mount() calls and loads its own modules, confirmed via `strings` against the
    real binary) -> disable the redundant /etc/modules-load.d entry -> reboot ->
    verify no bic_* modules are loaded or mounted -> only then remove the package.
    Aborts without touching the package if verification finds anything still
    loaded/mounted, rather than forcing a removal that would fight it.
    """
    host = connect_kwargs["host"]

    with RemoteHost(**connect_kwargs) as remote:
        ti = TargetInspector(remote)
        installed, _, package_manager = ti.check_installed()
        if not installed:
            _log(f"{host}: QDocSE is not installed.", on_progress)
            return True

        try:
            qid = ti.get_qid()
        except RuntimeError:
            qid = None

        _log(f"[1] Disabling QDocSEService/qdocsesubagent on {host}...", on_progress)
        # 2x the idle cap: stopping the wedged services this path exists for can stall
        # silently up to systemd's default 90s stop timeout.
        remote.run("systemctl disable --now QDocSEService qdocsesubagent", timeout=2 * remote.command_timeout)

        _log(f"[2] Disabling {host}'s modules-load.d entry...", on_progress)
        remote.run(
            "test -f /etc/modules-load.d/qdocse_modules.conf && "
            "mv /etc/modules-load.d/qdocse_modules.conf "
            "/etc/modules-load.d/qdocse_modules.conf.disabled-by-force-uninstall"
        )

    _log(f"[3] Rebooting {host}...", on_progress)
    if not reboot_and_wait(connect_kwargs, on_progress=on_progress):
        raise RuntimeError(f"{host} did not come back online after reboot.")

    with RemoteHost(**connect_kwargs) as remote:
        _log(f"[4] Verifying no QDocSE kernel modules are loaded/mounted on {host}...", on_progress)
        lsmod = remote.run("lsmod | grep -i '^bic_'").stdout.strip()
        mounts = remote.run("grep -i 'bic_' /proc/mounts").stdout.strip()
        if lsmod or mounts:
            raise RuntimeError(
                f"{host}: QDocSE modules are still loaded/mounted after reboot -- "
                "aborting rather than force a package removal that would fight them.\n"
                f"lsmod:\n{lsmod}\nmounts:\n{mounts}"
            )
        _log("    clean — nothing loaded or mounted.", on_progress)

        _log(f"[5] Removing package ({package_manager})...", on_progress)
        ok = remove_package(remote, package_manager, on_progress=on_progress)
        if not ok:
            _log(
                "[5b] Package's pre-removal script refused -- retrying with it bypassed "
                "(the post-removal cleanup script still runs)...",
                on_progress,
            )
            ok = remove_package_skip_prerm(remote, package_manager, on_progress=on_progress)
        if not ok:
            _log(
                "[5c] Package scripts unusable -- removing by manifest, then deleting "
                "runtime artifacts...",
                on_progress,
            )
            ok = remove_package_no_scripts(remote, package_manager, on_progress=on_progress)
        verified = ok and TargetInspector(remote).verify_uninstalled()

    if verified:
        _deregister_from_csp(host, qid, on_progress)
    return verified


def _connect_kwargs(args: argparse.Namespace) -> dict:
    defaults = config.find_target(args.host)
    host = args.host
    port = args.port or defaults.get("port", 22)
    user = args.user or defaults.get("user")
    key_file = args.key_file
    password = args.password
    if password is None and key_file is None:
        password = defaults.get("password") or getpass.getpass(f"Password for {user}@{host}: ")
    if not user:
        raise SystemExit("Missing --user and no matching entry in targets.toml.")
    return {"host": host, "port": port, "username": user, "password": password, "key_filename": key_file,
            "command_timeout": defaults.get("command_timeout")}


def status(connect_kwargs: dict) -> dict:
    """Comprehensive read-only status for one target: system info (os/kernel/arch), install
    status/version, QID, QDocSEConsole's own reported version/build/commit, license mode,
    and license expiry/type. console.view()'s richer detail (authorized/denied programs,
    watch points, encryption cipher, ...) is left out of this summary -- call console.py view
    directly for that. Makes no changes.
    """
    with RemoteHost(**connect_kwargs) as remote:
        ti = TargetInspector(remote)
        info = ti.get_system_info()
        installed, version_str, package_manager = ti.check_installed()
        result = {
            "os_name": info.os_name, "os_version": info.os_version,
            "kernel": info.kernel, "arch": info.arch,
            "installed": installed, "version": version_str, "package_manager": package_manager,
            "qid": None, "mode": "not_installed", "license_expires": None, "license_type": None,
            "qdocse_version": None, "build_time": None, "commit": None,
        }
        if installed:
            try:
                result["qid"] = ti.get_qid()
            except RuntimeError:
                # A package stranded mid-install/uninstall is present without a qid
                # (qid.txt appears at configure time); report the rest of the status
                # rather than dying -- same tolerance uninstall() extends to get_qid().
                pass
            result["mode"] = console.show_mode(remote)
            view_data = console.view(remote)
            result["license_expires"] = view_data.get("license_expires")
            result["license_type"] = view_data.get("license_type")
            # console.version()'s "version" is QDocSEConsole's own reported version (e.g.
            # '3.2.0'), distinct from "version" above (the installed package's version-release,
            # e.g. '3.2.0-1') -- kept under a separate key to avoid clobbering it.
            version_data = console.version(remote)
            result["qdocse_version"] = version_data.get("version")
            result["build_time"] = version_data.get("build_time")
            result["commit"] = version_data.get("commit")
    return result


def format_status(data: dict) -> str:
    """Formats status()'s dict as readable, grouped lines (one target's worth) -- shared by
    lifecycle.py's own CLI and fleet.py's per-host status printing."""
    lines = [f"os:        {data['os_name']} {data['os_version']} (kernel {data['kernel']}, {data['arch']})"]
    if not data["installed"]:
        lines.append("installed: False")
        return "\n".join(lines)
    lines.append(f"installed: True (version {data['version']}, {data['package_manager']})")
    if data.get("qdocse_version"):
        lines.append(f"qdocse:    {data['qdocse_version']} (build {data['build_time']}, commit {data['commit']})")
    lines.append(f"qid:       {data['qid']}")
    lines.append(f"mode:      {data['mode']}")
    if data["license_expires"]:
        lines.append(f"license:   expires {data['license_expires']}")
        lines.append(f"           type: {data['license_type']}")
    return "\n".join(lines)


def _cmd_status(args: argparse.Namespace) -> int:
    connect_kwargs = _connect_kwargs(args)
    print(format_status(status(connect_kwargs)))
    return 0


def _cmd_install(args: argparse.Namespace) -> int:
    connect_kwargs = _connect_kwargs(args)
    try:
        ok = install(
            connect_kwargs,
            args.version,
            resolve_build(args.version, args.build, args.source, print),
            source=args.source,
            local_dir=args.local_dir,
            domain=args.domain,
            on_progress=print,
        )
    except (RuntimeError, ValueError) as e:
        logger.error(str(e))
        return 1
    return 0 if ok else 1


def _cmd_uninstall(args: argparse.Namespace) -> int:
    connect_kwargs = _connect_kwargs(args)
    try:
        ok = uninstall(connect_kwargs, elevation_file=args.elevation_file, on_progress=print)
    except (RuntimeError, ValueError) as e:
        logger.error(str(e))
        return 1
    return 0 if ok else 1


def _cmd_activate(args: argparse.Namespace) -> int:
    connect_kwargs = _connect_kwargs(args)
    try:
        activate(connect_kwargs, duration=args.duration, mode=args.mode, on_progress=print)
    except (RuntimeError, ValueError) as e:
        logger.error(str(e))
        return 1
    return 0


def _cmd_renew(args: argparse.Namespace) -> int:
    connect_kwargs = _connect_kwargs(args)
    try:
        ok = renew(connect_kwargs, duration=args.duration, mode=args.mode, on_progress=print)
    except (RuntimeError, ValueError) as e:
        logger.error(str(e))
        return 1
    return 0 if ok else 1


def _cmd_elevate(args: argparse.Namespace) -> int:
    connect_kwargs = _connect_kwargs(args)
    try:
        ok = elevate(connect_kwargs, duration=args.duration, mode=args.mode, on_progress=print)
    except (RuntimeError, ValueError) as e:
        logger.error(str(e))
        return 1
    return 0 if ok else 1


def _cmd_reinstall(args: argparse.Namespace) -> int:
    connect_kwargs = _connect_kwargs(args)
    try:
        ok = reinstall(
            connect_kwargs,
            args.version,
            resolve_build(args.version, args.build, args.source, print),
            source=args.source,
            local_dir=args.local_dir,
            domain=args.domain,
            elevation_file=args.elevation_file,
            do_activate=args.activate,
            on_progress=print,
        )
    except (RuntimeError, ValueError) as e:
        logger.error(str(e))
        return 1
    return 0 if ok else 1


def _cmd_upgrade(args: argparse.Namespace) -> int:
    connect_kwargs = _connect_kwargs(args)
    try:
        ok = upgrade(
            connect_kwargs,
            args.version,
            resolve_build(args.version, args.build, args.source, print),
            source=args.source,
            local_dir=args.local_dir,
            domain=args.domain,
            elevation_file=args.elevation_file,
            on_progress=print,
        )
    except (RuntimeError, ValueError) as e:
        logger.error(str(e))
        return 1
    return 0 if ok else 1


def _cmd_force_uninstall(args: argparse.Namespace) -> int:
    if not args.force:
        logger.error(
            "Refusing to run without --force. force-uninstall disables QDocSEService, "
            "reboots the target, and bypasses the license-gated uninstall dance entirely -- "
            "only use it on a device that's genuinely stuck (pass --force to confirm)."
        )
        return 1
    connect_kwargs = _connect_kwargs(args)
    try:
        ok = force_uninstall(connect_kwargs, on_progress=print)
    except (RuntimeError, ValueError) as e:
        logger.error(str(e))
        return 1
    return 0 if ok else 1


def _add_connection_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--host", required=True, help="Target hostname or IP.")
    parser.add_argument("--port", type=int, help="SSH port (default: from targets.toml, or 22).")
    parser.add_argument("--user", help="SSH username (default: from targets.toml).")
    auth = parser.add_mutually_exclusive_group()
    auth.add_argument("--password", help="SSH password (default: from targets.toml, or prompted).")
    auth.add_argument("--key-file", help="Path to an SSH private key file.")


def _add_source_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--version", required=True, help="Release version (e.g. 3.2.0).")
    parser.add_argument("--build", required=True, help="Build number, or 'latest' for the newest build on --source.")
    parser.add_argument(
        "--source", choices=["csp", "release"], default="csp",
        help="Resolve+download from CSP (default) or the release server.",
    )
    parser.add_argument(
        "--local-dir", default=None,
        help="Local staging directory (default: var/downloads/csp or var/downloads/release, per --source).",
    )
    parser.add_argument(
        "--domain", help="Customer unitname to resolve the CSP owner id from (--source csp only)."
    )


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Install/upgrade/uninstall QDocSE on a target host, "
        "handling the install_prep+reboot dance."
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Show full SSH debug output.")
    subparsers = parser.add_subparsers(dest="command")
    parser.set_defaults(func=lambda args: (parser.print_help(), 1)[1])

    status_p = subparsers.add_parser(
        "status", help="Comprehensive read-only status: system info, install status, QID, license mode/expiry."
    )
    _add_connection_args(status_p)
    status_p.set_defaults(func=_cmd_status)

    install_p = subparsers.add_parser("install", help="Install QDocSE on a target with nothing installed.")
    _add_connection_args(install_p)
    _add_source_args(install_p)
    install_p.set_defaults(func=_cmd_install)

    uninstall_p = subparsers.add_parser("uninstall", help="Mode-aware uninstall (handles install_prep + reboot).")
    _add_connection_args(uninstall_p)
    uninstall_p.add_argument("--elevation-file", help="Local path to an externally-issued elevation file; if omitted and the device is De-elevated, one is generated locally instead.")
    uninstall_p.set_defaults(func=_cmd_uninstall)

    activate_p = subparsers.add_parser(
        "activate", help="Read QID from target, find its CSP device, generate and send activation.",
    )
    _add_connection_args(activate_p)
    activate_p.add_argument("--duration", type=int, default=2_678_400, help="License validity in seconds (default: 2678400 = 31 days).")
    activate_p.add_argument("--mode", type=int, default=5, help="License mode field baked into the .dat (default: 5).")
    activate_p.set_defaults(func=_cmd_activate)

    renew_p = subparsers.add_parser(
        "renew",
        help="Renew an expired/expiring license locally (renewrequest -> local .dat -> "
        "renewcommit), no CSP involved.",
    )
    _add_connection_args(renew_p)
    renew_p.add_argument("--duration", type=int, default=2_678_400, help="License validity in seconds (default: 2678400 = 31 days).")
    renew_p.add_argument("--mode", type=int, default=5, help="License mode field baked into the .dat (default: 5).")
    renew_p.set_defaults(func=_cmd_renew)

    elevate_p = subparsers.add_parser(
        "elevate",
        help="Move a De-elevated device to Elevated, generating the elevation file locally.",
    )
    _add_connection_args(elevate_p)
    elevate_p.add_argument("--duration", default="1h", help="Elevation time, e.g. 9d, 6h, 300m (default: 1h).")
    elevate_p.add_argument("--mode", type=int, default=5, help="License mode field baked into the .dat (default: 5).")
    elevate_p.set_defaults(func=_cmd_elevate)

    reinstall_p = subparsers.add_parser(
        "reinstall", help="Inspect target, uninstall if already installed, then install fresh from CSP.",
    )
    _add_connection_args(reinstall_p)
    _add_source_args(reinstall_p)
    reinstall_p.add_argument("--elevation-file", help="Local path to an externally-issued elevation file; if omitted and the device is De-elevated, one is generated locally instead.")
    reinstall_p.add_argument("--activate", action="store_true", help="Activate via CSP customer portal after install.")
    reinstall_p.set_defaults(func=_cmd_reinstall)

    upgrade_p = subparsers.add_parser(
        "upgrade", help="Mode-aware upgrade (handles install_prep + reboot + finalize)."
    )
    _add_connection_args(upgrade_p)
    _add_source_args(upgrade_p)
    upgrade_p.add_argument("--elevation-file", help="Local path to an externally-issued elevation file; if omitted and the device is De-elevated, one is generated locally instead.")
    upgrade_p.set_defaults(func=_cmd_upgrade)

    force_uninstall_p = subparsers.add_parser(
        "force-uninstall",
        help="LAST RESORT: disable module loading, reboot, then remove the package. "
        "Bypasses the license-gated uninstall dance entirely. Requires --force.",
    )
    _add_connection_args(force_uninstall_p)
    force_uninstall_p.add_argument(
        "--force", action="store_true",
        help="Required to actually run -- this reboots the target and disables QDocSEService.",
    )
    force_uninstall_p.set_defaults(func=_cmd_force_uninstall)

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
