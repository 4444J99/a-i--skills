#!/usr/bin/env python3
"""Release helper: update versions, changelog, and run refresh/validation."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD_DIR = ROOT / "distributions"
DOCS_DIR = ROOT / "docs"

VERSION_FILES = [
    ROOT / ".claude-plugin" / "marketplace.json",
    BUILD_DIR / "extensions" / "gemini" / "example-skills" / "gemini-extension.json",
]


def _run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def _update_versions(version: str) -> None:
    marketplace = VERSION_FILES[0]
    data = json.loads(marketplace.read_text(encoding="utf-8"))
    data.setdefault("metadata", {})["version"] = version
    marketplace.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    for path in VERSION_FILES[1:]:
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload["version"] = version
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _render_section(title: str, bullets: list[str]) -> str:
    if not bullets:
        return ""
    lines = [f"### {title}"]
    lines.extend([f"- {item}" for item in bullets])
    return "\n".join(lines)


def _extract_changelog_section(version: str) -> str:
    changelog = DOCS_DIR / "CHANGELOG.md"
    content = changelog.read_text(encoding="utf-8").splitlines()
    header = f"## [{version}]"
    start = None
    for idx, line in enumerate(content):
        if line.startswith(header):
            start = idx
            break
    if start is None:
        raise ValueError(f"CHANGELOG.md has no entry for {version}")

    end = len(content)
    for idx in range(start + 1, len(content)):
        if content[idx].startswith("## ["):
            end = idx
            break
    return "\n".join(content[start:end]).strip()


def _update_changelog(version: str, date_str: str, added: list[str], changed: list[str], fixed: list[str]) -> None:
    changelog = DOCS_DIR / "CHANGELOG.md"
    content = changelog.read_text(encoding="utf-8")

    entry_lines = [f"## [{version}] - {date_str}"]
    sections = [
        _render_section("Added", added),
        _render_section("Changed", changed),
        _render_section("Fixed", fixed),
    ]
    sections = [s for s in sections if s]
    if not sections:
        raise ValueError("Provide at least one --add/--change/--fix entry for the changelog.")
    entry_lines.extend(sections)
    entry = "\n".join(entry_lines) + "\n\n"

    marker = "\n## ["
    idx = content.find(marker)
    if idx == -1:
        content = content.rstrip() + "\n\n" + entry
    else:
        insert_at = idx + 1
        content = content[:insert_at] + entry + content[insert_at:]

    changelog.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare a release by bumping versions and updating CHANGELOG.md.")
    parser.add_argument("version", help="Release version (e.g., 1.2.0)")
    parser.add_argument("--date", help="Release date (YYYY-MM-DD). Defaults to today.")
    parser.add_argument("--add", action="append", default=[], help="Changelog entry under Added.")
    parser.add_argument("--change", action="append", default=[], help="Changelog entry under Changed.")
    parser.add_argument("--fix", action="append", default=[], help="Changelog entry under Fixed.")
    parser.add_argument("--skip-refresh", action="store_true", help="Skip refresh_skill_collections.py")
    parser.add_argument("--skip-validate", action="store_true", help="Skip validate_skills.py")
    parser.add_argument("--commit", action="store_true", help="Commit updated files.")
    parser.add_argument("--tag", action="store_true", help="Create a git tag for the release.")
    parser.add_argument("--push", action="store_true", help="Push commit and tags to remote.")
    parser.add_argument("--remote", default="origin", help="Git remote to push to (default: origin).")
    parser.add_argument("--tag-prefix", default="v", help="Prefix to use for tags (default: v).")
    parser.add_argument("--release", action="store_true", help="Create or update a GitHub release.")
    parser.add_argument("--notes-from-changelog", action="store_true", help="Use CHANGELOG section as release notes.")
    parser.add_argument("--notes", help="Explicit release notes to pass to gh release create/edit.")
    args = parser.parse_args()

    if not re.match(r"^\d+\.\d+\.\d+$", args.version):
        parser.error(f"invalid version '{args.version}': must be semver (e.g., 1.2.0)")

    date_str = args.date or dt.date.today().isoformat()

    _update_versions(args.version)
    _update_changelog(args.version, date_str, args.add, args.change, args.fix)

    if not args.skip_refresh:
        _run(["python3", "scripts/refresh_skill_collections.py"])
    if not args.skip_validate:
        _run(["python3", "scripts/validate_skills.py", "--collection", "example", "--unique"])
        _run(["python3", "scripts/validate_generated_dirs.py"])

    tag_name = f"{args.tag_prefix}{args.version}"

    if args.commit:
        _run(["git", "add", "-A"])
        _run(["git", "commit", "-m", f"Release {tag_name}"])

    if args.tag:
        _run(["git", "tag", "-a", tag_name, "-m", f"Release {tag_name}"])

    if args.push:
        if args.tag:
            _run(["git", "push", args.remote, "HEAD", "--tags"])
        else:
            _run(["git", "push", args.remote, "HEAD"])

    if args.release:
        if not shutil.which("gh"):
            raise SystemExit("ERROR: 'gh' CLI not found. Install from https://cli.github.com/")
        notes = args.notes
        if args.notes_from_changelog:
            notes = _extract_changelog_section(args.version)
        if not notes:
            raise ValueError("Release notes are required (use --notes or --notes-from-changelog).")
        # Create or edit release if it already exists.
        try:
            _run(["gh", "release", "create", tag_name, "--title", tag_name, "--notes", notes])
        except subprocess.CalledProcessError:
            _run(["gh", "release", "edit", tag_name, "--notes", notes])

    print(f"Updated versions and CHANGELOG for {args.version} ({date_str}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
