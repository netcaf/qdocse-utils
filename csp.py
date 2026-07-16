"""Self-contained client + CLI for the CSP Customer portal and SAMGR package server."""

import argparse
import base64
import logging
import os
import re
import sys
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Callable, Optional

import requests
import urllib3
from gmssl import sm3, func

import config
from downloads import discover_local_packages, latest_local_build

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)

_csp_config = config.load_csp()

CSP_CUSTOMER_URL = os.environ.get("CSP_CUSTOMER_URL", _csp_config["customer"]["url"])
CSP_CUSTOMER_UNITNAME = os.environ.get("CSP_CUSTOMER_UNITNAME", _csp_config["customer"]["unitname"])
CSP_CUSTOMER_USERNAME = os.environ.get("CSP_CUSTOMER_USERNAME", _csp_config["customer"]["username"])
CSP_CUSTOMER_PASSWORD = os.environ.get("CSP_CUSTOMER_PASSWORD", _csp_config["customer"].get("password", ""))

CSP_SAMGR_URL = os.environ.get("CSP_SAMGR_URL", _csp_config["samgr"]["url"])
CSP_SAMGR_USERNAME = os.environ.get("CSP_SAMGR_USERNAME", _csp_config["samgr"]["username"])
CSP_SAMGR_PASSWORD = os.environ.get("CSP_SAMGR_PASSWORD", _csp_config["samgr"].get("password", ""))


def _split_distro(distro: str) -> tuple:
    """Best-effort split of a release-server folder name (e.g. 'CentOS_7.6',
    'OracleLinux7.8-Kern4.14') into (os_name, os_version, os_kernel).

    Two formats need separate handling: the kernel marker is usually '-Kern' but sometimes
    '_Kern' (e.g. 'Kylin-V10SP3_Kern4.19.90-52.22.v2207-ARM' -- previously silently fell back
    to os_kernel="default"), and the version is usually trailing digits (e.g. 'CentOS_7.6')
    but sometimes a 'vNN' token followed by more text (e.g. 'UOS-Desktop-v20-Pro', where the
    version isn't at the end of the string -- previously produced os_version="").
    """
    kernel_match = re.search(r"[-_]Kern(.+)$", distro)
    os_kernel = kernel_match.group(1) if kernel_match else "default"
    base = distro[: kernel_match.start()] if kernel_match else distro

    version_match = re.search(r"_?(\d[\d.]*)$", base)
    if version_match:
        os_version = version_match.group(1)
        os_name = base[: version_match.start()].rstrip("_-")
        return os_name, os_version, os_kernel

    version_match = re.search(r"[-_][vV](\d[\d.]*)(?:[-_]|$)", base)
    if version_match:
        os_version = version_match.group(1)
        os_name = "-".join(p for p in (base[:version_match.start()], base[version_match.end():]) if p)
        return os_name, os_version, os_kernel

    return base, "", os_kernel


class CSPBase(ABC):
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.verify = False

    def generate_shadow(self, data: str) -> str:
        message = data.encode("utf-8")
        return sm3.sm3_hash(func.bytes_to_list(message))

    @abstractmethod
    def login(self) -> bool:
        pass

    def post(self, endpoint: str, data: Any = None, json: Any = None, files: Any = None) -> Optional[dict]:
        url = f"{self.base_url}/{endpoint}"
        response = self.session.post(url, data=data, json=json, files=files)
        if response.ok:
            return response.json()
        logger.error(f"Failed to post to '{url}': {response.status_code}")
        return None

    def get_raw(self, endpoint: str) -> Optional[requests.Response]:
        url = f"{self.base_url}/{endpoint}"
        response = self.session.get(url)
        if response.ok:
            return response
        logger.error(f"Failed to GET '{url}': {response.status_code}")
        return None

    def get_owner_id(self, domain: str) -> Optional[int]:
        """Resolves a unitname/domain to its numeric owner id (no login required)."""
        response = self.post("api/owner/n/domain", json={"domain": domain})
        if response and response.get("success", False):
            return response.get("owner")
        logger.error(f"Failed to resolve owner id for domain '{domain}'.")
        return None


