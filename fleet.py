"""Runs lifecycle.py's single-target operations (status/uninstall/install/activate/reinstall)
across a fleet of targets, one host's failure never stopping the rest -- sequentially by
default, or up to N hosts concurrently with -j/--jobs N (each streamed line then carries
a [host] prefix, and shared package downloads dedupe via lifecycle._download_once()).

Each function here is a thin per-host loop around an existing lifecycle.py function; no
install/uninstall/activate logic lives here. See DESIGN.md SS1's dependency graph.
"""

import argparse
import logging
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Optional

import paramiko

import config
import lifecycle

logger = logging.getLogger(__name__)


def _log(msg: str, on_progress: Optional[Callable[[str], None]] = None) -> None:
    logger.info(msg)
    if on_progress:
        on_progress(msg)


def _connect_kwargs_for_host(host: str) -> dict:
    defaults = config.find_target(host)
    return {
        "host": host,
        "port": defaults.get("port", 22),
        "username": defaults.get("user"),
        "password": defaults.get("password"),
        "key_filename": None,
        "command_timeout": defaults.get("command_timeout"),
    }


def _run_per_host(
    hosts: list,
    op: Callable[[dict, Optional[Callable[[str], None]]], bool],
    on_progress: Optional[Callable[[str], None]] = None,
    on_host_result: Optional[Callable[[str, dict], None]] = None,
    on_host_start: Optional[Callable[[str], None]] = None,
    parallel: int = 1,
) -> dict:
    """Runs op(connect_kwargs, on_progress) for each host, isolating failures so one bad
    host doesn't stop the rest. Shared by clean/install/activate/provision -- status has its
    own shape (comprehensive per-host fields, not just ok/error).

    parallel=1 (the default) keeps the sequential loop and untouched output. parallel>1
    runs up to that many hosts concurrently on threads; each host's streamed lines get a
    "[host] " prefix (they interleave across hosts, so the prefix is what keeps them
    attributable) and every callback fires under one lock so lines never tear.

    on_host_start(host) fires before a host's op begins and on_host_result(host, info) as it
    completes, so a CLI can frame each host's streamed progress and verdict instead of
    staying silent until the whole fleet is done; the full results dict is still returned
    at the end.
    """
    def run_one(host: str, progress: Optional[Callable[[str], None]]) -> dict:
        try:
            ok = op(_connect_kwargs_for_host(host), progress)
            return {"ok": ok, "error": None}
        except Exception as e:
            # str(e) or ...: some failures carry no message (paramiko surfaces a target
            # rebooting mid-command as a bare EOFError) and would print an unexplained FAILED.
            return {"ok": False, "error": str(e) or type(e).__name__}

    if parallel <= 1:
        results = {}
        for host in hosts:
            if on_host_start:
                on_host_start(host)
            results[host] = run_one(host, on_progress)
            if on_host_result:
                on_host_result(host, results[host])
        return results

    lock = threading.Lock()

    def locked(fn: Optional[Callable], *args) -> None:
        if fn:
            with lock:
                fn(*args)

    def worker(host: str) -> dict:
        locked(on_host_start, host)
        progress = None
        if on_progress:
            progress = lambda msg, h=host: locked(on_progress, f"[{h}] {msg}")
        info = run_one(host, progress)
        locked(on_host_result, host, info)
        return info

    with ThreadPoolExecutor(max_workers=parallel) as pool:
        futures = {host: pool.submit(worker, host) for host in hosts}
    return {host: futures[host].result() for host in hosts}


def fleet_status(
    hosts: list,
    on_host_result: Optional[Callable[[str, dict], None]] = None,
    parallel: int = 1,
) -> dict:
    """Comprehensive read-only status for every host: system info, install status, QID,
    license mode/expiry -- lifecycle.status() run per host. Makes no changes on any target.

    on_host_result streams each host's status dict as it completes (see _run_per_host);
    with parallel>1 it fires under a lock, so a multi-line status block prints intact.
    """
    def get_one(host: str) -> dict:
        try:
            return lifecycle.status(_connect_kwargs_for_host(host))
        except Exception as e:
            return {"error": str(e) or type(e).__name__}

    if parallel <= 1:
        results = {}
        for host in hosts:
            results[host] = get_one(host)
            if on_host_result:
                on_host_result(host, results[host])
        return results

    lock = threading.Lock()

    def worker(host: str) -> dict:
        info = get_one(host)
        if on_host_result:
            with lock:
                on_host_result(host, info)
        return info

    with ThreadPoolExecutor(max_workers=parallel) as pool:
        futures = {host: pool.submit(worker, host) for host in hosts}
    return {host: futures[host].result() for host in hosts}


