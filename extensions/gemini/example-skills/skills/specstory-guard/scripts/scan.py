from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass
from typing import Iterable

from patterns import ALLOWLIST, PATTERNS, SecretPattern


@dataclass(frozen=True)
class Finding:
    file_path: str
    line_number: int
    rule_name: str
    snippet: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scan .specstory/history for potential secrets.",
    )
    parser.add_argument(
        "--root",
        default=os.getcwd(),
        help="Repository root (default: current working directory)",
    )
    parser.add_argument(
        "--history-dir",
        default=None,
        help="Override history directory (relative to root)",
    )
    parser.add_argument(
        "--max-matches-per-file",
        type=int,
        default=5,
        help="Limit findings reported per file",
    )
    parser.add_argument(
        "--max-matches",
        type=int,
        default=50,
        help="Limit total findings reported",
    )
    parser.add_argument(
        "--format",
        choices=("text", "markdown"),
        default="text",
        help="Output format",
    )
    return parser.parse_args()


def resolve_history_dir(root: str, override: str | None) -> str:
    if override:
        return os.path.join(root, override)
    return os.path.join(root, ".specstory", "history")


def iter_history_files(history_dir: str) -> Iterable[str]:
    for base, _, files in os.walk(history_dir):
        for name in files:
            if name.endswith(".md"):
                yield os.path.join(base, name)


def load_user_allowlist() -> list[re.Pattern[str]]:
    raw = os.getenv("SPECSTORY_GUARD_ALLOWLIST", "").strip()
    if not raw:
        return []
    patterns: list[re.Pattern[str]] = []
    for entry in [item.strip() for item in raw.split(",") if item.strip()]:
        try:
            patterns.append(re.compile(entry))
        except re.error as exc:
            print(f"specstory-guard: invalid allowlist regex '{entry}': {exc}", file=sys.stderr)
    return patterns


def is_allowlisted(text: str, allowlist: list[re.Pattern[str]]) -> bool:
    return any(pattern.search(text) for pattern in allowlist)


def build_snippet(line: str, match: re.Match[str]) -> str:
    start, end = match.span()
    redacted = "<redacted>"
    snippet = f"{line[:start]}{redacted}{line[end:]}".strip()
    if len(snippet) > 200:
        snippet = f"{snippet[:200]}..."
    return snippet


def scan_file(
    file_path: str,
    patterns: list[SecretPattern],
    allowlist: list[re.Pattern[str]],
    max_matches_per_file: int,
) -> list[Finding]:
    findings: list[Finding] = []
    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as handle:
            for line_number, line in enumerate(handle, start=1):
                if is_allowlisted(line, allowlist):
                    continue
                for pattern in patterns:
                    match = pattern.regex.search(line)
                    if not match:
                        continue
                    if is_allowlisted(match.group(0), allowlist):
                        continue
                    findings.append(
                        Finding(
                            file_path=file_path,
                            line_number=line_number,
                            rule_name=pattern.name,
                            snippet=build_snippet(line, match),
                        )
                    )
                    if len(findings) >= max_matches_per_file:
                        return findings
                if len(findings) >= max_matches_per_file:
                    return findings
    except OSError as exc:
        print(f"specstory-guard: failed to read {file_path}: {exc}", file=sys.stderr)
    return findings


def format_findings(findings: list[Finding], output_format: str) -> str:
    if output_format == "markdown":
        lines = ["specstory-guard: potential secrets detected:"]
        for finding in findings:
            rel_path = os.path.relpath(finding.file_path, os.getcwd())
            lines.append(
                f"- `{rel_path}:{finding.line_number}` ({finding.rule_name}) {finding.snippet}"
            )
        return "\n".join(lines)
    lines = ["specstory-guard: potential secrets detected:"]
    for finding in findings:
        rel_path = os.path.relpath(finding.file_path, os.getcwd())
        lines.append(
            f"{rel_path}:{finding.line_number}: {finding.rule_name}: {finding.snippet}"
        )
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    root = os.path.abspath(args.root)
    history_dir = resolve_history_dir(root, args.history_dir)

    if not os.path.isdir(history_dir):
        return 0

    allowlist = ALLOWLIST + load_user_allowlist()
    findings: list[Finding] = []

    for file_path in iter_history_files(history_dir):
        findings.extend(
            scan_file(
                file_path=file_path,
                patterns=PATTERNS,
                allowlist=allowlist,
                max_matches_per_file=args.max_matches_per_file,
            )
        )
        if len(findings) >= args.max_matches:
            break

    if not findings:
        return 0

    print(format_findings(findings, args.format), file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
