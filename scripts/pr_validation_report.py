#!/usr/bin/env python3
"""Generate a JSON validation report for skills affected by a PR.

Determines which skills were changed relative to a base branch, validates
their SKILL.md frontmatter, and outputs a structured JSON report to stdout.
Exit code 0 on pass, 1 on fail.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

from skill_lib import extract_frontmatter_strict, parse_list_field

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
DOC_SKILLS_DIR = ROOT / "document-skills"
NAME_RE = re.compile(r"^[a-z0-9-]+$")

# Valid values for optional fields (mirrors validate_skills.py)
VALID_COMPLEXITY = {"beginner", "intermediate", "advanced"}
VALID_TIME_TO_LEARN = {"5min", "30min", "1hour", "multi-hour"}
VALID_SIDE_EFFECTS = {
    "creates-files", "modifies-git", "runs-commands",
    "network-access", "installs-packages", "reads-filesystem",
}
VALID_TIERS = {"core", "community"}
MIN_DESCRIPTION_LENGTH = 20
MAX_DESCRIPTION_LENGTH = 600


def _changed_files(base: str) -> list[str]:
    """Return files changed between base and HEAD."""
    result = subprocess.run(
        ["git", "diff", "--name-only", f"{base}...HEAD"],
        capture_output=True, text=True, cwd=ROOT,
    )
    if result.returncode != 0:
        # Fallback: compare against base directly (useful for initial commits)
        result = subprocess.run(
            ["git", "diff", "--name-only", base, "HEAD"],
            capture_output=True, text=True, cwd=ROOT,
        )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def _affected_skill_dirs(changed: list[str]) -> list[Path]:
    """Identify unique skill directories from changed file paths."""
    seen: set[Path] = set()
    for filepath in changed:
        parts = Path(filepath).parts
        # skills/<category>/<skill-name>/... -> 3+ parts
        if len(parts) >= 3 and parts[0] == "skills":
            skill_dir = ROOT / parts[0] / parts[1] / parts[2]
            if (skill_dir / "SKILL.md").exists():
                seen.add(skill_dir)
        # document-skills/<skill-name>/... -> 2+ parts
        elif len(parts) >= 2 and parts[0] == "document-skills":
            skill_dir = ROOT / parts[0] / parts[1]
            if (skill_dir / "SKILL.md").exists():
                seen.add(skill_dir)
    return sorted(seen, key=lambda p: p.name)


def _validate_skill(skill_dir: Path) -> tuple[list[str], list[str]]:
    """Validate a single skill. Returns (errors, warnings)."""
    errors: list[str] = []
    warnings: list[str] = []
    skill_file = skill_dir / "SKILL.md"

    try:
        text = skill_file.read_text(encoding="utf-8")
    except Exception as exc:  # noqa: BLE001
        return [f"unable to read SKILL.md ({exc})"], []

    try:
        data = extract_frontmatter_strict(text)
    except ValueError as exc:
        return [str(exc)], []

    name = data.get("name")
    description = data.get("description")

    if not name:
        errors.append("missing 'name' in frontmatter")
    elif name != skill_dir.name:
        errors.append(f"name '{name}' does not match directory '{skill_dir.name}'")
    elif not NAME_RE.match(name):
        errors.append(f"name '{name}' must be lowercase alnum + hyphen")

    if not description:
        errors.append("missing 'description' in frontmatter")
    else:
        if len(description) < MIN_DESCRIPTION_LENGTH:
            errors.append(
                f"description too short ({len(description)} chars, "
                f"minimum {MIN_DESCRIPTION_LENGTH})"
            )
        elif len(description) > MAX_DESCRIPTION_LENGTH:
            errors.append(
                f"description too long ({len(description)} chars, "
                f"maximum {MAX_DESCRIPTION_LENGTH})"
            )

    if not data.get("license"):
        warnings.append("missing 'license' field")

    # Validate optional fields
    complexity = data.get("complexity")
    if complexity and complexity not in VALID_COMPLEXITY:
        errors.append(
            f"invalid complexity '{complexity}', "
            f"must be one of: {', '.join(sorted(VALID_COMPLEXITY))}"
        )

    time_to_learn = data.get("time_to_learn")
    if time_to_learn and time_to_learn not in VALID_TIME_TO_LEARN:
        errors.append(
            f"invalid time_to_learn '{time_to_learn}', "
            f"must be one of: {', '.join(sorted(VALID_TIME_TO_LEARN))}"
        )

    for list_field in ("inputs", "outputs", "side_effects", "triggers", "complements", "includes"):
        raw = data.get(list_field)
        if raw:
            items = parse_list_field(raw)
            if not items:
                errors.append(f"'{list_field}' is present but empty or unparseable")
            if list_field == "side_effects":
                for item in items:
                    if item not in VALID_SIDE_EFFECTS:
                        errors.append(
                            f"invalid side_effect '{item}', "
                            f"must be one of: {', '.join(sorted(VALID_SIDE_EFFECTS))}"
                        )

    tier = data.get("tier")
    if tier and tier not in VALID_TIERS:
        errors.append(
            f"invalid tier '{tier}', "
            f"must be one of: {', '.join(sorted(VALID_TIERS))}"
        )

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate a JSON validation report for PR-affected skills.",
    )
    parser.add_argument(
        "--base",
        default="origin/main",
        help="Base ref for diff comparison (default: origin/main).",
    )
    args = parser.parse_args()

    changed = _changed_files(args.base)
    skill_dirs = _affected_skill_dirs(changed)

    all_errors: list[str] = []
    all_warnings: list[str] = []
    affected: list[dict[str, object]] = []

    for skill_dir in skill_dirs:
        errors, warnings = _validate_skill(skill_dir)
        rel_path = str(skill_dir.relative_to(ROOT))
        entry: dict[str, object] = {
            "name": skill_dir.name,
            "path": rel_path,
            "errors": errors,
            "warnings": warnings,
        }
        affected.append(entry)
        all_errors.extend(f"{rel_path}: {e}" for e in errors)
        all_warnings.extend(f"{rel_path}: {w}" for w in warnings)

    status = "fail" if all_errors else "pass"
    n_skills = len(affected)
    n_errors = len(all_errors)
    n_warnings = len(all_warnings)

    if status == "pass":
        summary = f"All {n_skills} affected skill(s) passed validation."
    else:
        summary = f"{n_errors} error(s) found across {n_skills} affected skill(s)."

    if n_warnings:
        summary += f" {n_warnings} warning(s)."

    report = {
        "status": status,
        "affected_skills": affected,
        "errors": all_errors,
        "warnings": all_warnings,
        "summary": summary,
    }

    json.dump(report, sys.stdout, indent=2)
    print()  # trailing newline

    return 0 if status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
