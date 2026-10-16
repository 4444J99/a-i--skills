#!/usr/bin/env python3
"""
Spec Directory Initializer - Scaffolds a new feature spec directory

Usage:
    init_spec_dir.py <feature-name> [--path <specs-dir>]

Examples:
    init_spec_dir.py user-authentication
    init_spec_dir.py real-time-chat --path ./specs
    init_spec_dir.py payment-flow --path /project/specs
"""

import argparse
import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
SPEC_TEMPLATE = SKILL_DIR / "assets" / "templates" / "spec-template.md"


def next_feature_number(specs_dir: Path) -> int:
    """Scan existing directories to determine the next feature number."""
    if not specs_dir.exists():
        return 1
    existing = []
    for child in specs_dir.iterdir():
        if child.is_dir():
            match = re.match(r"^(\d{3})-", child.name)
            if match:
                existing.append(int(match.group(1)))
    return max(existing, default=0) + 1


def load_template() -> str:
    """Load the spec template, falling back to a minimal default."""
    if SPEC_TEMPLATE.exists():
        return SPEC_TEMPLATE.read_text()
    return (
        "# Feature Specification: [FEATURE NAME]\n\n"
        "**Status**: Draft\n\n"
        "## User Scenarios & Testing\n\n"
        "## Requirements\n\n"
        "## Success Criteria\n"
    )


def init_spec_dir(feature_name: str, specs_path: str) -> Path | None:
    """
    Scaffold a feature spec directory with auto-numbering.

    Args:
        feature_name: Kebab-case feature name (e.g. 'user-auth')
        specs_path: Parent directory for spec folders

    Returns:
        Path to created directory, or None on error.
    """
    specs_dir = Path(specs_path).resolve()
    number = next_feature_number(specs_dir)
    dir_name = f"{number:03d}-{feature_name}"
    feature_dir = specs_dir / dir_name

    if feature_dir.exists():
        print(f"Error: directory already exists: {feature_dir}")
        return None

    # Create directory structure
    feature_dir.mkdir(parents=True)
    (feature_dir / "checklists").mkdir()

    # Write spec.md from template
    template = load_template()
    spec_content = template.replace("[FEATURE NAME]", feature_name.replace("-", " ").title())
    (feature_dir / "spec.md").write_text(spec_content)

    # Write minimal requirements checklist
    checklist = (
        f"# Requirements Checklist: {feature_name.replace('-', ' ').title()}\n\n"
        "## Content Quality\n\n"
        "- [ ] No implementation details (languages, frameworks, APIs)\n"
        "- [ ] Focused on user value and business needs\n"
        "- [ ] All mandatory sections completed\n\n"
        "## Requirement Completeness\n\n"
        "- [ ] No [NEEDS CLARIFICATION] markers remain\n"
        "- [ ] Requirements are testable and unambiguous\n"
        "- [ ] Success criteria are measurable\n"
        "- [ ] Edge cases identified\n"
        "- [ ] Scope clearly bounded\n"
    )
    (feature_dir / "checklists" / "requirements.md").write_text(checklist)

    # Report
    print(f"Created: {feature_dir}/")
    print(f"  spec.md")
    print(f"  checklists/requirements.md")
    print()
    print("Next steps:")
    print(f"  1. Edit {feature_dir}/spec.md — fill in user stories and requirements")
    print(f"  2. Run /speckit.specify to generate from description, or edit manually")
    print(f"  3. Run /speckit.plan when specification is ready")

    return feature_dir


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scaffold a new feature spec directory with auto-numbering."
    )
    parser.add_argument("feature_name", help="Kebab-case feature name (e.g. 'user-auth')")
    parser.add_argument("--path", default="./specs", help="Specs parent directory (default: ./specs)")
    args = parser.parse_args()

    result = init_spec_dir(args.feature_name, args.path)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
