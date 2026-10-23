#!/usr/bin/env python3
"""Build a provenance-preserving local skill collection; never activate skills.

Source JSON: [{"id": "claude", "path": "/path/to/skills", "kind": "runtime",
               "working_directory": "/optional/original/cwd"}].
An explicit root alias may resolve through a symlink; nested links are recorded,
never traversed. Objects are copies, not proof of installation compatibility.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager, nullcontext
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import shutil
import tempfile
import time

PRUNE = {".git", "node_modules", "__pycache__", ".pytest_cache", ".ruff_cache"}
GENERATED_NAMES = PRUNE | {".DS_Store"}
GENERATED_SUFFIXES = {".pyc", ".pyo"}
RUNTIME_PRUNE = {"transcripts", "projects", "logs"}
INDEX_PREVIEW_CHARS = 1024


class LimitError(ValueError):
    pass


class Limits:
    def __init__(self, **kwargs):
        self.values = dict(directories=200000, entries=1000000, packages=20000,
                           file_bytes=64 * 1024**2, package_bytes=256 * 1024**2,
                           seconds=180)
        self.values.update(kwargs)
        if any(value <= 0 for value in self.values.values()):
            raise ValueError("All limits must be positive")
        self.counts = {}
        self.started = time.monotonic()

    def check(self, key=None):
        if time.monotonic() - self.started > self.values["seconds"]:
            raise LimitError("wall-time limit exceeded")
        if key:
            self.counts[key] = self.counts.get(key, 0) + 1
            if self.counts[key] > self.values[key]:
                raise LimitError(f"{key} limit exceeded")


@contextmanager
def pinned_directory(directory: Path, expected=None):
    """Open canonical directory components without following replacement links."""
    directory = directory.absolute()
    before = expected if expected is not None else directory.lstat()
    if not stat.S_ISDIR(before.st_mode):
        raise ValueError(f"unsafe directory: {directory}")
    if not hasattr(os, "O_DIRECTORY") or not hasattr(os, "O_NOFOLLOW"):
        raise ValueError("No-follow directory descriptors are unavailable on this platform")
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    fd = os.open(directory.anchor, flags)
    try:
        for name in directory.parts[1:]:
            child_fd = os.open(name, flags, dir_fd=fd)
            os.close(fd)
            fd = child_fd
        opened = os.fstat(fd)
        if (before.st_dev, before.st_ino) != (opened.st_dev, opened.st_ino):
            raise ValueError(f"directory changed while opening: {directory}")
        yield fd
        after = directory.lstat()
        if not stat.S_ISDIR(after.st_mode) or (opened.st_dev, opened.st_ino) != (
            after.st_dev, after.st_ino
        ):
            raise ValueError(f"directory changed during inspection: {directory}")
    finally:
        os.close(fd)


def bounded_children(directory: Path, limits: Limits, directory_fd=None):
    """Charge each directory entry before retaining it for deterministic ordering."""
    children = []
    access = pinned_directory(directory) if directory_fd is None else nullcontext(directory_fd)
    with access as fd:
        with os.scandir(fd) as iterator:
            for entry in iterator:
                limits.check("entries")
                children.append(directory / entry.name)
    return sorted(children)


def inert_text(value) -> str:
    """Keep previews bounded and inert; full metadata remains in catalog.json."""
    if isinstance(value, str) and len(value) > INDEX_PREVIEW_CHARS:
        value = value[:INDEX_PREVIEW_CHARS] + "... [truncated]"
    return "".join(f"&#{ord(char)};" for char in json.dumps(value, ensure_ascii=False))


def validate_catalog(catalog):
    if not isinstance(catalog, dict) or not isinstance(catalog.get("objects"), dict):
        raise ValueError("Catalog needs an objects mapping")
    if not isinstance(catalog.get("incomplete"), bool):
        raise ValueError("Catalog needs a boolean incomplete field")
    if not isinstance(catalog.get("occurrences"), list) or not all(
        isinstance(item, dict) for item in catalog["occurrences"]
    ):
        raise ValueError("Catalog needs an occurrences list of objects")
    for key in ("events", "sources"):
        if not isinstance(catalog.get(key, []), list) or not all(
            isinstance(item, dict) for item in catalog.get(key, [])
        ):
            raise ValueError(f"Catalog needs a {key} list of objects")
    for digest, item in catalog["objects"].items():
        if not isinstance(item, dict) or not isinstance(item.get("path"), str):
            raise ValueError(f"Invalid object record: {digest}")
        files = item.get("files")
        if not isinstance(files, list) or not all(isinstance(entry, dict) for entry in files):
            raise ValueError(f"Invalid object manifest: {digest}")
    return catalog


def regular_bytes(path: Path, limits: Limits, expected=None, directory_fd=None) -> bytes:
    """Bound reads and refuse linked directories, special files and churn."""
    access = pinned_directory(path.parent) if directory_fd is None else nullcontext(directory_fd)
    with access as parent_fd:
        before = os.stat(path.name, dir_fd=parent_fd, follow_symlinks=False)
        if expected is not None and (before.st_dev, before.st_ino, before.st_mode) != (
            expected.st_dev, expected.st_ino, expected.st_mode
        ):
            raise ValueError(f"file changed before reading: {path}")
        if not stat.S_ISREG(before.st_mode):
            raise ValueError(f"not a regular file: {path}")
        if before.st_size > limits.values["file_bytes"]:
            raise LimitError(f"file size limit: {path}")
        fd = os.open(path.name, os.O_RDONLY | os.O_NOFOLLOW | getattr(os, "O_NONBLOCK", 0),
                     dir_fd=parent_fd)
        with os.fdopen(fd, "rb") as stream:
            opened = os.fstat(stream.fileno())
            if (before.st_dev, before.st_ino, before.st_mode) != (
                opened.st_dev, opened.st_ino, opened.st_mode
            ):
                raise ValueError(f"file changed while opening: {path}")
            data = stream.read(limits.values["file_bytes"] + 1)
            after = os.fstat(stream.fileno())
    limits.check()
    if len(data) > limits.values["file_bytes"]:
        raise LimitError(f"file size limit: {path}")
    if (opened.st_size, opened.st_mtime_ns, opened.st_ctime_ns, opened.st_mode) != (
        after.st_size, after.st_mtime_ns, after.st_ctime_ns, after.st_mode
    ):
        raise ValueError(f"file changed while reading: {path}")
    return data


def metadata(data: bytes, fallback: str) -> dict:
    """Extract common YAML scalars leniently, without interpreting YAML tags."""
    text = data.decode("utf-8-sig", errors="replace")
    result = {"name": fallback, "description": ""}
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return result
    for index, line in enumerate(lines[1:], 1):
        if line.strip() in {"---", "..."}:
            break
        match = re.match(r"^(name|description):\s*(.*)$", line)
        if not match:
            continue
        key, value = match.groups()
        if value in {"|", ">", "|-", ">-", "|+", ">+"}:
            continuation = []
            for following in lines[index + 1:]:
                if following and not following[0].isspace():
                    break
                continuation.append(following.strip())
            value = (" " if value.startswith(">") else "\n").join(continuation)
        elif len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        result[key] = value or result[key]
    return result


def package_manifest(root: Path, limits: Limits, excluded=None) -> tuple[str, list]:
    """Hash package resources, paths and executable bits, excluding generated state."""
    entries, pending, seen, total = [], [root], set(), 0
    while pending:
        directory = pending.pop()
        limits.check("directories")
        info = directory.lstat()
        if not stat.S_ISDIR(info.st_mode):
            raise ValueError(f"unsafe directory: {directory}")
        identity = (info.st_dev, info.st_ino)
        if identity in seen:
            raise ValueError(f"directory cycle: {directory}")
        seen.add(identity)
        with pinned_directory(directory, expected=info) as directory_fd:
            for child in bounded_children(directory, limits, directory_fd):
                info = os.stat(child.name, dir_fd=directory_fd, follow_symlinks=False)
                relative = child.relative_to(root).as_posix()
                if child.name in GENERATED_NAMES or child.suffix in GENERATED_SUFFIXES:
                    if excluded is not None:
                        excluded.append(relative)
                    continue
                if stat.S_ISDIR(info.st_mode):
                    entries.append({"path": relative, "type": "directory"})
                    pending.append(child)
                elif stat.S_ISREG(info.st_mode):
                    data = regular_bytes(child, limits, expected=info, directory_fd=directory_fd)
                    total += len(data)
                    if total > limits.values["package_bytes"]:
                        raise LimitError(f"package size limit: {root}")
                    entries.append(dict(path=relative, type="file", size=len(data),
                                        executable=info.st_mode & 0o111,
                                        sha256=hashlib.sha256(data).hexdigest()))
                else:
                    kind = "symlink" if stat.S_ISLNK(info.st_mode) else "special file"
                    raise ValueError(f"unsafe {kind}: {child}")
    entries.sort(key=lambda entry: entry["path"])
    digest = hashlib.sha256(json.dumps(entries, sort_keys=True,
                                      separators=(",", ":")).encode()).hexdigest()
    return digest, entries


def copy_package(source: Path, target: Path, entries: list, limits: Limits):
    target.mkdir(parents=True, exist_ok=False)
    for entry in entries:
        limits.check()
        destination = target / entry["path"]
        if entry["type"] == "directory":
            destination.mkdir(parents=True, exist_ok=True)
        else:
            origin = source / entry["path"]
            # Refuse a source directory exchanged for a link after inspection.
            if origin.resolve() != origin:
                raise ValueError(f"source gained a symlink: {origin}")
            data = regular_bytes(origin, limits)
            if hashlib.sha256(data).hexdigest() != entry["sha256"]:
                raise ValueError(f"source changed before copying: {origin}")
            destination.parent.mkdir(parents=True, exist_ok=True)
            with destination.open("xb") as stream:
                stream.write(data)
            destination.chmod(0o600 | entry["executable"])


def discover(root: Path, kind: str, limits: Limits, events: list):
    pending, seen = [root], set()
    while pending:
        directory = pending.pop()
        limits.check("directories")
        try:
            info = directory.lstat()
            if not stat.S_ISDIR(info.st_mode):
                raise ValueError("directory changed or is not a directory")
            identity = (info.st_dev, info.st_ino)
            if identity in seen:
                events.append(dict(path=str(directory), status="cycle-skipped"))
                continue
            seen.add(identity)
            with pinned_directory(directory, expected=info) as directory_fd:
                children = bounded_children(directory, limits, directory_fd)
                for child in children:
                    info = os.stat(child.name, dir_fd=directory_fd, follow_symlinks=False)
                    if stat.S_ISLNK(info.st_mode):
                        try:
                            os.stat(child.name, dir_fd=directory_fd)
                            status = "symlink-skipped"
                        except FileNotFoundError:
                            status = "broken-symlink"
                        except OSError:
                            status = "unresolved-symlink"
                        events.append(dict(path=str(child), status=status,
                                           target=os.readlink(child.name, dir_fd=directory_fd)))
                    if child.name.lower() == "skill.md" and directory != root:
                        limits.check("packages")
                        yield child
                    if stat.S_ISDIR(info.st_mode):
                        pruned = child.name in PRUNE or (kind == "runtime" and
                                                        child.name in RUNTIME_PRUNE)
                        if pruned:
                            events.append(dict(path=str(child), status="excluded-directory"))
                        else:
                            pending.append(child)
        except LimitError:
            raise
        except (OSError, ValueError) as error:
            events.append(dict(path=str(directory), status="scan-error", error=str(error)))


def resolve_sources(sources: list, output: Path) -> list:
    """Validate source declarations and overlap without creating any output paths."""
    resolved = []
    ids = set()
    if not isinstance(sources, list):
        raise ValueError("Sources must be a list")
    for source in sources:
        if not isinstance(source, dict) or not all(k in source for k in ("id", "path", "kind")):
            raise ValueError("Each source needs id, path and kind")
        if not all(isinstance(source[key], str) and source[key].strip()
                   for key in ("id", "path", "kind")):
            raise ValueError("Source id, path and kind must be nonempty strings")
        if source.get("working_directory") is not None and not isinstance(source["working_directory"], str):
            raise ValueError("Source working_directory must be a string or null")
        if source["id"] in ids:
            raise ValueError("Source IDs must be unique")
        ids.add(source["id"])
        root = Path(source["path"]).expanduser().absolute()
        try:
            canonical = root.resolve()
        except (OSError, RuntimeError):
            canonical = root
        if output == canonical or output in canonical.parents or canonical in output.parents:
            raise ValueError(f"Output/source overlap: {root}")
        resolved.append((source, root, canonical))
    return resolved


def _build(sources: list, output: Path, limits: Limits | None = None) -> dict:
    limits = limits or Limits()
    output = output.absolute()
    if output.is_symlink():
        raise ValueError("Output cannot be a symlink")
    output = output.resolve()
    resolved = resolve_sources(sources, output)
    if output.exists() and (not output.is_dir() or any(output.iterdir())):
        raise ValueError("Output must be a new or empty directory")
    output.mkdir(parents=True, exist_ok=True, mode=0o700)
    output.chmod(0o700)
    catalog = dict(schema_version=1, purpose="discovery and custody; no autoactivation",
                   standalone_compatibility="unverified", sources=[], occurrences=[],
                   objects={}, events=[], incomplete=False, limits=limits.values)
    catalog["exclusion_policy"] = dict(
        package_names=sorted(GENERATED_NAMES), package_suffixes=sorted(GENERATED_SUFFIXES),
        discovery_directories=sorted(PRUNE), runtime_only_directories=sorted(RUNTIME_PRUNE),
        note="Generated state is excluded from package identity and copies; actual package exclusions are recorded per occurrence.")
    for source, root, canonical in resolved:
        record = dict(source, resolved_path=str(canonical), status="scanned")
        catalog["sources"].append(record)
        if not canonical.is_dir():
            record["status"] = "missing-or-invalid-root"
            catalog["incomplete"] = True
            continue
        try:
            for skill in discover(canonical, source["kind"], limits, catalog["events"]):
                occurrence = dict(source_id=source["id"], source_kind=source["kind"],
                                  source_path=str(root / skill.relative_to(canonical)),
                                  resolved_path=str(skill), package_path=str(skill.parent),
                                  working_directory=source.get("working_directory"),
                                  status="needs-review", standalone_compatibility="unverified")
                catalog["occurrences"].append(occurrence)
                try:
                    occurrence.update(metadata(regular_bytes(skill, limits), skill.parent.name))
                    occurrence["excluded_generated_paths"] = []
                    digest, entries = package_manifest(skill.parent, limits,
                                                       occurrence["excluded_generated_paths"])
                    occurrence["package_sha256"] = digest
                    if digest not in catalog["objects"]:
                        target = output / "objects" / digest
                        try:
                            copy_package(skill.parent, target, entries, limits)
                            copied, copied_entries = package_manifest(target, limits)
                            if (copied, copied_entries) != (digest, entries):
                                raise ValueError(f"Copied package failed verification: {target}")
                        except BaseException:
                            if target.exists():
                                shutil.rmtree(target)
                            raise
                        catalog["objects"][digest] = dict(path=f"objects/{digest}",
                                                          verified=True, files=entries)
                    # Searchable metadata must describe the verified object,
                    # even if the source entrypoint changed before manifesting.
                    retained_skill = output / catalog["objects"][digest]["path"] / skill.name
                    occurrence.update(metadata(regular_bytes(retained_skill, limits), skill.parent.name))
                    occurrence["status"] = "copied-verified"
                except (OSError, ValueError) as error:
                    occurrence["error"] = str(error)
                    catalog["incomplete"] = True
                    if isinstance(error, LimitError):
                        raise
        except (OSError, ValueError) as error:
            record.update(status="incomplete", error=str(error))
            catalog["incomplete"] = True
    catalog["incomplete"] |= any(e["status"] in {"scan-error", "cycle-skipped"}
                                  for e in catalog["events"])
    groups, names = {}, {}
    for occurrence in catalog["occurrences"]:
        digest = occurrence.get("package_sha256")
        if digest:
            groups.setdefault(digest, []).append(occurrence["source_path"])
            names.setdefault(occurrence.get("name", ""), set()).add(digest)
    catalog["exact_duplicates"] = {key: value for key, value in groups.items() if len(value) > 1}
    catalog["same_name_variants"] = {key: sorted(value) for key, value in names.items() if len(value) > 1}
    catalog["counts"] = dict(occurrences=len(catalog["occurrences"]), objects=len(catalog["objects"]))
    (output / "catalog.json").write_text(json.dumps(catalog, indent=2) + "\n")
    lines = ["# Local skill catalog", "", "Discovery and custody only. No autoactivation.",
             "Standalone compatibility is unverified. Use the original source and working directory.",
             "Full provenance, exclusions, errors and limits are in catalog.json.", "",
             f"Incomplete: {catalog['incomplete']}. Occurrences: {len(catalog['occurrences'])}.", ""]
    for item in catalog["occurrences"]:
        lines.extend([f"- {inert_text(item.get('name', '?'))} — {inert_text(item['status'])}",
                      f"  source: {inert_text(item['source_path'])}",
                      f"  object: {inert_text(item.get('package_sha256', 'none'))}",
                      f"  working directory: {inert_text(item['working_directory'])}"])
    (output / "INDEX.md").write_text("\n".join(lines) + "\n")
    return catalog


def build(sources: list, output: Path, limits: Limits | None = None) -> dict:
    """Publish a complete snapshot by same-filesystem rename; failures are retryable."""
    output = output.absolute()
    if output.is_symlink():
        raise ValueError("Output cannot be a symlink")
    output = output.resolve()
    # Validate every source against the requested destination before any writes.
    resolve_sources(sources, output)
    if output.exists() and (not output.is_dir() or any(output.iterdir())):
        raise ValueError("Output must be a new or empty directory")
    output.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=f".{output.name}-", dir=output.parent))
    try:
        result = _build(sources, staging, limits)
        os.replace(staging, output)
        return result
    finally:
        if staging.exists():
            shutil.rmtree(staging)


def catalog_location(path: Path) -> Path:
    """Resolve the caller's explicit directory alias, preserving final-link refusal."""
    try:
        return path.parent.resolve() / path.name
    except RuntimeError as error:
        raise ValueError(f"Invalid catalog directory: {path.parent}") from error


