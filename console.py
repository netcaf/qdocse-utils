"""Client + CLI for running QDocSEConsole commands on a target host over SSH.

Each function below builds one QDocSEConsole invocation, runs it via RemoteHost, and parses
the raw stdout into the data actually useful to a caller (a mode string, an expiry date, the
list of authorized programs, ...) rather than leaving every caller to re-parse the same text.
raw() is the escape hatch for any subcommand not wrapped below -- see DESIGN.md SS5.2 for why
this stays one flat file of plain functions instead of a class-per-command package: the
project's other modules don't need it, and adding a command here only ever means adding one
function plus one CLI entry.

Deliberately depends on nothing but remote.py/config.py (not target.py) -- see DESIGN.md
SS1's dependency graph. This module only ever talks to the target (C); it has no idea A/B exist.
"""

import argparse
import getpass
import logging
import re
import shlex
import sys
from typing import Optional

import paramiko

import config
from remote import CommandResult, RemoteHost

logger = logging.getLogger(__name__)

CONSOLE_BIN = "QDocSEConsole"

_MODE_RE = re.compile(r"\b(unlicensed|de-elevated|elevated|learning)\b", re.IGNORECASE)
_VERSION_RE = re.compile(r"QDocument Version:\s*(\S+)\s+Build Time:\s*(\S+)\s+Commit:\s*(\S+)")
_EXPIRY_RE = re.compile(r"expir\w*\s*:?\s*(.+)", re.IGNORECASE)
_SECTION_DELIM_RE = re.compile(r"^#+\s*$", re.MULTILINE)

# bash's standard "command not found" exit code -- the one signal every command below checks
# to recognize "QDocSE isn't installed on this target" consistently, instead of each function
# leaking its own raw shell error text.
_NOT_INSTALLED_EXIT_CODE = 127
_NOT_INSTALLED_MESSAGE = "QDocSE is not installed on this target (QDocSEConsole not found on PATH)."


def run_console(remote: RemoteHost, args: list, timeout: int = 60) -> CommandResult:
    """Runs `QDocSEConsole -c <args...>` on remote. Every command below is one call to this.

    Wrapped in `bash -lc` so QDocSEConsole is on PATH for a non-interactive SSH session
    (plain exec_command doesn't source profile scripts).
    """
    argv = [CONSOLE_BIN, "-c", *args]
    command = " ".join(shlex.quote(a) for a in argv)
    return remote.run(f"bash -lc {shlex.quote(command)}", timeout=timeout)


def is_not_installed(result: CommandResult) -> bool:
    """The one check every function below uses to recognize 'QDocSE isn't installed' --
    single source of truth so that signal is detected the same way everywhere."""
    return result.exit_code == _NOT_INSTALLED_EXIT_CODE


def _error_message(result: CommandResult) -> str:
    """Common failure message for every command below. Normalizes the 'not installed' case
    to one fixed message instead of leaking the shell's raw 'command not found' text."""
    if is_not_installed(result):
        return _NOT_INSTALLED_MESSAGE
    return result.stderr.strip() or result.stdout.strip()


def show_mode(remote: RemoteHost) -> str:
    """Returns 'unlicensed' | 'de-elevated' | 'elevated' | 'learning' | 'not_installed' | 'unknown'.

    'not_installed' is reported distinctly from 'unknown' (the binary ran but its output
    didn't match any known mode) -- they're not the same thing: one means "there is no mode,
    nothing is installed", the other means "something unexpected happened while QDocSE
    presumably *is* installed".
    """
    result = run_console(remote, ["show_mode"])
    match = _MODE_RE.search(result.stdout)
    if match:
        return match.group(1).lower()
    if is_not_installed(result):
        return "not_installed"
    return "unknown"


def version(remote: RemoteHost) -> dict:
    """Parses `-c version`'s 'QDocument Version: X Build Time: Y Commit: Z' line."""
    result = run_console(remote, ["version"])
    data = {"raw": result.stdout.strip()}
    match = _VERSION_RE.search(result.stdout)
    if match:
        data["version"], data["build_time"], data["commit"] = match.groups()
    elif not result.ok:
        data["error"] = _error_message(result)
    return data


