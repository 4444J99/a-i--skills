# ADR 003: Default-on skill residency for the Claude bundle

- Status: Proposed
- Date: 2026-10-16

## Context

Claude Code (and the other runtimes the Domus connector links this bundle
into: Codex, Gemini CLI, OpenCode) puts every discovered skill's name and
description into resident context on every turn. The Claude bundle shipped
all 167 catalog skills, so each session paid for the whole catalog.

Measured on the host on 2026-10-16 with `scripts/skill_residency.py budget --live`:

| Root | Skills | Listing chars | Est. tokens (chars/4) |
|------|-------:|--------------:|----------------------:|
| `$CLAUDE_CONFIG_DIR/skills` (connector links into this release) | 168 | 51,371 | 12,843 |
| `~/.claude/skills` (resolves to the same directory) | 168 | 51,371 | 12,843 |

The second row is a duplicate. `CLAUDE_CONFIG_DIR` now points at the Limen
runtime root, so Claude Code no longer treats `~/.claude` as its own config
directory. It treats `~/.claude/skills` as a project skill directory scoped
to the home directory and lists every skill again as `Users/4jp:<name>`, with
a longer per-entry suffix. That symlink is owned by the Domus chezmoi source
and is removed there, not here.

Usage over every Claude session on disk (104 sessions,
`scripts/skill_residency.py usage --sessions 300 --catalog distributions/claude/skills`):
the only catalog skill ever invoked was `closeout` (60 sessions). Everything
else that was used (`verify`, `doctor`, `insights`, `schedule`,
`artifact-design`, `ship`, `vendor-insights`, `code-review`, `init`) is a
Claude Code built-in or a Limen project-scoped skill, not part of this
catalog.

## Decision

Partition the Claude bundle by an authored membership list.

- `config/runtime-catalog.json` gains `default_on`: the admission rule and,
  per resident skill, its `basis` (`usage`, `charter`, `structural`) and the
  evidence for it. This list is the single source of truth.
- `scripts/refresh_skill_collections.py` writes the resident skills to
  `distributions/claude/skills` and every other catalog skill to
  `distributions/claude/skills-catalog`, plus a one-line-per-skill index at
  `distributions/claude/CATALOG.md`. Each skill is copied once per runtime;
  nothing is duplicated. Codex, Gemini, and the direct directory are
  unchanged.
- A new resident skill, `skill-catalog`, is the doorway: it locates the
  release, searches `CATALOG.md`, and loads the chosen
  `skills-catalog/<name>/SKILL.md` in place. The full catalog stays one skill
  call away.
- `scripts/validate_generated_dirs.py` checks each bundle against its planned
  membership, so a skill in the wrong half fails validation.
- Removing `default_on` restores the full Claude bundle and retires the
  marker-owned `skills-catalog` directory and its index.

### Admission rule

A catalog skill is resident only if at least one holds:

1. **usage**: invoked in at least one of the host's last 50 Claude sessions,
   as reported by `scripts/skill_residency.py usage`;
