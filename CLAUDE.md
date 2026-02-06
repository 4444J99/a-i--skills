# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is the Anthropic AI Skills repository—a collection of example skills that extend Claude's capabilities. Each skill is a self-contained folder with a `SKILL.md` file containing YAML frontmatter and instructions.

Two skill collections exist:
- **Example skills**: Located in `skills/` directory, organized by category (e.g., `skills/creative/algorithmic-art/`, `skills/development/mcp-builder/`)
- **Document skills**: Reference implementations in `document-skills/` (docx, pdf, pptx, xlsx)

## Repository Structure

```
ai-skills/
├── README.md              # Repository documentation
├── CLAUDE.md              # Claude Code instructions (this file)
├── skills/                # All example skills (101), organized by category
│   ├── creative/          # Art, music, design (13 skills)
│   ├── data/              # Data analysis and ML (6 skills)
│   ├── development/       # Coding patterns and tools (26 skills, incl. bundles)
│   ├── documentation/     # Docs and GitHub profiles (4 skills)
│   ├── education/         # Teaching and learning (4 skills)
│   ├── integrations/      # Third-party integrations (9 skills)
│   ├── knowledge/         # Knowledge management (6 skills)
│   ├── professional/      # Business and career (11 skills)
│   ├── project-management/ # Planning and roadmaps (4 skills)
│   ├── security/          # Security and compliance (6 skills, incl. bundle)
│   ├── specialized/       # Niche domains (6 skills)
│   └── tools/             # Meta-skills and orchestration (6 skills)
├── document-skills/       # Reference document skills (4)
├── docs/                  # Documentation files
│   ├── CHANGELOG.md
│   ├── CONTRIBUTING.md
│   ├── ROADMAP.md
│   ├── api/               # Skill spec, federation schema, activation conditions
│   └── guides/            # Getting started, overrides, core-vs-community
├── agents/                # AI agent definitions
│   └── skill-planner.md   # Skill composition planner
├── commands/              # Slash commands
│   ├── plan-workflow.md   # /plan-workflow - generate skill chains
│   └── skill-health.md   # /skill-health - run health checks
├── scripts/               # Build and validation tools
├── staging/               # Skills in development
├── .build/                # Generated outputs (hidden)
│   ├── collections/       # Skill path lists + tier lists
│   ├── skills-registry.json  # Machine-readable skill metadata
│   ├── skills-lock.json   # Lockfile with SHA-256 hashes
│   ├── claude/            # Claude Code bundles
│   ├── codex/             # Codex bundles
│   ├── direct/            # Direct link directories
│   └── extensions/        # Gemini CLI extensions
└── .claude-plugin/        # Marketplace metadata
```

## Common Commands

```bash
# Refresh collections, registry, lockfile, and generated link directories
python3 scripts/refresh_skill_collections.py
python3 scripts/refresh_skill_collections.py --mode symlink  # Use symlinks instead of copies

# Validate skill frontmatter (run both for full validation)
python3 scripts/validate_skills.py --collection example --unique
python3 scripts/validate_skills.py --collection document --unique

# Verify generated bundles, registry, and lockfile are in sync
python3 scripts/validate_generated_dirs.py

# Run skill health checks (scripts, references, size metrics)
python3 scripts/skill_health_check.py                        # All skills
python3 scripts/skill_health_check.py --skill mcp-builder    # Single skill
python3 scripts/skill_health_check.py --json                 # JSON output

# PR validation report (for CI)
python3 scripts/pr_validation_report.py --base origin/main

# Full release workflow (bumps versions, updates changelog, commits, tags, pushes)
python3 scripts/release.py 1.2.0 \
  --change "Description" \
  --add "New feature" \
  --fix "Bug fix" \
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
description: What it does    # Task-focused sentence (20-600 chars)
license: MIT                 # Required: license type
# Optional semantic fields:
inputs: [source-code]        # What the skill expects
outputs: [test-report]       # What the skill produces
side_effects: [creates-files] # Environment changes
triggers: [user-asks-about-testing] # Activation conditions
complements: [verification-loop]    # Skills that pair well
includes: [skill-a, skill-b]       # Bundle: skills to install together
tier: core                          # Quality tier: core or community
---

# Instructions and content here
```

### Generated Directories (in .build/, managed by refresh script)
- `.build/collections/example-skills.txt` / `document-skills.txt` — skill path lists
- `.build/collections/core-skills.txt` / `community-skills.txt` — tier lists
- `.build/skills-registry.json` — machine-readable skill metadata (all frontmatter + resources)
- `.build/skills-lock.json` — lockfile with SHA-256 hashes per skill
- `.build/direct/example/` / `document/` — direct link directories
- `.build/codex/skills` / `.build/claude/skills` — agent-specific bundles
- `.build/extensions/gemini/*/skills` — Gemini CLI extensions

These are committed artifacts; include refreshed outputs in PRs that change skills. CI validates that generated files are up-to-date (no git diff allowed).

### Version Files (updated during releases)
- `.claude-plugin/marketplace.json` (metadata.version)
- `.build/extensions/gemini/example-skills/gemini-extension.json`
- `.build/extensions/gemini/document-skills/gemini-extension.json`

## Key Guidelines

- Skill `name` in frontmatter must exactly match the directory name
- All skills must have a `license` field (MIT for open skills)
- Skills are organized into category subdirectories; new skills must go in the appropriate category
- Document skills (docx, pdf, pptx, xlsx) are only in `document-skills/`, not in `skills/`
- No repo-wide test suite; run per-skill tests when they exist (e.g., `python3 document-skills/pdf/scripts/check_bounding_boxes_test.py`)
- Update `docs/THIRD_PARTY_NOTICES.md` when adding external assets
- CI includes secret detection for patterns like `sk-`, `ghp_`, `AKIA` in new files
