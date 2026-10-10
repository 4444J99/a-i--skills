#!/usr/bin/env python3
"""Generate a machine-readable skills registry JSON from SKILL.md frontmatter."""
from __future__ import annotations

import json
from pathlib import Path

from skill_lib import extract_frontmatter_strict, parse_list_field, skill_collections
from validate_skills import _validate_skill

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
BUILD_DIR = ROOT / "distributions"
OUTPUT_PATH = BUILD_DIR / "skills-registry.json"

# Fields that are stored as lists in the registry
LIST_FIELDS = (
    "prerequisites", "tags", "inputs", "outputs", "side_effects",
    "triggers", "complements", "includes",
    "governance_phases", "organ_affinity",
)


def _category_from_path(skill_dir: Path, base_dir: Path) -> str:
    """Derive category from directory structure (e.g., skills/development/x -> development)."""
    try:
        rel = skill_dir.relative_to(base_dir)
        parts = rel.parts
        if len(parts) >= 2:
            return parts[0]
    except ValueError:
        pass
    return "uncategorized"


def _build_skill_entry(
    skill_dir: Path, base_dir: Path, collection: str, *, root: Path | None = None,
) -> dict:
    skill_file = skill_dir / "SKILL.md"
    errors = _validate_skill(skill_dir, check_links=True)
    if errors:
        raise ValueError("\n".join(errors))
    text = skill_file.read_text(encoding="utf-8")
    fm = extract_frontmatter_strict(text)
    name = fm["name"]
    source_root = ROOT if root is None else root

    entry: dict = {
        "name": name,
        "description": fm.get("description", ""),
        "category": _category_from_path(skill_dir, base_dir),
        "collection": collection,
        "path": skill_dir.relative_to(source_root).as_posix(),
        "license": fm.get("license"),
        "complexity": fm.get("complexity"),
        "time_to_learn": fm.get("time_to_learn"),
        "tier": fm.get("tier"),
        "governance_norm_group": fm.get("governance_norm_group"),
        "governance_auto_activate": fm.get("governance_auto_activate") == "true",
    }
    if collection == "plugins":
        entry["plugin"] = skill_dir.relative_to(source_root / "plugins").parts[0]

    # Parse list fields
    for field in LIST_FIELDS:
        raw = fm.get(field)
        entry[field] = parse_list_field(raw) if raw else []

    # Resource directories
    entry["resources"] = {
        "scripts": sorted(p.name for p in (skill_dir / "scripts").iterdir()) if (skill_dir / "scripts").is_dir() else [],
        "references": sorted(p.name for p in (skill_dir / "references").iterdir()) if (skill_dir / "references").is_dir() else [],
        "assets": sorted(p.name for p in (skill_dir / "assets").iterdir()) if (skill_dir / "assets").is_dir() else [],
    }

    return entry


def _build_categories(skills: list[dict]) -> dict:
    categories: dict[str, dict] = {}
    for skill in skills:
        cat = skill["category"]
        if cat not in categories:
            categories[cat] = {"count": 0, "skills": []}
        categories[cat]["count"] += 1
        categories[cat]["skills"].append(skill["name"])
    return categories


def _build_bundles(skills: list[dict]) -> list[dict]:
    bundles = []
    for skill in skills:
        if skill.get("includes"):
            bundles.append({
                "name": skill["name"],
                "includes": skill["includes"],
            })
    return bundles


def build_registry(root: Path | None = None) -> dict:
    """Return the complete semantic registry, rejecting omitted/invalid sources."""
    root = ROOT if root is None else root
    collections = skill_collections(root)
    skills: list[dict] = []
    for collection, directories in collections.items():
        base = root / ("skills" if collection == "example" else "plugins")
        for directory in directories:
            skills.append(_build_skill_entry(directory, base, collection, root=root))
    if not skills:
        raise ValueError("No canonical skills found")
    skills.sort(key=lambda item: item["name"])
    names = {entry["name"] for entry in skills}
    for entry in skills:
        for field in ("includes", "complements"):
            missing = set(entry[field]) - names
            if missing:
                raise ValueError(f"{entry['name']}: {field} references unknown skills: {sorted(missing)}")

    config = json.loads((root / "config" / "runtime-catalog.json").read_text(encoding="utf-8"))
    repository = config.get("repository")
    if not isinstance(repository, str) or not repository:
        raise ValueError("runtime-catalog.json must declare repository")

    return {
        "version": "2.0",
        "repository": repository,
        "skills": skills,
        "categories": _build_categories(skills),
        "bundles": _build_bundles(skills),
    }


def main() -> int:
    registry = build_registry()
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(registry, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )
    OUTPUT_PATH.chmod(0o644)
    print(f"Registry generated: {len(registry['skills'])} skills -> {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
