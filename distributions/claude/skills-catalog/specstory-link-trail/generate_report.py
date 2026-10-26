#!/usr/bin/env python3
"""
Generate a markdown report from parsed WebFetch data.

Reads JSON from parse_webfetch.py and produces a formatted report with:
- Sessions grouped by file/date
- Successful vs failed fetches separated
- Deduplication with fetch counts
- Summary statistics

Usage:
    python generate_report.py <json_file>
    python generate_report.py -              # Read from stdin
    cat data.json | python generate_report.py -

Output: Markdown report to stdout
"""

import sys
import json
import re
from collections import defaultdict
from datetime import datetime
from typing import Optional


def extract_date_from_filename(filename: str) -> Optional[str]:
    """Extract date from SpecStory filename pattern: YYYY-MM-DD_HH-MM-SSZ"""
    # Match pattern like 2026-01-22_19-20-56Z
    match = re.search(r'(\d{4}-\d{2}-\d{2})_\d{2}-\d{2}-\d{2}Z', filename)
    if match:
        return match.group(1)
    return None


def extract_session_title(filename: str) -> str:
    """Extract human-readable title from filename."""
    # Remove path and extension
    name = filename.split('/')[-1]
    if name.endswith('.md'):
        name = name[:-3]

    # Remove timestamp prefix if present
    match = re.match(r'\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}Z-?(.*)$', name)
    if match:
        title = match.group(1)
        if title:
            # Convert dashes to spaces and capitalize
            return title.replace('-', ' ').strip()

    return name


def truncate_url(url: str, max_length: int = 60) -> str:
    """Truncate URL for display while keeping it recognizable."""
    if not url or len(url) <= max_length:
        return url or 'Unknown'

    # Try to keep the domain and some of the path
    parts = url.split('/')
    if len(parts) > 3:
        domain = '/'.join(parts[:3])
        if len(domain) < max_length - 5:
            remaining = max_length - len(domain) - 4
            return f"{domain}/...{url[-remaining:]}"

    return url[:max_length - 3] + '...'


def format_error(error: str, error_raw: Optional[str] = None) -> str:
    """Format error for display."""
    error_descriptions = {
        'ENOTFOUND': 'DNS lookup failed',
        'ETIMEDOUT': 'Connection timed out',
        'ECONNREFUSED': 'Connection refused',
        'ECONNRESET': 'Connection reset',
        'SSL_EXPIRED': 'SSL certificate expired',
        'SSL_MISMATCH': 'SSL hostname mismatch',
        'SSL_SELF_SIGNED': 'Self-signed certificate',
        'SSL_CHAIN': 'SSL certificate chain error',
        'CONTENT_TOO_LONG': 'Content exceeded size limit',
        'SOCKET_HANGUP': 'Connection dropped',
        'TIMEOUT': 'Request timed out',
        'EMPTY_RESPONSE': 'Empty response',
        'GENERIC_ERROR': 'Request failed',
    }

    # Handle HTTP errors
    if error and error.startswith('HTTP_'):
        code = error.replace('HTTP_', '')
        http_messages = {
            '400': 'Bad Request',
            '401': 'Unauthorized',
            '403': 'Forbidden',
            '404': 'Not Found',
            '429': 'Rate Limited',
            '500': 'Server Error',
            '502': 'Bad Gateway',
            '503': 'Service Unavailable',
        }
        return f"HTTP {code} ({http_messages.get(code, 'Error')})"

    return error_descriptions.get(error, error or 'Unknown error')


