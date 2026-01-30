"""Parsing utilities for specstory history files."""

import re
from datetime import datetime
from typing import Optional


def parse_date_from_filename(filename: str) -> Optional[datetime]:
    """Extract date from specstory filename format: YYYY-MM-DD_HH-MM-SSZ-title.md"""
    match = re.match(r"(\d{4}-\d{2}-\d{2})_(\d{2}-\d{2})", filename)
    if match:
        date_str = match.group(1)
        time_str = match.group(2).replace("-", ":")
        try:
            return datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        except ValueError:
            pass
    return None


def extract_title_from_filename(filename: str) -> str:
    """Extract human-readable title from filename."""
    # Remove date prefix and extension
    match = re.match(r"\d{4}-\d{2}-\d{2}_\d{2}-\d{2}(?:-\d{2})?Z?-?(.*)\.md", filename)
    if match and match.group(1):
        return match.group(1).replace("-", " ").strip()
    return filename


def extract_session_id(content: str) -> str:
    """Extract session UUID from specstory header."""
    match = re.search(r"Session\s+([a-f0-9-]{36})", content)
    return match.group(1) if match else "unknown"


def extract_messages(content: str) -> list[tuple[str, str, str]]:
    """
    Extract user/agent messages from specstory content.
    Returns list of (role, timestamp, message_text)
    """
    messages = []

    # Pattern for message headers: _**User (timestamp)**_ or _**Agent (...)**_
    pattern = r"_\*\*(\w+)(?:\s+\([^)]*\))?\s*\(([^)]+)\)\*\*_\s*(?:<!--[^>]+-->)?\s*(.*?)(?=_\*\*(?:User|Agent|Assistant)|$)"

    for match in re.finditer(pattern, content, re.DOTALL):
        role = match.group(1).lower()
        timestamp = match.group(2)
        text = match.group(3).strip()

        # Clean up the text - remove trailing ---
        text = re.sub(r"\n---\s*$", "", text).strip()

        if role in ("user", "agent", "assistant"):
            messages.append((role, timestamp, text))

    return messages


def extract_file_refs(content: str) -> list[str]:
    """Extract @file references from content."""
    # Match @path/to/file or @filename patterns
    refs = re.findall(r"@([\w./\-]+(?:\.\w+)?)", content)
    return list(set(refs))


def extract_tool_calls(content: str) -> dict[str, int]:
    """Extract tool call counts from content."""
    tools = {}

    # Pattern 1: Tool use: **ToolName**
    for match in re.finditer(r"Tool use:\s*\*\*(\w+)\*\*", content):
        tool = match.group(1)
        tools[tool] = tools.get(tool, 0) + 1

    # Pattern 2: <tool-use data-tool-name="ToolName">
    for match in re.finditer(r'data-tool-name="(\w+)"', content):
        tool = match.group(1)
        tools[tool] = tools.get(tool, 0) + 1

    return tools


def summarize_message(msg: str, max_len: int = 100) -> str:
    """Create a short summary of a message."""
    # Take first line or first N chars
    first_line = msg.split("\n")[0].strip()
    if len(first_line) > max_len:
        return first_line[:max_len-3] + "..."
    return first_line


def detect_goal(initial_message: str) -> str:
    """Extract the likely goal from the initial message."""
    msg_lower = initial_message.lower()

    # Look for explicit goal indicators
    patterns = [
        r"(?:help me|i want to|i need to|let's|please)\s+(.{10,80})",
        r"(?:fix|add|create|build|implement|update|refactor)\s+(.{10,80})",
        r"^(.{10,80})\?",  # Questions
    ]

    for pattern in patterns:
        match = re.search(pattern, msg_lower)
        if match:
            return match.group(1).strip()[:80]

    return summarize_message(initial_message, 80)
