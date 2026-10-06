"""Tests for the skill tooling in scripts/ and for repository invariants.

These run against the real repository tree, so they catch drift between the
skills, the generated bundles, the registry, and the plugin marketplace.
"""
from __future__ import annotations

import importlib
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

import skill_lib

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
PLUGINS_DIR = ROOT / "plugins"
SCRIPTS = ROOT / "scripts"

validate_skills = importlib.import_module("validate_skills")
generate_registry = importlib.import_module("generate_registry")
pr_validation_report = importlib.import_module("pr_validation_report")

# Names Claude Code reserves for official Anthropic marketplaces; a third-party
# marketplace must not use them (see the Claude Code marketplace reference).
RESERVED_MARKETPLACE_NAMES = {
    "claude-code-marketplace", "claude-code-plugins", "claude-plugins-official",
    "anthropic-marketplace", "anthropic-plugins", "agent-skills",
    "anthropic-agent-skills", "life-sciences", "knowledge-work-plugins",
}
MARKETPLACE_NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


def _write_skill(base: Path, name: str, frontmatter: str, body: str = "Body.\n") -> Path:
    skill_dir = base / name
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(f"---\n{frontmatter}---\n\n{body}", encoding="utf-8")
    return skill_dir


# --------------------------------------------------------------------------
# skill_lib
# --------------------------------------------------------------------------

def test_extract_frontmatter_parses_scalars_and_multiline_lists():
    text = (
        "---\n"
        "name: demo-skill\n"
        "description: A demo skill used by the test suite.\n"
        "# a comment line is ignored\n"
        "triggers:\n"
        "  - user-asks-about-demo\n"
        "  - file-type:*.demo\n"
        "---\n"
        "# Body\n"
    )
    data = skill_lib.extract_frontmatter(text)
    assert data["name"] == "demo-skill"
    assert data["description"] == "A demo skill used by the test suite."
    assert skill_lib.parse_list_field(data["triggers"]) == [
        "user-asks-about-demo",
        "file-type:*.demo",
    ]


def test_parse_list_field_inline_and_empty():
    assert skill_lib.parse_list_field("[a, b , c]") == ["a", "b", "c"]
    assert skill_lib.parse_list_field("") == []


def test_extract_frontmatter_lenient_vs_strict_on_malformed_input():
    assert skill_lib.extract_frontmatter("no frontmatter here") == {}
    with pytest.raises(ValueError):
        skill_lib.extract_frontmatter_strict("no frontmatter here")
    with pytest.raises(ValueError):
        skill_lib.extract_frontmatter_strict("---\nname: x\n")  # never closed
    with pytest.raises(ValueError):
        skill_lib.extract_frontmatter_strict("---\nthis line has no colon\n---\n")


def test_find_skill_dirs_ignores_base_dir(tmp_path):
    (tmp_path / "SKILL.md").write_text("---\nname: root\n---\n", encoding="utf-8")
    _write_skill(tmp_path / "cat", "b-skill", "name: b-skill\n")
    _write_skill(tmp_path / "cat", "a-skill", "name: a-skill\n")
    found = skill_lib.find_skill_dirs(tmp_path)
    assert [p.name for p in found] == ["a-skill", "b-skill"]


# --------------------------------------------------------------------------
# validate_skills rules
# --------------------------------------------------------------------------

GOOD_FM = (
    "name: good-skill\n"
    "description: Does a clearly described, task-focused thing for tests.\n"
    "license: MIT\n"
)


def test_validate_skill_accepts_well_formed_skill(tmp_path):
    skill = _write_skill(tmp_path, "good-skill", GOOD_FM)
    assert validate_skills._validate_skill(skill, check_links=True) == []


@pytest.mark.parametrize(
    "frontmatter, expected",
    [
        ("name: other-name\ndescription: A long enough description.\nlicense: MIT\n", "does not match directory"),
        ("name: bad-skill\ndescription: short\nlicense: MIT\n", "description too short"),
        ("name: bad-skill\ndescription: A long enough description here.\n", "missing 'license'"),
        ("name: bad-skill\nlicense: MIT\n", "missing 'description'"),
        ("name: bad-skill\ndescription: A long enough description.\nlicense: MIT\ncomplexity: expert\n", "complexity"),
    ],
)
def test_validate_skill_reports_rule_violations(tmp_path, frontmatter, expected):
    skill = _write_skill(tmp_path, "bad-skill", frontmatter)
    errors = validate_skills._validate_skill(skill)
    assert any(expected in e for e in errors), errors


def test_validate_skill_check_links_flags_missing_files(tmp_path):
    body = "See [the guide](references/guide.md) and `references/missing.md`.\n"
    skill = _write_skill(tmp_path, "good-skill", GOOD_FM, body)
    errors = validate_skills._validate_skill(skill, check_links=True)
    assert any("broken link" in e for e in errors)
    assert any("missing reference" in e for e in errors)
    # Links inside fenced code blocks are not treated as links.
    skill2 = _write_skill(tmp_path / "x", "good-skill", GOOD_FM, "```\n[x](nope.md)\n```\n")
    assert validate_skills._validate_skill(skill2, check_links=True) == []


