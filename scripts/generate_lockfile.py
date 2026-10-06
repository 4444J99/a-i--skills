#!/usr/bin/env python3
"""Generate distributions/skills-lock.json with hashes and metadata for all skills."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from skill_lib import find_skill_dirs

ROOT = Path(__file__).resolve().parents[1]
BUILD_DIR = ROOT / "distributions"
SKILLS_DIR = ROOT / "skills"
LOCK_FILE = BUILD_DIR / "skills-lock.json"


_IGNORED_NAMES = frozenset({".DS_Store", "__pycache__", ".pyc"})


def _sha256_tree(directory: Path) -> str:
    """Return hex SHA-256 digest of all files in a directory.

    Hashes are computed over sorted relative paths and their contents
    for deterministic output regardless of filesystem ordering.
    Skips OS-generated and cache files for cross-platform consistency.
    """
    h = hashlib.sha256()
    files = sorted(
        p for p in directory.rglob("*")
        if p.is_file() and p.name not in _IGNORED_NAMES
    )
    for filepath in files:
        rel = filepath.relative_to(directory)
        h.update(str(rel).encode("utf-8"))
        h.update(filepath.read_bytes())
    return h.hexdigest()


def main() -> int:
    skill_dirs = find_skill_dirs(SKILLS_DIR)

    if not skill_dirs:
        print("ERROR: no skills found", file=sys.stderr)
        return 1

    skills = []
    for skill_dir in skill_dirs:
        skills.append({
            "name": skill_dir.name,
            "path": str(skill_dir.relative_to(ROOT)),
            "sha256": _sha256_tree(skill_dir),
        })

    lockfile = {
        "version": "1.2",
        "skills": skills,
    }

    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    LOCK_FILE.write_text(
        json.dumps(lockfile, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"Generated {LOCK_FILE.relative_to(ROOT)} with {len(skills)} skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
