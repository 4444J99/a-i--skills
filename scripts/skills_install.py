#!/usr/bin/env python3
"""Build, verify, package and atomically activate standalone skills releases.

Python 3.11+ standard library only; supported hosts are macOS and Linux.
No generated file in the source checkout is an input to the build.
"""

from __future__ import annotations

import argparse
from contextlib import contextmanager
import fcntl
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile
import uuid

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
MANIFEST = "build-manifest.json"
KIND = "a-i-skills-release"
IGNORED = {".git", "__pycache__", ".DS_Store", ".pytest_cache"}


class InstallError(RuntimeError):
    """A failed build or unsafe installation state; current is preserved."""


def _json_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _ignored(name: str) -> bool:
    return name in IGNORED or name.endswith((".pyc", ".pyo"))


def _files(root: Path, *, ignore_caches: bool = False):
    """Walk regular files, refusing links and special files before copying."""
    for path in sorted(root.rglob("*")):
        if ignore_caches and any(_ignored(p) for p in path.relative_to(root).parts):
            continue
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode) or not (stat.S_ISREG(mode) or stat.S_ISDIR(mode)):
            raise InstallError(f"Unsupported link or special file: {path}")
        if stat.S_ISREG(mode):
            yield path


def _inventory(root: Path, *, exclude_manifest: bool = True) -> dict:
    result = {}
    for path in _files(root):
        relative = path.relative_to(root).as_posix()
        if exclude_manifest and relative == MANIFEST:
            continue
        content = path.read_bytes()
        result[relative] = {
            "sha256": hashlib.sha256(content).hexdigest(),
            "size": len(content),
            "mode": "100755" if path.stat().st_mode & 0o111 else "100644",
        }
    return result


def _copy_directory(source: Path, target: Path) -> None:
    if not source.is_dir() or source.is_symlink():
        raise InstallError(f"Missing canonical directory or unexpected link: {source}")
    list(_files(source, ignore_caches=True))
    shutil.copytree(
        source, target, ignore=lambda _, names: [n for n in names if _ignored(n)]
    )


def _copy_source(source: Path, stage: Path) -> dict:
    """Copy admitted skill folders, complete plugins, and build/runtime sources."""
    skills = source / "skills"
    if not skills.is_dir():
        raise InstallError(f"Missing canonical skills directory: {skills}")
    # Discovery must not silently omit a lowercase or mixed-case entrypoint.
    for path in _files(skills):
        if path.name.lower() == "skill.md" and path.name != "SKILL.md":
            raise InstallError(
                f"Normalize the canonical entrypoint before building: {path}"
            )
    entries = sorted(skills.rglob("SKILL.md"))
    if not entries:
        raise InstallError("The canonical catalog is empty")
    for entry in entries:
        relative = entry.parent.relative_to(source)
        if len(relative.parts) != 3:
            raise InstallError(
                f"Catalog skill must have skills/category/name layout: {relative}"
            )
        _copy_directory(entry.parent, stage / relative)
    for name in ("plugins", "scripts", "config"):
        _copy_directory(source / name, stage / name)
    for name in ("agents", "commands"):
        if (source / name).exists():
            _copy_directory(source / name, stage / name)
    for relative in (
        ".claude-plugin/plugin.json",
        "LICENSE",
        "docs/THIRD_PARTY_NOTICES.md",
    ):
        origin = source / relative
        if not origin.is_file() or origin.is_symlink():
            raise InstallError(f"Missing canonical file or unexpected link: {origin}")
        destination = stage / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(origin, destination)
    if (source / "docs/installation.md").is_file():
        shutil.copy2(source / "docs/installation.md", stage / "INSTALL.md")
    return _inventory(stage)


def _run(stage: Path, script: str, *arguments: str) -> None:
    target = stage / "scripts" / script
    if not target.is_file():
        raise InstallError(f"Required generator or validator is missing: {target}")
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    subprocess.run(
        [sys.executable, str(target), *arguments], cwd=stage, env=env, check=True
    )


