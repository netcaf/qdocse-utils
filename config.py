"""Loads release_server.toml / csp.toml / targets.toml, resolving credentials from secrets.toml.

Each config file resolves independently, per file: an override in the current working
directory (./targets.toml, ./secrets.toml, ...) wins over the repo's config/ default, so a
per-fleet workspace directory can carry its own targets while still sharing e.g. the repo's
credentials. Writes go back to whichever file was resolved. See _config_path().
"""

import logging
import os
import re
import sys
import tomllib
from typing import Any, Optional

logger = logging.getLogger(__name__)

CONFIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config")

# Runtime artifacts (download caches, per-host lifecycle state) live under var/ next to
# this file -- anchored to the repo, not os.getcwd(), so files land in the same place no
# matter where a command is run from, and stick around for manual inspection after a run.
VAR_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "var")

# Release-server download cache: var/downloads/release/{version}/{build}/{distro}/.
DEFAULT_DOWNLOAD_DIR = os.path.join(VAR_DIR, "downloads", "release")

# Packages re-downloaded from CSP (csp.download_package()):
# var/downloads/csp/{version}/{build}/{pkg_id}/. The pkg_id level keeps same-named
# packages for different distros apart when a parallel fleet run downloads several.
# A separate tree from the release cache so downloads.discover_local_packages() never scans
# them -- CSP filenames are pk_names (no .rpm/.deb suffix, no .kernel sidecar), not cache entries.
CSP_DOWNLOAD_DIR = os.path.join(VAR_DIR, "downloads", "csp")


def configure_logging(verbose: bool = False) -> None:
    """Quiet by default (only warnings/errors) so CLI output stays readable at a glance;
    -v/--verbose shows full SSH/SFTP protocol detail for troubleshooting."""
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.WARNING,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


# Effective paths already announced this process, so each file is reported once, not on
# every load (find_target() alone reloads targets.toml per host).
_announced_paths: set = set()


def _config_path(filename: str) -> str:
    """Resolves a config filename: ./<filename> in the current working directory if that
    file exists (cwd override), else the repo's config/ default.

    The effective path is reported once per process: a cwd override prints to stderr
    unconditionally -- running e.g. `fleet clean` against the wrong fleet because some
    directory happened to contain a targets.toml must never be silent -- while a
    default-path load only shows at INFO level (-v).
    """
    default_path = os.path.join(CONFIG_DIR, filename)
    cwd_path = os.path.abspath(filename)
    if cwd_path != default_path and os.path.isfile(cwd_path):
        if cwd_path not in _announced_paths:
            _announced_paths.add(cwd_path)
            print(f"config: using {cwd_path} (cwd override)", file=sys.stderr)
        return cwd_path
    if default_path not in _announced_paths:
        _announced_paths.add(default_path)
        logger.info(f"config: {filename} -> {default_path}")
    return default_path


def _load_toml(filename: str) -> dict:
    with open(_config_path(filename), "rb") as f:
        return tomllib.load(f)


def _toml_value(value) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    return '"' + str(value).replace("\\", "\\\\").replace('"', '\\"') + '"'


def _dump_table(table: dict) -> str:
    return "\n".join(f"{k} = {_toml_value(v)}" for k, v in table.items())


def _dump_toml(doc: dict) -> str:
    """Minimal TOML serializer: handles flat keys, one level of [section] tables,
    and one level of [[array]] tables -- sufficient for this project's config files."""
    lines = []
    scalars = {k: v for k, v in doc.items() if not isinstance(v, (dict, list))}
    if scalars:
        lines.append(_dump_table(scalars))
    for key, value in doc.items():
        if isinstance(value, dict):
            lines.append(f"\n[{key}]")
            lines.append(_dump_table(value))
        elif isinstance(value, list):
            for item in value:
                lines.append(f"\n[[{key}]]")
                lines.append(_dump_table(item))
    return "\n".join(lines) + "\n"


def _write_toml(filename: str, doc: dict) -> None:
    # Same resolution as reads, so an edit lands in the file it was loaded from -- reading
    # a cwd-override targets.toml but writing the repo default would silently fork the two.
    with open(_config_path(filename), "w") as f:
        f.write(_dump_toml(doc))