class CSPCustomer(CSPBase):
    def __init__(
        self,
        base_url: str = CSP_CUSTOMER_URL,
        unitname: str = CSP_CUSTOMER_UNITNAME,
        username: str = CSP_CUSTOMER_USERNAME,
        password: str = CSP_CUSTOMER_PASSWORD,
    ):
        super().__init__(base_url)
        self.unitname = unitname
        self.username = username
        self.password = password

    def login(self) -> bool:
        payload = {
            "domain": self.unitname,
            "email": self.username,
            "password": self.generate_shadow(self.password),
            "code": "",
            "picCode": "",
            "pinCode": "",
        }
        response = self.post("api/login/n/login", json=payload)
        if response and response.get("success", False):
            logger.info("CSPCustomer login successful.")
            return True
        logger.error("CSPCustomer login failed.")
        return False

    def get_device_list(self) -> list:
        response = self.post("api/dv/m/list", json={"type": None, "ugId": None})
        if response and response.get("success", False):
            logger.info("Get device list successful.")
            return response.get("dvs", [])
        logger.error("Get device list failed.")
        return []

    def activate_device(self, dat: bytes, device_id: int) -> bool:
        license_file_content = base64.b64encode(dat).decode("utf-8")
        if not license_file_content:
            logger.error("Activate device failed: license file is empty.")
            return False
        payload = {
            "byteBuf": license_file_content,
            "deviceId": device_id,
            "tt": 365,
        }
        response = self.post("api/sync/m/act", json=payload)
        if response and response.get("success", False):
            logger.info("Activate device successful.")
            return True
        err = response.get("errCode", "") if response else ""
        logger.error(f"Activate device failed. errCode = {err}")
        return False

    def delete_device(self, device_id: int) -> bool:
        response = self.post("api/dv/m/del", json={"id": device_id})
        if response and response.get("success", False):
            logger.info("Delete device successful.")
            return True
        err = response.get("errCode", "") if response else ""
        logger.error(f"Delete device failed. errCode = {err}")
        return False


