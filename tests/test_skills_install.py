"""Exercise installation outcomes against real canonical sources in isolation."""

from __future__ import annotations

import hashlib
from concurrent.futures import ThreadPoolExecutor
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import types

import pytest

import skills_install as installer

ROOT = Path(__file__).resolve().parents[1]
BUNDLES = (
    "distributions/claude/skills",
    "distributions/codex/skills",
    "distributions/direct/example",
    "distributions/extensions/gemini/example-skills/skills",
)


@pytest.fixture
def source(tmp_path):
    source = tmp_path / "fresh-checkout"
    source.mkdir()
    # Only canonical inputs. Neither distributions nor a generated marketplace
    # exists, even when this suite is run before tracked-output retirement.
    for name in ("skills", "plugins", "scripts", "config", "agents", "commands"):
        shutil.copytree(
            ROOT / name,
            source / name,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )
    for relative in (
        "LICENSE",
        "docs/THIRD_PARTY_NOTICES.md",
        ".claude-plugin/plugin.json",
    ):
        target = source / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / relative, target)
    assert not (source / "distributions").exists()
    assert not (source / ".claude-plugin/marketplace.json").exists()
    return source


def _registry(release):
    return json.loads((release / "distributions/skills-registry.json").read_text())[
        "skills"
    ]


def _new_skill(source):
    skill = source / "skills/education/installation-acceptance-example"
    skill.mkdir()
    (skill / "SKILL.md").write_text(
        "---\nname: installation-acceptance-example\n"
        "description: A temporary skill for verifying update and removal behavior.\n"
        "license: MIT\n---\n\nAn isolated test fixture.\n"
    )
    return skill


def test_acceptance_clean_install_update_removal_and_failed_update(
    source, tmp_path, monkeypatch
):
    prefix = tmp_path / "installation"
    original_names = {p.parent.name for p in (source / "skills").rglob("SKILL.md")}
    plugin_names = {p.parent.name for p in (source / "plugins").rglob("SKILL.md")}

    first = installer.install_release(prefix, source=source)
    first_path = installer.active_release(prefix)
    assert first["counts"] == {
        "catalog": len(original_names),
        "plugins": len(plugin_names),
    }
    assert first["counts"]["catalog"] > 100  # Full real catalog, not a toy fixture.
    assert {s["name"] for s in _registry(first_path)} == original_names | plugin_names
    for bundle in BUNDLES:
        assert {
            p.name for p in (first_path / bundle).iterdir() if p.is_dir()
        } == original_names
    assert not (source / "distributions").exists()  # Build did not mutate checkout.
    assert not (source / ".claude-plugin/marketplace.json").exists()

    # Test the registry consumer without a protocol server or model/network call.
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
        "test_mcp_loader", ROOT / "scripts/mcp-skill-server.py"
    )
    consumer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(consumer)
    loaded = consumer._load_skills()
    assert {s["name"] for s in loaded} == original_names | plugin_names
    assert all(Path(s["path"]).is_relative_to(first_path) for s in loaded)

    changed = source / "skills/education/recommendation-letter/SKILL.md"
    changed.write_text(
        changed.read_text() + "\nAcceptance revision from canonical source.\n"
    )
    added = _new_skill(source)
    second = installer.install_release(prefix, source=source)
    second_path = installer.active_release(prefix)
    assert second["build_id"] != first["build_id"]
    assert (prefix / "previous").resolve() == first_path
    loaded = consumer._load_skills()
    assert added.name in {s["name"] for s in loaded}
    assert all(Path(s["path"]).is_relative_to(second_path) for s in loaded)
    for bundle in BUNDLES:
        assert (second_path / bundle / added.name / "SKILL.md").is_file()
        assert (
            "Acceptance revision"
            in (second_path / bundle / "recommendation-letter/SKILL.md").read_text()
        )
        assert (
            "Acceptance revision"
            not in (first_path / bundle / "recommendation-letter/SKILL.md").read_text()
        )

    shutil.rmtree(added)
    third = installer.install_release(prefix, source=source)
    third_path = installer.active_release(prefix)
    assert third["build_id"] != second["build_id"]
    for bundle in BUNDLES:
        assert not (third_path / bundle / added.name).exists()
    assert added.name not in {s["name"] for s in _registry(third_path)}
    assert added.name not in (third_path / "distributions/skills-lock.json").read_text()
    assert not (third_path / added.relative_to(source)).exists()
    assert added.name not in {s["name"] for s in consumer._load_skills()}

    old_manifest = (third_path / installer.MANIFEST).read_bytes()
    old_previous = (prefix / "previous").resolve()
    (source / "scripts/generate_registry.py").write_text("raise SystemExit(73)\n")
    with pytest.raises(subprocess.CalledProcessError):
        installer.install_release(prefix, source=source)
    assert installer.active_release(prefix) == third_path
    assert (prefix / "previous").resolve() == old_previous
    assert (third_path / installer.MANIFEST).read_bytes() == old_manifest
    # Retained installation executes its own validation with source unavailable.
    shutil.rmtree(source)
    subprocess.run(
        [
            sys.executable,
            str(third_path / "scripts/skills_install.py"),
            "validate",
            "--release",
            str(third_path),
        ],
        check=True,
    )
    assert installer.validate_release(old_previous)["build_id"] == second["build_id"]


