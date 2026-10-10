# Verified skills installation

## Install from a checkout

Requirements: Git and Python 3.11 or later on macOS or Linux. Building and
installing the skills uses only Python's standard library. Individual skills
can require additional tools when invoked; the installer does not run their
workflows, install their dependencies, contact an LMS, or generate a letter.

```sh
git clone https://github.com/4444J99/a-i--skills.git
cd a-i--skills
python3 scripts/skills_install.py install
python3 scripts/skills_install.py path
```

The default installation prefix is `${XDG_DATA_HOME:-$HOME/.local/share}/ai-skills`.
Set `DOMUS_SKILLS_HOME` or pass `install --prefix /chosen/location` to select
another prefix. Pass the same prefix to `path` and `rollback`, or keep the
environment variable set for runtime consumers.

The installed release contains 167 main catalog definitions and 11 plugin
definitions. Claude, Codex, direct, and Gemini catalog bundles contain the 167
main catalog skills. The two complete plugin folders preserve their 11 skills,
shared references, agents, and manifests. They remain plugins rather than being
flattened into a directory that would break their relative resource paths.

## Connect a runtime

Use the stable `current` path for long-lived runtime registrations. Resolve it
once to a specific release when reading several files as one operation.

| Consumer | Verified installation path |
|---|---|
| Claude skills directory | `current/distributions/claude/skills` |
| Codex skills directory | `current/distributions/codex/skills` |
| Direct catalog | `current/distributions/direct/example` |
| Gemini catalog extension | `current/distributions/extensions/gemini/example-skills` |
| Claude plugin marketplace | `current/` (contains `.claude-plugin/marketplace.json`) |
| Complete plugins | `current/plugins/` |
| Registry | `current/distributions/skills-registry.json` |
| Lockfile | `current/distributions/skills-lock.json` |

For a new, empty runtime setup, point its skills directory at the corresponding
installed bundle. Preserve any existing personal skills before changing its
directory. The coordinated `domus-genoma` integration manages Claude's pointer,
the registry consumers, native Gemini extension registration, and Cowork's
separate writable copies. Its update transaction verifies the release before
changing consumers and rolls back its own changes on failure.

In Claude Code, add the absolute path to the installed `current` directory as a
local marketplace, then install `example-skills@a-i-skills`. The optional plugins
are `coliseum-from-grain@a-i-skills` and
`pentaphase-structural-architect@a-i-skills`. Plugin-manager caches can require
their own refresh; a local source registration alone does not prove a running
session has reloaded its cache.

Gemini's native local development link follows the stable installation path:

```sh
gemini extensions link --consent "$DOMUS_SKILLS_HOME/current/distributions/extensions/gemini/example-skills"
```

Set `DOMUS_SKILLS_HOME` to the selected prefix before using that example.
Domus calls the native CLI and verifies its registration. It preserves unrelated
extensions and treats a name collision as an error. Cowork's copy contains an
ownership manifest; local additions are retained, and edits to a managed file
stop an update until reconciled. Successful removals delete only previously
managed copies whose content still matches the recorded installation.

The optional MCP server still requires the separate `mcp` package. Run
`scripts/mcp-skill-server.py` after installing this catalog. It reads a verified
active release, refreshes its registry cache when `current` changes, and reports
installed absolute paths. `SKILLS_CUSTOM_DIR` remains an explicit local override.

## External skill managers

External directories and installers can discover this catalog. Their install
result can differ from the complete verified release: a generic installer may
copy an individual plugin skill without its enclosing package's shared files.
The October 10 [marketplace evaluation](marketplace-evaluation.md) records an
isolated probe of Vercel discovery and installation APIs in which a standalone
skill kept its supporting files, while all four of a plugin skill's links to
shared references failed to resolve despite a successful installation result.
Keep complete plugins registered through the verified local marketplace.
Verify a selected standalone skill's dependencies before
using another manager, and keep that manager outside the Domus-managed roots.

## Update and recover

Update a clean source checkout, then install again:

```sh
git pull --ff-only
python3 scripts/skills_install.py install
```