def fleet_clean(
    hosts: list,
    elevation_file: Optional[str] = None,
    force: bool = False,
    parallel: int = 1,
    on_progress: Optional[Callable[[str], None]] = None,
    on_host_result: Optional[Callable[[str, dict], None]] = None,
    on_host_start: Optional[Callable[[str], None]] = None,
) -> dict:
    """Uninstalls QDocSE from every host that has it installed (mode-aware, same as
    lifecycle.uninstall()).

    force=False (the default) never touches force_uninstall(), which stays manual/opt-in.
    force=True escalates a host whose mode-aware uninstall fails or errors to
    lifecycle.force_uninstall() -- which reboots that host and, if its own package
    scripts refuse, bypasses them -- so one wedged host (corrupted DB, expired license)
    still comes out clean without stopping the rest.
    """
    def op(connect_kwargs: dict, progress: Optional[Callable[[str], None]]) -> bool:
        error = None
        try:
            ok = lifecycle.uninstall(connect_kwargs, elevation_file=elevation_file, on_progress=progress)
        except Exception as e:
            if not force:
                raise
            ok, error = False, (str(e) or type(e).__name__)
        if ok or not force:
            return ok
        reason = f" ({error})" if error else ""
        _log(
            f"{connect_kwargs['host']}: mode-aware uninstall failed{reason} -- "
            "escalating to force-uninstall...",
            progress,
        )
        return lifecycle.force_uninstall(connect_kwargs, on_progress=progress)

    return _run_per_host(
        hosts, op, on_progress=on_progress, on_host_result=on_host_result,
        on_host_start=on_host_start, parallel=parallel,
    )


def fleet_install(
    hosts: list,
    version: str,
    build: str,
    source: str = "csp",
    parallel: int = 1,
    on_progress: Optional[Callable[[str], None]] = None,
    on_host_result: Optional[Callable[[str, dict], None]] = None,
    on_host_start: Optional[Callable[[str], None]] = None,
) -> dict:
    """Installs QDocSE on every host that doesn't already have it (lifecycle.install() is
    itself a no-op returning True for a host that's already installed)."""
    return _run_per_host(
        hosts,
        lambda ck, prog: lifecycle.install(ck, version, build, source=source, on_progress=prog),
        on_progress=on_progress,
        on_host_result=on_host_result,
        on_host_start=on_host_start,
        parallel=parallel,
    )


def fleet_activate(
    hosts: list,
    duration: int = 2_678_400,
    mode: int = 5,
    parallel: int = 1,
    on_progress: Optional[Callable[[str], None]] = None,
    on_host_result: Optional[Callable[[str, dict], None]] = None,
    on_host_start: Optional[Callable[[str], None]] = None,
) -> dict:
    """Activates every host via the CSP customer portal (lifecycle.activate())."""
    return _run_per_host(
        hosts,
        lambda ck, prog: lifecycle.activate(ck, duration=duration, mode=mode, on_progress=prog),
        on_progress=on_progress,
        on_host_result=on_host_result,
        on_host_start=on_host_start,
        parallel=parallel,
    )


