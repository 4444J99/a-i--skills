#!/usr/bin/env python3
"""Check health of skills by verifying references, scripts, and size metrics."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
DOC_SKILLS_DIR = ROOT / "document-skills"

VALID_SHEBANGS = ("#!/usr/bin/env ", "#!/bin/")


def _find_skill_dirs(base_dir: Path) -> list[Path]:
    """Find all skill directories containing a SKILL.md file."""
    return sorted(
        [p.parent for p in base_dir.rglob("SKILL.md") if p.parent != base_dir],
        key=lambda p: p.name,
    )


def _check_scripts(skill_dir: Path) -> list[str]:
    """Verify scripts exist and have proper shebangs."""
    issues: list[str] = []
    scripts_dir = skill_dir / "scripts"
    if not scripts_dir.is_dir():
        return issues

    for script in scripts_dir.iterdir():
        if script.is_dir() or script.name.startswith("."):
            continue
        # Skip package inits and test files — they aren't standalone CLI scripts
        if script.name == "__init__.py":
            continue
        if script.name.startswith("test_") or script.name.endswith("_test.py"):
            continue
        # Check shebang for executable-looking files (not .json, .tar.gz, etc.)
        if script.suffix in ("", ".py", ".sh", ".bash", ".zsh", ".rb", ".pl"):
            try:
                first_line = script.read_text(encoding="utf-8").splitlines()[0]
            except (UnicodeDecodeError, IndexError):
                continue
            if not any(first_line.startswith(s) for s in VALID_SHEBANGS):
                issues.append(f"scripts/{script.name}: missing or invalid shebang")
    return issues


def _check_references(skill_dir: Path) -> list[str]:
    """Verify referenced markdown files exist in references/ directory."""
    issues: list[str] = []
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
        return ["SKILL.md not found"]

    try:
        text = skill_file.read_text(encoding="utf-8")
    except Exception:  # noqa: BLE001
        return ["unable to read SKILL.md"]

    # Find references to references/*.md in backticks or markdown links
    import re
    ref_pattern = re.compile(r'`(references/[^`]+)`')
    link_pattern = re.compile(r'\[([^\]]+)\]\((references/[^)]+)\)')

    referenced: set[str] = set()
    for match in ref_pattern.finditer(text):
        referenced.add(match.group(1))
    for match in link_pattern.finditer(text):
        referenced.add(match.group(2))

    for ref_path in sorted(referenced):
        full_path = skill_dir / ref_path
        if not full_path.exists():
            issues.append(f"missing {ref_path}")

    return issues


def _count_resources(skill_dir: Path) -> dict[str, int]:
    """Count resource files in scripts/, references/, and assets/ directories."""
    counts: dict[str, int] = {}
    for subdir in ("scripts", "references", "assets"):
        path = skill_dir / subdir
        if path.is_dir():
            counts[subdir] = sum(1 for f in path.rglob("*") if f.is_file())
        else:
            counts[subdir] = 0
    return counts


def _skill_line_count(skill_dir: Path) -> int:
    """Return line count of SKILL.md."""
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
        return 0
    try:
        return len(skill_file.read_text(encoding="utf-8").splitlines())
    except Exception:  # noqa: BLE001
        return 0


def _check_skill(skill_dir: Path) -> dict[str, object]:
    """Run all health checks on a single skill."""
    issues: list[str] = []
    issues.extend(_check_scripts(skill_dir))
    issues.extend(_check_references(skill_dir))

    lines = _skill_line_count(skill_dir)
    counts = _count_resources(skill_dir)
    status = "healthy" if not issues else "issues"

    return {
        "name": skill_dir.name,
        "path": str(skill_dir.relative_to(ROOT)),
        "status": status,
        "issues": issues,
        "lines": lines,
        "scripts": counts.get("scripts", 0),
        "references": counts.get("references", 0),
        "assets": counts.get("assets", 0),
    }


def _print_table(results: list[dict[str, object]]) -> None:
    """Print a formatted table of health check results."""
    header = f"{'Skill':<35} {'Status':<10} {'Issues':<8} {'Lines':>6} {'Scripts':>8} {'Refs':>5} {'Assets':>7}"
    separator = "-" * len(header)
    print(header)
    print(separator)
    for r in results:
        issue_count = len(r["issues"])  # type: ignore[arg-type]
        status_display = r["status"] if issue_count == 0 else f"!{issue_count} issue(s)"
        print(
            f"{r['name']:<35} {status_display:<10} {issue_count:<8} "
            f"{r['lines']:>6} {r['scripts']:>8} {r['references']:>5} {r['assets']:>7}"
        )

    # Summary
    total = len(results)
    unhealthy = sum(1 for r in results if r["status"] != "healthy")
    print(separator)
    print(f"Total: {total} skills, {unhealthy} with issues")


def main() -> int:
    parser = argparse.ArgumentParser(description="Check health of skills.")
    parser.add_argument(
        "--skill",
        help="Check a single skill by name.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Output results as JSON.",
    )
    args = parser.parse_args()

    all_dirs = _find_skill_dirs(SKILLS_DIR) + _find_skill_dirs(DOC_SKILLS_DIR)

    if args.skill:
        matching = [d for d in all_dirs if d.name == args.skill]
        if not matching:
            print(f"ERROR: skill '{args.skill}' not found", file=sys.stderr)
            return 1
        skill_dirs = matching
    else:
        skill_dirs = all_dirs

    results = [_check_skill(d) for d in skill_dirs]

    if args.json_output:
        json.dump(results, sys.stdout, indent=2)
        print()
    else:
        _print_table(results)

    # Return 1 if any skill has issues
    has_issues = any(r["status"] != "healthy" for r in results)
    return 1 if has_issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
