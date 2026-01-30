#!/usr/bin/env python3
"""
Extract URLs from context surrounding a WebFetch block.

This helper scans backwards from a WebFetch position to find the likely URL
that was fetched, using multiple discovery strategies.
"""

import re
from typing import Optional, Tuple

# URL pattern - matches http:// or https:// URLs
URL_PATTERN = re.compile(
    r'https?://[^\s<>"\'\]\)]+',
    re.IGNORECASE
)

# Patterns that indicate a URL fetch request
FETCH_PATTERNS = [
    re.compile(r'(?:read|fetch|go to|visit|check|analyze|look at)\s+(https?://[^\s<>"\']+)', re.IGNORECASE),
    re.compile(r'(https?://[^\s<>"\']+)\s*(?:and|,|\s)', re.IGNORECASE),
]

# Domain pattern for domain analysis sessions - capture full domain
DOMAIN_PATTERN = re.compile(r'\b([a-zA-Z0-9][-a-zA-Z0-9]*(?:\.[a-zA-Z0-9][-a-zA-Z0-9]*)*\.[a-zA-Z]{2,})\b')

# Common TLDs for validation
COMMON_TLDS = ['com', 'org', 'net', 'io', 'ai', 'dev', 'co', 'it', 'de', 'fr', 'uk', 'kr', 'ua', 'tech', 'app', 'edu', 'gov', 'ac']


def extract_url_from_context(
    lines: list[str],
    webfetch_line_idx: int,
    lookback: int = 50,
    result_content: Optional[str] = None
) -> Tuple[Optional[str], str]:
    """
    Extract the URL that was likely fetched from surrounding context.

    Args:
        lines: All lines from the file
        webfetch_line_idx: Line index where WebFetch block starts
        lookback: Number of lines to look back
        result_content: Optional content of the WebFetch result (for inferring from headers)

    Returns:
        Tuple of (url, source) where source is one of:
        - "user_message": Found in a user message
        - "thinking": Found in a <think> block
        - "task_prompt": Found in a Task tool prompt
        - "result_content": Inferred from the result header
        - "inferred": Inferred from domain mention
        - "unknown": Could not determine
    """
    start_idx = max(0, webfetch_line_idx - lookback)
    context_lines = lines[start_idx:webfetch_line_idx]
    context = '\n'.join(context_lines)

    # Strategy 1: Look for explicit fetch patterns in user messages
    user_msg_match = find_url_in_user_message(context_lines)
    if user_msg_match:
        return user_msg_match, "user_message"

    # Strategy 2: Look in thinking blocks
    think_match = find_url_in_thinking(context)
    if think_match:
        return think_match, "thinking"

    # Strategy 3: Look in Task tool prompts (subagent spawning)
    task_match = find_url_in_task_prompt(context)
    if task_match:
        return task_match, "task_prompt"

    # Strategy 4: Find any URL in recent context (last 20 lines)
    recent_context = '\n'.join(context_lines[-20:])
    urls = URL_PATTERN.findall(recent_context)
    if urls:
        # Filter out common non-target URLs
        urls = [u for u in urls if not is_noise_url(u)]
        if urls:
            return urls[-1], "inferred"

    # Strategy 5: Infer from result content header (e.g., "# SpecStory: Company Overview")
    if result_content:
        result_url = infer_url_from_result(result_content)
        if result_url:
            return result_url, "result_content"

    # Strategy 6: Infer from domain mention (for domain analysis sessions)
    domain_match = find_domain_for_inference(context_lines[-30:])
    if domain_match:
        return f"https://{domain_match}", "inferred"

    return None, "unknown"


def infer_url_from_result(content: str) -> Optional[str]:
    """
    Infer the URL from the WebFetch result content.

    Strategies (in order):
    1. Look for explicit URLs in the result
    2. For error messages, extract domain from error text
    3. Look for domain patterns anywhere in the result
    """
    if not content:
        return None

    content_lower = content.lower()

    # Strategy 1: Look for explicit URLs in the result
    urls = URL_PATTERN.findall(content[:1000])
    if urls:
        urls = [u for u in urls if not is_noise_url(u)]
        if urls:
            return urls[0]

    # Strategy 2: For error messages, extract domain from error text
    # e.g., "getaddrinfo ENOTFOUND billyemail.com"
    # e.g., "Hostname/IP does not match certificate's altnames: Host: mailbox.in.ua"
    error_domain_patterns = [
        re.compile(r'ENOTFOUND\s+([a-zA-Z0-9][-a-zA-Z0-9]*(?:\.[a-zA-Z0-9][-a-zA-Z0-9]*)+)', re.IGNORECASE),
        re.compile(r'Host:\s*([a-zA-Z0-9][-a-zA-Z0-9]*(?:\.[a-zA-Z0-9][-a-zA-Z0-9]*)+)', re.IGNORECASE),
        re.compile(r'certificate.*?([a-zA-Z0-9][-a-zA-Z0-9]*\.[a-zA-Z]{2,})', re.IGNORECASE),
    ]
    for pattern in error_domain_patterns:
        match = pattern.search(content)
        if match:
            domain = match.group(1).strip().rstrip('.')
            if not is_noise_domain(domain):
                return f"https://{domain}"

    # Strategy 3: Look for domain patterns in the first part of content
    # This helps for results that mention the domain being analyzed
    domains = DOMAIN_PATTERN.findall(content[:500])
    if domains:
        # Filter out noise and pick the first valid domain
        for domain in domains:
            if not is_noise_domain(domain) and not is_noise_url(f"https://{domain}"):
                return f"https://{domain}"

    return None