def view(remote: RemoteHost) -> dict:
    """Parses `-c view`'s '#'*N-delimited sections into program lists + license/mode fields.

    Output looks like:
        ################################################################################
        List of programs authorized to access protected data files:
        <one program per line, or nothing>
        ################################################################################
        ...
        ################################################################################
        License Expires   : No License
        License Type      : none
        ...
        ################################################################################
    """
    result = run_console(remote, ["view"])
    text = result.stdout
    data: dict = {"raw": text.strip()}
    for chunk in _SECTION_DELIM_RE.split(text):
        lines = [line.strip() for line in chunk.splitlines() if line.strip()]
        if not lines:
            continue
        header = lines[0].lower()
        if header.startswith("list of programs authorized"):
            data["authorized_programs"] = lines[1:]
        elif header.startswith("list of programs denied"):
            data["denied_programs"] = lines[1:]
        elif header.startswith("list of watch points"):
            data["watch_points"] = lines[1:]
        elif ":" in lines[0]:
            # Key/value section (License Expires, License Type, Encryption Cipher, ...).
            for line in lines:
                if ":" in line:
                    key, _, value = line.partition(":")
                    data[key.strip().lower().replace(" ", "_")] = value.strip()
    if len(data) == 1 and not result.ok:  # only "raw", and the command itself failed
        data["error"] = _error_message(result)
    return data


def activate(remote: RemoteHost, file: str, duration: str) -> dict:
    """`-c activate -f <file> -t <duration>`. duration e.g. '9d', '6h', '300m'."""
    result = run_console(remote, ["activate", "-f", file, "-t", duration])
    data = {"activated": result.ok, "raw": result.stdout.strip()}
    match = _EXPIRY_RE.search(result.stdout)
    if match:
        data["expiry"] = match.group(1).strip()
    if not result.ok:
        data["error"] = _error_message(result)
    return data


def elevate(remote: RemoteHost, file: str, duration: str) -> dict:
    """`-c elevate -ef <file> -t <duration>`. Moves De-elevated -> Elevated."""
    result = run_console(remote, ["elevate", "-ef", file, "-t", duration])
    data = {"elevated": result.ok, "raw": result.stdout.strip()}
    if not result.ok:
        data["error"] = _error_message(result)
    return data


def renewrequest(remote: RemoteHost, remote_path: str = "/tmp/qdocse_renew_request.txt") -> dict:
    """`-c renewrequest -rf <remote_path>`. Returns the pending-renewal request number
    (the file's first line) that a matching renewal .dat must be encoded with as its
    qid -- NOT the device's real qid. See helpers/codec.py's LicKind.RENEWAL docstring."""
    result = run_console(remote, ["renewrequest", "-rf", remote_path])
    if not result.ok:
        return {"ok": False, "error": _error_message(result)}
    try:
        raw_content = remote.read_remote_prefix(remote_path, 256).decode().strip()
    except OSError as e:
        return {"ok": False, "error": f"could not read {remote_path}: {e}"}
    lines = [line for line in raw_content.splitlines() if line.strip()]
    if not lines:
        return {"ok": False, "error": f"{remote_path} was empty"}
    try:
        request_number = int(lines[0])
    except ValueError:
        return {"ok": False, "error": f"unexpected renewrequest content: {raw_content!r}"}
    return {"ok": True, "request_number": request_number, "raw": raw_content}


def renewcommit(remote: RemoteHost, file: str) -> dict:
    """`-c renewcommit -f <file>`. Applies a renewal file encoded for the request
    number returned by renewrequest()."""
    result = run_console(remote, ["renewcommit", "-f", file])
    data = {"ok": result.ok, "raw": result.stdout.strip()}
    if not result.ok:
        data["error"] = _error_message(result)
    return data


