"""Regression coverage for installer review findings and interrupted activation."""
from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import types

import pytest

import skills_install as installer
from generate_lockfile import build_lockfile
from generate_registry import build_registry
from test_skill_tooling import canonical_source as canonical_source, _refresh
from validate_generated_dirs import validate_generated


@pytest.fixture
def small_source(canonical_source):
    (canonical_source / "LICENSE").write_text("MIT\n")
    (canonical_source / "docs").mkdir()
    (canonical_source / "docs/THIRD_PARTY_NOTICES.md").write_text("Test fixtures.\n")
    return canonical_source


@pytest.mark.parametrize("operation", ["install", "rollback"])
@pytest.mark.parametrize("pointer", ["current", "previous"])
@pytest.mark.parametrize("error_type", [OSError, KeyboardInterrupt])
def test_post_replace_failure_restores_both_pointers(
    small_source, tmp_path, monkeypatch, operation, pointer, error_type
):
    prefix = tmp_path / "installation"
    installer.install_release(prefix, source=small_source)
    entry = small_source / "skills/data/good-skill/SKILL.md"
    entry.write_text(entry.read_text() + "\nRevision two.\n")
    installer.install_release(prefix, source=small_source)
    before = {name: (prefix / name).readlink() for name in ("current", "previous")}
    current = installer.active_release(prefix)
    entry.write_text(entry.read_text() + "\nRevision three.\n")
    replace = installer._replace_pointer
    injected = False

    def fail_after_replace(prefix, name, target):
        nonlocal injected
        replace(prefix, name, target)
        if name == pointer and not injected:
            injected = True
            raise error_type("post-replace interruption")

    monkeypatch.setattr(installer, "_replace_pointer", fail_after_replace)
    with pytest.raises(error_type, match="post-replace"):
        if operation == "install":
            installer.install_release(prefix, source=small_source)
        else:
            installer.rollback(prefix, current)
    assert injected
    assert {name: (prefix / name).readlink() for name in before} == before
    assert installer.active_release(prefix) == current


def test_path_stdout_is_only_verified_absolute_path(small_source, tmp_path):
    prefix = tmp_path / "installation"
    installer.install_release(prefix, source=small_source)
    expected = installer.active_release(prefix)
    result = subprocess.run(
        [sys.executable, str(expected / "scripts/skills_install.py"), "path",
         "--prefix", str(prefix)],
        cwd=tmp_path, capture_output=True, text=True, check=True,
    )
    assert result.stdout == str(expected) + "\n"
    assert "Generated runtime output" in result.stderr


def test_mcp_cache_hits_validate_integrity_without_semantic_subprocesses(
    small_source, tmp_path, monkeypatch
):
    prefix = tmp_path / "installation"
    installer.install_release(prefix, source=small_source)
    class ProtocolStub:
        def __init__(self, *args, **kwargs):
            pass
        def tool(self, *args, **kwargs):
            return lambda function: function
    protocol = types.ModuleType("mcp.server.fastmcp")
    protocol.FastMCP = ProtocolStub
    monkeypatch.setitem(sys.modules, "mcp.server.fastmcp", protocol)
    monkeypatch.setenv("DOMUS_SKILLS_HOME", str(prefix))
    spec = importlib.util.spec_from_file_location(
        "review_mcp_loader", Path(__file__).parents[1] / "scripts/mcp-skill-server.py"
    )
    consumer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(consumer)
    calls = []
    run = installer._run
    def record(*args):
        calls.append(args[1])
        return run(*args)
    monkeypatch.setattr(installer, "_run", record)
    first = consumer._load_skills()
    assert len(calls) == 2
    assert consumer._load_skills() is first
    assert len(calls) == 2
    entry = small_source / "skills/data/good-skill/SKILL.md"
    entry.write_text(entry.read_text() + "\nNew release.\n")
    installer.install_release(prefix, source=small_source)
    calls.clear()
    second = consumer._load_skills()
    assert second is not first
    assert len(calls) == 2
    assert consumer._load_skills() is second
    assert len(calls) == 2
    payload = Path(second[0]["path"]) / "SKILL.md"
    payload.chmod(0o644)
    payload.write_text(payload.read_text() + "\nTampering.\n")
    with pytest.raises(installer.InstallError, match="payload differs"):
        consumer._load_skills()
    assert len(calls) == 2


@pytest.mark.parametrize("existing", [False, True])
def test_skip_marketplace_preserves_absent_or_stale_file(canonical_source, existing):
    marketplace = canonical_source / ".claude-plugin/marketplace.json"
    if existing:
        marketplace.write_text('{"intentionally": "stale"}\n')
    before = marketplace.read_bytes() if existing else None
    result = subprocess.run(
        [sys.executable, str(canonical_source / "scripts/refresh_skill_collections.py"),
         "--skip-marketplace", "--skip-readme", "--skip-ecosystem"],
        capture_output=True, text=True,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert (marketplace.read_bytes() if marketplace.exists() else None) == before
    assert validate_generated(canonical_source, skip_marketplace=True) == []
    assert any("marketplace.json" in error for error in validate_generated(canonical_source))


def test_caches_are_excluded_from_locks_copies_and_generated_audit(canonical_source):
    source = canonical_source / "skills/data/good-skill"
    for relative in (".DS_Store", "cached.pyc", "__pycache__/cached.pyc", ".pytest_cache/state", "scripts/cached.pyc", "scripts/__pycache__/cached.pyc"):
        path = source / relative
        path.parent.mkdir(exist_ok=True)
        path.write_text("host-local cache")
    result = _refresh(canonical_source)
    assert result.returncode == 0, result.stdout + result.stderr
    lock = build_lockfile(canonical_source)
    records = next(s for s in lock["skills"] if s["name"] == "good-skill")["files"]
    assert {r["path"] for r in records} == {"SKILL.md", "scripts/run.sh"}
    registry = build_registry(canonical_source)
    entry = next(s for s in registry["skills"] if s["name"] == "good-skill")
    assert entry["resources"]["scripts"] == ["run.sh"]
    target = canonical_source / "distributions/codex/skills/good-skill"
    assert not (target / ".DS_Store").exists()
    assert not (target / "__pycache__").exists()
    (target / ".DS_Store").write_text("Finder cache")
    (target / "__pycache__").mkdir()
    (target / "__pycache__/cached.pyc").write_text("bytecode")
    assert validate_generated(canonical_source) == []

def test_installer_imports_from_unrelated_working_directory(tmp_path):
    module = Path(__file__).parents[1] / "scripts/skills_install.py"
    subprocess.run(
        [sys.executable, "-I", "-B", "-c",
         "import importlib.util,sys; "
         "s=importlib.util.spec_from_file_location('isolated_installer',sys.argv[1]); "
         "m=importlib.util.module_from_spec(s); s.loader.exec_module(m); "
         "assert m._ignored('cached.pyc')",
         str(module)],
        cwd=tmp_path, check=True,
    )
