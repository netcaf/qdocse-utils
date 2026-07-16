#!/usr/bin/env python3
"""Single entry point for every CLI in this repo: `qdu.py <command> ...` maps the first
argument to the module of the same name and hands the remaining args to that module's
existing main(argv), so `qdu.py csp samgr list` is exactly `python csp.py samgr list`.
Each module stays independently runnable (DESIGN.md §1) -- this file adds one place to
discover and run everything; it replaces nothing.

Modules are imported lazily, one per invocation, so no command pays the import cost
(paramiko, requests, gmssl, ...) -- or a broken import -- of the other six.
"""

import importlib
import os
import sys

# One entry per CLI module, ordered by lifecycle flow: fetch a build (release/csp),
# inspect the machine (target), operate on it (console/lifecycle), fan out (fleet);
# remote last as the low-level escape hatch. Summaries mirror each module's own
# argparse description.
COMMANDS = {
    "release": "Browse and download packages from the release archive.",
    "csp": "CSP Customer portal and SAMGR package server.",
    "target": "Detect a target's OS/distro and resolve it to a release package.",
    "console": "Run QDocSEConsole commands on a target host over SSH.",
    "lifecycle": "Install/upgrade/uninstall QDocSE on a target host.",
    "fleet": "Run lifecycle operations across the whole fleet of targets.",
    "remote": "Run a command on a remote Linux host over SSH.",
}

PROG = os.path.basename(sys.argv[0])


def _print_help(file=sys.stdout) -> None:
    width = max(map(len, COMMANDS))
    lines = [f"usage: {PROG} <command> [args...]", "", "Commands:"]
    lines += [f"  {name:<{width}}  {summary}" for name, summary in COMMANDS.items()]
    lines += ["", f"Run '{PROG} <command> --help' for details on a command."]
    print("\n".join(lines), file=file)


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if not argv:
        _print_help()
        return 1
    if argv[0] in ("-h", "--help", "help"):
        _print_help()
        return 0
    name, rest = argv[0], argv[1:]
    if name not in COMMANDS:
        print(f"{PROG}: unknown command '{name}'\n", file=sys.stderr)
        _print_help(file=sys.stderr)
        return 2
    # argparse derives its usage/help prog from basename(sys.argv[0]); rewrite it so the
    # delegated module's --help reads "qdu.py <command> ..." instead of a bare "qdu.py ...".
    sys.argv[0] = f"{PROG} {name}"
    return importlib.import_module(name).main(rest)


if __name__ == "__main__":
    sys.exit(main())
