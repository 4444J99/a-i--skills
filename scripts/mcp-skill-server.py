#!/usr/bin/env python3
"""MCP server for skill discovery and management.

Provides tools for searching, browsing, and planning with skills.
Loads from skills-registry.json when available, falls back to scanning SKILL.md files.

Requires: pip install mcp
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Any

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    raise SystemExit(
        "mcp package required. Install with: pip install mcp"
    )

# Ensure scripts/ is importable
sys.path.insert(0, str(Path(__file__).resolve().parent))
from skill_lib import extract_frontmatter, parse_list_field

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
DOC_SKILLS_DIR = ROOT / "document-skills"
BUILD_DIR = ROOT / ".build"
REGISTRY_PATH = BUILD_DIR / "skills-registry.json"

mcp = FastMCP("ai-skills")

# ---------------------------------------------------------------------------
# Skill loading
# ---------------------------------------------------------------------------

_skills_cache: list[dict] | None = None


def _scan_skills() -> list[dict]:
    """Scan SKILL.md files to build skill list (fallback when no registry)."""
    skills: list[dict] = []
    for base_dir, collection in [(SKILLS_DIR, "example"), (DOC_SKILLS_DIR, "document")]:
        for skill_md in sorted(base_dir.rglob("SKILL.md")):
            skill_dir = skill_md.parent
            if skill_dir == base_dir:
                continue
            try:
                text = skill_md.read_text(encoding="utf-8")
            except OSError:
                continue
            fm = extract_frontmatter(text)
            name = fm.get("name")
            if not name or name != skill_dir.name:
                continue
            # Derive category
            try:
                rel = skill_dir.relative_to(base_dir)
                category = rel.parts[0] if len(rel.parts) >= 2 else "uncategorized"
            except ValueError:
                category = "uncategorized"

            skills.append({
                "name": name,
                "description": fm.get("description", ""),
                "category": category,
                "collection": collection,
                "path": str(skill_dir.relative_to(ROOT)),
                "tags": parse_list_field(fm.get("tags", "")),
                "triggers": parse_list_field(fm.get("triggers", "")),
                "complements": parse_list_field(fm.get("complements", "")),
                "includes": parse_list_field(fm.get("includes", "")),
                "inputs": parse_list_field(fm.get("inputs", "")),
                "outputs": parse_list_field(fm.get("outputs", "")),
                "side_effects": parse_list_field(fm.get("side_effects", "")),
                "tier": fm.get("tier"),
                "complexity": fm.get("complexity"),
                "source": "repo",
            })
    return skills


def _load_skills() -> list[dict]:
    """Load skills from registry JSON or by scanning. Supports custom directory."""
    global _skills_cache
    if _skills_cache is not None:
        return _skills_cache

    skills: list[dict] = []

    # Load from registry if available
    if REGISTRY_PATH.exists():
        try:
            data = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
            skills = data.get("skills", [])
            for s in skills:
                s["source"] = "repo"
        except (json.JSONDecodeError, OSError):
            skills = _scan_skills()
    else:
        skills = _scan_skills()

    # Load custom skills directory (Oh My Zsh pattern)
    custom_dir = os.environ.get("SKILLS_CUSTOM_DIR")
    if custom_dir:
        custom_path = Path(custom_dir)
        if custom_path.is_dir():
            repo_names = {s["name"] for s in skills}
            for skill_md in sorted(custom_path.rglob("SKILL.md")):
                skill_dir = skill_md.parent
                if skill_dir == custom_path:
                    continue
                try:
                    text = skill_md.read_text(encoding="utf-8")
                except OSError:
                    continue
                fm = extract_frontmatter(text)
                name = fm.get("name")
                if not name or name != skill_dir.name:
                    continue

                custom_skill = {
                    "name": name,
                    "description": fm.get("description", ""),
                    "category": "custom",
                    "collection": "custom",
                    "path": str(skill_dir),
                    "tags": parse_list_field(fm.get("tags", "")),
                    "triggers": parse_list_field(fm.get("triggers", "")),
                    "complements": parse_list_field(fm.get("complements", "")),
                    "includes": parse_list_field(fm.get("includes", "")),
                    "inputs": parse_list_field(fm.get("inputs", "")),
                    "outputs": parse_list_field(fm.get("outputs", "")),
                    "side_effects": parse_list_field(fm.get("side_effects", "")),
                    "tier": fm.get("tier"),
                    "complexity": fm.get("complexity"),
                    "source": "custom",
                }

                # Custom skills override repo skills with same name
                if name in repo_names:
                    skills = [s for s in skills if s["name"] != name]
                skills.append(custom_skill)

    _skills_cache = skills
    return skills


# ---------------------------------------------------------------------------
# MCP Tools
# ---------------------------------------------------------------------------


@mcp.tool()
def search_skills(query: str, category: str = "", tier: str = "") -> str:
    """Search skills by keyword. Matches against name, description, and tags.

    Args:
        query: Search term (matched against name, description, tags)
        category: Optional category filter (e.g., "development", "security")
        tier: Optional tier filter ("core" or "community")
    """
    skills = _load_skills()
    query_lower = query.lower()
    results = []

    for skill in skills:
        if category and skill.get("category") != category:
            continue
        if tier and skill.get("tier") != tier:
            continue

        # Score based on match quality
        score = 0
        name = skill["name"]
        desc = skill.get("description", "").lower()
        tags = [t.lower() for t in skill.get("tags", [])]

        if query_lower == name:
            score = 100
        elif query_lower in name:
            score = 80
        elif any(query_lower == t for t in tags):
            score = 70
        elif any(query_lower in t for t in tags):
            score = 60
        elif query_lower in desc:
            score = 40

        if score > 0:
            results.append((score, skill))

    results.sort(key=lambda x: (-x[0], x[1]["name"]))
    top = results[:10]

    if not top:
        return f"No skills found matching '{query}'."

    lines = [f"Found {len(top)} skill(s) matching '{query}':\n"]
    for _, skill in top:
        source_tag = " [custom]" if skill.get("source") == "custom" else ""
        bundle_tag = " [bundle]" if skill.get("includes") else ""
        tier_tag = f" ({skill['tier']})" if skill.get("tier") else ""
        lines.append(
            f"  {skill['name']}{tier_tag}{bundle_tag}{source_tag}\n"
            f"    {skill.get('description', 'No description')[:120]}\n"
            f"    Category: {skill.get('category', 'unknown')} | "
            f"Path: {skill.get('path', 'unknown')}"
        )
    return "\n".join(lines)


@mcp.tool()
def get_skill_info(name: str) -> str:
    """Get detailed information about a specific skill.

    Args:
        name: The skill name (e.g., "mcp-builder", "tdd-workflow")
    """
    skills = _load_skills()
    skill = next((s for s in skills if s["name"] == name), None)
    if not skill:
        return f"Skill '{name}' not found."

    lines = [f"# {skill['name']}\n"]
    lines.append(f"**Description**: {skill.get('description', 'N/A')}")
    lines.append(f"**Category**: {skill.get('category', 'N/A')}")
    lines.append(f"**Collection**: {skill.get('collection', 'N/A')}")
    lines.append(f"**Path**: {skill.get('path', 'N/A')}")

    if skill.get("tier"):
        lines.append(f"**Tier**: {skill['tier']}")
    if skill.get("complexity"):
        lines.append(f"**Complexity**: {skill['complexity']}")
    if skill.get("source") == "custom":
        lines.append("**Source**: Custom override")

    if skill.get("inputs"):
        lines.append(f"\n**Inputs**: {', '.join(skill['inputs'])}")
    if skill.get("outputs"):
        lines.append(f"**Outputs**: {', '.join(skill['outputs'])}")
    if skill.get("side_effects"):
        lines.append(f"**Side Effects**: {', '.join(skill['side_effects'])}")
    if skill.get("triggers"):
        lines.append(f"**Triggers**: {', '.join(skill['triggers'])}")
    if skill.get("tags"):
        lines.append(f"**Tags**: {', '.join(skill['tags'])}")
    if skill.get("complements"):
        lines.append(f"\n**Complements**: {', '.join(skill['complements'])}")

    # Bundle info
    if skill.get("includes"):
        lines.append(f"\n**Bundle** ({len(skill['includes'])} skills):")
        for included in skill["includes"]:
            lines.append(f"  - {included}")

    return "\n".join(lines)


@mcp.tool()
def find_complementary_skills(skill_name: str) -> str:
    """Find skills that complement a given skill.

    Args:
        skill_name: The skill to find complements for
    """
    skills = _load_skills()
    skill = next((s for s in skills if s["name"] == skill_name), None)
    if not skill:
        return f"Skill '{skill_name}' not found."

    complements = set(skill.get("complements", []))

    # Also find skills that list this skill as a complement
    for other in skills:
        if skill_name in other.get("complements", []):
            complements.add(other["name"])

    # Find skills with overlapping tags
    skill_tags = set(skill.get("tags", []))
    tag_matches: list[tuple[int, str]] = []
    for other in skills:
        if other["name"] == skill_name or other["name"] in complements:
            continue
        other_tags = set(other.get("tags", []))
        overlap = len(skill_tags & other_tags)
        if overlap >= 2:
            tag_matches.append((overlap, other["name"]))

    tag_matches.sort(key=lambda x: -x[0])

    lines = [f"Complements for '{skill_name}':\n"]

    if complements:
        lines.append("**Declared complements:**")
        for c in sorted(complements):
            comp_skill = next((s for s in skills if s["name"] == c), None)
            desc = comp_skill["description"][:80] if comp_skill else "Not found in registry"
            lines.append(f"  - {c}: {desc}")

    if tag_matches[:5]:
        lines.append("\n**Related by tags:**")
        for _, name in tag_matches[:5]:
            related = next((s for s in skills if s["name"] == name), None)
            if related:
                lines.append(f"  - {name}: {related['description'][:80]}")

    if not complements and not tag_matches:
        lines.append("No complements found.")

    return "\n".join(lines)


@mcp.tool()
def suggest_skills_for_context(
    file_patterns: str = "",
    keywords: str = "",
    project_files: str = "",
) -> str:
    """Suggest relevant skills based on activation triggers matching current context.

    Args:
        file_patterns: Comma-separated file patterns in the project (e.g., "*.test.ts, *.py")
        keywords: Comma-separated keywords from user request (e.g., "testing, api, security")
        project_files: Comma-separated project files that exist (e.g., "package.json, Dockerfile")
    """
    skills = _load_skills()
    scored: list[tuple[int, dict]] = []

    file_pats = [p.strip() for p in file_patterns.split(",") if p.strip()]
    kws = [k.strip().lower() for k in keywords.split(",") if k.strip()]
    proj_files = [f.strip() for f in project_files.split(",") if f.strip()]

    for skill in skills:
        score = 0
        triggers = skill.get("triggers", [])

        for trigger in triggers:
            # user-asks-about-<topic>
            if trigger.startswith("user-asks-about-"):
                topic = trigger[len("user-asks-about-"):]
                if any(topic in kw or kw in topic for kw in kws):
                    score += 30

            # project-has-<pattern>
            elif trigger.startswith("project-has-"):
                pattern = trigger[len("project-has-"):]
                normalized = pattern.replace("-", ".").replace("_", ".")
                if any(normalized in f.lower().replace("-", ".") for f in proj_files):
                    score += 25

            # file-type:<glob>
            elif trigger.startswith("file-type:"):
                glob_pat = trigger[len("file-type:"):]
                ext = glob_pat.lstrip("*")
                if any(ext in fp for fp in file_pats):
                    score += 20

            # context:<keyword>
            elif trigger.startswith("context:"):
                ctx = trigger[len("context:"):]
                if any(ctx in kw or kw in ctx for kw in kws):
                    score += 15

        # Also match on tags
        tags = [t.lower() for t in skill.get("tags", [])]
        for kw in kws:
            if any(kw == t or kw in t for t in tags):
                score += 10

        if score > 0:
            scored.append((score, skill))

    scored.sort(key=lambda x: (-x[0], x[1]["name"]))
    top = scored[:8]

    if not top:
        return "No skills match the given context. Try broader keywords."

    lines = ["Suggested skills for current context:\n"]
    for score, skill in top:
        tier_tag = f" ({skill['tier']})" if skill.get("tier") else ""
        lines.append(
            f"  [{score}] {skill['name']}{tier_tag}\n"
            f"       {skill.get('description', '')[:100]}"
        )
    return "\n".join(lines)


@mcp.tool()
def plan_skill_chain(goal: str) -> str:
    """Suggest a chain of skills to accomplish a goal using inputs/outputs compatibility.

    Args:
        goal: High-level description of what you want to accomplish
    """
    skills = _load_skills()
    goal_lower = goal.lower()

    # Score skills by relevance to the goal
    scored: list[tuple[int, dict]] = []
    for skill in skills:
        score = 0
        name = skill["name"]
        desc = skill.get("description", "").lower()
        tags = [t.lower() for t in skill.get("tags", [])]

        goal_words = re.findall(r'\w+', goal_lower)
        for word in goal_words:
            if len(word) < 3:
                continue
            if word in name:
                score += 20
            if word in desc:
                score += 10
            if any(word in t for t in tags):
                score += 15

        if score > 0:
            scored.append((score, skill))

    scored.sort(key=lambda x: -x[0])
    relevant = [s for _, s in scored[:10]]

    if not relevant:
        return f"No skills found relevant to: {goal}"

    # Build a suggested chain based on outputs -> inputs matching
    chain: list[dict] = []
    available_outputs: set[str] = set()

    # Greedy chain building: pick skills whose inputs are satisfied
    remaining = list(relevant)
    for _ in range(len(remaining)):
        best = None
        best_score = -1
        for skill in remaining:
            inputs = set(skill.get("inputs", []))
            satisfied = len(inputs & available_outputs)
            unsatisfied = len(inputs - available_outputs)
            # Prefer skills with more satisfied inputs, fewer unsatisfied
            s = satisfied * 10 - unsatisfied * 5
            if not chain:
                s = 0  # First skill has no dependency preference
            if s > best_score or (s == best_score and not chain):
                best_score = s
                best = skill
        if best:
            chain.append(best)
            remaining.remove(best)
            available_outputs.update(best.get("outputs", []))

    # Add complementary skills
    complement_names: set[str] = set()
    for skill in chain:
        complement_names.update(skill.get("complements", []))
    complement_names -= {s["name"] for s in chain}

    lines = [f"Suggested skill chain for: {goal}\n"]
    lines.append("## Chain (ordered by dependency):\n")
    for i, skill in enumerate(chain, 1):
        inputs = ", ".join(skill.get("inputs", [])) or "none"
        outputs = ", ".join(skill.get("outputs", [])) or "none"
        lines.append(
            f"{i}. **{skill['name']}** ({skill.get('category', 'unknown')})\n"
            f"   Inputs: {inputs}\n"
            f"   Outputs: {outputs}"
        )

    if complement_names:
        lines.append("\n## Also consider:")
        for name in sorted(complement_names):
            comp = next((s for s in skills if s["name"] == name), None)
            if comp:
                lines.append(f"  - {name}: {comp.get('description', '')[:80]}")

    return "\n".join(lines)


@mcp.tool()
def list_categories() -> str:
    """List all skill categories with counts."""
    skills = _load_skills()
    categories: dict[str, int] = {}
    for skill in skills:
        cat = skill.get("category", "uncategorized")
        categories[cat] = categories.get(cat, 0) + 1

    lines = [f"Skill categories ({len(categories)} total, {len(skills)} skills):\n"]
    for cat in sorted(categories.keys()):
        lines.append(f"  {cat}: {categories[cat]} skills")
    return "\n".join(lines)


@mcp.tool()
def list_bundles() -> str:
    """List all skill bundles (packs) with their included skills."""
    skills = _load_skills()
    bundles = [s for s in skills if s.get("includes")]

    if not bundles:
        return "No skill bundles found."

    lines = [f"Skill bundles ({len(bundles)}):\n"]
    for bundle in bundles:
        lines.append(
            f"**{bundle['name']}** ({len(bundle['includes'])} skills)\n"
            f"  {bundle.get('description', '')[:120]}\n"
            f"  Includes: {', '.join(bundle['includes'])}"
        )
    return "\n".join(lines)


if __name__ == "__main__":
    mcp.run()