class CSPSAMGR(CSPBase):
    def __init__(
        self,
        base_url: str = CSP_SAMGR_URL,
        username: str = CSP_SAMGR_USERNAME,
        password: str = CSP_SAMGR_PASSWORD,
    ):
        super().__init__(base_url)
        self.username = username
        self.password = password

    def login(self) -> bool:
        payload = {
            "username": self.username,
            "password": self.generate_shadow(self.password),
        }
        response = self.post("api/sa/n/login", json=payload)
        if response and response.get("success", False):
            logger.info("CSPSAMGR login successful.")
            return True
        logger.error("CSPSAMGR login failed.")
        return False

    def query_packages(self) -> list:
        """Query all packages currently registered on the server."""
        response = self.post("api/sa/pk/pks", json={})
        if response and response.get("errCode") == 0:
            packages = response.get("pks", [])
            logger.info(f"Query packages successful: {len(packages)} package(s) found.")
            return packages
        logger.error("Query packages failed.")
        return []

    def latest_build(self, version: str) -> Optional[str]:
        """The newest build registered on the server for version, or None if there is none.

        Reads the pkVersion tags upload_tagged_packages() writes ('{version}-{build}').
        "Newest" uses the same ordering as release.ReleaseServer.list_builds() and
        downloads.latest_local_build(): numeric builds sort numerically, non-numeric ones
        after them alphabetically, and the last one wins.
        """
        prefix = f"{version}-"
        builds = {
            p["pkVersion"][len(prefix):]
            for p in self.query_packages()
            if (p.get("pkVersion") or "").startswith(prefix)
        }
        if not builds:
            return None
        return sorted(builds, key=lambda b: (0, int(b)) if b.isdigit() else (1, b))[-1]

    def get_package_info(self, pk_id: int) -> Optional[dict]:
        """Query detailed info for a single package by id."""
        response = self.post("api/sa/pk/info", json={"id": pk_id})
        if response and response.get("errCode") == 0:
            logger.info(f"Query package info successful: id={pk_id}")
            return response.get("info")
        logger.error(f"Query package info failed: id={pk_id}")
        return None

    def upload_package(self, file_path: str, pk_id: int = 0) -> Optional[dict]:
        """Upload a package file (.rpm/.deb) to the server.

        pk_id is 0 for a new package, or an existing package id to replace its file.
        """
        if not os.path.isfile(file_path):
            logger.error(f"Upload package failed: '{file_path}' is not a file.")
            return None
        filename = os.path.basename(file_path)
        with open(file_path, "rb") as f:
            files = {"multipartFile": (filename, f, "application/octet-stream")}
            response = self.post(f"api/sa/pk/upload/{pk_id}", files=files)
        if response and response.get("success", False):
            logger.info(f"Upload package successful: id={response.get('id')}, pkName={response.get('pkName')}")
            return response
        logger.error(f"Upload package failed for '{file_path}'.")
        return None

    def edit_package(
        self,
        pk_id: int,
        pk_name: str,
        pk_version: str,
        os_name: str = "default",
        os_type: int = 0,
        os_version: str = "",
        os_kernel: str = "default",
        pk_type: int = 0,
    ) -> bool:
        """Edit the metadata of a previously uploaded package. Internal only -- no standalone
        CLI command; called by upload_tagged_packages() right after upload_package(). To fix
        metadata on an already-registered package from the CLI, delete it and re-upload."""
        payload = {
            "id": pk_id,
            "pkName": pk_name,
            "pkVersion": pk_version,
            "osName": os_name,
            "osType": os_type,
            "osVersion": os_version,
            "osKernel": os_kernel,
            "type": pk_type,
        }
        response = self.post("api/sa/pk/edit", json=payload)
        if response and response.get("success", False):
            logger.info(f"Edit package successful: id={pk_id}")
            return True
        logger.error(f"Edit package failed: id={pk_id}")
        return False

    def delete_package(self, pk_id: int) -> bool:
        """Delete a package from the server by id."""
        response = self.post("api/sa/pk/del", json={"id": pk_id})
        if response and response.get("success", False):
            logger.info(f"Delete package successful: id={pk_id}")
            return True
        logger.error(f"Delete package failed: id={pk_id}")
        return False

    def delete_tagged_packages(
        self,
        os_type: int = 0,
        os_name: Optional[str] = None,
        os_version: Optional[str] = None,
        os_kernel: Optional[str] = None,
    ) -> list:
        """Deletes every automation-uploaded package (osName prefixed 'auto-' -- guards
        against ever touching a manual upload) matching the System/System Name/System
        Version/Kernel hierarchy the CSP download page browses by (osType/osName/osVersion/
        osKernel): each level cascades, give os_name alone to match every version/kernel
        under that name, add os_version to narrow within it, add os_kernel for an exact
        match. os_type defaults to 0 (Linux, the only value upload_tagged_packages() ever
        produces); os_name/os_version/os_kernel default to no filter (match anything).

        Returns the list of deleted package ids.
        """
        prefix = "auto-"
        matches = [
            p
            for p in self.query_packages()
            if (p.get("osName") or "").startswith(prefix)
            and p.get("osType") == os_type
            and (os_name is None or p.get("osName") == f"{prefix}{os_name}")
            and (os_version is None or p.get("osVersion") == os_version)
            and (os_kernel is None or p.get("osKernel") == os_kernel)
        ]
        deleted = []
        for pkg in matches:
            if self.delete_package(pkg["id"]):
                deleted.append(pkg["id"])
        return deleted

    def upload_tagged_packages(
        self, entries: list, tag: str = "auto", on_progress: Optional[Callable[[str], None]] = None
    ) -> list:
        """Uploads+registers package(s). entries is a list of dicts with "local_path" and,
        optionally, "version"/"build"/"pk_id", plus one of:

        - "distro": the distro's osName/osVersion/osKernel are auto-derived from the distro
          folder-naming convention via _split_distro(). This is the shape
          discover_local_packages() (or release.py's download_all()) produces. If the
          entry also has "kernel_version" (discover_local_packages() reads it from the
          download-time sidecar), that exact compiled-for kernel is used for osKernel
          instead of _split_distro()'s guess.
        - "os_name" (optionally with "os_version"/"os_kernel"/"os_type"): the distro's name/
          version used directly, no parsing -- for one-off files that don't follow the
          qdocse distro convention (e.g. a Windows package), where _split_distro() has
          nothing to parse.
        - neither: the file is uploaded as-is with no metadata derived or tagged -- edit
          metadata manually afterward if needed.

        Either tagging path also needs "version"/"build". The CSP download page's fields
        end up populated as: osName ("System Name") = '{tag}-{version}-{build}' (e.g.
        'auto-3.2.0-148' -- the release identity, so a customer filters by release first),
        osVersion ("System Version") = '{distroName}-{distroVersion}' (e.g. 'CentOS-7.3' --
        the distro identity), osKernel ("Kernel") = the exact compiled-for kernel. "pk_id",
        if present, replaces that existing package's file instead of creating one.

        Tagged entries are skipped if a package with the same pkVersion ('{version}-{build}')
        and the same osVersion (the distro identity, since every distro in one release now
        shares the same osName -- pkVersion+osName alone can't tell two distros in the same
        build apart) is already registered -- otherwise re-running upload for the same build
        piles up duplicate entries.

        on_progress, if given, is called with one already-formatted line per package as it
        completes.
        """
        if not entries:
            return []

        existing = {(p["pkVersion"], p["osVersion"]) for p in self.query_packages()}
        width = max(
            (len(e.get("distro") or e.get("os_name") or os.path.basename(e["local_path"])) for e in entries),
            default=0,
        )
        results = []
        for entry in entries:
            local_path = entry["local_path"]
            distro = entry.get("distro")
            os_name_raw = entry.get("os_name")
            label = distro or os_name_raw or os.path.basename(local_path)

            pk_version = os_name_tagged = os_version_tagged = os_kernel = os_type = None
            if entry.get("version") and entry.get("build") and (distro or os_name_raw):
                if distro:
                    os_name, os_version, os_kernel = _split_distro(distro)
                    # Prefer the exact kernel read from the package's own install-script
                    # check (discover_local_packages()'s "kernel_version", from the
                    # download-time sidecar) over the abbreviated value guessed from the
                    # distro folder name.
                    os_kernel = entry.get("kernel_version") or os_kernel
                else:
                    os_name = os_name_raw
                    os_version = entry.get("os_version") or ""
                    os_kernel = entry.get("os_kernel") or "default"
                os_type = entry.get("os_type") or 0
                pk_version = f"{entry['version']}-{entry['build']}"
                os_name_tagged = f"{tag}-{pk_version}"
                os_version_tagged = f"{os_name}-{os_version}" if os_version else os_name
                if (pk_version, os_version_tagged) in existing:
                    if on_progress:
                        on_progress(f"{label:<{width}}  SKIPPED: already exists ({pk_version}/{os_version_tagged})")
                    continue

            result = self.upload_package(local_path, pk_id=entry.get("pk_id", 0))
            if result is None:
                if on_progress:
                    on_progress(f"{label:<{width}}  FAILED: upload failed for '{local_path}'")
                continue

            pk_id = result["id"]
            if pk_version is not None:
                self.edit_package(
                    pk_id,
                    pk_name=os.path.basename(local_path),
                    pk_version=pk_version,
                    os_name=os_name_tagged,
                    os_type=os_type,
                    os_version=os_version_tagged,
                    os_kernel=os_kernel,
                )
            results.append({"id": pk_id, "distro": distro, "local_path": local_path})
            if on_progress:
                on_progress(f"{label:<{width}}  id={pk_id}")
        return results

    def download_package(self, pk_id: int, local_dir: str, owner: int) -> Optional[str]:
        """Downloads a package file by id into local_dir, returning the local path.

        owner is the numeric id returned by get_owner_id(domain) for the customer's unitname
        (the download endpoint is scoped by owner, not by the SAMGR session alone).
        """
        response = self.get_raw(f"api/sa/pk/dw/{owner}/{pk_id}/0")
        if response is None:
            return None

        disposition = response.headers.get("Content-Disposition", "")
        match = re.search(r'filename=([^;]+)', disposition)
        filename = match.group(1).strip('"') if match else f"package_{pk_id}"

        os.makedirs(local_dir, exist_ok=True)
        local_path = os.path.join(local_dir, filename)
        with open(local_path, "wb") as f:
            f.write(response.content)
        logger.info(f"Download package successful: id={pk_id} -> '{local_path}'")
        return local_path