def test_failed_fresh_build_never_publishes_partial_output(source, tmp_path):
    (source / "scripts/generate_lockfile.py").unlink()
    output = tmp_path / "release"
    with pytest.raises(subprocess.CalledProcessError):
        installer.build_release(source, output)
    assert not output.exists()
    prefix = tmp_path / "install"
    with pytest.raises(subprocess.CalledProcessError):
        installer.install_release(prefix, source=source)
    assert not (prefix / "current").exists()
    assert not list(prefix.glob(".install-stage-*"))


def test_installer_preserves_unmanaged_current_directory(source, tmp_path):
    prefix = tmp_path / "install"
    current = prefix / "current"
    current.mkdir(parents=True)
    (current / "personal.txt").write_text("Preserve this file")
    with pytest.raises(installer.InstallError, match="unmanaged"):
        installer.install_release(prefix, source=source)
    assert (current / "personal.txt").read_text() == "Preserve this file"


@pytest.mark.parametrize(
    "damage", ["bundle", "lock", "descriptor", "executable", "unmanifested-cache"]
)
def test_complete_validation_rejects_damaged_releases(source, tmp_path, damage):
    release = tmp_path / "release"
    installer.build_release(source, release)
    if damage == "bundle":
        target = release / BUNDLES[0] / "recommendation-letter/SKILL.md"
        target.write_text(target.read_text() + "\nUnexpected change\n")
    elif damage == "lock":
        (release / "distributions/skills-lock.json").unlink()
    elif damage == "descriptor":
        (
            release
            / "distributions/extensions/gemini/example-skills/gemini-extension.json"
        ).unlink()
    elif damage == "executable":
        target = release / "scripts/skills_install.py"
        target.chmod(target.stat().st_mode ^ 0o111)
    else:
        target = release / "scripts/__pycache__/unexpected.txt"
        target.parent.mkdir()
        target.write_text("Every payload file must be accounted for")
    with pytest.raises(installer.InstallError, match="payload"):
        installer.validate_release(release)


def test_generated_validator_catches_corruption_even_with_refreshed_manifest(
    source, tmp_path
):
    release = tmp_path / "release"
    installer.build_release(source, release)
    target = release / BUNDLES[1] / "recommendation-letter/SKILL.md"
    target.write_text(target.read_text() + "\nGenerated copy drift\n")
    manifest = json.loads((release / installer.MANIFEST).read_text())
    manifest["files"] = installer._inventory(release)
    del manifest["build_id"]
    manifest["build_id"] = hashlib.sha256(installer._json_bytes(manifest)).hexdigest()
    (release / installer.MANIFEST).write_text(json.dumps(manifest))
    with pytest.raises(subprocess.CalledProcessError):
        installer.validate_release(release)


def test_rollback_is_guarded_and_idempotent_install_preserves_history(source, tmp_path):
    prefix = tmp_path / "installation"
    first = installer.install_release(prefix, source=source)
    first_path = installer.active_release(prefix)
    _new_skill(source)
    installer.install_release(prefix, source=source)
    second_path = installer.active_release(prefix)
    assert second_path != first_path
    installer.install_release(prefix, source=source)
    assert (prefix / "previous").resolve() == first_path
    with pytest.raises(installer.InstallError, match="Current moved"):
        installer.rollback(prefix, first_path)
    assert installer.active_release(prefix) == second_path
    installer.rollback(prefix, second_path)
    assert (
        installer.validate_release(installer.active_release(prefix))["build_id"]
        == first["build_id"]
    )


