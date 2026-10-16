#!/usr/bin/env python3
"""
Spec Validator - Checks specification completeness by stage

Usage:
    validate_spec.py <spec-dir> [--stage specify|plan|tasks|all]

Examples:
    validate_spec.py specs/001-user-auth --stage specify
    validate_spec.py specs/002-chat --stage plan
    validate_spec.py specs/003-payments --stage all
"""

import argparse
import re
import sys
from pathlib import Path

STAGES = ("specify", "plan", "tasks", "all")

REQUIRED_SPEC_SECTIONS = [
    "User Scenarios",
    "Requirements",
    "Success Criteria",
]


def check_file_exists(path: Path, label: str, errors: list[str]) -> bool:
    """Check that a file exists and is non-empty."""
    if not path.exists():
        errors.append(f"Missing: {label} ({path.name})")
        return False
    if path.stat().st_size == 0:
        errors.append(f"Empty: {label} ({path.name})")
        return False
    return True


def check_sections(content: str, sections: list[str], filename: str, errors: list[str]) -> None:
    """Verify that expected markdown sections are present."""
    for section in sections:
        if section.lower() not in content.lower():
            errors.append(f"{filename}: missing section '{section}'")


def count_markers(content: str, marker: str) -> int:
    """Count occurrences of a marker string."""
    return content.lower().count(marker.lower())


def validate_specify(spec_dir: Path) -> tuple[list[str], list[str]]:
    """Validate the specify stage: spec.md and checklists."""
    errors: list[str] = []
    warnings: list[str] = []

    spec_md = spec_dir / "spec.md"
    if not check_file_exists(spec_md, "Feature specification", errors):
        return errors, warnings

    content = spec_md.read_text()

    # Required sections
    check_sections(content, REQUIRED_SPEC_SECTIONS, "spec.md", errors)

    # Clarification markers
    clarification_count = count_markers(content, "[NEEDS CLARIFICATION")
    if clarification_count > 3:
        warnings.append(
            f"spec.md: {clarification_count} [NEEDS CLARIFICATION] markers (recommended max: 3)"
        )

    # User stories should have priorities
    story_headers = re.findall(r"###\s+User Story\s+\d+", content)
    if story_headers:
        priority_count = len(re.findall(r"\(Priority:\s*P\d+\)", content))
        if priority_count < len(story_headers):
            warnings.append(
                f"spec.md: {len(story_headers)} user stories but only {priority_count} have priority labels"
            )
    else:
        warnings.append("spec.md: no user stories found (expected '### User Story N' headers)")

    # Checklists directory
    checklists = spec_dir / "checklists"
    if not checklists.is_dir():
        errors.append("Missing: checklists/ directory")
    elif not any(checklists.iterdir()):
        warnings.append("checklists/ directory is empty")

    return errors, warnings


def validate_plan(spec_dir: Path) -> tuple[list[str], list[str]]:
    """Validate the plan stage: plan.md, research.md, data-model.md, contracts/."""
    errors: list[str] = []
    warnings: list[str] = []

    check_file_exists(spec_dir / "plan.md", "Implementation plan", errors)
    check_file_exists(spec_dir / "research.md", "Research document", errors)
    check_file_exists(spec_dir / "data-model.md", "Data model", errors)

    contracts = spec_dir / "contracts"
    if not contracts.is_dir():
        errors.append("Missing: contracts/ directory")
    elif not any(contracts.iterdir()):
        warnings.append("contracts/ directory is empty")

    return errors, warnings


def validate_tasks(spec_dir: Path) -> tuple[list[str], list[str]]:
    """Validate the tasks stage: tasks.md with numbered tasks."""
    errors: list[str] = []
    warnings: list[str] = []

    tasks_md = spec_dir / "tasks.md"
    if not check_file_exists(tasks_md, "Task list", errors):
        return errors, warnings

    content = tasks_md.read_text()

    # Numbered tasks (T001, T002, ...)
    task_ids = re.findall(r"T\d{3}", content)
    if not task_ids:
        errors.append("tasks.md: no numbered tasks found (expected T001, T002, ...)")
    else:
        # Check for phase structure
        if "Phase" not in content and "phase" not in content:
            warnings.append("tasks.md: no phase structure detected")

        # Check for user story labels
        story_labels = re.findall(r"\[US\d+\]", content)
        if not story_labels:
            warnings.append("tasks.md: no user story labels found (expected [US1], [US2], ...)")

    return errors, warnings


def run_validation(spec_dir: Path, stage: str) -> int:
    """Run validation for the specified stage(s). Returns exit code."""
    all_errors: list[str] = []
    all_warnings: list[str] = []

    stages_to_run = STAGES[:-1] if stage == "all" else [stage]

    for s in stages_to_run:
        if s == "specify":
            errs, warns = validate_specify(spec_dir)
        elif s == "plan":
            errs, warns = validate_plan(spec_dir)
        elif s == "tasks":
            errs, warns = validate_tasks(spec_dir)
        else:
            continue

        if errs or warns:
            print(f"\n[{s}]")
        for e in errs:
            print(f"  ERROR: {e}")
        for w in warns:
            print(f"  WARN:  {w}")
        all_errors.extend(errs)
        all_warnings.extend(warns)

    # Summary
    print()
    if all_errors:
        print(f"FAIL: {len(all_errors)} error(s), {len(all_warnings)} warning(s)")
        return 1
    elif all_warnings:
        print(f"PASS with {len(all_warnings)} warning(s)")
        return 0
    else:
        print("PASS: all checks passed")
        return 0


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate spec directory completeness by stage."
    )
    parser.add_argument("spec_dir", help="Path to feature spec directory")
    parser.add_argument(
        "--stage",
        choices=STAGES,
        default="all",
        help="Validation stage (default: all)",
    )
    args = parser.parse_args()

    spec_dir = Path(args.spec_dir).resolve()
    if not spec_dir.is_dir():
        print(f"Error: not a directory: {spec_dir}")
        sys.exit(1)

    print(f"Validating: {spec_dir}")
    print(f"Stage: {args.stage}")
    sys.exit(run_validation(spec_dir, args.stage))


if __name__ == "__main__":
    main()
