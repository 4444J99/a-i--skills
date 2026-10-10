#!/usr/bin/env python3
"""Rebuild all runtime bundles and metadata from canonical source only."""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

from skill_lib import extract_frontmatter_strict, find_plugin_dirs, skill_collections

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
PLUGINS_DIR = ROOT / "plugins"
BUILD_DIR = ROOT / "distributions"
ECOSYSTEM_YAML = ROOT / "ecosystem.yaml"
README = ROOT / "README.md"
NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")


def _json_text(value: object) -> str:
    return json.dumps(value, indent=2) + "\n"


def _list_text(values: list[str]) -> str:
    return "".join(value + "\n" for value in values)


def _source_manifest(path: Path) -> dict:
    if path.is_symlink():
        raise ValueError(f"Source descriptor must not be a symlink: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise TypeError(f"{path}: source descriptor must be a JSON object")
    for field in ("name", "description", "version"):
        if not isinstance(data.get(field), str) or not data[field].strip():
            raise ValueError(f"{path}: missing source metadata {field!r}")
    if not NAME_RE.fullmatch(data["name"]):
        raise ValueError(f"{path}: invalid plugin name {data['name']!r}")
    return data


def _runtime_config(root: Path) -> dict:
    path = root / "config" / "runtime-catalog.json"
    if path.is_symlink():
        raise ValueError(f"Canonical config must not be a symlink: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise TypeError(f"{path}: runtime catalog must be a JSON object")
    if data.get("schema_version") != 1:
        raise ValueError(f"{path}: unsupported schema_version")
    if not isinstance(data.get("repository"), str) or "/" not in data["repository"]:
        raise ValueError(f"{path}: repository must be owner/name")
    marketplace = data.get("marketplace", {})
    if not isinstance(marketplace, dict):
        raise TypeError(f"{path}: marketplace must be an object")
    if not NAME_RE.fullmatch(str(marketplace.get("name", ""))):
        raise ValueError(f"{path}: invalid marketplace name")
    if not isinstance(marketplace.get("description"), str) or not marketplace["description"]:
        raise ValueError(f"{path}: marketplace description is required")
    gemini = data.get("gemini", {})
    if not isinstance(gemini, dict):
        raise TypeError(f"{path}: gemini must be an object")
    context = gemini.get("context_file")
    if not isinstance(context, str) or not context or Path(context).name != context or context in (".", ".."):
        raise ValueError(f"{path}: Gemini context_file must be a filename")
    if not isinstance(gemini.get("label"), str) or not gemini["label"]:
        raise ValueError(f"{path}: Gemini label is required")
    purposes = data.get("purpose_collections")
    if not isinstance(purposes, dict):
        raise TypeError(f"{path}: purpose_collections must be an object")
    for label, names in purposes.items():
        if not NAME_RE.fullmatch(label) or not isinstance(names, list):
            raise ValueError(f"{path}: invalid purpose collection {label!r}")
        if any(not isinstance(name, str) or not NAME_RE.fullmatch(name) for name in names):
            raise ValueError(f"{path}: invalid names in purpose collection {label!r}")
        if len(names) != len(set(names)):
            raise ValueError(f"{path}: duplicate names in purpose collection {label!r}")
    return data


def _bundle_targets(root: Path) -> list[Path]:
    catalog = _source_manifest(root / ".claude-plugin" / "plugin.json")
    return [
        root / "distributions" / "direct" / "example",
        root / "distributions" / "codex" / "skills",
        root / "distributions" / "claude" / "skills",
        root / "distributions" / "extensions" / "gemini" / catalog["name"] / "skills",
    ]


def expected_metadata(root: Path) -> dict[str, str]:
    """Describe every generated descriptor/list/context without reading output."""
    config = _runtime_config(root)
    catalog = _source_manifest(root / ".claude-plugin" / "plugin.json")
    owner = catalog.get("author")
    if not isinstance(owner, dict) or not owner.get("name"):
        raise ValueError("The source catalog plugin descriptor must declare its author")
    collections = skill_collections(root)
    examples = collections["example"]
    plugins = collections["plugins"]
    example_paths = [path.relative_to(root).as_posix() for path in examples]
    plugin_paths = [path.relative_to(root).as_posix() for path in plugins]
    if not examples:
        raise ValueError("The canonical catalog contains no skills")

    entries = [{
        "name": catalog["name"],
        "description": catalog["description"],
        "source": "./",
        "strict": True,
        "skills": ["./" + path for path in example_paths],
    }]
    for directory in find_plugin_dirs(root / "plugins"):
        manifest = _source_manifest(directory / ".claude-plugin" / "plugin.json")
        if manifest["name"] != directory.name:
            raise ValueError(f"Plugin descriptor name does not match its folder: {directory}")
        entries.append({
            "name": manifest["name"],
            "description": manifest["description"],
            "source": "./" + directory.relative_to(root).as_posix(),
        })
    if len({entry["name"] for entry in entries}) != len(entries):
        raise ValueError("Duplicate plugin names in the source catalog")

    result = {
        ".claude-plugin/marketplace.json": _json_text({
            "name": config["marketplace"]["name"],
            "owner": owner,
            "metadata": {
                "description": config["marketplace"]["description"],
                "version": catalog["version"],
            },
            "plugins": entries,
        }),
        "distributions/collections/example-skills.txt": _list_text(example_paths),
        "distributions/collections/plugin-skills.txt": _list_text(plugin_paths),
    }
    groups: dict[str, list[str]] = {
        "core-skills": [], "community-skills": [], "governance-norms": [], "auto-activate-skills": [],
    }
    categories: dict[str, list[str]] = {}
    complexities: dict[str, list[str]] = {}
    for directory in examples:
        metadata = extract_frontmatter_strict((directory / "SKILL.md").read_text(encoding="utf-8"))
        relative = directory.relative_to(root).as_posix()
        category = directory.relative_to(root / "skills").parts[0]
        categories.setdefault(category, []).append(directory.name)
        if metadata.get("complexity"):
            complexities.setdefault(metadata["complexity"], []).append(directory.name)
        if metadata.get("tier") in ("core", "community"):
            groups[metadata["tier"] + "-skills"].append(relative)
        if metadata.get("governance_norm_group"):
            groups["governance-norms"].append(relative)
        if metadata.get("governance_auto_activate") == "true":
            groups["auto-activate-skills"].append(relative)
    for label, values in groups.items():
        result[f"distributions/collections/{label}.txt"] = _list_text(values)
    for category, values in sorted(categories.items()):
        result[f"distributions/collections/by-category/{category}.txt"] = _list_text(values)
    for complexity, values in sorted(complexities.items()):
        result[f"distributions/collections/by-complexity/{complexity}.txt"] = _list_text(values)
    names = {path.name for path in examples}
    for purpose, selected in sorted(config["purpose_collections"].items()):
        unknown = set(selected) - names
        if unknown:
            raise ValueError(f"Purpose collection {purpose!r} references unknown catalog skills: {sorted(unknown)}")
        result[f"distributions/collections/by-purpose/{purpose}.txt"] = _list_text(sorted(selected))

    gemini_root = f"distributions/extensions/gemini/{catalog['name']}"
    context_file = config["gemini"]["context_file"]
    result[f"{gemini_root}/gemini-extension.json"] = _json_text({
        "name": catalog["name"],
        "version": catalog["version"],
        "label": config["gemini"]["label"],
        "description": catalog["description"],
        "contextFileName": context_file,
    })
    result[f"{gemini_root}/{context_file}"] = (
        f"# {config['gemini']['label']}\n\n"
        f"This generated extension contains {len(examples)} catalog skills from "
        f"{config['repository']} at catalog version {catalog['version']}.\n\n"
        "Read a skill's instructions from skills/<name>/SKILL.md and its bundled "
        "resources when needed. Each folder is a complete copy of canonical source.\n\n"
        "Build updates from the repository with scripts/skills_install.py. "
        "Generated extension files are replaced only after the staged release passes validation.\n"
    )
    result["distributions/collections/README.md"] = (
        "# Generated skill collections\n\n"
        f"The catalog contains {len(examples)} skills; complete plugin packages contain "
        f"{len(plugins)} additional definitions.\n\n"
        "example-skills.txt and plugin-skills.txt contain paths relative to the release root. "
        "Category, complexity, and purpose collections contain catalog skill names. "
        "Purpose membership is canonical in config/runtime-catalog.json; all other lists "
        "are derived from source folders and frontmatter.\n"
    )
    for runtime in ("claude", "codex"):
        result[f"distributions/{runtime}/README.md"] = (
            f"# {runtime.title()} skill bundle\n\n"
            f"skills/ contains complete copies of all {len(examples)} catalog skills. "
            "Plugin packages remain intact under ../../plugins in the release root "
            "so their shared resources, agents, and source descriptors remain available.\n\n"
            "Install and update using scripts/skills_install.py from the repository root.\n"
        )
    result["distributions/extensions/gemini/README.md"] = (
        "# Generated Gemini extension\n\n"
        f"{catalog['name']}/ contains the extension descriptor, context file, "
        f"and all {len(examples)} catalog skill folders. The version and description "
        "come from .claude-plugin/plugin.json. Build and validate a release before installation.\n"
    )
    return result


def _ensure_generated_dir(path: Path) -> None:
    if path.is_symlink() or any(parent.is_symlink() for parent in path.parents):
        raise RuntimeError(f"Refusing to write through a generated-directory symlink: {path}")
    path.mkdir(parents=True, exist_ok=True)
    marker = path / ".skills-generated"
    if marker.is_symlink():
        raise RuntimeError(f"Generated marker must not be a symlink: {marker}")
    if marker.exists():
        return
    if any(path.iterdir()):
        raise RuntimeError(f"Refusing to modify non-empty directory without marker: {path}")
    marker.write_text("generated by scripts/refresh_skill_collections.py\n", encoding="utf-8")


def _sync_links(target_dir: Path, sources: list[Path], mode: str) -> None:
    _ensure_generated_dir(target_dir)
    expected = {src.name: src for src in sources}
    if len(expected) != len(sources):
        raise ValueError("Duplicate names cannot be flattened into a runtime bundle")
    for entry in target_dir.iterdir():
        if entry.name == ".skills-generated":
            continue
        if entry.name not in expected:
            if entry.is_symlink() or entry.is_file():
                entry.unlink()
            elif entry.is_dir():
                shutil.rmtree(entry)
    for name, src in expected.items():
        destination = target_dir / name
        if destination.is_symlink() or destination.is_file():
            destination.unlink()
        elif destination.exists():
            shutil.rmtree(destination)
        if mode == "copy":
            shutil.copytree(src, destination)
        else:
            destination.symlink_to(os.path.relpath(src, target_dir), target_is_directory=True)


def _write_metadata(root: Path, metadata: dict[str, str]) -> None:
    # Collection lists are entirely generated; their authored membership is in
    # config/runtime-catalog.json. Remove stale category/purpose outputs on refresh.
    collection_root = root / "distributions" / "collections"
    if collection_root.is_symlink() or any(parent.is_symlink() for parent in collection_root.parents):
        raise ValueError(f"Generated collections must not be written through a symlink: {collection_root}")
    if collection_root.exists():
        for path in collection_root.rglob("*"):
            if path.is_symlink():
                raise ValueError(f"Generated metadata must not be a symlink: {path}")
            if path.is_file() and path.relative_to(root).as_posix() not in metadata:
                path.unlink()
    for relative, contents in metadata.items():
        destination = root / relative
        if destination.is_symlink() or any(parent.is_symlink() for parent in destination.parents if parent != root):
            raise ValueError(f"Generated metadata must not be written through a symlink: {destination}")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(contents, encoding="utf-8")
        destination.chmod(0o644)


def _update_ecosystem_yaml(skill_count: int, category_count: int) -> bool:
    if not ECOSYSTEM_YAML.exists():
        return False
    text = ECOSYSTEM_YAML.read_text(encoding="utf-8")
    suffix = "category" if category_count == 1 else "categories"
    changed = re.sub(r"\d+\+?\s+skills\s+across\s+\d+\s+categor(?:y|ies)",
                     f"{skill_count} skills across {category_count} {suffix}", text)
    if changed == text:
        return False
    ECOSYSTEM_YAML.write_text(changed, encoding="utf-8")
    return True


def _update_readme(skill_count: int, category_count: int, example_count: int,
                   per_category_counts: dict[str, int]) -> bool:
    if not README.exists():
        return False
    text = README.read_text(encoding="utf-8")
    original = text
    suffix = "category" if category_count == 1 else "categories"
    text = re.sub(r"\d+\+?\s+skills\s+across\s+\d+\s+categor(?:y|ies)",
                  f"{skill_count} skills across {category_count} {suffix}", text)
    text = re.sub(r"\d+\+?\s+skills\s+are\s+organized\s+into\s+\d+\s+categor(?:y|ies)",
                  f"{skill_count} skills are organized into {category_count} {suffix}", text)
    text = re.sub(r"(skills/\s*#\s*)\d+\+?\s+example\s+skills",
                  rf"\g<1>{example_count} example skills", text)
    for category, count in per_category_counts.items():
        pattern = rf"(├──|└──)(\s+){re.escape(category)}/(\s*#\s*)\d+\s+skills"
        text = re.sub(pattern, rf"\1\g<2>{category}/\g<3>{count} skills", text)
    if text == original:
        return False
    README.write_text(text, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=["symlink", "copy"], default="copy")
    parser.add_argument("--skip-marketplace", action="store_true")
    parser.add_argument("--skip-ecosystem", action="store_true")
    parser.add_argument("--skip-readme", action="store_true")
    args = parser.parse_args()
    scripts_dir = Path(__file__).resolve().parent
    required = ["validate_skills.py", "generate_registry.py", "generate_lockfile.py", "validate_generated_dirs.py"]
    try:
        for script_name in required:
            if not (scripts_dir / script_name).is_file():
                raise FileNotFoundError(f"Required generator/validator missing: {script_name}")
        subprocess.run([sys.executable, str(scripts_dir / "validate_skills.py"),
                        "--collection", "all", "--unique", "--check-links"], check=True)
        metadata = expected_metadata(ROOT)
        if args.skip_marketplace:
            del metadata[".claude-plugin/marketplace.json"]
        _write_metadata(ROOT, metadata)
        examples = skill_collections(ROOT)["example"]
        for target in _bundle_targets(ROOT):
            _sync_links(target, examples, args.mode)
        for script_name in ("generate_registry.py", "generate_lockfile.py"):
            subprocess.run([sys.executable, str(scripts_dir / script_name)], check=True)
        if args.mode == "copy":
            subprocess.run([sys.executable, str(scripts_dir / "validate_generated_dirs.py")], check=True)
        counts: dict[str, int] = {}
        for directory in examples:
            category = directory.relative_to(SKILLS_DIR).parts[0]
            counts[category] = counts.get(category, 0) + 1
        if not args.skip_ecosystem:
            _update_ecosystem_yaml(len(examples), len(counts))
        if not args.skip_readme:
            _update_readme(len(examples), len(counts), len(examples), counts)
    except (OSError, ValueError, TypeError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"ERROR: runtime generation failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
