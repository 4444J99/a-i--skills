#!/usr/bin/env python3
"""Validate generated skill bundle directories are in sync and not symlinked."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD_DIR = ROOT / ".build"

BUNDLES = {
    "example": {
        "list": BUILD_DIR / "collections" / "example-skills.txt",
        "targets": [
            BUILD_DIR / "direct" / "example",
            BUILD_DIR / "codex" / "skills",
            BUILD_DIR / "claude" / "skills",
            BUILD_DIR / "extensions" / "gemini" / "example-skills" / "skills",
        ],
    },
    "document": {
        "list": BUILD_DIR / "collections" / "document-skills.txt",
        "targets": [
            BUILD_DIR / "direct" / "document",
            BUILD_DIR / "codex" / "skills-document",
            BUILD_DIR / "claude" / "skills-document",
            BUILD_DIR / "extensions" / "gemini" / "document-skills" / "skills",
        ],
    },
}


def _load_list(path: Path) -> list[str]:
    if not path.exists():
        raise FileNotFoundError(f"Missing collection list: {path}")
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _check_marker(target: Path, errors: list[str]) -> None:
    marker = target / ".skills-generated"
    if not marker.exists():
        errors.append(f"{target}: missing .skills-generated marker")


def _check_no_symlinks(target: Path, errors: list[str]) -> None:
    for path in target.rglob("*"):
        if path.is_symlink():
            errors.append(f"{target}: contains symlink {path}")


def _check_top_level(target: Path, expected_names: set[str], errors: list[str]) -> None:
    if not target.exists():
        errors.append(f"{target}: missing target directory")
        return

    actual = {
        p.name
        for p in target.iterdir()
        if p.is_dir() and p.name != ".skills-generated"
    }
    missing = expected_names - actual
    extra = actual - expected_names
    if missing:
        errors.append(f"{target}: missing {sorted(missing)}")
    if extra:
        errors.append(f"{target}: extra {sorted(extra)}")


def _check_registry(errors: list[str]) -> None:
    """Verify skills-registry.json exists and has a plausible skill count."""
    import json as _json

    registry_path = BUILD_DIR / "skills-registry.json"
    if not registry_path.exists():
        errors.append(f"{registry_path}: missing skills-registry.json")
        return

    try:
        data = _json.loads(registry_path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        errors.append(f"{registry_path}: invalid JSON ({exc})")
        return

    skills = data.get("skills", [])
    if not skills:
        errors.append(f"{registry_path}: registry contains no skills")

    # Cross-check with example-skills.txt count
    example_list = BUILD_DIR / "collections" / "example-skills.txt"
    if example_list.exists():
        expected_count = len(_load_list(example_list))
        example_skills = [s for s in skills if s.get("collection") == "example"]
        if len(example_skills) != expected_count:
            errors.append(
                f"{registry_path}: example skill count mismatch "
                f"(registry={len(example_skills)}, list={expected_count})"
            )


def _check_lockfile(errors: list[str]) -> None:
    """Verify skills-lock.json exists and skill count matches collections."""
    lockfile_path = BUILD_DIR / "skills-lock.json"
    if not lockfile_path.exists():
        # Lockfile is optional but warn
        return

    import json as _json
    try:
        data = _json.loads(lockfile_path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        errors.append(f"{lockfile_path}: invalid JSON ({exc})")
        return

    lock_skills = data.get("skills", [])
    # Cross-check count against combined collection lists
    total_expected = 0
    for collection in ("example-skills.txt", "document-skills.txt"):
        list_path = BUILD_DIR / "collections" / collection
        if list_path.exists():
            total_expected += len(_load_list(list_path))
    if total_expected and len(lock_skills) != total_expected:
        errors.append(
            f"{lockfile_path}: skill count mismatch "
            f"(lockfile={len(lock_skills)}, collections={total_expected})"
        )


def main() -> int:
    errors: list[str] = []

    for bundle_name, bundle in BUNDLES.items():
        list_path = bundle["list"]
        expected_paths = _load_list(list_path)
        expected_names = {Path(path).name for path in expected_paths}
        for target in bundle["targets"]:
            _check_marker(target, errors)
            _check_no_symlinks(target, errors)
            _check_top_level(target, expected_names, errors)

    _check_registry(errors)
    _check_lockfile(errors)

    if errors:
        for err in errors:
            print(f"ERROR: {err}")
        return 1

    print("Generated bundle directories are valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