def _format_epoch_ms(epoch_ms: int) -> str:
    return datetime.fromtimestamp(epoch_ms / 1000).strftime("%Y-%m-%d %H:%M:%S")


def _print_package(pkg: dict) -> None:
    print(
        f"id={pkg['id']} pkName={pkg['pkName']} pkVersion={pkg['pkVersion']} "
        f"osName={pkg['osName']} osType={pkg['osType']} osVersion={pkg['osVersion']} "
        f"osKernel={pkg['osKernel']} "
        f"createTime={_format_epoch_ms(pkg['createTime'])} updateTime={_format_epoch_ms(pkg['updateTime'])}"
    )


_TREE_LEVEL_LABELS = [
    lambda v: f"osType={v}",
    lambda v: v,
    lambda v: f"osVersion={v}",
    lambda v: f"osKernel={v}",
]


def _print_packages_tree(packages: list) -> None:
    """Groups packages osType > osName > osVersion > osKernel, mirroring the upload dialog's
    selection order (system type > system name > system version > system kernel), with
    pkVersion/pkName/id/createTime as leaf details. osType is shown as the raw numeric value
    since the server doesn't expose a Linux/Linux-arm/Window label for it.

    Levels are labeled (osVersion=.../osKernel=...) so a bare value like '-' or a kernel
    string isn't ambiguous about which field it is. A run of levels that each have only one
    child (e.g. one osName has exactly one osVersion which has exactly one osKernel) is
    collapsed onto a single line instead of staircasing one value per line.
    """
    tree: dict = {}
    for pkg in packages:
        os_type = pkg["osType"] if pkg["osType"] is not None else "-"
        os_name = pkg["osName"] or "-"
        os_version = pkg["osVersion"] or "-"
        os_kernel = pkg["osKernel"] or "-"
        (
            tree.setdefault(os_type, {})
            .setdefault(os_name, {})
            .setdefault(os_version, {})
            .setdefault(os_kernel, [])
            .append(pkg)
        )

    def walk(node, depth: int, prefix: str) -> None:
        keys = list(node)
        for i, key in enumerate(keys):
            last = i == len(keys) - 1
            connector = "└─" if last else "├─"
            child_prefix = prefix + ("   " if last else "│  ")

            label_parts = [_TREE_LEVEL_LABELS[depth](key)]
            value = node[key]
            d = depth + 1
            while isinstance(value, dict) and len(value) == 1:
                (sub_key, sub_value), = value.items()
                label_parts.append(_TREE_LEVEL_LABELS[d](sub_key))
                value = sub_value
                d += 1

            print(f"{prefix}{connector} {'  '.join(label_parts)}")
            if isinstance(value, dict):
                walk(value, d, child_prefix)
            else:
                for j, pkg in enumerate(value):
                    leaf_connector = "└─" if j == len(value) - 1 else "├─"
                    print(
                        f"{child_prefix}{leaf_connector} pkVersion={pkg['pkVersion']}  "
                        f"id={pkg['id']}  {pkg['pkName']}  {_format_epoch_ms(pkg['createTime'])}"
                    )

    walk(tree, 0, "")


