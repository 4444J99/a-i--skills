#!/usr/bin/env python3
"""Validate SKILL.md frontmatter and naming conventions."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC_SKILLS_DIR = ROOT / "document-skills"
NAME_RE = re.compile(r"^[a-z0-9-]+$")


def _find_skill_dirs(base_dir: Path) -> list[Path]:
    return sorted(
        [p for p in base_dir.iterdir() if p.is_dir() and (p / "SKILL.md").exists()],
        key=lambda p: p.name,
    )


def _extract_frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing YAML frontmatter opening '---'")

    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        raise ValueError("missing YAML frontmatter closing '---'")

    data: dict[str, str] = {}
    current_key = None
    for raw in lines[1:end]:
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith(" ") or raw.startswith("\t"):
            if current_key:
                data[current_key] = f"{data[current_key]}\n{raw.lstrip()}"
            continue
        key, sep, value = raw.partition(":")
        if not sep:
            raise ValueError(f"invalid frontmatter line: {raw}")
        current_key = key.strip()
        data[current_key] = value.strip()
    return data


def _validate_skill(skill_dir: Path) -> list[str]:
    errors = []
    skill_file = skill_dir / "SKILL.md"
    try:
        text = skill_file.read_text(encoding="utf-8")
    except Exception as exc:  # noqa: BLE001
        return [f"{skill_dir}: unable to read SKILL.md ({exc})"]

    try:
        data = _extract_frontmatter(text)
    except ValueError as exc:
        return [f"{skill_dir}: {exc}"]

    name = data.get("name")
    description = data.get("description")

    if not name:
        errors.append(f"{skill_dir}: missing 'name' in frontmatter")
    elif name != skill_dir.name:
        errors.append(
            f"{skill_dir}: name '{name}' does not match directory '{skill_dir.name}'"
        )
    elif not NAME_RE.match(name):
        errors.append(f"{skill_dir}: name '{name}' must be lowercase alnum + hyphen")

    if not description:
        errors.append(f"{skill_dir}: missing 'description' in frontmatter")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate skill frontmatter.")
    parser.add_argument(
        "--collection",
        choices=["example", "document", "all"],
        default="all",
        help="Which skill collection to validate.",
    )
    parser.add_argument(
        "--unique",
        action="store_true",
        help="Fail if skill names are duplicated in the selected collection.",
    )
    args = parser.parse_args()

    if args.collection == "example":
        skill_dirs = _find_skill_dirs(ROOT)
    elif args.collection == "document":
        skill_dirs = _find_skill_dirs(DOC_SKILLS_DIR)
    else:
        skill_dirs = _find_skill_dirs(ROOT) + _find_skill_dirs(DOC_SKILLS_DIR)

    errors: list[str] = []
    name_counts: dict[str, int] = {}

    for skill_dir in skill_dirs:
        errors.extend(_validate_skill(skill_dir))
        name_counts[skill_dir.name] = name_counts.get(skill_dir.name, 0) + 1

    if args.unique:
        duplicates = [name for name, count in name_counts.items() if count > 1]
        if duplicates:
            dup_list = ", ".join(sorted(duplicates))
            errors.append(f"duplicate skill names in collection: {dup_list}")

    if errors:
        for err in errors:
            print(f"ERROR: {err}")
        return 1

    print(f"Validated {len(skill_dirs)} skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
