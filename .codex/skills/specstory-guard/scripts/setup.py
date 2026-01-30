from __future__ import annotations

import argparse
import os
import shutil
import stat
import subprocess
import sys


HOOK_MARKER = "specstory-guard"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install specstory-guard git hooks.")
    subparsers = parser.add_subparsers(dest="command")

    install = subparsers.add_parser("install", help="Install the pre-commit hook")
    install.add_argument("--force", action="store_true", help="Overwrite existing hook")

    subparsers.add_parser("uninstall", help="Remove the pre-commit hook")

    args = parser.parse_args()
    if args.command is None:
        args.command = "install"
        args.force = False
    return args


def repo_root() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except (subprocess.SubprocessError, FileNotFoundError):
        return os.getcwd()


def skill_root() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def hook_source_path(hook_name: str) -> str:
    return os.path.join(skill_root(), "hooks", hook_name)


def hook_dest_path(root: str, hook_name: str) -> str:
    return os.path.join(root, ".git", "hooks", hook_name)


def ensure_executable(path: str) -> None:
    current = os.stat(path).st_mode
    os.chmod(path, current | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def is_guard_hook(path: str) -> bool:
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            return HOOK_MARKER in handle.read()
    except OSError:
        return False


def install_hook(root: str, hook_name: str, force: bool) -> int:
    source = hook_source_path(hook_name)
    destination = hook_dest_path(root, hook_name)

    if not os.path.isfile(source):
        print(f"specstory-guard: missing hook template at {source}", file=sys.stderr)
        return 1

    os.makedirs(os.path.dirname(destination), exist_ok=True)

    if os.path.exists(destination) and not force and not is_guard_hook(destination):
        print(
            "specstory-guard: existing hook found; use --force to overwrite",
            file=sys.stderr,
        )
        return 1

    shutil.copyfile(source, destination)
    ensure_executable(destination)
    print(f"specstory-guard: installed {hook_name} hook")
    return 0


def uninstall_hook(root: str, hook_name: str) -> int:
    destination = hook_dest_path(root, hook_name)
    if not os.path.exists(destination):
        print("specstory-guard: hook not installed")
        return 0

    if not is_guard_hook(destination):
        print(
            "specstory-guard: hook not managed by specstory-guard; refusing to remove",
            file=sys.stderr,
        )
        return 1

    os.remove(destination)
    print(f"specstory-guard: removed {hook_name} hook")
    return 0


def main() -> int:
    args = parse_args()
    root = repo_root()
    hook_name = "pre-commit"

    if args.command == "install":
        return install_hook(root, hook_name, args.force)
    if args.command == "uninstall":
        return uninstall_hook(root, hook_name)

    print("specstory-guard: unknown command", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
