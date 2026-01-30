#!/usr/bin/env python3
"""
Parse WebFetch tool uses from SpecStory history files.

Extracts all WebFetch instances with their URLs, results, and status.
Handles large files via streaming and outputs structured JSON.

Usage:
    python parse_webfetch.py <file_or_glob_pattern> [...]
    python parse_webfetch.py .specstory/history/*.md
    python parse_webfetch.py .specstory/history/2026-01-22*.md

Output: JSON array to stdout
"""

import sys
import re
import json
import glob
from pathlib import Path
from typing import Iterator, Optional
from dataclasses import dataclass, asdict

# Import the URL extraction helper
from extract_urls_context import extract_url_from_context


@dataclass
class WebFetchResult:
    """Represents a single WebFetch tool use."""
    url: Optional[str]
    url_source: str  # user_message, thinking, task_prompt, inferred, unknown
    success: bool
    summary: Optional[str]
    error: Optional[str]
    error_raw: Optional[str]
    line_number: int
    file: str


# Error patterns to detect failed fetches
ERROR_PATTERNS = [
    (re.compile(r'getaddrinfo ENOTFOUND', re.IGNORECASE), 'ENOTFOUND'),
    (re.compile(r'ETIMEDOUT', re.IGNORECASE), 'ETIMEDOUT'),
    (re.compile(r'ECONNREFUSED', re.IGNORECASE), 'ECONNREFUSED'),
    (re.compile(r'ECONNRESET', re.IGNORECASE), 'ECONNRESET'),
    (re.compile(r'Request failed with status code (\d+)'), 'HTTP_ERROR'),
    (re.compile(r'certificate has expired', re.IGNORECASE), 'SSL_EXPIRED'),
    (re.compile(r'Hostname/IP does not match certificate', re.IGNORECASE), 'SSL_MISMATCH'),
    (re.compile(r'self[- ]signed certificate', re.IGNORECASE), 'SSL_SELF_SIGNED'),
    (re.compile(r'unable to verify the first certificate', re.IGNORECASE), 'SSL_CHAIN'),
    (re.compile(r'Prompt is too long', re.IGNORECASE), 'CONTENT_TOO_LONG'),
    (re.compile(r'socket hang up', re.IGNORECASE), 'SOCKET_HANGUP'),
    (re.compile(r'timeout', re.IGNORECASE), 'TIMEOUT'),
]

# WebFetch block start pattern
WEBFETCH_START = re.compile(
    r'<tool-use[^>]*data-tool-name="WebFetch"[^>]*>',
    re.IGNORECASE
)

# End of tool-use block
TOOLUSE_END = '</tool-use>'


def parse_file(filepath: Path) -> Iterator[WebFetchResult]:
    """
    Parse a single SpecStory history file for WebFetch uses.

    Uses line-by-line streaming to handle large files.
    """
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Warning: Could not read {filepath}: {e}", file=sys.stderr)
        return

    i = 0
    while i < len(lines):
        line = lines[i]

        # Look for WebFetch block start
        if WEBFETCH_START.search(line):
            webfetch_start_line = i + 1  # 1-indexed for reporting

            # Extract the content of this WebFetch block
            content_lines = []
            in_code_block = False
            j = i + 1

            while j < len(lines):
                current_line = lines[j]

                # Check for end of tool-use
                if TOOLUSE_END in current_line:
                    break

                # Track code blocks (where the result content is)
                if current_line.strip().startswith('```'):
                    if in_code_block:
                        in_code_block = False
                    else:
                        in_code_block = True
                        j += 1
                        continue

                if in_code_block:
                    content_lines.append(current_line)

                j += 1

            # Process the extracted content
            content = ''.join(content_lines).strip()

            # Find the URL from context (pass content for result-based inference)
            url, url_source = extract_url_from_context(lines, i, result_content=content)

            # Determine success/failure and extract error info
            success, error, error_raw = analyze_result(content)

            # Generate summary for successful fetches
            summary = None
            if success and content:
                summary = generate_summary(content)

            yield WebFetchResult(
                url=url,
                url_source=url_source,
                success=success,
                summary=summary,
                error=error,
                error_raw=error_raw if error else None,
                line_number=webfetch_start_line,
                file=str(filepath)
            )

            # Move past this block
            i = j

        i += 1