def _cmd_samgr_list(csp: CSPSAMGR, args: argparse.Namespace) -> int:
    packages = csp.query_packages()
    _print_packages_tree(packages)
    return 0


def _cmd_samgr_info(csp: CSPSAMGR, args: argparse.Namespace) -> int:
    info = csp.get_package_info(args.id)
    if info is None:
        return 1
    _print_package(info)
    return 0


def _cmd_samgr_upload(csp: CSPSAMGR, args: argparse.Namespace) -> int:
    if args.file:
        if args.distro and args.os_name:
            logger.error("--distro and --os-name are alternatives -- use only one.")
            return 2
        if args.build == "latest":
            logger.error("--build latest is only valid for batch discovery -- with --file, --build is a literal tag.")
            return 2
        entries = [
            {
                "local_path": args.file,
                "pk_id": 0,
                "version": args.version,
                "build": args.build,
                "distro": args.distro,
                "os_name": args.os_name,
                "os_version": args.os_version,
                "os_kernel": args.os_kernel,
                "os_type": args.os_type,
            }
        ]
    else:
        if args.os_name:
            logger.error("--os-name is only valid with --file.")
            return 2
        if not args.version or not args.build:
            logger.error(
                "--version and --build are required for batch upload (omitting them would "
                "upload every downloaded build under var/downloads/release at once)."
            )
            return 2
        build = args.build
        if build == "latest":
            build = latest_local_build(config.DEFAULT_DOWNLOAD_DIR, args.version)
            if build is None:
                print(f"No downloaded builds found under '{config.DEFAULT_DOWNLOAD_DIR}' for version {args.version}.")
                return 1
            print(f"--build latest -> {build} (newest downloaded build for version {args.version})")
        entries = discover_local_packages(
            config.DEFAULT_DOWNLOAD_DIR, version=args.version, build=build, distro=args.distro
        )
        if not entries:
            print(f"No downloaded packages found under '{config.DEFAULT_DOWNLOAD_DIR}' matching the given filters.")
            return 1
    results = csp.upload_tagged_packages(entries, on_progress=print)
    print(f"Uploaded {len(results)}/{len(entries)} package(s) to CSP.")
    return 0 if results else 1


