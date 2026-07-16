"""Client for browsing and downloading packages from the qdocse release archive."""

import argparse
import getpass
import logging
import os
import posixpath
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from typing import Callable, Optional

import paramiko

import config
from downloads import KERNEL_SIDECAR_SUFFIX
from remote import RemoteHost

logger = logging.getLogger(__name__)

VERSION_DIR_RE = re.compile(r"^qdocse-(\d+\.\d+\.\d+(?:-\w+)?)$")
PACKAGE_SUBDIR = "CSP"
PACKAGE_EXTENSIONS = ("rpm", "deb")

# qdocse's installers refuse to install on a kernel they weren't built for: the .rpm's %pre
# scriptlet does `if [ ${KERNV} != "<uname>" ]; then ... exit 1; fi`, and the .deb's preinst
# assigns `KERNEL_NUMBER="<uname>"` and checks the same way. Either form gives the exact
# `uname -r` the package's kernel modules were compiled against -- the authoritative target,
# unlike guessing it from the release-server folder's distro-naming convention.
_RPM_KERNEL_CHECK_RE = re.compile(r"KERNV\}?\s*!=\s*\"([^\"]+)\"")
_DEB_KERNEL_CHECK_RE = re.compile(r'KERNEL_NUMBER\s*=\s*"([^"]+)"')
_RPM_HEADER_PREFIX_BYTES = 256 * 1024


def _search_kernel_check(pattern: re.Pattern, text: str) -> Optional[str]:
    match = pattern.search(text)
    return match.group(1) if match else None


def extract_local_kernel_version(local_path: str) -> Optional[str]:
    """Reads the exact compiled-for kernel version from an already-downloaded local package
    file -- the same install-script version gate as ReleaseServer.get_package_kernel_version(),
    but run directly against the local file instead of probing the release server over SSH.
    Returns None if the package has no such check or isn't .rpm/.deb.
    """
    if local_path.endswith(".rpm"):
        try:
            result = subprocess.run(["rpm", "-qp", "--scripts", local_path], capture_output=True, text=True)
        except FileNotFoundError:
            logger.error("'rpm' is not installed locally; can't read .rpm kernel-version checks.")
            return None
        return _search_kernel_check(_RPM_KERNEL_CHECK_RE, result.stdout)
    if local_path.endswith(".deb"):
        quoted = shlex.quote(local_path)
        result = subprocess.run(
            f"dpkg-deb -I {quoted} preinst 2>/dev/null || "
            f"ar p {quoted} control.tar.xz 2>/dev/null | tar -xJO ./preinst 2>/dev/null || "
            f"ar p {quoted} control.tar.gz 2>/dev/null | tar -xzO ./preinst 2>/dev/null",
            shell=True,
            capture_output=True,
            text=True,
        )
        return _search_kernel_check(_DEB_KERNEL_CHECK_RE, result.stdout)
    return None