def analyze_result(content: str) -> tuple[bool, Optional[str], Optional[str]]:
    """
    Analyze WebFetch result content to determine success/failure.

    Returns: (success, error_type, error_raw)
    """
    if not content:
        return False, 'EMPTY_RESPONSE', None

    # Check for known error patterns
    for pattern, error_type in ERROR_PATTERNS:
        match = pattern.search(content)
        if match:
            error_raw = content[:200].strip()
            # For HTTP errors, include the status code
            if error_type == 'HTTP_ERROR' and match.groups():
                error_type = f'HTTP_{match.group(1)}'
            return False, error_type, error_raw

    # Check content length - very short responses are often errors
    if len(content) < 50:
        # But some short responses are valid (e.g., redirects)
        if any(word in content.lower() for word in ['redirect', 'moved']):
            return True, None, None
        # Check if it looks like an error message
        if any(word in content.lower() for word in ['error', 'failed', 'denied', 'forbidden']):
            return False, 'GENERIC_ERROR', content[:200].strip()

    # Assume success if no error patterns matched
    return True, None, None


def generate_summary(content: str, max_length: int = 200) -> str:
    """Generate a brief summary of successful fetch content."""
    # Try to extract a title or first meaningful line
    lines = content.strip().split('\n')

    # Look for a header
    for line in lines[:5]:
        line = line.strip()
        if line.startswith('#'):
            # Remove markdown header markers
            title = line.lstrip('#').strip()
            if title:
                return title[:max_length]

    # Look for "What They Do" or similar sections
    overview_patterns = [
        r'##\s*What They Do\s*\n+(.+)',
        r'##\s*Overview\s*\n+(.+)',
        r'##\s*Company Overview\s*\n+(.+)',
        r'##\s*Business Description\s*\n+(.+)',
    ]

    for pattern in overview_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            summary = match.group(1).strip()
            return summary[:max_length]

    # Fall back to first non-empty, non-header line
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#') and not line.startswith('-'):
            return line[:max_length]

    return content[:max_length]


def expand_paths(patterns: list[str]) -> list[Path]:
    """Expand glob patterns and return list of files."""
    files = []
    for pattern in patterns:
        # Check if it's a glob pattern
        if '*' in pattern or '?' in pattern:
            matches = glob.glob(pattern, recursive=True)
            files.extend(Path(m) for m in matches)
        else:
            path = Path(pattern)
            if path.exists():
                files.append(path)
            else:
                print(f"Warning: File not found: {pattern}", file=sys.stderr)

    # Remove duplicates while preserving order
    seen = set()
    unique_files = []
    for f in files:
        resolved = f.resolve()
        if resolved not in seen:
            seen.add(resolved)
            unique_files.append(f)

    return sorted(unique_files, key=lambda p: p.name)


def main():
    if len(sys.argv) < 2:
        print("Usage: python parse_webfetch.py <file_or_pattern> [...]", file=sys.stderr)
        print("Example: python parse_webfetch.py .specstory/history/*.md", file=sys.stderr)
        sys.exit(1)

    patterns = sys.argv[1:]
    files = expand_paths(patterns)

    if not files:
        print("No files found matching the provided patterns.", file=sys.stderr)
        sys.exit(1)

    print(f"Processing {len(files)} file(s)...", file=sys.stderr)

    results = []
    for filepath in files:
        for result in parse_file(filepath):
            results.append(asdict(result))

    # Output JSON to stdout
    print(json.dumps(results, indent=2))

    print(f"Found {len(results)} WebFetch instance(s).", file=sys.stderr)


if __name__ == '__main__':
    main()