def find_url_in_user_message(lines: list[str]) -> Optional[str]:
    """Find URL in user message blocks."""
    in_user_msg = False
    user_msg_content = []

    for line in reversed(lines):
        if '_**User' in line:
            in_user_msg = True
            continue
        if in_user_msg:
            if line.startswith('_**') or line.startswith('---'):
                # End of user message block, check what we found
                content = '\n'.join(reversed(user_msg_content))
                for pattern in FETCH_PATTERNS:
                    match = pattern.search(content)
                    if match:
                        return match.group(1) if match.lastindex else match.group(0)
                # Also try simple URL extraction
                urls = URL_PATTERN.findall(content)
                if urls:
                    return urls[0]
                break
            user_msg_content.append(line)

    return None


def find_url_in_thinking(context: str) -> Optional[str]:
    """Find URL mentioned in <think> blocks."""
    think_pattern = re.compile(r'<think>.*?</think>', re.DOTALL)
    think_blocks = think_pattern.findall(context)

    for block in reversed(think_blocks):
        # Look for fetch-related URL mentions
        for pattern in FETCH_PATTERNS:
            match = pattern.search(block)
            if match:
                return match.group(1) if match.lastindex else match.group(0)

        # Try simple URL extraction
        urls = URL_PATTERN.findall(block)
        if urls:
            urls = [u for u in urls if not is_noise_url(u)]
            if urls:
                return urls[-1]

    return None


def find_url_in_task_prompt(context: str) -> Optional[str]:
    """Find URL in Task tool prompts that spawned subagents."""
    task_pattern = re.compile(
        r'<tool-use[^>]*data-tool-name="Task"[^>]*>.*?</tool-use>',
        re.DOTALL
    )
    task_blocks = task_pattern.findall(context)

    for block in reversed(task_blocks):
        urls = URL_PATTERN.findall(block)
        if urls:
            urls = [u for u in urls if not is_noise_url(u)]
            if urls:
                return urls[-1]

        # Also look for domain patterns in task prompts
        domains = DOMAIN_PATTERN.findall(block)
        if domains:
            # Reconstruct domain from tuple (DOMAIN_PATTERN captures groups)
            for domain_parts in domains:
                if isinstance(domain_parts, tuple):
                    continue
                domain = domain_parts
                if not is_noise_domain(domain):
                    return f"https://{domain}"

    return None


def find_domain_for_inference(lines: list[str]) -> Optional[str]:
    """Find a domain that was likely being analyzed."""
    # Look for domain patterns in recent lines
    for line in reversed(lines):
        # Skip tool output lines
        if '<tool-use' in line or '</tool-use>' in line:
            continue

        domains = DOMAIN_PATTERN.findall(line)
        for domain in domains:
            if isinstance(domain, str) and not is_noise_domain(domain):
                return domain

    return None


def is_noise_url(url: str) -> bool:
    """Check if URL is likely noise (not the target of a fetch)."""
    noise_patterns = [
        'github.com/anthropics',
        'claude.com/docs',
        'json-schema.org',
        'localhost',
        '127.0.0.1',
        'example.com',  # Unless explicitly being analyzed
    ]
    url_lower = url.lower()

    # Check for noise patterns
    if any(pattern in url_lower for pattern in noise_patterns):
        return True

    # Check for file extensions that aren't real domains
    fake_tld_patterns = [
        r'\.md$', r'\.js$', r'\.ts$', r'\.py$', r'\.json$', r'\.yaml$', r'\.yml$',
        r'\.sh$', r'\.css$', r'\.html$', r'\.txt$', r'\.xml$', r'\.toml$',
    ]
    for pattern in fake_tld_patterns:
        if re.search(pattern, url_lower):
            return True

    return False


def is_noise_domain(domain: str) -> bool:
    """Check if domain is likely noise."""
    noise_domains = [
        'github.com',
        'claude.com',
        'anthropic.com',
        'example.com',
        'localhost',
        'schema.org',
    ]
    domain_lower = domain.lower()

    # Check exact matches
    if domain_lower in noise_domains:
        return True

    # Check subdomain matches
    if any(domain_lower.endswith('.' + nd) for nd in noise_domains):
        return True

    # Check for file extensions masquerading as TLDs
    file_extensions = [
        '.md', '.js', '.ts', '.jsx', '.tsx', '.py', '.json', '.yaml', '.yml',
        '.sh', '.css', '.html', '.txt', '.xml', '.toml', '.rb', '.go', '.rs',
        '.vue', '.svelte', '.astro', '.php', '.java', '.c', '.cpp', '.h',
    ]
    if any(domain_lower.endswith(ext) for ext in file_extensions):
        return True

    # Check for common non-domain patterns
    tech_names = [
        'next.js', 'react.js', 'vue.js', 'node.js', 'express.js',
        'skill.md', 'readme.md', 'settings.json', 'package.json',
        # JavaScript/API patterns that look like domains
        'location.href', 'window.location', 'document.location',
        'tweet.fields', 'user.fields', 'media.fields',
        # Other false positives
        'e.g.', 'i.e.', 'etc.',
    ]
    if domain_lower in tech_names:
        return True

    # Check if it looks like a JavaScript property access pattern
    if '.href' in domain_lower or '.fields' in domain_lower:
        return True

    return False


if __name__ == '__main__':
    # Simple test
    test_lines = [
        "_**User (2026-01-22T19:27:48.418Z)**_",
        "",
        "read https://specstory.com and analyze it",
        "",
        "---",
        "",
        "_**Agent**_",
        "",
        '<tool-use data-tool-type="unknown" data-tool-name="WebFetch">',
    ]

    url, source = extract_url_from_context(test_lines, len(test_lines) - 1)
    print(f"URL: {url}, Source: {source}")
