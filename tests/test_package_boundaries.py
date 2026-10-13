"""Keep optional source files and overlapping package outputs inside their boundaries."""

from concurrent.futures import ThreadPoolExecutor
import fcntl
import hashlib
import json
from pathlib import Path
import shutil
import threading

import pytest

import skills_install as installer

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def package_source(tmp_path):
    """A small canonical catalog, built by the real generators and validators."""
    source = tmp_path / "source"
    skill = source / "skills/testing/package-probe"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text(
        "---\nname: package-probe\n"
        "description: A temporary catalog for testing package publication boundaries.\n"
        "license: MIT\n---\n\nAn isolated package fixture.\n"
    )
    (source / "plugins").mkdir()
    shutil.copytree(
        ROOT / "scripts", source / "scripts",
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
    )
    for relative in ("LICENSE", "docs/THIRD_PARTY_NOTICES.md", ".claude-plugin/plugin.json"):
        destination = source / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / relative, destination)
    config = json.loads((ROOT / "config/runtime-catalog.json").read_text())
    config["purpose_collections"] = {}
    (source / "config").mkdir()
    (source / "config/runtime-catalog.json").write_text(json.dumps(config))
    return source


@pytest.mark.parametrize("alias", ["guide", "dangling-guide", "docs", "docs-without-guide"])
def test_build_rejects_guide_aliases_before_copying_source(
    package_source, tmp_path, monkeypatch, alias
):
    external = tmp_path / "external"
    external.mkdir()
    guide = package_source / "docs/installation.md"
    if alias.startswith("docs"):
        (package_source / "docs").rename(external / "docs")
        (package_source / "docs").symlink_to(external / "docs", target_is_directory=True)
        if alias == "docs":
            guide.write_text("External guide must never enter the package.\n")
    else:
        target = external / "guide.md"
        if alias == "guide":
            target.write_text("External guide must never enter the package.\n")
        guide.symlink_to(target)

    copied = []
    original_copy = installer._copy_directory

    def observed_copy(origin, destination):
        copied.append(origin)
        return original_copy(origin, destination)

    monkeypatch.setattr(installer, "_copy_directory", observed_copy)
    output = tmp_path / "release"
    with pytest.raises(installer.InstallError, match="link"):
        installer.build_release(package_source, output)
    assert copied == []
    assert not output.exists()


@pytest.mark.parametrize("include_guide", [False, True])
def test_build_accepts_missing_or_regular_optional_guide(
    package_source, tmp_path, include_guide
):
    content = "Install the verified release using its bundled installer.\n"
    if include_guide:
        (package_source / "docs/installation.md").write_text(content)
    release = tmp_path / "release"
    manifest = installer.build_release(package_source, release)
    assert (release / "INSTALL.md").is_file() is include_guide
    assert ("INSTALL.md" in manifest["files"]) is include_guide
    if include_guide:
        assert (release / "INSTALL.md").read_text() == content


@pytest.mark.parametrize("checksum_name_first", [False, True])
def test_overlapping_archive_checksum_publications_preserve_one_complete_pair(
    package_source, tmp_path, monkeypatch, checksum_name_first
):
    release = tmp_path / "release"
    installer.build_release(package_source, release)
    output = tmp_path / "published/catalog.tar.gz"
    outputs = [output, output.with_name(output.name + ".sha256")]
    if checksum_name_first:
        outputs.reverse()

    first_validating = threading.Event()
    allow_first = threading.Event()
    second_lock_attempted = threading.Event()
    role = threading.local()
    probe = {}
    original_validate = installer.validate_release
    original_flock = fcntl.flock

    def paused_validate(path, **kwargs):
        if getattr(role, "name", None) == "first":
            first_validating.set()
            assert allow_first.wait(15), "First pack was never released by the test"
        return original_validate(path, **kwargs)

    def observed_flock(fd, operation):
        if getattr(role, "name", None) != "second":
            return original_flock(fd, operation)
        # A real nonblocking probe establishes whether the first publisher owns
        # a conflicting lock. No elapsed-time assumption decides the outcome.
        try:
            original_flock(fd, operation | fcntl.LOCK_NB)
        except BlockingIOError:
            probe["blocked"] = True
            second_lock_attempted.set()
            return original_flock(fd, operation)
        else:
            probe["blocked"] = False
            second_lock_attempted.set()

    def pack_as(name, destination):
        role.name = name
        return installer.pack_release(release, destination)

    monkeypatch.setattr(installer, "validate_release", paused_validate)
    monkeypatch.setattr(fcntl, "flock", observed_flock)
    with ThreadPoolExecutor(max_workers=2) as pool:
        first = pool.submit(pack_as, "first", outputs[0])
        try:
            assert first_validating.wait(15), "First pack never reached validation"
            second = pool.submit(pack_as, "second", outputs[1])
            assert second_lock_attempted.wait(15), "Second pack never attempted its lock"
            if not probe["blocked"]:
                # With disjoint locks the second pack finishes after both have
                # admitted absent outputs, reproducing the replacement race.
                second.result(timeout=15)
        finally:
            allow_first.set()
        successes = []
        failures = []
        for destination, future in zip(outputs, (first, second)):
            try:
                successes.append((destination, future.result(timeout=15)))
            except installer.InstallError as exc:
                failures.append(str(exc))

    assert len(successes) == 1
    assert len(failures) == 1 and "already exists" in failures[0]
    destination, result = successes[0]
    digest = result["sha256"]
    assert hashlib.sha256(destination.read_bytes()).hexdigest() == digest
    assert destination.with_name(destination.name + ".sha256").read_text() == (
        f"{digest}  {destination.name}\n"
    )
