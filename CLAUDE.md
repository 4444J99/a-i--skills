# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is Anthony Padavano's (4444J99) agent skills repository—a catalog of skills that extend AI coding agents' capabilities. Each skill is a self-contained folder with a `SKILL.md` file containing YAML frontmatter and instructions.

Skill locations:
- **Catalog skills**: Located in `skills/` directory, organized by category (e.g., `skills/creative/algorithmic-art/`, `skills/development/mcp-builder/`). 165 skills across 12 categories.
- **Plugin skills**: Claude Code plugins under `plugins/` (11 skills).

## Repository Structure

```
ai-skills/
├── README.md              # Repository documentation
├── CLAUDE.md              # Claude Code instructions (this file)
├── skills/                # All example skills (142), organized by category
│   ├── creative/          # Art, music, design (15 skills)
│   ├── data/              # Data analysis and ML (8 skills)
│   ├── development/       # Coding patterns and tools (47 skills, incl. bundles)
│   ├── documentation/     # Docs and GitHub profiles (7 skills)
│   ├── education/         # Teaching and learning (4 skills)
│   ├── integrations/      # Third-party integrations (14 skills)
│   ├── knowledge/         # Knowledge management (7 skills)
│   ├── professional/      # Business and career (12 skills)
│   ├── project-management/ # Planning and roadmaps (6 skills)
│   ├── security/          # Security and compliance (6 skills, incl. bundle)
│   ├── specialized/       # Niche domains (6 skills)
│   └── tools/             # Meta-skills and orchestration (11 skills)
├── plugins/               # Claude Code plugins (11 skills)
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
├── distributions/         # Committed canonical outputs
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

# Validate skill frontmatter
python3 scripts/validate_skills.py --collection example --unique --check-links

# Run the tooling test suite
python3 -m pytest

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

### Generated Directories (in distributions/, managed by refresh script)
- `distributions/collections/example-skills.txt` — skill path list
- `distributions/collections/core-skills.txt` / `community-skills.txt` — tier lists
- `distributions/skills-registry.json` — machine-readable skill metadata (all frontmatter + resources)
- `distributions/skills-lock.json` — lockfile with SHA-256 hashes per skill
- `distributions/direct/example/` — direct link directory
- `distributions/codex/skills` / `distributions/claude/skills` — agent-specific bundles
- `distributions/extensions/gemini/*/skills` — Gemini CLI extensions

These are committed artifacts; include refreshed outputs in PRs that change skills. CI validates that generated files are up-to-date (no git diff allowed).

### Version Files (updated during releases)
- `.claude-plugin/marketplace.json` (metadata.version)
- `distributions/extensions/gemini/example-skills/gemini-extension.json`

## Key Guidelines

- Skill `name` in frontmatter must exactly match the directory name
- All skills must have a `license` field (MIT for open skills)
- Skills are organized into category subdirectories; new skills must go in the appropriate category
- Only redistributable (open-licensed) skills belong here; Anthropic's document skills (docx, pdf, pptx, xlsx) are all-rights-reserved and must not be re-added
- Repo-wide tests live in `tests/` (`python3 -m pytest`); CI runs them
- Update `docs/THIRD_PARTY_NOTICES.md` when adding external assets
- CI includes secret detection for patterns like `sk-`, `ghp_`, `AKIA` in new files

## GitHub MCP Usage Policy

**IMPORTANT:** This repo exists locally. ALWAYS use local filesystem tools (Read, Grep, Glob) to read files — NEVER use `mcp__github__get_file_contents` or similar GitHub MCP tools for content that exists on disk. GitHub MCP tools trigger API content filtering errors on repos with security-domain content (security skills contain terms like STRIDE, XSS, SQL injection that trip the output filter).

Use GitHub MCP tools ONLY for operations that require the GitHub API:
- Setting repo description/topics (`update_pull_request`, etc.)
- Creating/managing issues and PRs
- Managing labels, releases, branches

For these API-only operations, always set `minimal_output: true` where the parameter is available.

<!-- ORGANVM:AUTO:START -->
## System Context (auto-generated — do not edit)

**Organ:** ORGAN-IV (Orchestration) | **Tier:** standard | **Status:** GRADUATED
**Org:** `organvm-iv-taxis` | **Repo:** `a-i--skills`

### Edges
- *No inter-repo edges declared in seed.yaml*

### Siblings in Orchestration
`orchestration-start-here`, `petasum-super-petasum`, `universal-node-network`, `.github`, `agentic-titan`, `agent--claude-smith`, `tool-interaction-design`, `system-governance-framework`, `reverse-engine-recursive-run`, `collective-persona-operations`, `contrib--adenhq-hive`, `contrib--ipqwery-ipapi-py`, `contrib--primeinc-github-stars`, `contrib--temporal-sdk-python`, `contrib--dbt-mcp` ... and 6 more

### Governance
- *Standard ORGANVM governance applies*

*Last synced: 2026-05-23T00:26:31Z*

## Active Handoff Protocol

If `.conductor/active-handoff.md` exists, **READ IT FIRST** before doing any work.
It contains constraints, locked files, conventions, and completed work from the
originating agent. You MUST honor all constraints listed there.

If the handoff says "CROSS-VERIFICATION REQUIRED", your self-assessment will
NOT be trusted. A different agent will verify your output against these constraints.

## Session Review Protocol

At the end of each session that produces or modifies files:
1. Run `organvm session review --latest` to get a session summary
2. Check for unimplemented plans: `organvm session plans --project .`
3. Export significant sessions: `organvm session export <id> --slug <slug>`
4. Run `organvm prompts distill --dry-run` to detect uncovered operational patterns

Transcripts are on-demand (never committed):
- `organvm session transcript <id>` — conversation summary
- `organvm session transcript <id> --unabridged` — full audit trail
- `organvm session prompts <id>` — human prompts only


## System Library

Plans: 269 indexed | Chains: 5 available | SOPs: 8 active
Discover: `organvm plans search <query>` | `organvm chains list` | `organvm sop lifecycle`
Library: `/Users/4jp/Code/organvm/praxis-perpetua/library`


## Active Directives

| Scope | Phase | Name | Description |
|-------|-------|------|-------------|
| system | any | atomic-clock | The Atomic Clock |
| system | any | execution-sequence | Execution Sequence |
| system | any | multi-agent-dispatch | Multi-Agent Dispatch |
| system | any | session-handoff-avalanche | Session Handoff Avalanche |
| system | any | system-loops | System Loops |
| system | any | prompting-standards | Prompting Standards |
| system | any | background-task-resilience | background-task-resilience |
| system | any | context-window-conservation | context-window-conservation |
| system | any | session-self-critique | session-self-critique |
| system | any | the-descent-protocol | the-descent-protocol |
| system | any | the-membrane-protocol | the-membrane-protocol |
| system | any | theory-to-concrete-gate | theory-to-concrete-gate |
| system | any | triangulation-protocol | triangulation-protocol |
| unknown | any | SOP-001_REPOSITORY_SEEDING | SOP-001: Repository Seeding Procedure |
| unknown | any | SOP-002_WORKSPACE_AUDIT | SOP-002: Comprehensive Workspace Audit Procedure |
| unknown | any | SOP-003_GOVERNANCE_PROMOTION | SOP-003: Governance Promotion Procedure |
| unknown | any | SOP-004_SEED_YAML_VALIDATION | SOP-004: Seed.yaml Validation Procedure |
| unknown | any | SOP-005_ORGAN_CLASSIFICATION | SOP-005: Organ Classification Procedure |
| unknown | any | SOP-006_PHASE_TRANSITION | SOP-006: Phase Transition Procedure |
| unknown | any | SOP-007_CLAUDE_MD_GENERATION | SOP-007: CLAUDE.md Generation Procedure |
| unknown | any | SOP-008_DEPENDENCY_MAPPING | SOP-008: Dependency Mapping Procedure |
| unknown | any | SOP-009_IRF_ASSIGNMENT | SOP-009: IRF Assignment Procedure |
| unknown | any | SOP-010_MULTI_REPO_ORCHESTRATION | SOP-010: Multi-Repo Orchestration Procedure |

Linked skills: SOP-TRIADIC-REVIEW-PROTOCOL, cicd-resilience-and-recovery, continuous-learning-agent, evaluation-to-growth, genesis-dna, multi-agent-workforce-planner, promotion-and-state-transitions, quality-gate-baseline-calibration, repo-onboarding-and-habitat-creation, session-self-critique, structural-integrity-audit, the-membrane-protocol, triple-reference


**Prompting (Anthropic)**: context 200K tokens, format: XML tags, thinking: extended thinking (budget_tokens)


## Atomization Pipeline

Run `organvm atoms pipeline --write && organvm atoms fanout --write` to generate task queue.


## System Density (auto-generated)

AMMOI: 25% | Edges: 0 | Tensions: 0 | Clusters: 0 | Adv: 27 | Events(24h): 37975
Structure: 8 organs / 148 repos / 1654 components (depth 17) | Inference: 0% | Organs: META-ORGANVM:63%, ORGAN-I:53%, ORGAN-II:48%, ORGAN-III:54% +5 more
Last pulse: 2026-05-23T00:26:28 | Δ24h: n/a | Δ7d: n/a


## Dialect Identity (Trivium)

**Dialect:** GOVERNANCE_LOGIC | **Classical Parallel:** Rhetoric | **Translation Role:** The Meta-Logic — governance rules ARE propositions

Strongest translations: I (formal), V (structural), META (structural)

Scan: `organvm trivium scan IV <OTHER>` | Matrix: `organvm trivium matrix` | Synthesize: `organvm trivium synthesize`


## Logos Documentation Layer

**Status:** ACTIVE | **Symmetry:** 0.5 (DREAM)

Nature demands a documentation counterpart. This formation maintains its narrative record in `docs/logos/`.

### The Tetradic Counterpart
- **[Telos (Idealized Form)](../docs/logos/telos.md)** — The dream and theoretical grounding.
- **[Pragma (Concrete State)](../docs/logos/pragma.md)** — The honest account of what exists.
- **[Praxis (Remediation Plan)](../docs/logos/praxis.md)** — The attack vectors for evolution.
- **[Receptio (Reception)](../docs/logos/receptio.md)** — The account of the constructed polis.

### Alchemical I/O
- **[Source & Transmutation](../docs/logos/alchemical-io.md)** — Narrative of inputs, process, and returns.



*Compliance: Record exists without implementation.*

<!-- ORGANVM:AUTO:END -->



















## ⚡ Conductor OS Integration
This repository is a managed component of the ORGANVM meta-workspace.
- **Orchestration:** Use `conductor patch` for system status and work queue.
- **Lifecycle:** Follow the `FRAME -> SHAPE -> BUILD -> PROVE` workflow.
- **Governance:** Promotions are managed via `conductor wip promote`.
- **Intelligence:** Conductor MCP tools are available for routing and mission synthesis.