class ReleaseServer:
    """Browses the release archive's version/build/distro tree and fetches packages.

    Expected layout: {base_path}/qdocse-{version}/{build}/{distro}/CSP/*.rpm
    """

    def __init__(self, remote: RemoteHost, base_path: str):
        self.remote = remote
        self.base_path = base_path

    def _ls(self, path: str) -> list:
        result = self.remote.run(f"ls -1 {path}")
        if not result.ok:
            logger.error(f"Failed to list '{path}': {result.stderr.strip()}")
            return []
        return [line for line in result.stdout.splitlines() if line]

    def list_versions(self) -> list:
        """List available release versions (e.g. '3.2.0'), ignoring non-release dirs like 'test1'."""
        versions = []
        for name in self._ls(self.base_path):
            match = VERSION_DIR_RE.match(name)
            if match:
                versions.append(match.group(1))
        return versions

    def list_builds(self, version: str) -> list:
        """List build numbers available for a given version, sorted numerically (build dirs
        like 'test1'/'verify1' that aren't purely numeric sort after the numeric ones, alphabetically)."""
        builds = self._ls(posixpath.join(self.base_path, f"qdocse-{version}"))
        return sorted(builds, key=lambda b: (0, int(b)) if b.isdigit() else (1, b))

    def list_distros(self, version: str, build: str) -> list:
        """List distro directory names available for a given version/build."""
        return self._ls(posixpath.join(self.base_path, f"qdocse-{version}", build))

    def find_package(self, version: str, build: str, distro: str) -> Optional[str]:
        """Find the installer package path for a given version/build/distro, or None if not found.

        The CSP/ directory also holds test scripts and tooling (kfb, server, test_*, ...), so
        match only files starting with 'qdocse'. Different distro families package differently
        (.rpm for RPM-based distros, .deb for Debian/Ubuntu) -- try both extensions.
        """
        csp_dir = posixpath.join(self.base_path, f"qdocse-{version}", build, distro, PACKAGE_SUBDIR)
        for ext in PACKAGE_EXTENSIONS:
            result = self.remote.run(f"ls -1 {csp_dir}/qdocse*.{ext}")
            if result.ok:
                paths = [line for line in result.stdout.splitlines() if line]
                if paths:
                    return paths[0]
        logger.error(f"No package found in '{csp_dir}' (tried: {', '.join(PACKAGE_EXTENSIONS)})")
        return None

    def get_package_kernel_version(self, remote_path: str) -> Optional[str]:
        """Reads the exact kernel version (a `uname -r` string) a package's kernel modules
        were compiled against, straight out of its install script's own version gate -- see
        the module-level _RPM_KERNEL_CHECK_RE/_DEB_KERNEL_CHECK_RE comment. Returns None if
        the package has no such check (e.g. a Windows .zip/.msi) or the file isn't .rpm/.deb.
        """
        if remote_path.endswith(".rpm"):
            return self._get_rpm_kernel_version(remote_path)
        if remote_path.endswith(".deb"):
            return self._get_deb_kernel_version(remote_path)
        return None

    def _get_rpm_kernel_version(self, remote_path: str) -> Optional[str]:
        """The release server doesn't have `rpm` installed, so fetch just the file's header
        (well before the multi-MB payload -- 256KB comfortably covers it for these packages)
        via SFTP and query it with rpm locally instead of downloading the whole package."""
        header = self.remote.read_remote_prefix(remote_path, _RPM_HEADER_PREFIX_BYTES)
        with tempfile.NamedTemporaryFile(suffix=".rpm") as tmp:
            tmp.write(header)
            tmp.flush()
            try:
                result = subprocess.run(["rpm", "-qp", "--scripts", tmp.name], capture_output=True, text=True)
            except FileNotFoundError:
                logger.error("'rpm' is not installed locally; can't read .rpm kernel-version checks.")
                return None
        return _search_kernel_check(_RPM_KERNEL_CHECK_RE, result.stdout)

    def _get_deb_kernel_version(self, remote_path: str) -> Optional[str]:
        """Unlike rpm, the release server does have `ar`/`tar`, so this stays a remote query."""
        quoted = shlex.quote(remote_path)
        result = self.remote.run(
            f"dpkg-deb -I {quoted} preinst 2>/dev/null || "
            f"ar p {quoted} control.tar.xz 2>/dev/null | tar -xJO ./preinst 2>/dev/null || "
            f"ar p {quoted} control.tar.gz 2>/dev/null | tar -xzO ./preinst 2>/dev/null"
        )
        return _search_kernel_check(_DEB_KERNEL_CHECK_RE, result.stdout)

    def build_kernel_map(self, version: str, build: str, distros: Optional[list] = None) -> dict:
        """Maps each distro in version/build to its package's compiled-for kernel version (or
        None if it has none -- see get_package_kernel_version). Computing this once per
        (version, build) lets callers resolve many targets against the same build without
        re-probing every package's install script once per target.
        """
        if distros is None:
            distros = self.list_distros(version, build)
        kernel_map = {}
        for distro in distros:
            remote_path = self.find_package(version, build, distro)
            kernel_map[distro] = self.get_package_kernel_version(remote_path) if remote_path else None
        return kernel_map

    def download_package(self, version: str, build: str, distro: str, local_dir: str) -> str:
        """Download the package for a given version/build/distro into local_dir.

        Lands under local_dir/{version}/{build}/{distro}/ rather than local_dir directly --
        many distros share the same package filename (only arch varies, e.g.
        'qdocse-3.2.0-1.x86_64.rpm'), so a flat directory would silently overwrite across
        distros when downloading more than one in the same run.

        Always re-downloads, wiping out any existing contents of the destination directory
        first. Also writes a KERNEL_SIDECAR_SUFFIX sidecar file with the package's compiled-for
        kernel version (see extract_local_kernel_version()), so later steps -- e.g. csp.py's
        upload tagging -- don't need to re-extract it themselves.
        """
        remote_path = self.find_package(version, build, distro)
        if remote_path is None:
            raise FileNotFoundError(f"No package found for {version}/{build}/{distro}")

        dest_dir = os.path.join(local_dir, version, build, distro)
        if os.path.isdir(dest_dir):
            shutil.rmtree(dest_dir)
        os.makedirs(dest_dir, exist_ok=True)
        local_path = os.path.join(dest_dir, posixpath.basename(remote_path))

        self.remote.download(remote_path, local_path)

        kernel_version = extract_local_kernel_version(local_path)
        if kernel_version:
            with open(local_path + KERNEL_SIDECAR_SUFFIX, "w") as f:
                f.write(kernel_version + "\n")

        return local_path

    def download_all(
        self,
        version: str,
        local_dir: str,
        build: Optional[str] = None,
        distro: Optional[str] = None,
        on_progress: Optional[Callable[[str], None]] = None,
    ) -> list:
        """Downloads package(s) for version, defaulting build to the latest available and
        distro to every distro available for that build.

        on_progress, if given, is called with one already-formatted, aligned line per
        distro as it completes -- lets callers show live progress for a long batch instead
        of going silent until everything finishes.
        """
        if build is None:
            builds = self.list_builds(version)
            if not builds:
                raise RuntimeError(f"No builds found for version '{version}'.")
            build = builds[-1]

        distros = [distro] if distro else self.list_distros(version, build)
        width = max((len(d) for d in distros), default=0)
        entries = []
        for d in distros:
            try:
                local_path = self.download_package(version, build, d, local_dir)
                entries.append({"version": version, "build": build, "distro": d, "local_path": local_path})
                if on_progress:
                    on_progress(f"{d:<{width}}  {os.path.relpath(local_path)}")
            except FileNotFoundError as e:
                if on_progress:
                    on_progress(f"{d:<{width}}  FAILED: {e}")
        return entries


