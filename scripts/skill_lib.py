"""Shared utilities for skill frontmatter parsing and directory discovery."""
from __future__ import annotations

from pathlib import Path


def find_skill_dirs(base_dir: Path) -> list[Path]:
    """Discover admitted entrypoints without silently dropping case mistakes.

    Canonical source must be portable, self-contained files. Reject symlinks and
    noncanonical spellings such as ``skill.md`` before they can disappear from
    a generated catalog.
    """
    if base_dir.is_symlink():
        raise ValueError(f"Canonical source must not be a symlink: {base_dir}")
    for path in base_dir.rglob("*"):
        if path.is_symlink():
            raise ValueError(f"Canonical source contains a symlink: {path}")
        if path.is_file() and path.name.casefold() == "skill.md" and path.name != "SKILL.md":
            raise ValueError(f"Noncanonical skill entrypoint (rename to SKILL.md): {path}")
    return sorted(
        [p.parent for p in base_dir.rglob("SKILL.md") if p.parent != base_dir],
        key=lambda p: (p.name, str(p)),
    )


def find_plugin_dirs(plugins_dir: Path) -> list[Path]:
    """Return every plugin, requiring its source descriptor to be present."""
    if not plugins_dir.exists():
        return []
    result = []
    for path in sorted(plugins_dir.iterdir()):
        if path.is_symlink():
            raise ValueError(f"Canonical plugin must not be a symlink: {path}")
        if not path.is_dir():
            continue
        manifest = path / ".claude-plugin" / "plugin.json"
        if not manifest.is_file() or manifest.is_symlink():
            raise ValueError(f"Missing canonical plugin descriptor: {manifest}")
        result.append(path)
    return result


def skill_collections(root: Path) -> dict[str, list[Path]]:
    """Discover all admitted catalog and plugin skills and require unique names."""
    if not (root / "skills").is_dir():
        raise ValueError(f"Missing canonical skills directory: {root / 'skills'}")
    result = {"example": find_skill_dirs(root / "skills"), "plugins": []}
    # Discover the entire plugin tree as well, so misplaced/lowercase entrypoints
    # cannot fall outside a manifest's default skills/ directory unnoticed.
    all_plugin_skills = find_skill_dirs(root / "plugins")
    for plugin in find_plugin_dirs(root / "plugins"):
        result["plugins"].extend(find_skill_dirs(plugin / "skills"))
    if set(all_plugin_skills) != set(result["plugins"]):
        raise ValueError("Plugin entrypoints must live under plugins/<name>/skills/")
    names: set[str] = set()
    for skill in result["example"] + result["plugins"]:
        if skill.name in names:
            raise ValueError(f"Duplicate canonical skill name: {skill.name}")
        names.add(skill.name)
    result["plugins"].sort(key=lambda path: path.name)
    return result


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
        if raw.startswith((" ", "\t")):
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
        if raw.startswith((" ", "\t")):
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
