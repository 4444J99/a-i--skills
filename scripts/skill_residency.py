#!/usr/bin/env python3
"""Measure what a skill root costs every session, and which skills earn residency.

Agents load each discovered skill's name and description into resident context
on every turn. ``budget`` measures that cost for one or more skill roots in the
same ``- name: description`` form the listing uses (characters, and tokens
estimated as characters / 4). ``usage`` reads Claude Code transcripts and counts,
per skill, how many of the most recent sessions invoked it through the Skill
tool or as a slash command. Both commands only read; neither writes anything.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

from skill_lib import extract_frontmatter

COMMAND_TAG = re.compile(r"<command-name>/?([A-Za-z0-9:_-]+)</command-name>")


def _description(metadata: dict[str, str]) -> str:
    value = metadata.get("description", "")
    if value[:1] in (">", "|"):
        value = value[1:]
    value = " ".join(part.strip() for part in value.splitlines() if part.strip())
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1]
    return value.strip()


def listing_entries(root: Path) -> list[tuple[str, str]]:
    """Return (name, description) for each skill directly under ``root``."""
    entries = []
    for entry in sorted(root.iterdir()) if root.is_dir() else []:
        skill = entry / "SKILL.md"
        if not skill.is_file():
            continue
        metadata = extract_frontmatter(skill.read_text(encoding="utf-8"))
        entries.append((metadata.get("name") or entry.name, _description(metadata)))
    return entries


def budget(root: Path) -> dict:
    entries = listing_entries(root)
    characters = sum(len(f"- {name}: {description}\n") for name, description in entries)
    return {
        "root": str(root),
        "skills": len(entries),
        "listing_chars": characters,
        "estimated_tokens": round(characters / 4),
    }


def live_roots() -> list[Path]:
    """Every skill root a Claude session on this host can discover, as configured."""
    home = Path.home()
    config = Path(os.environ.get("CLAUDE_CONFIG_DIR") or home / ".claude")
    release = Path(os.environ.get("DOMUS_SKILLS_HOME") or home / ".local/share/ai-skills") / "current"
    return [
        release / "distributions/claude/skills",
        config / "skills",
        home / ".claude/skills",
        home / ".agents/skills",
    ]


def _with_identity(rows: list[dict]) -> list[dict]:
    """Flag roots that resolve to an earlier root: each is listed again in full."""
    seen: dict[str, str] = {}
    for row in rows:
        real = os.path.realpath(row["root"])
        row["resolves_to"] = real
        row["duplicate_of"] = seen.get(real)
        seen.setdefault(real, row["root"])
    return rows


def _sessions(transcripts: Path, limit: int) -> list[Path]:
    files = [path for path in transcripts.rglob("*.jsonl") if "subagents" not in path.parts]
    files.sort(key=lambda path: path.stat().st_mtime, reverse=True)
    return files[:limit]


def _invocations(line: str) -> set[str]:
    found: set[str] = set()
    if '"Skill"' not in line and "<command-name>" not in line:
        return found
    try:
        record = json.loads(line)
    except ValueError:
        return found
    message = record.get("message") if isinstance(record, dict) else None
    content = message.get("content") if isinstance(message, dict) else None
    blocks = content if isinstance(content, list) else [content]
    for block in blocks:
        if isinstance(block, dict) and block.get("type") == "tool_use" and block.get("name") == "Skill":
            name = (block.get("input") or {}).get("skill")
            if isinstance(name, str) and name:
                found.add(name.rsplit(":", 1)[-1].lstrip("/"))
        text = block.get("text") if isinstance(block, dict) else block
        if record.get("type") == "user" and isinstance(text, str):
            found.update(match.rsplit(":", 1)[-1] for match in COMMAND_TAG.findall(text))
    return found


def usage(transcripts: Path, limit: int) -> dict:
    sessions = _sessions(transcripts, limit)
    per_skill: Counter[str] = Counter()
    for session in sessions:
        used: set[str] = set()
        with session.open(encoding="utf-8", errors="replace") as handle:
            for line in handle:
                used |= _invocations(line)
        per_skill.update(used)
    return {
        "transcripts": str(transcripts),
        "sessions_read": len(sessions),
        "sessions_per_skill": dict(per_skill.most_common()),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    measure = commands.add_parser("budget", help="resident listing size of skill roots")
    measure.add_argument("roots", nargs="*", type=Path)
    measure.add_argument("--live", action="store_true", help="also measure this host's configured runtime roots")
    observed = commands.add_parser("usage", help="skills invoked in recent Claude sessions")
    observed.add_argument("transcripts", nargs="?", type=Path,
                          help="Claude projects directory (default: $CLAUDE_CONFIG_DIR/projects)")
    observed.add_argument("--sessions", type=int, default=50)
    observed.add_argument("--catalog", type=Path, help="skills root; mark which used names it holds")
    args = parser.parse_args()
    if args.command == "budget":
        roots = list(args.roots) + (live_roots() if args.live else [])
        if not roots:
            parser.error("budget needs at least one root or --live")
        rows = _with_identity([budget(root) for root in roots])
        total = sum(row["listing_chars"] for row in rows)
        print(json.dumps({"roots": rows, "total_listing_chars": total,
                          "total_estimated_tokens": round(total / 4)}, indent=2))
        return 0
    if args.transcripts is None:
        config = Path(os.environ.get("CLAUDE_CONFIG_DIR") or Path.home() / ".claude")
        args.transcripts = config / "projects"
    if not args.transcripts.is_dir():
        print(f"Not a directory: {args.transcripts}", file=sys.stderr)
        return 1
    report = usage(args.transcripts, args.sessions)
    if args.catalog:
        held = {name for name, _ in listing_entries(args.catalog)}
        report["catalog_skills_used"] = sorted(set(report["sessions_per_skill"]) & held)
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