def generate_report(data: list[dict]) -> str:
    """Generate markdown report from parsed WebFetch data."""
    if not data:
        return "# Link Trail Report\n\nNo WebFetch instances found.\n"

    # Group by file
    by_file = defaultdict(list)
    for item in data:
        by_file[item['file']].append(item)

    # Sort files by date (extracted from filename)
    sorted_files = sorted(
        by_file.keys(),
        key=lambda f: extract_date_from_filename(f) or '0000-00-00',
        reverse=True
    )

    # Calculate global stats
    total_fetches = len(data)
    successful = sum(1 for d in data if d['success'])
    failed = total_fetches - successful

    # Track unique URLs across all files
    all_urls = defaultdict(int)
    for item in data:
        if item['url']:
            all_urls[item['url']] += 1

    unique_urls = len(all_urls)
    duplicate_fetches = sum(1 for count in all_urls.values() if count > 1)

    # Build report
    lines = []
    lines.append("# Link Trail Report")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- **Total WebFetch calls:** {total_fetches}")
    lines.append(f"- **Unique URLs:** {unique_urls}")
    lines.append(f"- **Successful:** {successful} ({successful/total_fetches*100:.0f}%)")
    lines.append(f"- **Failed:** {failed} ({failed/total_fetches*100:.0f}%)")
    if duplicate_fetches:
        lines.append(f"- **URLs fetched multiple times:** {duplicate_fetches}")
    lines.append(f"- **Sessions analyzed:** {len(by_file)}")
    lines.append("")

    # Report by session
    lines.append("---")
    lines.append("")

    for filepath in sorted_files:
        items = by_file[filepath]
        date = extract_date_from_filename(filepath)
        title = extract_session_title(filepath)

        lines.append(f"## {date or 'Unknown Date'}: {title or 'Session'}")
        lines.append("")
        lines.append(f"**File:** `{filepath.split('/')[-1]}`")
        lines.append(f"**Total fetches:** {len(items)}")
        lines.append("")

        # Separate successful and failed
        successes = [i for i in items if i['success']]
        failures = [i for i in items if not i['success']]

        # Deduplicate within session
        success_by_url = defaultdict(list)
        for item in successes:
            url = item['url'] or 'Unknown'
            success_by_url[url].append(item)

        failure_by_url = defaultdict(list)
        for item in failures:
            url = item['url'] or 'Unknown'
            failure_by_url[url].append(item)

        if successes:
            lines.append(f"### Successful ({len(successes)})")
            lines.append("")
            lines.append("| URL | Summary |")
            lines.append("|-----|---------|")

            for url, items_list in sorted(success_by_url.items()):
                display_url = truncate_url(url)
                summary = items_list[0].get('summary', 'No summary')
                count_note = f" (x{len(items_list)})" if len(items_list) > 1 else ""
                # Escape pipe characters in summary
                summary = (summary or 'No summary').replace('|', '\\|')
                lines.append(f"| {display_url}{count_note} | {summary} |")

            lines.append("")

        if failures:
            lines.append(f"### Failed ({len(failures)})")
            lines.append("")
            lines.append("| URL | Error |")
            lines.append("|-----|-------|")

            for url, items_list in sorted(failure_by_url.items()):
                display_url = truncate_url(url)
                error = format_error(
                    items_list[0].get('error'),
                    items_list[0].get('error_raw')
                )
                count_note = f" (x{len(items_list)})" if len(items_list) > 1 else ""
                lines.append(f"| {display_url}{count_note} | {error} |")

            lines.append("")

        lines.append("---")
        lines.append("")

    # Add URL index if there are URLs fetched multiple times
    multi_fetch_urls = {url: count for url, count in all_urls.items() if count > 1}
    if multi_fetch_urls:
        lines.append("## URLs Fetched Multiple Times")
        lines.append("")
        lines.append("| URL | Times Fetched |")
        lines.append("|-----|---------------|")
        for url, count in sorted(multi_fetch_urls.items(), key=lambda x: -x[1]):
            lines.append(f"| {truncate_url(url)} | {count} |")
        lines.append("")

    # Footer
    lines.append("---")
    lines.append(f"*Generated by link-trail skill*")

    return '\n'.join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_report.py <json_file>", file=sys.stderr)
        print("       python generate_report.py -  # read from stdin", file=sys.stderr)
        sys.exit(1)

    input_source = sys.argv[1]

    try:
        if input_source == '-':
            data = json.load(sys.stdin)
        else:
            with open(input_source, 'r', encoding='utf-8') as f:
                data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: File not found: {input_source}", file=sys.stderr)
        sys.exit(1)

    report = generate_report(data)
    print(report)


if __name__ == '__main__':
    main()
