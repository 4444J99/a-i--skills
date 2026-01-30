#!/usr/bin/env python3
"""
Specstory Yak Shave Analyzer

Analyzes .specstory/history files to detect when coding sessions
drifted off track from their original goal.
"""

import argparse
import json
import sys
from dataclasses import asdict
from datetime import datetime, timedelta
from pathlib import Path

from lib import (
    SessionAnalysis,
    parse_date_from_filename,
    analyze_session,
    format_report,
    find_specstory_path,
    get_git_author,
    get_install_instructions,
)


def main():
    parser = argparse.ArgumentParser(
        description="Analyze specstory sessions for yak shaving patterns"
    )
    parser.add_argument("--days", type=int, default=7, help="Analyze last N days (default: 7)")
    parser.add_argument("--from", dest="from_date", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--to", dest="to_date", help="End date (YYYY-MM-DD)")
    parser.add_argument("--path", help="Path to .specstory/history directory")
    parser.add_argument("--top", type=int, default=5, help="Show top N worst yak shaves")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--verbose", action="store_true", help="Show detailed analysis")
    parser.add_argument("--by-mtime", action="store_true", help="Filter by file modification time instead of filename date")
    parser.add_argument("-o", "--output", help="Write report to markdown file (e.g., yak-report.md)")

    args = parser.parse_args()

    # Find specstory path
    if args.path:
        history_path = Path(args.path)
    else:
        history_path = find_specstory_path()

    if not history_path or not history_path.exists():
        print(get_install_instructions(), file=sys.stderr)
        sys.exit(1)

    # Determine date range
    if args.from_date:
        start_date = datetime.strptime(args.from_date, "%Y-%m-%d")
    else:
        start_date = datetime.now() - timedelta(days=args.days)

    if args.to_date:
        end_date = datetime.strptime(args.to_date, "%Y-%m-%d")
    else:
        end_date = datetime.now()

    # Find matching files
    analyses = []
    for filepath in sorted(history_path.glob("*.md")):
        # Determine file date based on filter mode
        if args.by_mtime:
            file_date = datetime.fromtimestamp(filepath.stat().st_mtime)
        else:
            file_date = parse_date_from_filename(filepath.name)

        if file_date and start_date <= file_date <= end_date:
            analysis = analyze_session(filepath)
            if analysis:
                # Get git author for this file
                analysis.author = get_git_author(filepath)
                analyses.append(analysis)

    # Generate output
    if args.json:
        output_content = json.dumps({
            "date_range": {"from": start_date.isoformat(), "to": end_date.isoformat()},
            "sessions_analyzed": len(analyses),
            "average_score": sum(a.yak_shave_score for a in analyses) / len(analyses) if analyses else 0,
            "sessions": [asdict(a) for a in sorted(analyses, key=lambda x: x.yak_shave_score, reverse=True)]
        }, indent=2, default=str)
    else:
        output_content = format_report(analyses, args)

    # Write to file or stdout
    if args.output:
        output_path = Path(args.output)
        # Add .md extension if not present and not JSON
        if not args.json and not output_path.suffix:
            output_path = output_path.with_suffix(".md")
        elif args.json and not output_path.suffix:
            output_path = output_path.with_suffix(".json")

        output_path.write_text(output_content, encoding="utf-8")
        print(f"Report written to: {output_path}", file=sys.stderr)
        print(output_path)  # Print path to stdout for easy piping/capture
    else:
        print(output_content)


if __name__ == "__main__":
    main()
