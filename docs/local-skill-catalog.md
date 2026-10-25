# Local skill consolidation

The curated catalog and a machine's installed skills are different inventories.
Use `scripts/local_skill_catalog.py` to assemble a private, deduplicated snapshot
of explicitly named local stores without changing the stores themselves.

This complements `skills_install.py`, which builds and installs admitted catalog
releases. A local snapshot does not admit its contents into the public catalog,
grant a license, activate a plugin, or prove cross-agent execution compatibility.

## Sources

Create a private JSON array with one entry per source root:

```json
[
  {"id": "shared", "path": "/absolute/path/to/shared/skills", "kind": "installed"},
  {"id": "runtime", "path": "/absolute/path/to/agent-runtime", "kind": "runtime"},
  {"id": "project", "path": "/absolute/path/to/project/.claude/skills", "kind": "repo", "working_directory": "/absolute/path/to/project"}
]
```

Include current and legacy runtime roots explicitly where both still contain
skills. Label caches and worktrees accurately; presence on disk is not proof of
installation. Keep the roots, private catalog, and copied third-party packages
outside public Git history. Do not scan session databases or conversation stores.

Use `"kind": "runtime"` for agent runtime roots: that kind prunes directories
named `transcripts`, `projects`, and `logs` during discovery. Other kinds retain
those directory names, so they must point only at intended skill collections,
not a broad agent home or conversation store. Pruning these names is not a
general privacy classifier; choose the narrowest source roots that contain the
skills you intend to catalog.

Each source is a collection root: a `SKILL.md` directly in that root is ignored.
Source IDs, paths, and kinds must be nonempty strings. Builds use a private
sibling staging directory and publish with one rename. Failed publication leaves
the destination available for retry; an uncatchable process termination may
leave a hidden staging directory, which does not block a fresh attempt.

Build into a new destination outside every source root:

```sh
python3 scripts/local_skill_catalog.py --sources /private/roots.json --output /private/consolidated-skills
```

The catalog preserves source occurrences, names and descriptions, working
directories, whole-package hashes, exact duplicate groups, and divergent variants.
Objects contain one verified physical copy per distinct eligible package.
Identical `SKILL.md` text alone is insufficient to deduplicate a package: scripts,
references, assets, relative paths, and executable bits participate in identity.
Packages with unsupported links or special files remain visible for review.

Query occurrences, source roots, and review events without executing a skill.
Search warns and exits with status 2 when catalog coverage is incomplete:

```sh
python3 scripts/local_skill_catalog.py --catalog /private/consolidated-skills/catalog.json --find insights
```

`--max-file-bytes` limits each package file (default 64 MiB). The separate
`--max-catalog-bytes` limit bounds the aggregate `catalog.json` during both
publication and reads (default 256 MiB). If the catalog exceeds that bound,
the staged build is discarded and the requested output is not published. Use
the same catalog bound when building, searching, and verifying a larger catalog.
An inaccessible source is recorded as incomplete without discarding eligible
packages collected from other sources.

## Insights

Search warns and exits 2 when catalog coverage is incomplete, including when no
matches are found. Verification separately reports retained-object integrity and
catalog completeness. Directory enumeration applies entry and time bounds before
sorting; index metadata is rendered as inert text.

Claude Code's `/insights` is a built-in command rather than a separately installed
plugin. It analyzes local Claude sessions. See the publisher's
[usage-pattern documentation](https://code.claude.com/docs/en/costs#analyze-your-usage-patterns).

If an existing `vendor-insights` skill is found, retain its repository context.
For example, a skill invoking `scripts/vendor-insights.py` needs that owning
repository as its working directory and the companion scripts in place. Copying
the entrypoint does not make those dependencies portable. Prefer the existing
implementation to creating another report engine.

## Housekeeping boundaries

Consolidation removes redundant physical copies from the generated snapshot only.
It does not delete, replace, disable, or move vendor caches, synced skill copies,
active plugin packages, repository sources, or user state. Distinct versions and
same-name variants remain separate; never choose a winner from a timestamp alone.

Before a later live cutover, resolve each consumer's source owner and effective
runtime path, validate dependencies and supported activation, and preserve a
recoverable previous configuration. Managed configuration must change through its
owning source. A missing pointer target is a finding, not permission to replace a
different active store. Incomplete scans and review-only entries must remain
visible in acceptance evidence.

Run the scoped tests with:

```sh
python3 -m unittest discover -s tests -p test_local_skill_catalog.py
```
