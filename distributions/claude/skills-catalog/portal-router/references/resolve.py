#!/usr/bin/env python3
"""portal-router resolver — the engine of the first forged arm.

Walks every mirrored ecosystem in ~/_arms/mirror/ (Claude, Codex, Gemini,
.agents, a-i--skills, OpenCode, OpenClaw) plus our own Zone-1 ~/_arms/skills/,
normalizes their heterogeneous capability units into one record shape, and
answers cross-agent capability queries. This is what `_arms` is uniquely
positioned to do: it is the only vantage point that sees all ecosystems at once.

stdlib only — no pip deps (light on its feet). Follows symlinks (the mirror
entries ARE symlinks; without -L/followlinks the portal looks empty).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ARMS = Path(os.path.expanduser("~/_arms"))
MIRROR = ARMS / "mirror"
OURS = ARMS / "skills"

# Per-ecosystem invocation hint, keyed by mirror link name (or "ours" for Zone 1).
INVOKE = {
    "ours": "OUR arm — load via `~/_arms/arm show ours <name>` or promote to a-i--skills",
    "claude": "Claude: `/<name>` or the Skill tool",
    "agents": ".agents pool: load from ~/.agents/skills/<name>",
    "codex": "Codex: skill at ~/.codex/skills/<name>",
    "gemini": "Gemini: skill at ~/.gemini/skills/<name>",
    "source": "a-i--skills distribution source (canonical; deploy via skills-registry)",
    "opencode-commands": "OpenCode: `/<name>` command",
    "openclaw-extensions": "OpenClaw extension",
    "openclaw-agents": "OpenClaw agent",
}

# Directories never worth walking into.
PRUNE = {".git", "node_modules", ".build", "__pycache__", ".venv", "dist", "build"}
# Filenames that are not capability units.
SKIP_NAMES = {"readme.md", "agents.md", "changelog.md", "license.md", "contributing.md"}


def _read_frontmatter(path: Path) -> tuple[dict, str]:
    """Return (frontmatter_dict, first_body_line). Tolerant of malformed YAML —
    we only need name/description, so we parse those two keys by hand."""
    fm: dict[str, str] = {}
    first_body = ""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except (OSError, UnicodeError):
        return fm, first_body
    lines = text.splitlines()
    i = 0
    if lines and lines[0].strip() == "---":
        i = 1
        while i < len(lines) and lines[i].strip() != "---":
            line = lines[i]
            if ":" in line and not line.startswith((" ", "\t", "-")):
                key, _, val = line.partition(":")
                fm[key.strip().lower()] = val.strip().strip("\"'")
            i += 1
        i += 1  # skip closing ---
    for line in lines[i:]:
        if line.strip():
            first_body = line.strip()
            break
    return fm, first_body


def _unit_type(eco: str, path: Path) -> str:
    name = path.name.lower()
    parts = {p.lower() for p in path.parts}
    if name == "skill.md" or ".skill" in path.parent.name.lower():
        return "skill"
    if "commands" in parts or eco == "opencode-commands":
        return "command"
    if "agents" in parts or eco == "openclaw-agents":
        return "agent"
    if eco == "openclaw-extensions":
        return "extension"
    return "skill"


def _derive_name(eco: str, path: Path, fm: dict) -> str:
    if fm.get("name"):
        return fm["name"]
    if path.name.lower() == "skill.md":
        # parent dir is the skill name; strip a trailing .skill if present
        return path.parent.name.removesuffix(".skill")
    return path.stem


def _walk(eco: str, root: Path, max_depth: int = 4):
    """Yield capability-unit records under root, following symlinks."""
    root_depth = len(root.parts)
    for dirpath, dirnames, filenames in os.walk(root, followlinks=True):
        depth = len(Path(dirpath).parts) - root_depth
        if depth >= max_depth:
            dirnames[:] = []
        dirnames[:] = [d for d in dirnames if d not in PRUNE]
        for fn in filenames:
            if not fn.lower().endswith(".md"):
                continue
            if fn.lower() in SKIP_NAMES:
                continue
            path = Path(dirpath) / fn
            fm, body = _read_frontmatter(path)
            desc = fm.get("description") or body or "(no description)"
            yield {
                "ecosystem": eco,
                "type": _unit_type(eco, path),
                "name": _derive_name(eco, path, fm),
                "description": desc,
                "path": str(path),
                "invoke": INVOKE.get(eco, f"{eco}: {path}"),
                "triggers": fm.get("triggers", ""),
            }


def build_index() -> list[dict]:
    units: list[dict] = []
    seen: set[tuple] = set()
    sources: list[tuple[str, Path]] = []
    if OURS.is_dir():
        sources.append(("ours", OURS))
    if MIRROR.is_dir():
        for link in sorted(MIRROR.iterdir()):
            target = link.resolve()
            if target.exists():
                sources.append((link.name, link))
    for eco, root in sources:
        for rec in _walk(eco, root):
            key = (rec["ecosystem"], rec["name"], rec["type"])
            if key in seen:
                continue
            seen.add(key)
            units.append(rec)
    units.sort(key=lambda r: (r["ecosystem"], r["name"]))
    return units


def _score(rec: dict, tokens: list[str]) -> int:
    name = rec["name"].lower()
    desc = rec["description"].lower()
    trig = rec["triggers"].lower()
    path = rec["path"].lower()
    s = 0
    for tk in tokens:
        if tk in name:
            s += 5
        if tk in trig:
            s += 3
        if tk in desc:
            s += 2
        if tk in path:
            s += 1
    return s


def cmd_find(args):
    tokens = [t.lower() for t in args.query if t.strip()]
    idx = build_index()
    scored = [(r, _score(r, tokens)) for r in idx]
    hits = sorted((p for p in scored if p[1] > 0), key=lambda p: -p[1])
    hits = hits[: args.limit]
    if args.json:
        print(json.dumps([{**r, "score": s} for r, s in hits], indent=2))
        return 0 if hits else 1
    if not hits:
        print(f"No capability across the portal matches: {' '.join(args.query)}")
        return 1
    print(f"╭─ portal-router · {len(hits)} match(es) for '{' '.join(args.query)}' "
          f"across {len({r['ecosystem'] for r, _ in hits})} ecosystem(s)")
    for r, s in hits:
        print(f"│  [{r['ecosystem']:<18}] {r['type']:<9} {r['name']}  (score {s})")
        print(f"│      {r['description'][:110]}")
        print(f"│      ↳ {r['invoke']}")
    print("╰─ load one through the portal:  ~/_arms/arm show <ecosystem> <name>")
    return 0


def cmd_list(args):
    idx = build_index()
    if args.ecosystem:
        idx = [r for r in idx if r["ecosystem"] == args.ecosystem]
    if args.json:
        print(json.dumps(idx, indent=2))
        return 0
    by_eco: dict[str, int] = {}
    for r in idx:
        by_eco[r["ecosystem"]] = by_eco.get(r["ecosystem"], 0) + 1
    print(f"╭─ portal index · {len(idx)} capabilities across {len(by_eco)} ecosystems")
    for eco, n in sorted(by_eco.items()):
        print(f"│  {eco:<20} {n}")
    print("╰─ detail:  ~/_arms/arm list <ecosystem>   ·   ~/_arms/arm find <query>")
    if args.ecosystem:
        for r in idx:
            print(f"   {r['type']:<9} {r['name']}")
    return 0


def cmd_show(args):
    idx = build_index()
    matches = [r for r in idx
               if r["ecosystem"] == args.ecosystem and r["name"] == args.name]
    if not matches:
        # fall back to name-only match across ecosystems
        matches = [r for r in idx if r["name"] == args.name]
    if not matches:
        print(f"Not found in portal: {args.ecosystem}/{args.name}", file=sys.stderr)
        return 1
    rec = matches[0]
    print(f"# {rec['name']}  [{rec['ecosystem']} · {rec['type']}]")
    print(f"# invoke: {rec['invoke']}")
    print(f"# path:   {rec['path']}")
    print("# " + "─" * 60)
    try:
        sys.stdout.write(Path(rec["path"]).read_text(encoding="utf-8", errors="replace"))
    except OSError as e:
        print(f"(could not read unit: {e})", file=sys.stderr)
        return 1
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(prog="portal-router",
                                description="cross-agent capability resolver for _arms")
    sub = p.add_subparsers(dest="cmd", required=True)

    f = sub.add_parser("find", help="rank capabilities matching a query")
    f.add_argument("query", nargs="+")
    f.add_argument("--limit", type=int, default=12)
    f.add_argument("--json", action="store_true")
    f.set_defaults(func=cmd_find)

    l = sub.add_parser("list", help="list the portal index")
    l.add_argument("ecosystem", nargs="?")
    l.add_argument("--json", action="store_true")
    l.set_defaults(func=cmd_list)

    s = sub.add_parser("show", help="load one capability through the portal")
    s.add_argument("ecosystem")
    s.add_argument("name")
    s.set_defaults(func=cmd_show)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
