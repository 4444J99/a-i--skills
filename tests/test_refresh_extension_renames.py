"""Configuration renames retire only proven generated Gemini output."""

from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

import validate_generated_dirs


ROOT = Path(__file__).resolve().parents[1]


def refresh(root):
    return subprocess.run(
        [sys.executable, str(root / "scripts/refresh_skill_collections.py"),
         "--skip-readme", "--skip-ecosystem"],
        cwd=root, capture_output=True, text=True,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )


@pytest.fixture
def generated_catalog(tmp_path):
    root = tmp_path / "catalog"
    root.mkdir()
    shutil.copytree(
        ROOT / "scripts", root / "scripts",
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
    )
    skill = root / "skills/testing/rename-example/SKILL.md"
    skill.parent.mkdir(parents=True)
    skill.write_text(
        "---\nname: rename-example\n"
        "description: Exercise catalog metadata renames without losing source.\n"
        "license: MIT\n---\n\nCanonical instructions must survive refresh.\n"
    )
    documents = {
        ".claude-plugin/plugin.json": {
            "name": "example-skills",
            "description": "Catalog rename acceptance fixture.",
            "version": "1.0.0", "author": {"name": "Catalog Owner"}, "license": "MIT",
        },
        "config/runtime-catalog.json": {
            "schema_version": 1, "repository": "example/catalog",
            "marketplace": {"name": "rename-catalog", "description": "Rename fixture."},
            "gemini": {"label": "Catalog Skills", "context_file": "GEMINI.md"},
            "purpose_collections": {},
        },
    }
    for relative, value in documents.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value) + "\n")
    result = refresh(root)
    assert result.returncode == 0, result.stdout + result.stderr
    return root


def rename_config(root, name="renamed-skills", context="CONTEXT.md"):
    for relative, key, value in (
        (".claude-plugin/plugin.json", "name", name),
        ("config/runtime-catalog.json", "context_file", context),
    ):
        path = root / relative
        data = json.loads(path.read_text())
        (data["gemini"] if key == "context_file" else data)[key] = value
        path.write_text(json.dumps(data) + "\n")


def snapshot(root):
    result = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            result[relative] = ("link", os.readlink(path))
        elif path.is_file():
            result[relative] = ("file", path.stat().st_mode & 0o777, path.read_bytes())
        else:
            result[relative] = ("directory", path.stat().st_mode & 0o777)
    return result


@pytest.mark.parametrize("name,context", [
    ("example-skills", "CONTEXT.md"),
    ("renamed-skills", "GEMINI.md"),
    ("renamed-skills", "CONTEXT.md"),
])
def test_refresh_accepts_catalog_and_context_renames(generated_catalog, name, context):
    root = generated_catalog
    canonical = snapshot(root / "skills")
    rename_config(root, name, context)

    result = refresh(root)

    assert result.returncode == 0, result.stdout + result.stderr
    assert validate_generated_dirs.validate_generated(root) == []
    extension = root / "distributions/extensions/gemini" / name
    assert {p.name for p in extension.iterdir()} == {
        "skills", "gemini-extension.json", context,
    }
    assert json.loads((extension / "gemini-extension.json").read_text())[
        "contextFileName"
    ] == context
    if name != "example-skills":
        assert not (extension.parent / "example-skills").exists()
    assert snapshot(root / "skills") == canonical
    before = snapshot(root / "distributions")
    repeated = refresh(root)
    assert repeated.returncode == 0, repeated.stdout + repeated.stderr
    assert snapshot(root / "distributions") == before


