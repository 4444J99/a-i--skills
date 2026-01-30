from __future__ import annotations

import os
import subprocess
import sys


USAGE = """Usage:
  python scripts/guard.py install [--force]
  python scripts/guard.py scan [--root PATH] [--history-dir PATH] [--format text|markdown]
  python scripts/guard.py uninstall
"""


def script_path(name: str) -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), name))


def run_python(script: str, args: list[str]) -> int:
    return subprocess.call([sys.executable, script, *args])


def main() -> int:
    args = sys.argv[1:]
    command = args[0] if args else "install"
    command_args = args[1:] if args else []

    if command in {"-h", "--help", "help"}:
        print(USAGE)
        return 0

    if command in {"scan", "check"}:
        return run_python(script_path("scan.py"), command_args)

    if command in {"install", "uninstall"}:
        return run_python(script_path("setup.py"), [command, *command_args])

    print(f"specstory-guard: unknown command '{command}'", file=sys.stderr)
    print(USAGE, file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