def verify(catalog_path: Path, limits: Limits | None = None) -> dict:
    limits = limits or Limits()
    catalog_path = catalog_location(catalog_path)
    catalog = validate_catalog(json.loads(regular_bytes(catalog_path, limits)))
    failures = []
    for index, occurrence in enumerate(catalog["occurrences"]):
        if occurrence.get("status") == "copied-verified":
            digest = occurrence.get("package_sha256")
            if not isinstance(digest, str) or digest not in catalog["objects"]:
                failures.append(f"occurrences[{index}]: unregistered object {digest}")
    for digest, item in catalog["objects"].items():
        try:
            if not re.fullmatch(r"[0-9a-f]{64}", digest) or item["path"] != f"objects/{digest}":
                raise ValueError("Invalid object path")
            root = catalog_path.parent.resolve() / item["path"]
            if root.resolve() != root:
                raise ValueError("Object path contains symlink")
            actual, entries = package_manifest(root, limits)
            if actual != digest or entries != item["files"]:
                raise ValueError("Object hash or manifest mismatch")
        except (OSError, ValueError) as error:
            failures.append(f"{digest}: {error}")
    objects_root = catalog_path.parent.resolve() / "objects"
    orphan_objects = []
    if objects_root.is_symlink():
        failures.append("objects directory is a symlink")
    elif objects_root.exists():
        orphan_objects = sorted(path.name for path in bounded_children(objects_root, limits)
                                if path.name not in catalog["objects"])
    complete = not catalog.get("incomplete", True)
    retained_verified = not failures
    return dict(verified=retained_verified and complete and not orphan_objects,
                retained_objects_verified=retained_verified, catalog_complete=complete,
                object_count=len(catalog["objects"]), orphan_objects=orphan_objects,
                failures=failures)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sources", type=Path, help="JSON source list")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--catalog", type=Path)
    parser.add_argument("--find", help="Case-insensitive name, description or path search")
    parser.add_argument("--verify", action="store_true")
    for name, default in Limits().values.items():
        parser.add_argument(f"--max-{name.replace('_', '-')}", type=int, default=default)
    args = parser.parse_args()
    try:
        limits = Limits(**{name: getattr(args, f"max_{name}") for name in Limits().values})
        if args.catalog and args.verify:
            report = verify(args.catalog, limits)
            print(json.dumps(report, indent=2))
            return int(not report["verified"])
        if args.catalog and args.find is not None:
            data = validate_catalog(json.loads(regular_bytes(catalog_location(args.catalog), limits)))
            for collection in ("occurrences", "events", "sources"):
                for item in data.get(collection, []):
                    if args.find.casefold() in json.dumps(item, ensure_ascii=False).casefold():
                        print(json.dumps(item, ensure_ascii=False))
            if data["incomplete"]:
                print("Warning: results are from an incomplete catalog", file=sys.stderr)
                return 2
            return 0
        if not args.sources or not args.output:
            parser.error("Use --sources + --output, or --catalog + --find/--verify")
        catalog = build(json.loads(args.sources.read_text()), args.output, limits)
        print(json.dumps(dict(catalog=str(args.output / "catalog.json"),
                              incomplete=catalog["incomplete"], **catalog["counts"])))
        return 2 if catalog["incomplete"] else 0
    except (OSError, ValueError) as error:
        parser.exit(1, f"Error: {error}\n")


if __name__ == "__main__":
    raise SystemExit(main())
