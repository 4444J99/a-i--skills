#!/usr/bin/env python3
"""Apply governance metadata from mapping file to all SKILL.md frontmatter.

Reads governance_mapping.json and injects new fields into each skill's
SKILL.md frontmatter. Existing fields are preserved. List fields can be
merged or replaced based on the mapping entry's mode flags.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
MAPPING_PATH = Path(__file__).resolve().parent / "governance_mapping.json"

GOVERNANCE_FIELDS = (
    "governance_phases", "governance_norm_group",
    "governance_auto_activate", "organ_affinity",
)
LIST_MERGE_FIELDS = ("triggers", "complements")


def _find_all_skills() -> dict[str, Path]:
    """Return {skill_name: skill_dir} for all skills."""
    skills: dict[str, Path] = {}
    for base in (SKILLS_DIR,):
        for skill_file in base.rglob("SKILL.md"):
            skill_dir = skill_file.parent
            if skill_dir != base:
                skills[skill_dir.name] = skill_dir
    return skills


def _parse_frontmatter_bounds(text: str) -> tuple[int, int] | None:
    """Return (start, end) line indices of frontmatter delimiters."""
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return (0, i)
    return None


def _format_list(items: list[str]) -> str:
    """Format a list as YAML inline: [a, b, c]."""
    return "[" + ", ".join(items) + "]"


def _parse_existing_list(fm_text: str, field: str) -> list[str]:
    """Extract existing list field values from frontmatter text."""
    pattern = re.compile(rf"^{re.escape(field)}:\s*(.+)$", re.MULTILINE)
    match = pattern.search(fm_text)
    if not match:
        return []
    value = match.group(1).strip()
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1]
        return [item.strip() for item in inner.split(",") if item.strip()]
    return []


def _apply_to_skill(skill_dir: Path, mapping: dict) -> bool:
    """Apply governance metadata to a single SKILL.md. Returns True if modified."""
    skill_file = skill_dir / "SKILL.md"
    text = skill_file.read_text(encoding="utf-8")
    bounds = _parse_frontmatter_bounds(text)
    if bounds is None:
        print(f"  SKIP {skill_dir.name}: no frontmatter")
        return False

    lines = text.splitlines(keepends=True)
    start, end = bounds
    fm_text = "".join(lines[start + 1 : end])

    new_lines: list[str] = []

    # Add governance fields
    for field in GOVERNANCE_FIELDS:
        if field not in mapping:
            continue
        value = mapping[field]
        # Remove existing line for this field if present
        fm_text = re.sub(
            rf"^{re.escape(field)}:.*\n?", "", fm_text, flags=re.MULTILINE
        )
        if isinstance(value, list):
            if value:
                new_lines.append(f"{field}: {_format_list(value)}\n")
        elif isinstance(value, bool):
            if value:
                new_lines.append(f"{field}: true\n")
        elif value:
            new_lines.append(f"{field}: {value}\n")

    # Handle triggers and complements (merge or replace)
    for field in LIST_MERGE_FIELDS:
        if field not in mapping:
            continue
        new_items = mapping[field]
        mode = mapping.get(f"{field}_mode", "replace")
        if mode == "merge":
            existing = _parse_existing_list(fm_text, field)
            merged = list(dict.fromkeys(existing + new_items))
            fm_text = re.sub(
                rf"^{re.escape(field)}:.*\n?", "", fm_text, flags=re.MULTILINE
            )
            new_lines.append(f"{field}: {_format_list(merged)}\n")
        else:
            fm_text = re.sub(
                rf"^{re.escape(field)}:.*\n?", "", fm_text, flags=re.MULTILINE
            )
            if new_items:
                new_lines.append(f"{field}: {_format_list(new_items)}\n")

    if not new_lines:
        return False

    # Reconstruct the file
    reconstructed = (
        lines[0]
        + fm_text.rstrip("\n") + "\n"
        + "".join(new_lines)
        + lines[end]
        + "".join(lines[end + 1 :])
    )

    skill_file.write_text(reconstructed, encoding="utf-8")
    return True


def main() -> int:
    mapping = json.loads(MAPPING_PATH.read_text(encoding="utf-8"))
    skills = _find_all_skills()

    meta = mapping.pop("_meta", {})
    print(f"Mapping version: {meta.get('version', 'unknown')}")
    print(f"Skills found: {len(skills)}")
    print(f"Mappings loaded: {len(mapping)}")
    print()

    modified = 0
    skipped = 0
    missing = 0

    for skill_name, skill_mapping in sorted(mapping.items()):
        if skill_name in skills:
            if _apply_to_skill(skills[skill_name], skill_mapping):
                print(f"  OK   {skill_name}")
                modified += 1
            else:
                print(f"  SKIP {skill_name} (no changes)")
                skipped += 1
        else:
            print(f"  MISS {skill_name} (not found on disk)")
            missing += 1

    mapped_names = set(mapping.keys())
    unmapped = set(skills.keys()) - mapped_names
    if unmapped:
        print(f"\nWARNING: {len(unmapped)} skills not in mapping:")
        for name in sorted(unmapped):
            print(f"  {name}")

    print(f"\nDone: {modified} modified, {skipped} skipped, {missing} missing")
    return 1 if missing > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