def fleet_provision(
    hosts: list,
    version: str,
    build: str,
    source: str = "csp",
    parallel: int = 1,
    on_progress: Optional[Callable[[str], None]] = None,
    on_host_result: Optional[Callable[[str, dict], None]] = None,
    on_host_start: Optional[Callable[[str], None]] = None,
) -> dict:
    """Clean (if needed) -> install -> activate, per host. Delegates to lifecycle.reinstall()
    rather than looping fleet_clean/fleet_install/fleet_activate separately, so a host whose
    clean fails doesn't still get an install attempt -- reinstall() already short-circuits
    per host on the first failed step.
    """
    return _run_per_host(
        hosts,
        lambda ck, prog: lifecycle.reinstall(ck, version, build, source=source, do_activate=True, on_progress=prog),
        on_progress=on_progress,
        on_host_result=on_host_result,
        on_host_start=on_host_start,
        parallel=parallel,
    )


def _format_result_line(host: str, info: dict) -> str:
    if "ok" in info:
        status = "OK" if info["ok"] else "FAILED"
    else:
        status = "ERROR" if info.get("error") else "OK"
    extra = ", ".join(
        f"{k}={v}" for k, v in info.items() if k not in ("ok", "error") and v is not None
    )
    line = f"{host}: {status}"
    if extra:
        line += f" ({extra})"
    if info.get("error"):
        line += f" -- {info['error']}"
    return line


def _print_host_result(host: str, info: dict) -> None:
    print(_format_result_line(host, info))


def _host_separator_printer() -> Callable[[str], None]:
    """Returns an on_host_start callback printing a blank line between consecutive hosts'
    streamed output, so one host's progress reads apart from the next."""
    seen = 0

    def _print(host: str) -> None:
        nonlocal seen
        if seen:
            print()
        seen += 1

    return _print


def _print_fleet_summary(results: dict) -> None:
    """Compact all-hosts recap after the streamed per-host output has scrolled by.
    Skipped for a single host -- it would just repeat the line printed a moment ago.
    """
    if len(results) < 2:
        return
    print("\nSummary:")
    for host, info in results.items():
        print(f"  {_format_result_line(host, info)}")


def _add_hosts_args(parser: argparse.ArgumentParser) -> None:
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--all", action="store_true", help="Run across every target in targets.toml.")
    group.add_argument(
        "--host", action="append", default=[], metavar="HOST",
        help="Target hostname/IP (repeatable). Alternative to --all.",
    )
    parser.add_argument(
        "-j", "--jobs", type=int, default=1, metavar="N",
        help="Run up to N hosts concurrently (default: 1 = sequential; with N>1 each "
        "streamed line carries a [host] prefix).",
    )


def _resolve_hosts(args: argparse.Namespace) -> list:
    if args.all:
        return [t["host"] for t in config.load_targets()]
    return args.host


def _cmd_status(args: argparse.Namespace) -> int:
    hosts = _resolve_hosts(args)
    printed = 0

    def _print_one(host: str, info: dict) -> None:
        nonlocal printed
        if printed:
            print()
        printed += 1
        print(f"{host}:")
        if info.get("error"):
            print(f"  ERROR: {info['error']}")
            return
        for line in lifecycle.format_status(info).splitlines():
            print(f"  {line}")

    results = fleet_status(hosts, on_host_result=_print_one, parallel=max(1, args.jobs))
    return 0 if all(r.get("error") is None for r in results.values()) else 1


def _cmd_clean(args: argparse.Namespace) -> int:
    hosts = _resolve_hosts(args)
    parallel = max(1, args.jobs)
    results = fleet_clean(
        hosts, elevation_file=args.elevation_file, force=args.force, parallel=parallel,
        on_progress=print, on_host_result=_print_host_result,
        # The blank-line separator frames one host's block of output; interleaved
        # parallel output has no blocks to frame, the [host] prefix does that job.
        on_host_start=_host_separator_printer() if parallel == 1 else None,
    )
    _print_fleet_summary(results)
    return 0 if all(r["ok"] for r in results.values()) else 1


def _cmd_install(args: argparse.Namespace) -> int:
    hosts = _resolve_hosts(args)
    try:
        # Resolved once up front, not per host, so every host in this run gets the same build.
        build = lifecycle.resolve_build(args.version, args.build, args.source, print)
    except (RuntimeError, ValueError) as e:
        logger.error(str(e))
        return 1
    parallel = max(1, args.jobs)
    results = fleet_install(
        hosts, args.version, build, source=args.source, parallel=parallel, on_progress=print,
        on_host_result=_print_host_result,
        on_host_start=_host_separator_printer() if parallel == 1 else None,
    )
    _print_fleet_summary(results)
    return 0 if all(r["ok"] for r in results.values()) else 1