def finalize(remote: RemoteHost) -> dict:
    """`-c finalize`. Returns to De-elevated mode, ending Elevated/Learning early."""
    result = run_console(remote, ["finalize"])
    data = {"ok": result.ok, "raw": result.stdout.strip()}
    if not result.ok:
        data["error"] = _error_message(result)
    return data


def install_prep(remote: RemoteHost, mode: str) -> dict:
    """`-c install_prep <on|off>`. Only valid in Elevated/Learning; 'on' requires a reboot
    before an upgrade/uninstall, and expires (re-establishing full security) after 40 minutes
    if that reboot doesn't happen. Aliases uninstall_prep/upgrade_prep are the same command."""
    if mode not in ("on", "off"):
        raise ValueError(f"install_prep mode must be 'on' or 'off', got: {mode!r}")
    result = run_console(remote, ["install_prep", mode])
    data = {"ok": result.ok, "raw": result.stdout.strip()}
    if not result.ok:
        data["error"] = _error_message(result)
    return data


def raw(remote: RemoteHost, args: list) -> CommandResult:
    """Passthrough for any subcommand not wrapped above, e.g. raw(remote, ["list_acls"])."""
    return run_console(remote, args)


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


def _print_dict(data: dict) -> None:
    for key, value in data.items():
        if key == "raw":
            continue
        if isinstance(value, list):
            print(f"{key}:")
            for item in value:
                print(f"  - {item}")
        else:
            print(f"{key}: {value}")


def _cmd_show_mode(remote: RemoteHost, args: argparse.Namespace) -> int:
    mode = show_mode(remote)
    if mode == "not_installed":
        print(f"error: {_NOT_INSTALLED_MESSAGE}")
        return 1
    if mode == "unknown":
        print("error: show_mode returned unrecognized output.")
        return 1
    print(mode)
    return 0


def _cmd_version(remote: RemoteHost, args: argparse.Namespace) -> int:
    data = version(remote)
    _print_dict(data)
    return 1 if "error" in data else 0


def _cmd_view(remote: RemoteHost, args: argparse.Namespace) -> int:
    data = view(remote)
    _print_dict(data)
    return 1 if "error" in data else 0


def _cmd_activate(remote: RemoteHost, args: argparse.Namespace) -> int:
    data = activate(remote, args.file, args.duration)
    _print_dict(data)
    return 0 if data["activated"] else 1


def _cmd_elevate(remote: RemoteHost, args: argparse.Namespace) -> int:
    data = elevate(remote, args.file, args.duration)
    _print_dict(data)
    return 0 if data["elevated"] else 1


def _cmd_renewrequest(remote: RemoteHost, args: argparse.Namespace) -> int:
    data = renewrequest(remote, args.remote_file)
    _print_dict(data)
    return 0 if data["ok"] else 1


def _cmd_renewcommit(remote: RemoteHost, args: argparse.Namespace) -> int:
    data = renewcommit(remote, args.file)
    _print_dict(data)
    return 0 if data["ok"] else 1


def _cmd_finalize(remote: RemoteHost, args: argparse.Namespace) -> int:
    data = finalize(remote)
    _print_dict(data)
    return 0 if data["ok"] else 1


def _cmd_install_prep(remote: RemoteHost, args: argparse.Namespace) -> int:
    data = install_prep(remote, args.mode)
    _print_dict(data)
    return 0 if data["ok"] else 1


def _cmd_raw(remote: RemoteHost, args: argparse.Namespace) -> int:
    # argparse.REMAINDER captures a leading '--' separator literally; strip it so
    # `console.py raw --host X -- list_acls` doesn't pass '--' to QDocSEConsole itself.
    console_args = args.console_args[1:] if args.console_args[:1] == ["--"] else args.console_args
    result = raw(remote, console_args)
    sys.stdout.write(result.stdout)
    sys.stderr.write(result.stderr)
    return result.exit_code