def test_repository_skills_pass_validation():
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "validate_skills.py"),
         "--collection", "example", "--unique", "--check-links"],
        capture_output=True, text=True, cwd=ROOT,
    )
    assert result.returncode == 0, result.stdout + result.stderr


# --------------------------------------------------------------------------
# registry, generated bundles, PR report helpers
# --------------------------------------------------------------------------

def test_registry_matches_skill_tree():
    registry = json.loads((ROOT / "distributions" / "skills-registry.json").read_text(encoding="utf-8"))
    assert registry["repository"] == "4444J99/a-i--skills"
    names = {s["name"] for s in registry["skills"]}
    on_disk = {p.name for p in skill_lib.find_skill_dirs(SKILLS_DIR)}
    assert names == on_disk
    assert {s["collection"] for s in registry["skills"]} == {"example"}


def test_build_skill_entry_derives_category_and_resources(tmp_path, monkeypatch):
    monkeypatch.setattr(generate_registry, "ROOT", tmp_path)
    base = tmp_path / "skills"
    skill = _write_skill(
        base / "data", "good-skill",
        GOOD_FM + "complexity: beginner\ncomplements: [other-skill]\n",
    )
    (skill / "references").mkdir()
    (skill / "references" / "guide.md").write_text("x", encoding="utf-8")
    entry = generate_registry._build_skill_entry(skill, base, "example")
    assert entry is not None
    assert entry["name"] == "good-skill"
    assert entry["category"] == "data"
    assert entry["collection"] == "example"
    assert entry["path"] == "skills/data/good-skill"
    assert entry["complements"] == ["other-skill"]
    assert entry["resources"]["references"] == ["guide.md"]
    # A name/directory mismatch is skipped rather than registered.
    bad = _write_skill(base / "data", "mismatch", "name: something-else\n")
    assert generate_registry._build_skill_entry(bad, base, "example") is None


def test_generated_bundles_are_in_sync():
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "validate_generated_dirs.py")],
        capture_output=True, text=True, cwd=ROOT,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_pr_report_maps_changed_files_to_skill_dirs():
    some_skill = skill_lib.find_skill_dirs(SKILLS_DIR)[0]
    rel = some_skill.relative_to(ROOT)
    changed = [
        str(rel / "SKILL.md"),
        str(rel / "references" / "x.md"),
        "README.md",
        "skills/not-a-category-file.md",
    ]
    affected = pr_validation_report._affected_skill_dirs(changed)
    assert affected == [some_skill]


# --------------------------------------------------------------------------
# marketplace manifest
# --------------------------------------------------------------------------

def test_marketplace_manifest_is_valid_and_owned_by_repo_owner():
    data = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    assert MARKETPLACE_NAME_RE.match(data["name"])
    assert data["name"] not in RESERVED_MARKETPLACE_NAMES
    assert data["owner"]["name"]
    assert "anthropic" not in json.dumps(data["owner"]).lower()

    names = [p["name"] for p in data["plugins"]]
    assert len(names) == len(set(names))
    for plugin in data["plugins"]:
        source = plugin["source"]
        assert source.startswith("./") and ".." not in source
        plugin_root = (ROOT / source).resolve()
        assert plugin_root.is_dir(), source
        has_manifest = (plugin_root / ".claude-plugin" / "plugin.json").exists()
        skills = plugin.get("skills", [])
        # strict=false + plugin.json + component fields is a load-time conflict.
        if has_manifest and skills:
            assert plugin.get("strict", True) is True, plugin["name"]
        for skill_path in skills:
            assert (ROOT / skill_path / "SKILL.md").exists(), skill_path


def test_marketplace_lists_every_catalog_skill():
    data = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    catalog = next(p for p in data["plugins"] if p["name"] == "example-skills")
    listed = {Path(s).name for s in catalog["skills"]}
    assert listed == {p.name for p in skill_lib.find_skill_dirs(SKILLS_DIR)}


# --------------------------------------------------------------------------
# licensing guard
# --------------------------------------------------------------------------

def test_no_all_rights_reserved_licenses_in_tree():
    """Only redistributable (open-licensed) skills may ship in this repo."""
    offenders = []
    for base in (SKILLS_DIR, PLUGINS_DIR, ROOT / "distributions"):
        for lic in base.rglob("LICENSE*"):
            if lic.is_file() and "all rights reserved" in lic.read_text(encoding="utf-8", errors="ignore").lower():
                offenders.append(str(lic.relative_to(ROOT)))
    assert offenders == []
    assert not (ROOT / "document-skills").exists()
