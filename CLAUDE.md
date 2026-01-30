# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is the Anthropic AI Skills repository—a collection of example skills that extend Claude's capabilities. Each skill is a self-contained folder with a `SKILL.md` file containing YAML frontmatter and instructions.

Two skill collections exist:
- **Example skills**: Top-level directories (e.g., `algorithmic-art/`, `mcp-builder/`)
- **Document skills**: Reference implementations in `document-skills/` (docx, pdf, pptx, xlsx)

## Common Commands

```bash
# Refresh collections and generated link directories after adding/removing skills
python3 scripts/refresh_skill_collections.py

# Validate skill frontmatter (run both for full validation)
python3 scripts/validate_skills.py --collection example --unique
python3 scripts/validate_skills.py --collection document --unique

# Verify generated bundles are in sync
python3 scripts/validate_generated_dirs.py

# Full release workflow (bumps versions, updates changelog, commits, tags, pushes)
python3 scripts/release.py 1.2.0 \
  --change "Description" \
  --add "New feature" \
  --commit --tag --push --release --notes-from-changelog
```

## Architecture

### Skill Structure
```
my-skill/
  SKILL.md          # Required: YAML frontmatter + markdown instructions
  scripts/          # Optional: executable helpers
  references/       # Optional: supporting documentation
  assets/           # Optional: templates, resources
```

### SKILL.md Format
```markdown
---
name: my-skill-name          # Must match folder name, lowercase + hyphens
description: What it does    # Task-focused sentence
---

# Instructions and content here
```

### Generated Directories (managed by refresh script)
- `collections/example-skills.txt` / `collections/document-skills.txt` — skill path lists
- `skills/` / `skills-document/` — link directories
- `.codex/skills` / `.claude/skills` — agent-specific bundles
- `extensions/gemini/*/skills` — Gemini CLI extensions

These are committed artifacts; include refreshed outputs in PRs that change skills.

### Version Files (updated during releases)
- `.claude-plugin/marketplace.json` (metadata.version)
- `extensions/gemini/example-skills/gemini-extension.json`
- `extensions/gemini/document-skills/gemini-extension.json`

## Key Guidelines

- Skill `name` in frontmatter must exactly match the directory name
- Install only one collection at a time to avoid duplicate skill names (docx, pdf, pptx, xlsx exist in both sets)
- No repo-wide test suite; run per-skill tests when they exist (e.g., `python3 document-skills/pdf/scripts/check_bounding_boxes_test.py`)
- Update `THIRD_PARTY_NOTICES.md` when adding external assets