def _cmd_samgr_delete(csp: CSPSAMGR, args: argparse.Namespace) -> int:
    if args.id is not None:
        ok = csp.delete_package(args.id)
        return 0 if ok else 1

    if not any([args.system_name, args.system_version, args.kernel]):
        logger.error(
            "Refusing to delete every auto-tagged package system-wide -- provide --id, or "
            "at least one of --system-name, --system-version, --kernel."
        )
        return 2

    if args.system_name and args.system_name.startswith("auto-"):
        # delete_tagged_packages() prepends 'auto-' itself; passing the prefixed value
        # through would match 'auto-auto-...' and silently delete nothing.
        args.system_name = args.system_name[len("auto-"):]
        print(f"--system-name: 'auto-' is added automatically -- matching osName 'auto-{args.system_name}'.")

    deleted = csp.delete_tagged_packages(
        os_type=args.system, os_name=args.system_name, os_version=args.system_version, os_kernel=args.kernel,
    )
    for pk_id in deleted:
        print(f"id={pk_id}: deleted")
    filters = ", ".join(
        f"{k}='{v}'" for k, v in
        (("system_name", args.system_name), ("system_version", args.system_version), ("kernel", args.kernel))
        if v is not None
    )
    print(f"Deleted {len(deleted)} auto-tagged package(s) ({filters}).")
    return 0


def _cmd_samgr_download(csp: CSPSAMGR, args: argparse.Namespace) -> int:
    owner = csp.get_owner_id(CSP_CUSTOMER_UNITNAME)
    if owner is None:
        return 1
    local_path = csp.download_package(args.id, config.CSP_DOWNLOAD_DIR, owner=owner)
    if local_path is None:
        return 1
    print(local_path)
    return 0


def _cmd_customer_devices(csp: CSPCustomer, args: argparse.Namespace) -> int:
    for device in csp.get_device_list():
        print(device)
    return 0


def _cmd_customer_activate(csp: CSPCustomer, args: argparse.Namespace) -> int:
    with open(args.file, "rb") as f:
        dat = f.read()
    ok = csp.activate_device(dat, args.device_id)
    return 0 if ok else 1


