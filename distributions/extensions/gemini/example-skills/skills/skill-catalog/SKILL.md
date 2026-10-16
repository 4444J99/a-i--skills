---
name: skill-catalog
description: Doorway to the full skill catalog. Only a few skills stay resident in every session; the rest live on demand. Use when a task might match a specialized skill that is not in the resident list (design, testing, security, writing, data, deployment, teaching, and so on), or when the user names a skill that is not listed. Finds the matching catalog skill and loads its instructions in place.
license: MIT
complexity: beginner
time_to_learn: 5min
tier: core
tags:
  - skill-discovery
  - on-demand-loading
  - context-budget
inputs:
  - task-description
outputs:
  - loaded-skill-instructions
side_effects:
  - reads-filesystem
  - runs-commands
triggers:
  - user-names-an-unlisted-skill
  - task-matches-a-specialized-domain
complements:
  - closeout
---

# Skill Catalog

Agents list every resident skill's name and description on every turn, so the
resident set is kept to the skills that earn it (see
`docs/adr/003-default-on-skill-residency.md` in the skills repository). Every other catalog skill is
installed beside it and loads on demand through this doorway. Nothing is
missing; it is one lookup away.

## Locate the release

The verified release root is printed by the installer:

```bash
python3 "${DOMUS_SKILLS_HOME:-$HOME/.local/share/ai-skills}/current/scripts/skills_install.py" path
```

Call that root `RELEASE`. The on-demand skills live in
`RELEASE/distributions/claude/skills-catalog/<name>/`, and
`RELEASE/distributions/claude/CATALOG.md` indexes them, one line per skill:
name, category, description.

## Find and load a skill

1. Search the index for the task's domain words instead of reading all of it:

   ```bash
   grep -i -E 'accessib|wcag' "$RELEASE/distributions/claude/CATALOG.md"
   ```

   Purpose lists in `RELEASE/distributions/collections/by-purpose/` and
   category lists in `by-category/` narrow a broad domain.
2. Read `RELEASE/distributions/claude/skills-catalog/<name>/SKILL.md` and
   follow it exactly as if the skill had been invoked. Its `scripts/`,
   `references/`, and `assets/` paths are relative to that folder.
3. Tell the user which catalog skill you loaded, so the choice is visible.

If nothing matches, say so and do the task directly; do not stretch an
unrelated skill to fit.

## Promoting a skill to resident

A skill earns residency by use or by a charter naming it. When a catalog skill
keeps being loaded through this doorway, add it to `default_on` in
`config/runtime-catalog.json` of the skills repository with its basis and
evidence, then rebuild the release. `scripts/skill_residency.py usage` reports
which skills recent sessions actually invoked.