def _cmd_list_versions(rs: ReleaseServer, args: argparse.Namespace) -> int:
    for version in rs.list_versions():
        print(version)
    return 0


def _cmd_list_builds(rs: ReleaseServer, args: argparse.Namespace) -> int:
    for build in rs.list_builds(args.version):
        print(build)
    return 0


def _cmd_list_distros(rs: ReleaseServer, args: argparse.Namespace) -> int:
    for distro in rs.list_distros(args.version, args.build):
        print(distro)
    return 0


def _cmd_find(rs: ReleaseServer, args: argparse.Namespace) -> int:
    path = rs.find_package(args.version, args.build, args.distro)
    if path is None:
        return 1
    print(path)
    return 0


def _cmd_download(rs: ReleaseServer, args: argparse.Namespace) -> int:
    entries = rs.download_all(
        args.version,
        args.local_dir,
        build=args.build,
        distro=args.distro,
        on_progress=print,
    )
    print(f"Downloaded {len(entries)} package(s) for {args.version}/{entries[0]['build'] if entries else args.build}.")
    return 0 if entries else 1


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Browse and download packages from the release archive.")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Show full SSH/SFTP debug output (quiet by default)."
    )

    subparsers = parser.add_subparsers(dest="command")

    list_p = subparsers.add_parser("list", help="List versions/builds/distros.")
    list_sub = list_p.add_subparsers(dest="list_command")

    list_sub.add_parser("versions", help="List available release versions.").set_defaults(func=_cmd_list_versions)

    list_builds = list_sub.add_parser("builds", help="List build numbers for a version.")
    list_builds.add_argument("--version", required=True, help="Release version (e.g. 3.2.0).")
    list_builds.set_defaults(func=_cmd_list_builds)

    list_distros = list_sub.add_parser("distros", help="List distro types for a version/build.")
    list_distros.add_argument("--version", required=True, help="Release version (e.g. 3.2.0).")
    list_distros.add_argument("--build", required=True, help="Build number.")
    list_distros.set_defaults(func=_cmd_list_distros)

    find = subparsers.add_parser("find", help="Find the package path for a version/build/distro.")
    find.add_argument("--version", required=True, help="Release version (e.g. 3.2.0).")
    find.add_argument("--build", required=True, help="Build number.")
    find.add_argument("--distro", required=True, help="Distro directory name.")
    find.set_defaults(func=_cmd_find)

    download = subparsers.add_parser("download", help="Download package(s) for a version.")
    download.add_argument("--version", required=True, help="Release version (e.g. 3.2.0).")
    download.add_argument("--build", help="Build number (default: latest available build).")
    download.add_argument("--distro", help="Distro directory name (default: every distro for the build).")
    download.add_argument(
        "--local-dir", default=config.DEFAULT_DOWNLOAD_DIR,
        help="Local directory to download into (default: var/downloads/release).",
    )
    download.set_defaults(func=_cmd_download)

    parser.list_parser = list_p  # so main() can print list's own help if given with no leaf command
    return parser


def main(argv: Optional[list] = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    config.configure_logging(args.verbose)

    if args.command is None:
        parser.print_help()
        return 1
    if args.command == "list" and args.list_command is None:
        parser.list_parser.print_help()
        return 1

    defaults = config.load_release_server()
    host = defaults.get("host")
    user = defaults.get("user")
    base_path = defaults.get("base_path")
    if not host or not user or not base_path:
        logger.error("Missing host/user/base_path in release_server.toml.")
        return 2

    password = defaults.get("password") or getpass.getpass(f"Password for {user}@{host}: ")

    try:
        with RemoteHost(
            host=host,
            port=defaults.get("port", 22),
            username=user,
            password=password,
        ) as remote:
            rs = ReleaseServer(remote, base_path=base_path)
            return args.func(rs, args)
    except (paramiko.SSHException, OSError) as e:
        logger.error(f"SSH connection failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
