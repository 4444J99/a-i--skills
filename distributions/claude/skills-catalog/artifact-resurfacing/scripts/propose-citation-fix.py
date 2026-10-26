#!/usr/bin/env python3
"""
propose-citation-fix.py

Propose-only citation fix for artifact-resurfacing Phase 3 (Polish).

Given a target file, a stale path (the wrong location currently cited), and a
canonical path (the correct location on disk), emit a unified diff to stdout
that rewrites the citations. The script NEVER writes the target file.

The conductor reviews the diff and applies (or rejects) it via the Edit tool.

Usage:
    python3 propose-citation-fix.py \\
        --file <target-file> \\
        --stale-path <wrong-path-as-cited> \\
        --canonical-path <correct-path>

    # Multiple replacements in one pass:
    python3 propose-citation-fix.py \\
        --file <target> \\
        --replace <stale>=<canonical> \\
        --replace <stale2>=<canonical2>

Exit codes:
    0 — diff emitted (or no-op: zero changes found)
    1 — argument error
    2 — target file unreadable
"""

from __future__ import annotations

import argparse
import difflib
import os
import sys
from pathlib import Path


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Propose a citation-fix unified diff. Never writes the target file."
    )
    p.add_argument("--file", required=True, help="Target file (CLAUDE.md, MEMORY.md, etc.)")
    p.add_argument(
        "--stale-path",
        action="append",
        default=[],
        help="A wrong path currently cited in the target. Can be passed multiple times.",
    )
    p.add_argument(
        "--canonical-path",
        action="append",
        default=[],
        help="The correct path on disk. Match by position to --stale-path.",
    )
    p.add_argument(
        "--replace",
        action="append",
        default=[],
        help="Compact form: <stale>=<canonical>. Can be passed multiple times.",
    )
    p.add_argument(
        "--context-lines",
        type=int,
        default=3,
        help="Lines of context in unified diff (default 3)",
    )
    return p.parse_args(argv)


def build_replacements(args: argparse.Namespace) -> list[tuple[str, str]]:
    """Combine --stale-path/--canonical-path pairs and --replace stale=canonical."""
    if len(args.stale_path) != len(args.canonical_path):
        raise SystemExit(
            "error: --stale-path and --canonical-path must be paired (same count)."
        )

    pairs: list[tuple[str, str]] = list(zip(args.stale_path, args.canonical_path))

    for spec in args.replace:
        if "=" not in spec:
            raise SystemExit(f"error: --replace must use form stale=canonical, got: {spec}")
        stale, _, canonical = spec.partition("=")
        if not stale or not canonical:
            raise SystemExit(f"error: --replace requires both sides non-empty: {spec}")
        pairs.append((stale, canonical))

    if not pairs:
        raise SystemExit(
            "error: no replacements specified. Use --stale-path + --canonical-path, "
            "or --replace stale=canonical."
        )
    return pairs


def apply_replacements_in_memory(content: str, pairs: list[tuple[str, str]]) -> str:
    """Apply each replacement in order, in memory. Never touches disk."""
    for stale, canonical in pairs:
        content = content.replace(stale, canonical)
    return content


def emit_unified_diff(
    original: str, proposed: str, filename: str, context_lines: int
) -> None:
    """Print a unified diff to stdout. No file writes."""
    diff = difflib.unified_diff(
        original.splitlines(keepends=True),
        proposed.splitlines(keepends=True),
        fromfile=f"a/{filename}",
        tofile=f"b/{filename}",
        n=context_lines,
    )
    sys.stdout.writelines(diff)


def count_replacements(content: str, pairs: list[tuple[str, str]]) -> dict[str, int]:
    """Count how many times each stale string was found before substitution."""
    return {stale: content.count(stale) for stale, _ in pairs}


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])

    target = Path(os.path.expanduser(args.file))
    if not target.is_file():
        print(f"error: target file not found or not readable: {target}", file=sys.stderr)
        return 2

    try:
        original = target.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        print(f"error: cannot read {target}: {exc}", file=sys.stderr)
        return 2

    pairs = build_replacements(args)
    counts = count_replacements(original, pairs)

    if all(c == 0 for c in counts.values()):
        # No changes found; surface to stderr (stdout reserved for diff), exit 0.
        print(
            f"info: none of the {len(pairs)} stale paths were found in {target.name}. "
            f"No diff emitted.",
            file=sys.stderr,
        )
        for stale, count in counts.items():
            print(f"  - {stale!r}: {count} occurrences", file=sys.stderr)
        return 0

    proposed = apply_replacements_in_memory(original, pairs)

    if proposed == original:
        print("info: replacements produced no change. No diff emitted.", file=sys.stderr)
        return 0

    # Header summary on stderr; diff on stdout.
    print(
        f"info: proposing {sum(counts.values())} replacements across "
        f"{sum(1 for c in counts.values() if c > 0)} distinct stale paths in {target.name}.",
        file=sys.stderr,
    )
    for stale, count in counts.items():
        if count > 0:
            print(f"  - {stale!r}: {count} occurrences", file=sys.stderr)
    print(
        "info: diff emitted to stdout. The conductor reviews and applies "
        "via Edit. This script does NOT write the file.",
        file=sys.stderr,
    )

    emit_unified_diff(original, proposed, str(target), args.context_lines)
    return 0


if __name__ == "__main__":
    sys.exit(main())
