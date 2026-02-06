#!/usr/bin/env python3
"""Generate .build/skills-lock.json with hashes and metadata for all skills."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from skill_lib import find_skill_dirs

ROOT = Path(__file__).resolve().parents[1]
BUILD_DIR = ROOT / ".build"
SKILLS_DIR = ROOT / "skills"
DOC_SKILLS_DIR = ROOT / "document-skills"
LOCK_FILE = BUILD_DIR / "skills-lock.json"


def _sha256_tree(directory: Path) -> str:
    """Return hex SHA-256 digest of all files in a directory.

    Hashes are computed over sorted relative paths and their contents
    for deterministic output regardless of filesystem ordering.
    """
    h = hashlib.sha256()
    files = sorted(
        p for p in directory.rglob("*") if p.is_file()
    )
    for filepath in files:
        rel = filepath.relative_to(directory)
        h.update(str(rel).encode("utf-8"))
        h.update(filepath.read_bytes())
    return h.hexdigest()


def _git_head() -> str:
    """Return the current HEAD commit hash."""
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        cwd=ROOT,
        check=True,
    )
    return result.stdout.strip()


def main() -> int:
    skill_dirs = find_skill_dirs(SKILLS_DIR) + find_skill_dirs(DOC_SKILLS_DIR)

    if not skill_dirs:
        print("ERROR: no skills found", file=sys.stderr)
        return 1

    git_commit = _git_head()

    skills = []
    for skill_dir in skill_dirs:
        skills.append({
            "name": skill_dir.name,
            "path": str(skill_dir.relative_to(ROOT)),
            "sha256": _sha256_tree(skill_dir),
        })

    lockfile = {
        "version": "1.2",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "git_commit": git_commit,
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
