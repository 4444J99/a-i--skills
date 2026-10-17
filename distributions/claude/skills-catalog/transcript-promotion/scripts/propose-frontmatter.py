#!/usr/bin/env python3
"""propose-frontmatter.py — generate canonical frontmatter for a promoted artifact.

Phase 2 of the transcript-promotion protocol. Reads an extracted body from disk,
prepends YAML frontmatter conforming to the LOG #1 precedent shape, and writes the
result to the target plan-file path.

Series-aware: when invoked with --series and --series-index, links to sibling entries
in the same series via the related: block, allowing later members to discover earlier
ones.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from datetime import date

SERIES_SIBLINGS = {
    "engine-log": {
        1: "2026-05-20-statusline-options-reference.md",
        2: "2026-05-20-hooks-options-reference.md",
        3: "2026-05-20-subagents-options-reference.md",
    },
}


def build_frontmatter(args: argparse.Namespace) -> str:
    related_lines: list[str] = []
    if args.series and args.series in SERIES_SIBLINGS:
        siblings = SERIES_SIBLINGS[args.series]
        for idx, slug in sorted(siblings.items()):
            if idx == args.series_index:
                continue
            related_lines.append(f"  - {slug} (series sibling, index {idx})")
    for url in args.related_url or []:
        related_lines.append(f"  - {url}")
    related_block = "\n".join(related_lines) if related_lines else "  - (no related artifacts declared)"

    return f"""---
title: {args.title}
date: {args.date}
scope: {args.scope}
status: reference
extracted_from: {args.extracted_from}
extraction_date: {args.extraction_date}
series: {args.series or "(none)"}
series_index: {args.series_index if args.series else "(n/a)"}
related:
{related_block}
---

# {args.title}

## Why this file exists

Delivered inline during session(s) recorded in `{args.extracted_from}`. Promoted to a plan file on {args.extraction_date} via the `transcript-promotion` skill so the content becomes surface-discoverable via `~/.claude/plans/` and propagated to chezmoi-source + remote per Universal Rule #2. The body below is the verbatim transcript-canonical slice — re-authoring is forbidden by Phase 1 of the protocol.

---

"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--title", required=True)
    parser.add_argument("--date", required=True, help="Original delivery date YYYY-MM-DD")
    parser.add_argument("--scope", required=True, choices=("home", "repo", "organ"))
    parser.add_argument("--extracted-from", required=True)
    parser.add_argument(
        "--extraction-date",
        default=date.today().isoformat(),
        help="Promotion date (default: today)",
    )
    parser.add_argument("--series", default=None, help="e.g., engine-log")
    parser.add_argument("--series-index", type=int, default=None)
    parser.add_argument("--related-url", action="append", default=[])
    parser.add_argument("--body", required=True, help="Path to extracted body file")
    parser.add_argument("--output", required=True, help="Target plan-file path")
    args = parser.parse_args()

    body_path = Path(args.body)
    if not body_path.exists():
        print(f"body file not found: {body_path}", file=sys.stderr)
        return 1

    if args.series and args.series_index is None:
        print("--series-index required when --series is set", file=sys.stderr)
        return 2

    frontmatter = build_frontmatter(args)
    body = body_path.read_text(encoding="utf-8")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(frontmatter + body, encoding="utf-8")

    print(f"wrote {output_path} ({len(frontmatter) + len(body)} bytes)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
