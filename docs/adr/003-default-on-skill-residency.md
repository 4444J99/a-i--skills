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
