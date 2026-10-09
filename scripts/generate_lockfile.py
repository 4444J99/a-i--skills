#!/usr/bin/env python3
"""Generate a complete content-and-executable-mode lock for admitted sources."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from skill_lib import find_plugin_dirs, skill_collections

ROOT = Path(__file__).resolve().parents[1]
BUILD_DIR = ROOT / "distributions"
SKILLS_DIR = ROOT / "skills"
LOCK_FILE = BUILD_DIR / "skills-lock.json"
HASH_ALGORITHM = "sha256-tree-v2"


def _file_records(directory: Path) -> list[dict]:
    """Describe every regular file by relative path, bytes, and executable bit.

    No filename concatenation ambiguity, host paths, mtimes, or UID/GID values
    participate in the digest. Symlinks and special files are not installable
    canonical source and fail instead of escaping the folder being locked.
    """
    if directory.is_symlink() or not directory.is_dir():
        raise ValueError(f"Expected a real source directory: {directory}")
    result = []
    for path in sorted(directory.rglob("*"), key=lambda p: p.relative_to(directory).as_posix()):
        if path.is_symlink():
            raise ValueError(f"Source contains a symlink: {path}")
        if path.is_dir():
            continue
        if not path.is_file():
            raise ValueError(f"Source contains a non-regular file: {path}")
        data = path.read_bytes()
        result.append({
            "path": path.relative_to(directory).as_posix(),
            "sha256": hashlib.sha256(data).hexdigest(),
            "size": len(data),
            "executable": bool(path.stat().st_mode & 0o111),
        })
    return result


def _hash_records(records: list[dict]) -> str:
    encoded = json.dumps(records, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(HASH_ALGORITHM.encode("ascii") + b"\0" + encoded).hexdigest()


def _sha256_tree(directory: Path) -> str:
    return _hash_records(_file_records(directory))


def _locked_folder(directory: Path, root: Path) -> dict:
    records = _file_records(directory)
    return {
        "name": directory.name,
        "path": directory.relative_to(root).as_posix(),
        "sha256": _hash_records(records),
        "files": records,
    }


def build_lockfile(root: Path | None = None) -> dict:
    root = ROOT if root is None else root
    collections = skill_collections(root)
    directories = sorted(collections["example"] + collections["plugins"], key=lambda p: p.name)
    if not directories:
        raise ValueError("No canonical skills found")
    return {
        "version": "2.0",
        "hash_algorithm": HASH_ALGORITHM,
        "skills": [_locked_folder(directory, root) for directory in directories],
        # Plugin skills can reference shared resources and agents outside their
        # own folders. Lock the complete plugin as well as its skill definitions.
        "plugins": [_locked_folder(directory, root) for directory in find_plugin_dirs(root / "plugins")],
    }


def main() -> int:
    lockfile = build_lockfile()
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    LOCK_FILE.write_text(
        json.dumps(lockfile, indent=2) + "\n",
        encoding="utf-8",
    )
    LOCK_FILE.chmod(0o644)

    print(f"Generated {LOCK_FILE.relative_to(ROOT)} with {len(lockfile['skills'])} skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