@pytest.mark.parametrize("damage", [
    "empty-object", "array", "missing-context", "unsafe-context", "absent-context",
])
def test_refresh_repairs_unusable_current_descriptor(generated_catalog, damage):
    root = generated_catalog
    extension = root / "distributions/extensions/gemini/example-skills"
    descriptor = extension / "gemini-extension.json"
    expected_descriptor = json.loads(descriptor.read_text())
    value = dict(expected_descriptor)
    if damage == "empty-object":
        value = {}
    elif damage == "array":
        value = []
    elif damage == "missing-context":
        del value["contextFileName"]
    elif damage == "unsafe-context":
        value["contextFileName"] = "../../../../private-context.md"
    else:
        value["contextFileName"] = "absent-context.md"
    descriptor.write_text(json.dumps(value))
    private = root / "private-context.md"
    private.write_text("Keep this unowned source context.\n")
    canonical = snapshot(root / "skills")

    result = refresh(root)

    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(descriptor.read_text()) == expected_descriptor
    assert validate_generated_dirs.validate_generated(root) == []
    assert snapshot(root / "skills") == canonical
    assert private.read_text() == "Keep this unowned source context.\n"


@pytest.mark.parametrize("unowned", ["file", "directory", "other-extension"])
def test_refresh_preserves_unknown_extension_siblings(generated_catalog, unowned):
    root = generated_catalog
    extension = root / "distributions/extensions/gemini/example-skills"
    extra = extension / "personal-note.md"
    if unowned == "directory":
        extra = extension / "personal-notes/note.md"
        extra.parent.mkdir()
    elif unowned == "other-extension":
        extra = extension.parent / "zz-personal/note.md"
        extra.parent.mkdir()
    extra.write_text("This unowned material must not be deleted.\n")
    rename_config(root)
    before = snapshot(root / "distributions")

    result = refresh(root)

    assert result.returncode != 0
    assert "unowned" in result.stderr.lower()
    assert snapshot(root / "distributions") == before


@pytest.mark.parametrize("damage", [
    "missing-marker", "invalid-marker", "edited-context", "unsafe-context-path",
])
def test_refresh_requires_ownership_of_obsolete_output(generated_catalog, damage):
    root = generated_catalog
    extension = root / "distributions/extensions/gemini/example-skills"
    marker = extension / "skills/.skills-generated"
    if damage == "missing-marker":
        marker.unlink()
    elif damage == "invalid-marker":
        marker.write_text("This is not the generator's ownership marker.\n")
    elif damage == "edited-context":
        (extension / "GEMINI.md").write_text("Personal context edits must survive.\n")
    else:
        descriptor = extension / "gemini-extension.json"
        value = json.loads(descriptor.read_text())
        value["contextFileName"] = "../../../../skills/testing/rename-example/SKILL.md"
        descriptor.write_text(json.dumps(value))
    rename_config(root)
    before = snapshot(root / "distributions")
    source_before = snapshot(root / "skills")

    result = refresh(root)

    assert result.returncode != 0
    assert snapshot(root / "distributions") == before
    assert snapshot(root / "skills") == source_before


@pytest.mark.parametrize("alias", [
    "extension", "skills", "marker", "descriptor", "context",
])
def test_refresh_cleanup_rejects_symlinks_without_touching_source(
    generated_catalog, tmp_path, alias
):
    root = generated_catalog
    extension = root / "distributions/extensions/gemini/example-skills"
    selected = {
        "extension": extension,
        "skills": extension / "skills",
        "marker": extension / "skills/.skills-generated",
        "descriptor": extension / "gemini-extension.json",
        "context": extension / "GEMINI.md",
    }[alias]
    outside = tmp_path / "unowned-source"
    if selected.is_dir():
        shutil.copytree(selected, outside)
        shutil.rmtree(selected)
    else:
        outside.mkdir()
        outside = outside / selected.name
        shutil.copy2(selected, outside)
        selected.unlink()
    selected.symlink_to(outside, target_is_directory=outside.is_dir())
    rename_config(root)
    before = snapshot(root / "distributions")
    source_before = snapshot(outside if outside.is_dir() else outside.parent)

    result = refresh(root)

    assert result.returncode != 0
    assert "symlink" in result.stderr.lower()
    assert snapshot(root / "distributions") == before
    assert snapshot(outside if outside.is_dir() else outside.parent) == source_before