def _cmd_customer_delete(csp: CSPCustomer, args: argparse.Namespace) -> int:
    ok = csp.delete_device(args.device_id)
    return 0 if ok else 1


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="CLI for the CSP Customer portal and SAMGR package server.")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Show full HTTP debug output (quiet by default)."
    )
    top = parser.add_subparsers(dest="group")

    samgr = top.add_parser("samgr", help="SAMGR package management.")
    samgr_sub = samgr.add_subparsers(dest="command")
    samgr.set_defaults(func=lambda csp, args: (samgr.print_help(), 1)[1])

    samgr_sub.add_parser("list", help="List all packages on the server.").set_defaults(func=_cmd_samgr_list)

    info = samgr_sub.add_parser("info", help="Show detailed info for one package.")
    info.add_argument("--id", type=int, required=True, help="Package id.")
    info.set_defaults(func=_cmd_samgr_info)

    upload = samgr_sub.add_parser(
        "upload",
        help="Upload a single file (--file), or batch-discover already-downloaded package(s) "
        "from var/downloads/release (--version + --build).",
    )
    upload.add_argument("--file", help="A single file to upload (alternative to batch discovery below).")
    upload.add_argument(
        "--version",
        help="Without --file, required -- restricts batch discovery to this version. With --file, "
        "optional -- used (with --build) to build pkVersion and tag the upload.",
    )
    upload.add_argument(
        "--build",
        help="Without --file, required -- restricts batch discovery to this build; 'latest' picks the "
        "newest build already downloaded for --version. With --file, "
        "optional -- used (with --version) to build pkVersion and tag the upload.",
    )
    upload.add_argument(
        "--distro",
        help="Distro name. With --file, derives osName/osVersion/osKernel from it (skip for non-qdocse files, "
        "e.g. a Windows zip -- use --os-name instead). Without --file, filters batch discovery down to one distro.",
    )
    upload.add_argument(
        "--os-name",
        help="With --file only: explicit osName, alternative to --distro for files that don't follow the "
        "qdocse distro convention (e.g. a Windows package).",
    )
    upload.add_argument("--os-version", default="", help="With --file + --os-name: osVersion (default: '').")
    upload.add_argument("--os-kernel", default="default", help="With --file + --os-name: osKernel (default: 'default').")
    upload.add_argument(
        "--os-type", type=int, default=0, help="With --file + --os-name: osType, e.g. 0=Linux, 1=Windows (default: 0)."
    )
    upload.set_defaults(func=_cmd_samgr_upload)

    delete = samgr_sub.add_parser(
        "delete",
        help="Delete a single package by id (--id), or bulk-delete automation-uploaded packages "
        "matching any combination of System/System Name/System Version/Kernel filters.",
    )
    delete.add_argument("--id", type=int, help="Package id to delete directly (alternative to bulk matching below).")
    delete.add_argument(
        "--system", type=int, default=0, metavar="OSTYPE",
        help="Bulk mode only: osType filter (0=Linux, default: 0).",
    )
    delete.add_argument(
        "--system-name", metavar="NAME",
        help="Bulk mode only: osName filter -- the release identity, e.g. '3.2.0-148' (see "
        "csp.upload_tagged_packages()). The 'auto-' tag prefix is added automatically (a "
        "redundant leading 'auto-' in the value is stripped). Alone (no --system-version/"
        "--kernel), matches every distro/kernel published for that release -- i.e. "
        "'unpublish this whole release'.",
    )
    delete.add_argument(
        "--system-version", metavar="VERSION",
        help="Bulk mode only: osVersion filter -- the distro identity, e.g. 'CentOS-7.3' "
        "(exact match), narrows within --system-name.",
    )
    delete.add_argument(
        "--kernel", metavar="KERNEL",
        help="Bulk mode only: osKernel filter, narrows to one exact kernel (the finest level).",
    )
    delete.set_defaults(func=_cmd_samgr_delete)

    download = samgr_sub.add_parser("download", help="Download a package file by id into var/downloads/csp.")
    download.add_argument("--id", type=int, required=True, help="Package id.")
    download.set_defaults(func=_cmd_samgr_download)

    customer = top.add_parser("customer", help="CSP Customer portal device management.")
    customer_sub = customer.add_subparsers(dest="command")
    customer.set_defaults(func=lambda csp, args: (customer.print_help(), 1)[1])

    customer_sub.add_parser("devices", help="List devices.").set_defaults(func=_cmd_customer_devices)

    activate = customer_sub.add_parser("activate", help="Activate a device with a license file.")
    activate.add_argument("--file", required=True, help="Path to the license file.")
    activate.add_argument("--device-id", type=int, required=True, help="Device id.")
    activate.set_defaults(func=_cmd_customer_activate)

    delete_device = customer_sub.add_parser("delete", help="Delete a device by id.")
    delete_device.add_argument("--device-id", type=int, required=True, help="Device id.")
    delete_device.set_defaults(func=_cmd_customer_delete)

    return parser


def main(argv: Optional[list] = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    config.configure_logging(args.verbose)

    if args.group is None:
        parser.print_help()
        return 1
    if args.command is None:
        return args.func(None, args)

    if args.group == "samgr":
        csp: Any = CSPSAMGR()
    else:
        csp = CSPCustomer()

    if not csp.login():
        return 1

    return args.func(csp, args)


if __name__ == "__main__":
    sys.exit(main())