def _load_secrets() -> dict:
    try:
        return _load_toml("secrets.toml")
    except FileNotFoundError:
        return {}


def _resolve(entry: dict, secrets: dict) -> dict:
    """Merge a structural entry with its secret (looked up by secret_ref), if any."""
    secret_ref = entry.get("secret_ref")
    resolved = dict(entry)
    if secret_ref and secret_ref in secrets:
        resolved.update(secrets[secret_ref])
    return resolved


def load_release_server() -> dict:
    """Returns release_server.toml merged with its secret (host/port/user/password/base_path)."""
    return _resolve(_load_toml("release_server.toml"), _load_secrets())


def load_csp() -> dict[str, dict]:
    """Returns {'customer': {...}, 'samgr': {...}}, each merged with its secret."""
    structure = _load_toml("csp.toml")
    secrets = _load_secrets()
    return {section: _resolve(entry, secrets) for section, entry in structure.items()}


def load_distro_map() -> dict[str, str]:
    """Returns {"{os_name}|{os_version}": distro_dir_name} from distro_map.toml."""
    try:
        structure = _load_toml("distro_map.toml")
    except FileNotFoundError:
        return {}
    return {f"{m['os_name']}|{m['os_version']}": m["distro"] for m in structure.get("mappings", [])}


def load_targets() -> list[dict]:
    """Returns a list of target dicts, each merged with [defaults] and its secret."""
    structure = _load_toml("targets.toml")
    secrets = _load_secrets()
    defaults = structure.get("defaults", {})
    targets = []
    for target in structure.get("targets", []):
        merged: dict[str, Any] = {**defaults, **target}
        targets.append(_resolve(merged, secrets))
    return targets


def add_target(host: str, port: Optional[int] = None, user: Optional[str] = None, password: Optional[str] = None) -> None:
    """Adds a target to targets.toml. Raises ValueError if host already exists.

    Only fields differing from [defaults] are stored on the entry. If a password is
    given, it's written to secrets.toml under a new secret_ref named after the host.
    """
    structure = _load_toml("targets.toml")
    targets = structure.setdefault("targets", [])
    if any(t.get("host") == host for t in targets):
        raise ValueError(f"Target '{host}' already exists.")

    defaults = structure.get("defaults", {})
    entry: dict[str, Any] = {"host": host}
    if port is not None and port != defaults.get("port"):
        entry["port"] = port
    if user is not None and user != defaults.get("user"):
        entry["user"] = user

    if password is not None:
        secret_ref = "target_" + re.sub(r"[^a-zA-Z0-9]", "_", host)
        entry["secret_ref"] = secret_ref
        secrets = _load_secrets()
        secrets[secret_ref] = {"password": password}
        _write_toml("secrets.toml", secrets)

    targets.append(entry)
    _write_toml("targets.toml", structure)


def find_target(host: str) -> dict:
    """Returns the resolved target dict for host from targets.toml, or {} if not found."""
    return next((t for t in load_targets() if t.get("host") == host), {})


def remove_target(host: str) -> None:
    """Removes a target from targets.toml by host. Raises ValueError if not found.

    Also removes the target's own secret_ref entry from secrets.toml, unless it's
    still referenced by [defaults] or another remaining target.
    """
    structure = _load_toml("targets.toml")
    targets = structure.get("targets", [])
    removed = [t for t in targets if t.get("host") == host]
    if not removed:
        raise ValueError(f"Target '{host}' not found.")

    remaining = [t for t in targets if t.get("host") != host]
    structure["targets"] = remaining
    _write_toml("targets.toml", structure)

    still_referenced = {structure.get("defaults", {}).get("secret_ref")}
    still_referenced.update(t.get("secret_ref") for t in remaining)
    for target in removed:
        secret_ref = target.get("secret_ref")
        if secret_ref and secret_ref not in still_referenced:
            secrets = _load_secrets()
            if secret_ref in secrets:
                del secrets[secret_ref]
                _write_toml("secrets.toml", secrets)