2. **charter**: a governing charter (the Tier-0 `CLAUDE.md`, or a governed
   repository's `CLAUDE.md`/`AGENTS.md`) names it as a procedure to follow;
3. **structural**: it is the doorway to the on-demand catalog.

Initial members: `closeout` (usage and charter), `voice-enforcement` (charter),
`skill-catalog` (structural). A usage-basis skill that drops to zero uses in
the window and has no charter reference leaves on the next change to the list.

## Alternatives rejected

- **`skillOverrides` generated into the chezmoi settings template.** Claude
  only; the four other runtimes the connector serves keep the full listing.
  It also splits truth across two repositories (catalog here, the override
  list in Domus) and keeps 167 links in every runtime root just to hide them.
- **A Claude plugin that is off by default.** The marketplace plugin already
  exists, but enablement is Claude-only, plugin skills are namespaced, and a
  plugin copy would be a second copy of the catalog beside the bundle.

## Consequences

- Resident listing for this bundle drops from 167 skills / 50,795 chars
  (~12,699 tokens) to 3 skills / 1,164 chars (~291 tokens). With the Domus
  duplicate root removed, the per-session listing falls from about 25,700
  tokens to under 500.
- Every runtime that links `current/distributions/claude/skills` gets the
  smaller set without any connector change. Links a connector already created
  for skills that are now on demand stay until that connector's own undo or
  reapply runs; this repository does not edit runtime roots.
- Promoting a skill is a one-entry change to `default_on` with its evidence,
  followed by a release build.

## Decision 2: skill roots on the host

Claude Code must discover each skill through exactly one root:
`$CLAUDE_CONFIG_DIR/skills`. Two other candidates were considered.

- **`~/.claude/skills` stops being a skills root now.** Its chezmoi source
  (`private_dot_claude/symlink_skills.tmpl`) is dead. `.claude/**` has been in
  Domus `.chezmoiignore` since #427, so the live link was created out of band
  and chezmoi can neither manage nor remove it (ignored paths are never acted
  on by `.chezmoiremove`). The source deletion lands in
  4444J99/domus-genoma-private#443. The live link is removed once on the host
  with `rm ~/.claude/skills`, which deletes only the link.
- **`~/.claude` itself is not retired yet.** It is the `legacy-home` symlink,
  and about 70 consumers still read or write it by hard-coded path (inventory
  below). Several of those writers produce live state there today. Retiring it
  first requires moving those consumers onto one resolver
  (`$CLAUDE_CONFIG_DIR`, or Limen's `harness_paths` / `agent_config_paths`).
- **`~/.agents/skills` is not a Claude root.** Claude Code does not read it,
  and nothing on Domus main bridges it into `$CLAUDE_CONFIG_DIR/skills`.
  Claude currently gets the 22 agent-neutral #431 skills only as the 22 files
  in `$CLAUDE_CONFIG_DIR/commands/*.md`. Those files must not be removed until
  a bridge links each `~/.agents/skills/<name>` into
  `$CLAUDE_CONFIG_DIR/skills`. That bridge belongs in the Domus connector
  that already owns runtime-root links (`domus-agent-skills`, Domus #435/#436),
  as a second source beside this bundle. They are commands without long
  descriptions, so their resident cost is small, and they stay default-on.

### What still reads or writes `~/.claude` (2026-10-16 inventory)

Read-only sweep of `~/.local/bin`, `~/.local/lib`, the live runtime settings
and hooks, Domus source, Limen release source, LaunchAgents, zsh startup and
other agents' configs. "Honors" means it resolves `$CLAUDE_CONFIG_DIR` first.

| Area | Consumers (examples) | Access | Honors |
|------|----------------------|--------|--------|
| Memory sync | `domus-memory-sync` | reads projects/*/memory, plans | yes, but exits 78 when the config dir is not `~/.claude` (see below) |
| Memory readers | Limen `memoria.py`, `covenant.py`, `evocator.py`, `session-orient.py`, `substrate-check` | read `projects/*/memory` | no |
| Session readers | Limen `session_sources.py`, `corpus-feed.py`, `quicken.py`, `vendor-insights.py` (partial), `claude-workflow-guard.py` (partial) | read `projects/*.jsonl` | mostly no |
| Live hooks writing legacy | live `settings.json` fleetview digest, `chezmoi-source-lock.sh` (locks), `insights-capture.sh` (usage-data) | write | no |
| Hook/settings tooling | `substrate-check`, `check-agent-hooks-drift`, `resolve-audit`, `process-audit-daily.sh`, Limen `heal-hook-drift.sh` (writes hooks), `heal-hook-wiring.py`, `armed-valve-audit.py`, `dialogs-silenced.sh` | read/write `settings.json`, `hooks/` | no |
| Plans | `plans-index`, `build-unified-plan-index`, `sync-plans-to-session-meta`, `inject-session-id`, Limen `plans-lifecycle-audit.py` (partial) | read/write `plans/` | no; Limen `harness_paths.py` and `prompt_sources.py` do |
| Session scratch | `session-tldr-*`, `thread-*`, `memdiag`, `sysdiag`, `scheduled-task-audit-bookend`, `insights-list/diff/drift`, `housekeeping-lint` | write | no; `insights-snapshot` does |
| Skills | `domus` doctor `critical_links`, `~/.local/lib/domus_skills.py` `prepare_claude` | read `skills` | no; `domus-agent-skills` does |
| Charter readers | `agent-surface-healthcheck`, `constitution-budget`, Limen `operating_system_health.py` | read `CLAUDE.md` | no |
| MCP state | `resolve-audit`, `resolve-bootstrap` (writes), Limen `mcp-auth-verify.py` | `~/.claude.json`, auth cache | no; Limen `agent_config_paths.py` does |
| Tests | Limen `cli/tests` (35 files), `scripts/tests` (8), Domus `test_agent_runtime_layout.py` | fixtures | n/a |

No LaunchAgent, zsh startup file, Codex, Cursor, VS Code or Gemini config reads
`~/.claude`.

Two defects found on the way, outside this change:

- `domus-memory-sync` refuses to run (exit 78) whenever the config dir is not
  `~/.claude`, and the live hooks call it with `2>/dev/null; true`, so memory
  sync has been silently off since the relocation (errors logged in
  `~/.local/state/domus/memory-sync.log`).
- The instructions name `pretooluse-guard-dispatch.sh` as the hard-deny
  layer, but the live settings do not reference it yet; the converged runtime
  adapter expects it only after the runtime settings are applied, so the
  guard is off until that apply happens.