def test_activation_error_preserves_current_and_previous(source, tmp_path, monkeypatch):
    prefix = tmp_path / "installation"
    installer.install_release(prefix, source=source)
    first = installer.active_release(prefix)
    _new_skill(source)
    original = installer._replace_pointer

    def fail_current(prefix, name, target):
        if name == "current":
            raise OSError("simulated activation failure")
        return original(prefix, name, target)

    monkeypatch.setattr(installer, "_replace_pointer", fail_current)
    with pytest.raises(OSError, match="simulated"):
        installer.install_release(prefix, source=source)
    assert installer.active_release(prefix) == first
    assert not (prefix / "previous").exists()
    installer.validate_release(first)


def test_release_tarball_is_reproducible_and_installs_without_source(source, tmp_path):
    release = tmp_path / "release"
    manifest = installer.build_release(source, release)
    digest = installer.pack_release(release, tmp_path / "first.tar.gz")
    assert installer.pack_release(release, tmp_path / "second.tar.gz") == digest
    assert (tmp_path / "first.tar.gz.sha256").read_text().split()[0] == digest
    with tarfile.open(tmp_path / "first.tar.gz") as archive:
        archive.extractall(tmp_path / "extracted", filter="data")
    packaged = tmp_path / "extracted/ai-skills"
    assert installer.validate_release(packaged) == manifest
    shutil.rmtree(source)
    shutil.rmtree(release)
    prefix = tmp_path / "installation"
    subprocess.run(
        [
            sys.executable,
            str(packaged / "scripts/skills_install.py"),
            "install",
            "--release",
            str(packaged),
            "--prefix",
            str(prefix),
        ],
        check=True,
    )
    assert installer.validate_release(installer.active_release(prefix)) == manifest
    installer.rollback(prefix, installer.active_release(prefix))
    assert not (prefix / "current").exists()


def test_build_refuses_lowercase_entrypoints_and_source_symlinks(source, tmp_path):
    entry = source / "skills/education/recommendation-letter/SKILL.md"
    entry.rename(entry.with_name("skill.md"))
    with pytest.raises(installer.InstallError, match="Normalize"):
        installer.build_release(source, tmp_path / "lowercase")
    entry.with_name("skill.md").rename(entry)
    entry.with_name("external-file").symlink_to(tmp_path / "outside")
    with pytest.raises(installer.InstallError, match="Unsupported link"):
        installer.build_release(source, tmp_path / "symlink")


def test_pack_refuses_output_inside_its_input_release(source, tmp_path):
    release = tmp_path / "release"
    manifest = installer.build_release(source, release)
    with pytest.raises(installer.InstallError, match="outside the release"):
        installer.pack_release(release, release / "nested/output.tar.gz")
    assert not (release / "nested").exists()
    assert installer.validate_release(release) == manifest


def test_pack_serializes_competing_archive_and_checksum_publications(source, tmp_path):
    first = tmp_path / "first-release"
    installer.build_release(source, first)
    _new_skill(source)
    second = tmp_path / "second-release"
    installer.build_release(source, second)
    output = tmp_path / "shared.tar.gz"
    with ThreadPoolExecutor(max_workers=2) as pool:
        attempts = [
            pool.submit(installer.pack_release, release, output)
            for release in (first, second)
        ]
        successes = []
        for attempt in attempts:
            try:
                successes.append(attempt.result())
            except installer.InstallError as exc:
                assert "already exists" in str(exc)
    assert len(successes) == 1
    assert hashlib.sha256(output.read_bytes()).hexdigest() == successes[0]
    assert (
        output.with_name(output.name + ".sha256").read_text().split()[0] == successes[0]
    )


def test_release_version_comes_from_canonical_descriptor(source, monkeypatch):
    import release as release_helper

    descriptor = source / ".claude-plugin/plugin.json"
    monkeypatch.setattr(release_helper, "VERSION_FILE", descriptor)
    release_helper._update_versions("3.2.1")
    assert json.loads(descriptor.read_text())["version"] == "3.2.1"
    assert not (source / "distributions").exists()
    assert not (source / ".claude-plugin/marketplace.json").exists()