def _add_connection_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--host", required=True, help="Target hostname or IP.")
    parser.add_argument("--port", type=int, help="SSH port (default: from targets.toml, or 22).")
    parser.add_argument("--user", help="SSH username (default: from targets.toml).")
    auth = parser.add_mutually_exclusive_group()
    auth.add_argument("--password", help="SSH password (default: from targets.toml, or prompted).")
    auth.add_argument("--key-file", help="Path to an SSH private key file.")


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run QDocSEConsole commands on a target host over SSH.")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Show full SSH debug output (quiet by default)."
    )

    # Connection args live on each subparser (not the top-level parser) so they can be given
    # either before or after the subcommand, e.g. both of these work:
    #   console.py --host X show_mode
    #   console.py show_mode --host X
    subparsers = parser.add_subparsers(dest="command")

    show_mode_p = subparsers.add_parser(
        "show_mode", help="Print the current QDocSE mode (or 'not_installed' if it isn't installed)."
    )
    _add_connection_args(show_mode_p)
    show_mode_p.set_defaults(func=_cmd_show_mode)

    version_p = subparsers.add_parser("version", help="Print QDocSE version/build info.")
    _add_connection_args(version_p)
    version_p.set_defaults(func=_cmd_version)

    view_p = subparsers.add_parser(
        "view", help="Print authorized/denied programs, watch points, and license/mode info."
    )
    _add_connection_args(view_p)
    view_p.set_defaults(func=_cmd_view)

    activate_p = subparsers.add_parser("activate", help="Apply a license/activation file.")
    _add_connection_args(activate_p)
    activate_p.add_argument("--file", required=True, help="Path to the license/activation file (on the target).")
    activate_p.add_argument("--duration", required=True, help="Elevation time, e.g. 9d, 6h, 300m.")
    activate_p.set_defaults(func=_cmd_activate)

    elevate_p = subparsers.add_parser("elevate", help="Apply an elevation file (De-elevated -> Elevated).")
    _add_connection_args(elevate_p)
    elevate_p.add_argument("--file", required=True, help="Path to the elevation file (on the target).")
    elevate_p.add_argument("--duration", required=True, help="Elevation time, e.g. 9d, 6h, 300m.")
    elevate_p.set_defaults(func=_cmd_elevate)

    renewrequest_p = subparsers.add_parser(
        "renewrequest", help="Generate a pending-renewal request number (for renewcommit)."
    )
    _add_connection_args(renewrequest_p)
    renewrequest_p.add_argument(
        "--remote-file", default="/tmp/qdocse_renew_request.txt",
        help="Remote path to write the request file to (default: /tmp/qdocse_renew_request.txt).",
    )
    renewrequest_p.set_defaults(func=_cmd_renewrequest)

    renewcommit_p = subparsers.add_parser("renewcommit", help="Apply a renewal file.")
    _add_connection_args(renewcommit_p)
    renewcommit_p.add_argument("--file", required=True, help="Path to the renewal file (on the target).")
    renewcommit_p.set_defaults(func=_cmd_renewcommit)

    finalize_p = subparsers.add_parser("finalize", help="Return to De-elevated mode early.")
    _add_connection_args(finalize_p)
    finalize_p.set_defaults(func=_cmd_finalize)

    install_prep_p = subparsers.add_parser(
        "install_prep", help="Prepare for upgrade/uninstall (Elevated/Learning only; requires a reboot after)."
    )
    _add_connection_args(install_prep_p)
    install_prep_p.add_argument("mode", choices=["on", "off"])
    install_prep_p.set_defaults(func=_cmd_install_prep)

    raw_p = subparsers.add_parser("raw", help="Run any QDocSEConsole subcommand not wrapped above.")
    _add_connection_args(raw_p)
    raw_p.add_argument("console_args", nargs=argparse.REMAINDER, help="Args passed after '-c', e.g. list_acls")
    raw_p.set_defaults(func=_cmd_raw)

    return parser


def main(argv: Optional[list] = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    config.configure_logging(args.verbose)

    if args.command is None:
        parser.print_help()
        return 1

    connect_kwargs = _connect_kwargs(args)
    try:
        with RemoteHost(**connect_kwargs) as remote:
            return args.func(remote, args)
    except (paramiko.SSHException, OSError) as e:
        logger.error(f"SSH connection failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