The builder copies canonical skill folders, complete plugins, runtime commands,
build scripts, configuration, and license notices to a staging directory. It
validates all admitted definitions, regenerates the marketplace, collections,
four catalog bundles, registry, lockfile, and Gemini descriptors, and validates
their exact membership, contents, metadata, and executable bits. Missing or
failed generators fail the build. A lowercase entrypoint in admitted source is
an error; it cannot silently disappear from the catalog.

A complete file manifest records the release's source commit when available,
its canonical-input digest, version, definition counts, every payload file's
SHA-256 and executable mode, and a deterministic release identity. This detects
drift and corruption; it is not a publisher signature. The build never uses a
checkout's generated `distributions/` or marketplace as input.

Only a validated release is moved into `releases/<build-id>`. A filesystem lock
serializes installation, and replacing the `current` symlink activates the
release in one operation. `previous` retains the preceding release. Existing
releases are read-only, updates do not edit their files, and the installer does
not garbage-collect them. A failed generation or validation leaves both
installation pointers unchanged. Disk use therefore grows with distinct
retained releases; remove old releases only after confirming no consumer needs
them.

An explicit rollback requires the release you intend to undo:

```sh
skills_release=$(python3 scripts/skills_install.py path)
python3 scripts/skills_install.py rollback --expected-current "$skills_release"
```

If a different installation has become current, rollback refuses to undo it.
If there was no preceding installation, rollback removes only the matching
current pointer; the release itself remains retained. Automation can also pass
`install --expected-current /exact/release` or `--expected-current none` to reject
an update based on an outdated starting state.

## Build and install an artifact

Build without activating anything:

```sh
python3 scripts/skills_install.py build --output out/release
python3 scripts/skills_install.py validate --release out/release
python3 scripts/skills_install.py pack --release out/release --output out/ai-skills.tar.gz
```

`build --output` requires an absent destination. A partially generated directory
is never published there. Packaging produces a deterministic tarball and the
adjacent `ai-skills.tar.gz.sha256` checksum. The tarball contains `ai-skills/`
with everything needed to validate and install the release without its original
checkout. After verifying the downloaded checksum and extracting the archive:

```sh
python3 ai-skills/scripts/skills_install.py validate --release ai-skills
python3 ai-skills/scripts/skills_install.py install --release ai-skills
```

The **Skills installation** workflow runs the acceptance tests and publishes
the validated tarball and checksum as an artifact on pull requests and main.
When a new GitHub release is published, the same workflow requires its tag to
match the canonical plugin version, then attaches the validated assets without
overwriting existing assets. The historical `v1.2.0` release has no package
assets; this change does not turn that old tag into a release of the new code.

## Acceptance and retirement gates

Run the executable acceptance sequence:

```sh
python3 -m pip install -r requirements-dev.txt
python3 -m pytest -v tests/test_skills_install.py
```

The tests use the real catalog in an isolated source copy with no generated
output. They install it, change a canonical skill and add a temporary skill,
install the update, remove the temporary skill and verify stale copies vanish,
then force a registry generator failure. The active release and its previous
release remain valid and usable after the source copy is removed. Additional
checks cover absent generators, malformed/corrupt outputs, execution-mode
changes, unmanaged installation paths, activation failure, guarded rollback,
and reproducible artifact installation without a checkout.

These checks exercise the filesystem installation contract. On October 9, 2026,
Claude Code 2.1.296 accepted the generated local marketplace and installed all
three plugin packages in isolated settings. Gemini CLI 0.63.0 linked the verified
extension at the stable `current` path and discovered all 167 catalog skills.
The [acceptance evidence](evidence/2026-10-09-skills-installation.json) records
the candidate manifest used for these checks.
They do not exercise a signed-in model invocation or a running Cowork application.
Domus's fixture tests establish copy and adapter recovery behavior; a personal
host smoke test remains necessary before retiring its previous runtime setup.

This implementation addresses the install/use gap in [issue #23](https://github.com/4444J99/a-i--skills/issues/23).
Issue completion still needs the merged/default-branch result and available
release evidence. Tracked distributions and private snapshots remain until the
coordinated installer and Domus changes are accepted. Snapshot retirement also
requires file-level reconciliation and a working replacement for `_agent`'s
snapshot-dependent scanner and package references.
