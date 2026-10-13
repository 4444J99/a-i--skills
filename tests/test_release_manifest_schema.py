"""Malformed release summaries must fail before an installation is activated."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil

import pytest

import skills_install as installer


ROOT = Path(__file__).resolve().parents[1]
MISSING = object()


@pytest.fixture(scope="module")
def verified_release(tmp_path_factory):
    release = tmp_path_factory.mktemp("manifest-schema") / "release"
    installer.build_release(ROOT, release)
    return release


def _write_manifest(release, manifest):
    manifest.pop("build_id", None)
    manifest["build_id"] = hashlib.sha256(
        installer._json_bytes(manifest)
    ).hexdigest()
    (release / installer.MANIFEST).write_text(json.dumps(manifest) + "\n")


def test_missing_counts_cannot_activate_a_release(verified_release, tmp_path):
    prefix = tmp_path / "installation"
    installer.install_release(prefix, release=verified_release)
    original_current = installer.active_release(prefix)
    original_previous = (prefix / "previous").readlink() if (
        prefix / "previous"
    ).is_symlink() else None

    candidate = tmp_path / "candidate"
    shutil.copytree(verified_release, candidate)
    manifest = json.loads((candidate / installer.MANIFEST).read_text())
    del manifest["counts"]
    _write_manifest(candidate, manifest)

    failure = None
    try:
        installer.install_release(prefix, release=candidate)
    except Exception as exc:
        failure = exc

    assert installer.active_release(prefix) == original_current, (
        f"Malformed manifest activated before failure: {failure!r}"
    )
    actual_previous = (prefix / "previous").readlink() if (
        prefix / "previous"
    ).is_symlink() else None
    assert actual_previous == original_previous
    assert isinstance(failure, installer.InstallError)
    assert "counts" in str(failure)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("counts", MISSING),
        ("counts", None),
        ("counts", []),
        ("counts.catalog", MISSING),
        ("counts.plugins", MISSING),
        ("counts.catalog", True),
        ("counts.plugins", False),
        ("counts.catalog", -1),
        ("counts.plugins", -1),
        ("counts.catalog", "167"),
        ("counts.plugins", 11.0),
        ("version", MISSING),
        ("version", None),
        ("version", " "),
        ("source", MISSING),
        ("source", []),
        ("source.repository", MISSING),
        ("source.repository", False),
        ("source.commit", MISSING),
        ("source.commit", []),
        ("source.input_sha256", MISSING),
        ("source.input_sha256", False),
        ("files", MISSING),
        ("files", []),
    ],
)
def test_schema_errors_are_reported_even_without_semantic_validation(
    verified_release, field, value
):
    manifest_path = verified_release / installer.MANIFEST
    original = manifest_path.read_bytes()
    manifest = json.loads(original)
    parent = manifest
    parts = field.split(".")
    for part in parts[:-1]:
        parent = parent[part]
    if value is MISSING:
        del parent[parts[-1]]
    else:
        parent[parts[-1]] = value
    try:
        _write_manifest(verified_release, manifest)
        with pytest.raises(installer.InstallError) as failure:
            installer.validate_release(verified_release, semantic=False)
        assert field in str(failure.value)
    finally:
        manifest_path.write_bytes(original)


@pytest.mark.parametrize("manifest", [None, [], "not an object", 1])
def test_manifest_must_be_an_object(tmp_path, manifest):
    (tmp_path / installer.MANIFEST).write_text(json.dumps(manifest))
    with pytest.raises(installer.InstallError, match="JSON object"):
        installer.validate_release(tmp_path, semantic=False)


@pytest.mark.parametrize("schema_version", [True, 1.0, "1", None])
def test_schema_version_requires_the_supported_integer(
    verified_release, schema_version
):
    manifest_path = verified_release / installer.MANIFEST
    original = manifest_path.read_bytes()
    manifest = json.loads(original)
    manifest["schema_version"] = schema_version
    try:
        _write_manifest(verified_release, manifest)
        with pytest.raises(installer.InstallError, match="Unsupported"):
            installer.validate_release(verified_release, semantic=False)
    finally:
        manifest_path.write_bytes(original)


@pytest.mark.parametrize("value", [True, False, -1, 1.0])
def test_file_sizes_require_nonnegative_integers(verified_release, value):
    manifest_path = verified_release / installer.MANIFEST
    original = manifest_path.read_bytes()
    manifest = json.loads(original)
    relative = next(iter(manifest["files"]))
    manifest["files"][relative]["size"] = value
    try:
        _write_manifest(verified_release, manifest)
        with pytest.raises(installer.InstallError) as failure:
            installer.validate_release(verified_release, semantic=False)
        assert "size" in str(failure.value)
    finally:
        manifest_path.write_bytes(original)


def test_schema_preserves_source_free_and_unrestricted_version_metadata(
    verified_release,
):
    manifest_path = verified_release / installer.MANIFEST
    original = manifest_path.read_bytes()
    manifest = json.loads(original)
    manifest["source"]["commit"] = None
    manifest["version"] = "release-2026.10"
    try:
        _write_manifest(verified_release, manifest)
        validated = installer.validate_release(verified_release, semantic=False)
        assert validated["source"]["commit"] is None
        assert validated["version"] == "release-2026.10"
        assert validated["counts"] == json.loads(original)["counts"]
    finally:
        manifest_path.write_bytes(original)