def _source_commit(source: Path) -> str | None:
    try:
        top = subprocess.check_output(
            ["git", "-C", str(source), "rev-parse", "--show-toplevel"],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        if Path(top).resolve() != source.resolve():
            return None
        return subprocess.check_output(
            ["git", "-C", str(source), "rev-parse", "HEAD"],
            text=True,
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


@contextmanager
def _lock(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    flags = os.O_RDWR | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(path, flags, 0o600)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        yield
    finally:
        os.close(fd)


def validate_release(release: Path, *, semantic: bool = True) -> dict:
    release = release.resolve(strict=True)
    manifest_path = release / MANIFEST
    if manifest_path.is_symlink():
        raise InstallError("Release manifest must be a regular file")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("schema_version") != 1 or manifest.get("kind") != KIND:
        raise InstallError("Unsupported or missing release manifest")
    identity = dict(manifest)
    build_id = identity.pop("build_id", None)
    if build_id != hashlib.sha256(_json_bytes(identity)).hexdigest():
        raise InstallError("Release manifest identity mismatch")
    if _inventory(release) != manifest.get("files"):
        raise InstallError("Release payload differs from its complete file manifest")
    if semantic:
        _run(
            release,
            "validate_skills.py",
            "--collection",
            "all",
            "--unique",
            "--check-links",
        )
        _run(release, "validate_generated_dirs.py")
    return manifest


def build_release(source: Path, output: Path) -> dict:
    source = source.resolve(strict=True)
    output = output.absolute()
    for canonical in (
        "skills", "plugins", "scripts", "config", ".claude-plugin", "agents", "commands"
    ):
        if output.resolve().is_relative_to(source / canonical):
            raise InstallError(
                "Build output must be outside canonical source directories"
            )
    output.parent.mkdir(parents=True, exist_ok=True)
    with _lock(output.parent / f".{output.name}.build.lock"):
        if output.exists() or output.is_symlink():
            raise InstallError(
                f"Build output already exists; choose a fresh directory: {output}"
            )
        with tempfile.TemporaryDirectory(
            prefix=".skills-stage-", dir=output.parent
        ) as temporary:
            stage = Path(temporary) / "release"
            stage.mkdir()
            inputs = _copy_source(source, stage)
            _run(
                stage,
                "validate_skills.py",
                "--collection",
                "all",
                "--unique",
                "--check-links",
            )
            _run(
                stage,
                "refresh_skill_collections.py",
                "--skip-readme",
                "--skip-ecosystem",
            )
            _run(stage, "validate_generated_dirs.py")
            registry = json.loads(
                (stage / "distributions/skills-registry.json").read_text()
            )
            plugin = json.loads((stage / ".claude-plugin/plugin.json").read_text())
            manifest = {
                "schema_version": 1,
                "kind": KIND,
                "version": plugin["version"],
                "source": {
                    "repository": registry["repository"],
                    "commit": _source_commit(source),
                    "input_sha256": hashlib.sha256(_json_bytes(inputs)).hexdigest(),
                },
                "counts": {
                    "catalog": sum(
                        s["collection"] == "example" for s in registry["skills"]
                    ),
                    "plugins": sum(
                        s["collection"] == "plugins" for s in registry["skills"]
                    ),
                },
                "files": _inventory(stage),
            }
            manifest["build_id"] = hashlib.sha256(_json_bytes(manifest)).hexdigest()
            (stage / MANIFEST).write_text(
                json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
            )
            validate_release(stage, semantic=False)
            os.replace(stage, output)
            return manifest


def default_prefix() -> Path:
    configured = os.environ.get("DOMUS_SKILLS_HOME")
    if configured:
        return Path(configured).expanduser().absolute()
    return (
        Path(os.environ.get("XDG_DATA_HOME", str(Path.home() / ".local/share")))
        / "ai-skills"
    )


def _pointer(prefix: Path, name: str) -> Path | None:
    path = prefix / name
    if not path.is_symlink():
        if path.exists():
            raise InstallError(f"Refusing to replace an unmanaged path: {path}")
        return None
    target = path.resolve(strict=True)
    if target.parent != (prefix / "releases").resolve():
        raise InstallError(
            f"Managed {name} points outside this installation's releases"
        )
    if not (target / MANIFEST).is_file():
        raise InstallError(f"Managed {name} does not name a release")
    return target


def _replace_pointer(prefix: Path, name: str, target: Path | None) -> None:
    path = prefix / name
    if target is None:
        path.unlink(missing_ok=True)
        return
    temporary = prefix / f".{name}-{uuid.uuid4().hex}"
    try:
        temporary.symlink_to(os.path.relpath(target, prefix), target_is_directory=True)
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def _make_readonly(release: Path) -> None:
    for path in _files(release):
        path.chmod(0o555 if path.stat().st_mode & 0o111 else 0o444)
    for directory in sorted(
        (p for p in release.rglob("*") if p.is_dir()), reverse=True
    ):
        directory.chmod(0o555)
    release.chmod(0o555)


def _make_writable(root: Path) -> None:
    """Permit cleanup of a copied read-only release in our own staging directory."""
    root.chmod(0o755)
    for path in root.rglob("*"):
        if path.is_dir():
            path.chmod(0o755)


def install_release(
    prefix: Path,
    *,
    source: Path = ROOT,
    release: Path | None = None,
    expected_current: str | None = None,
) -> dict:
    prefix = prefix.expanduser().resolve()
    with _lock(prefix / ".install.lock"):
        old_current = _pointer(prefix, "current")
        old_previous = _pointer(prefix, "previous")
        if expected_current is not None:
            expected = (
                None
                if expected_current == "none"
                else Path(expected_current).resolve(strict=True)
            )
            if old_current != expected:
                raise InstallError(
                    "Current moved; refusing an update based on a stale installation"
                )
        releases = prefix / "releases"
        releases.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(
            prefix=".install-stage-", dir=prefix
        ) as temporary:
            candidate = Path(temporary) / "release"
            try:
                if release is None:
                    manifest = build_release(source, candidate)
                else:
                    validate_release(release)
                    _copy_directory(release.resolve(strict=True), candidate)
                    _make_writable(candidate)
                    manifest = validate_release(candidate)
                destination = releases / manifest["build_id"]
                if destination.exists():
                    if validate_release(destination) != manifest:
                        raise InstallError(
                            "Existing release conflicts with the candidate"
                        )
                else:
                    os.replace(candidate, destination)
                _make_readonly(destination)
                if old_current != destination:
                    try:
                        _replace_pointer(prefix, "previous", old_current)
                        # The only activation operation: readers see old or new.
                        _replace_pointer(prefix, "current", destination)
                    except BaseException:
                        _replace_pointer(prefix, "previous", old_previous)
                        raise
                return {
                    "release": str(destination),
                    "build_id": manifest["build_id"],
                    "previous": str(old_current)
                    if old_current and old_current != destination
                    else (str(old_previous) if old_previous else None),
                    "counts": manifest["counts"],
                }
            finally:
                if candidate.exists():
                    _make_writable(candidate)


def rollback(prefix: Path, expected_current: Path) -> dict:
    prefix = prefix.expanduser().resolve()
    with _lock(prefix / ".install.lock"):
        current = _pointer(prefix, "current")
        if current is None or current != expected_current.resolve(strict=True):
            raise InstallError("Current moved; refusing to undo another installation")
        previous = _pointer(prefix, "previous")
        if previous:
            validate_release(previous)
        _replace_pointer(prefix, "current", previous)
        _replace_pointer(prefix, "previous", current if previous else None)
        return {
            "release": str(previous) if previous else None,
            "rolled_back": str(current),
        }


def active_release(prefix: Path | None = None) -> Path:
    prefix = (prefix or default_prefix()).expanduser().resolve()
    release = _pointer(prefix, "current")
    if release is None:
        raise InstallError(
            f"No installed release at {prefix}; run scripts/skills_install.py install"
        )
    return release


def pack_release(release: Path, output: Path) -> str:
    release = release.resolve(strict=True)
    output = output.expanduser().absolute()
    checksum = output.with_name(output.name + ".sha256")
    # Check resolved paths before making a directory or lock inside the input.
    if output.resolve().is_relative_to(release) or checksum.resolve().is_relative_to(
        release
    ):
        raise InstallError("Archive and checksum must be outside the release")
    output.parent.mkdir(parents=True, exist_ok=True)
    with _lock(output.parent / f".{output.name}.pack.lock"):
        if any(path.exists() or path.is_symlink() for path in (output, checksum)):
            raise InstallError(
                "Archive or checksum already exists; choose a fresh output path"
            )
        manifest = validate_release(release)
        manifest_bytes = (release / MANIFEST).read_bytes()
        if json.loads(manifest_bytes) != manifest:
            raise InstallError("Release manifest changed while packaging")
        with tempfile.TemporaryDirectory(
            prefix=".skills-pack-", dir=output.parent
        ) as temporary:
            archive = Path(temporary) / "release.tar.gz"
            with (
                archive.open("wb") as raw,
                gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as gz,
            ):
                with tarfile.open(
                    mode="w", fileobj=gz, format=tarfile.PAX_FORMAT
                ) as tar:
                    expected = dict(manifest["files"])
                    expected[MANIFEST] = {
                        "sha256": hashlib.sha256(manifest_bytes).hexdigest(),
                        "mode": "100644",
                    }
                    for relative, record in sorted(expected.items()):
                        data = (release / relative).read_bytes()
                        if hashlib.sha256(data).hexdigest() != record["sha256"]:
                            raise InstallError(
                                f"Release changed while packaging: {relative}"
                            )
                        entry = tarfile.TarInfo("ai-skills/" + relative)
                        entry.size = len(data)
                        entry.mode = 0o755 if record["mode"] == "100755" else 0o644
                        entry.mtime = 0
                        tar.addfile(entry, io.BytesIO(data))
            digest = hashlib.sha256(archive.read_bytes()).hexdigest()
            checksum_temporary = Path(temporary) / "checksum"
            checksum_temporary.write_text(
                f"{digest}  {output.name}\n", encoding="utf-8"
            )
            os.replace(archive, output)
            try:
                os.replace(checksum_temporary, checksum)
            except BaseException:
                output.unlink()  # Never leave a package without its matching checksum.
                raise
        return digest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    build = commands.add_parser(
        "build", help="Build an absent output directory from canonical source"
    )
    build.add_argument("--source", type=Path, default=ROOT)
    build.add_argument("--output", type=Path, required=True)
    install = commands.add_parser(
        "install", help="Build or verify a release, then atomically activate it"
    )
    install.add_argument("--prefix", type=Path, default=default_prefix())
    install.add_argument("--source", type=Path, default=ROOT)
    install.add_argument(
        "--release", type=Path, help="Install this prebuilt release instead of building"
    )
    install.add_argument(
        "--expected-current", help="Require this exact current release, or 'none'"
    )
    validate = commands.add_parser(
        "validate", help="Verify all release bytes and runtime contracts"
    )
    validate.add_argument("--release", type=Path, required=True)
    undo = commands.add_parser(
        "rollback", help="Restore previous if current still matches the caller"
    )
    undo.add_argument("--prefix", type=Path, default=default_prefix())
    undo.add_argument("--expected-current", type=Path, required=True)
    path = commands.add_parser(
        "path", help="Print the active, verified release directory"
    )
    path.add_argument("--prefix", type=Path, default=default_prefix())
    pack = commands.add_parser(
        "pack", help="Create a deterministic release tarball and SHA-256 checksum"
    )
    pack.add_argument("--release", type=Path, required=True)
    pack.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "build":
            manifest = build_release(args.source, args.output)
            result = {
                "release": str(args.output),
                "build_id": manifest["build_id"],
                "counts": manifest["counts"],
            }
        elif args.command == "install":
            result = install_release(
                args.prefix,
                source=args.source,
                release=args.release,
                expected_current=args.expected_current,
            )
        elif args.command == "validate":
            manifest = validate_release(args.release)
            result = {
                "valid": True,
                "build_id": manifest["build_id"],
                "counts": manifest["counts"],
            }
        elif args.command == "rollback":
            result = rollback(args.prefix, args.expected_current)
        elif args.command == "pack":
            result = {
                "archive": str(args.output),
                "sha256": pack_release(args.release, args.output),
            }
        else:
            release = active_release(args.prefix)
            validate_release(release, semantic=False)
            print(release)
            return 0
        print(json.dumps(result, sort_keys=True))
        return 0
    except (
        InstallError,
        OSError,
        ValueError,
        KeyError,
        subprocess.CalledProcessError,
    ) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