def _cmd_activate(args: argparse.Namespace) -> int:
    hosts = _resolve_hosts(args)
    parallel = max(1, args.jobs)
    results = fleet_activate(
        hosts, duration=args.duration, mode=args.mode, parallel=parallel, on_progress=print,
        on_host_result=_print_host_result,
        on_host_start=_host_separator_printer() if parallel == 1 else None,
    )
    _print_fleet_summary(results)
    return 0 if all(r["ok"] for r in results.values()) else 1


def _cmd_provision(args: argparse.Namespace) -> int:
    hosts = _resolve_hosts(args)
    try:
        # Resolved once up front, not per host, so every host in this run gets the same build.
        build = lifecycle.resolve_build(args.version, args.build, args.source, print)
    except (RuntimeError, ValueError) as e:
        logger.error(str(e))
        return 1
    parallel = max(1, args.jobs)
    results = fleet_provision(
        hosts, args.version, build, source=args.source, parallel=parallel, on_progress=print,
        on_host_result=_print_host_result,
        on_host_start=_host_separator_printer() if parallel == 1 else None,
    )
    _print_fleet_summary(results)
    return 0 if all(r["ok"] for r in results.values()) else 1


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Runs lifecycle.py operations (status/clean/install/activate/provision) across a fleet of targets."
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Show full SSH debug output (quiet by default)."
    )
    subparsers = parser.add_subparsers(dest="command")
    parser.set_defaults(func=lambda args: (parser.print_help(), 1)[1])

    status = subparsers.add_parser(
        "status",
        help="Read-only: comprehensive per-host status (system info, install, QID, license mode/expiry).",
    )
    _add_hosts_args(status)
    status.set_defaults(func=_cmd_status)

    clean = subparsers.add_parser(
        "clean",
        help="Uninstall QDocSE from every target that has it installed (mode-aware; "
        "add --force to escalate wedged hosts).",
    )
    _add_hosts_args(clean)
    clean.add_argument(
        "--elevation-file",
        help="Local path to an externally-issued elevation file; if omitted and a target is "
        "De-elevated, one is generated locally instead.",
    )
    clean.add_argument(
        "--force",
        action="store_true",
        help="Escalate a host whose mode-aware uninstall fails to lifecycle's force-uninstall: "
        "reboots that host and bypasses the package's own scripts if they refuse.",
    )
    clean.set_defaults(func=_cmd_clean)

    install = subparsers.add_parser("install", help="Install QDocSE on every target that doesn't already have it.")
    _add_hosts_args(install)
    install.add_argument("--version", required=True, help="Release version (e.g. 3.2.0).")
    install.add_argument("--build", required=True, help="Build number, or 'latest' for the newest build on --source.")
    install.add_argument(
        "--source", choices=["csp", "release"], default="csp", help="Resolve+download from CSP (default) or the release server."
    )
    install.set_defaults(func=_cmd_install)

    activate = subparsers.add_parser("activate", help="Activate every target via the CSP customer portal.")
    _add_hosts_args(activate)
    activate.add_argument("--duration", type=int, default=2_678_400, help="License validity in seconds (default: 2678400 = 31 days).")
    activate.add_argument("--mode", type=int, default=5, help="License mode field baked into the .dat (default: 5).")
    activate.set_defaults(func=_cmd_activate)

    provision = subparsers.add_parser(
        "provision", help="Clean (if installed) -> install -> activate, per target."
    )
    _add_hosts_args(provision)
    provision.add_argument("--version", required=True, help="Release version (e.g. 3.2.0).")
    provision.add_argument("--build", required=True, help="Build number, or 'latest' for the newest build on --source.")
    provision.add_argument(
        "--source", choices=["csp", "release"], default="csp", help="Resolve+download from CSP (default) or the release server."
    )
    provision.set_defaults(func=_cmd_provision)

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
