"""Shared utilities for skill frontmatter parsing and directory discovery."""
from __future__ import annotations

from pathlib import Path


def find_skill_dirs(base_dir: Path) -> list[Path]:
    """Return sorted list of directories containing a SKILL.md file."""
    return sorted(
        [p.parent for p in base_dir.rglob("SKILL.md") if p.parent != base_dir],
        key=lambda p: p.name,
    )


def extract_frontmatter(text: str) -> dict[str, str]:
    """Parse YAML frontmatter from a SKILL.md file (lenient).

    Returns an empty dict on malformed input instead of raising.
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return {}

    data: dict[str, str] = {}
    current_key = None
    for raw in lines[1:end]:
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith(" ") or raw.startswith("\t"):
            if current_key:
                data[current_key] = f"{data[current_key]}\n{raw.lstrip()}"
            continue
        key, sep, value = raw.partition(":")
        if not sep:
            continue
        current_key = key.strip()
        data[current_key] = value.strip()
    return data


def extract_frontmatter_strict(text: str) -> dict[str, str]:
    """Parse YAML frontmatter from a SKILL.md file (strict).

    Raises ValueError on malformed input.
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing YAML frontmatter opening '---'")

    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        raise ValueError("missing YAML frontmatter closing '---'")

    data: dict[str, str] = {}
    current_key = None
    for raw in lines[1:end]:
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith(" ") or raw.startswith("\t"):
            if current_key:
                data[current_key] = f"{data[current_key]}\n{raw.lstrip()}"
            continue
        key, sep, value = raw.partition(":")
        if not sep:
            raise ValueError(f"invalid frontmatter line: {raw}")
        current_key = key.strip()
        data[current_key] = value.strip()
    return data


def parse_list_field(value: str) -> list[str]:
    """Parse a frontmatter list field value into individual items.

    Handles both inline format ``[a, b, c]`` and multiline YAML (joined with
    newlines, each line starting with ``- ``).
    """
    if not value:
        return []
    stripped = value.strip()
    if stripped.startswith("[") and stripped.endswith("]"):
        inner = stripped[1:-1]
        return [item.strip() for item in inner.split(",") if item.strip()]
    items: list[str] = []
    for line in stripped.split("\n"):
        line = line.strip()
        if line.startswith("- "):
            items.append(line[2:].strip())
        elif line:
            items.append(line)
    return items
