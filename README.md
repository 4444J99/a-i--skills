[![ORGAN-IV: Taxis](https://img.shields.io/badge/ORGAN--IV-Taxis-e65100?style=flat-square)](https://github.com/organvm-iv-taxis)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue?style=flat-square)](./LICENSE)
[![Skills](https://img.shields.io/badge/Skills-101-4CAF50?style=flat-square)](./docs/CATEGORIES.md)

# a-i--skills

**A composable skill framework for AI agent orchestration** -- 101 production-ready skill modules spanning creative, technical, enterprise, and governance domains, organized into a federated registry with multi-agent runtime support.

> Part of [ORGAN-IV: Taxis](https://github.com/organvm-iv-taxis) -- the orchestration and governance layer of the [ORGAN system](https://github.com/meta-organvm).

---

## Table of Contents

- [Product Overview](#product-overview)
- [Why This Exists](#why-this-exists)
- [Orchestration Philosophy](#orchestration-philosophy)
- [Technical Architecture](#technical-architecture)
- [Installation and Quick Start](#installation-and-quick-start)
- [Skill Catalog](#skill-catalog)
- [Skill Specification Format](#skill-specification-format)
- [Federation Protocol](#federation-protocol)
- [Tooling and Scripts](#tooling-and-scripts)
- [Cross-Organ Integration](#cross-organ-integration)
- [Related Work](#related-work)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

---

## Product Overview

`a-i--skills` is a structured repository of 101 AI agent skills -- self-contained instruction modules that teach large language models how to perform specialized tasks in a repeatable, composable way. Each skill is a directory containing a `SKILL.md` file with YAML frontmatter (metadata for discovery and activation) and Markdown content (the actual instructions an agent follows).

The repository serves three distinct functions:

1. **Skill Library** -- A browsable catalog of 101 skills across 12 categories, from algorithmic art generation to security threat modeling, each with standardized metadata, optional helper scripts, reference documentation, and asset templates.

2. **Orchestration Infrastructure** -- Python tooling for skill validation, registry generation, health checking, and multi-agent bundle distribution. A built-in MCP (Model Context Protocol) server enables runtime skill discovery and planning.

3. **Federation Specification** -- A published protocol that allows third-party skill repositories to be discovered, validated, and consumed by any compatible agent, enabling a decentralized ecosystem of interoperable skill providers.

The skills themselves range from beginner-level single-file instructions to advanced multi-file modules with executable scripts, OOXML schema references, and comprehensive troubleshooting guides. Four document-processing skills (DOCX, PDF, PPTX, XLSX) demonstrate production-grade complexity -- these are the same skills that power Claude's native document creation capabilities.

### Key Metrics

| Dimension | Value |
|-----------|-------|
| Total skills | 101 (97 example + 4 document) |
| Skill categories | 12 |
| Multi-agent runtimes supported | 4 (Claude Code, Codex, Gemini CLI, Claude API) |
| Total files | ~3,745 |
| Repository size | ~5.2 MB |
| Federation schema version | 1.1 (stable) |
| Skill spec version | Current |

---

## Why This Exists

AI agents are increasingly capable of executing complex, multi-step tasks, but their effectiveness depends heavily on the quality of instruction they receive. A generic prompt produces generic output. A well-structured skill -- with domain-specific vocabulary, explicit constraints, worked examples, and validation criteria -- produces expert-level output repeatedly.

The challenge is organizational: how do you manage dozens or hundreds of such skills across multiple agent runtimes, ensure they remain valid as specifications evolve, and enable external contributors to build compatible skills without centralized coordination?

This repository answers that question with three architectural decisions:

- **Convention over configuration.** Every skill follows the same directory structure and frontmatter schema. No build system, no dependency manager, no runtime framework. A skill is a folder with a Markdown file.
- **Validation over trust.** Python scripts enforce naming conventions, frontmatter completeness, link integrity, and cross-reference accuracy. CI runs these checks on every pull request.
- **Federation over centralization.** The published federation schema means anyone can build a compatible skill repository. Agents discover skills by scanning for `SKILL.md` files, not by consulting a central registry.

---

## Orchestration Philosophy

Within the ORGAN system, ORGAN-IV (Taxis) is the governance and orchestration layer. Its repositories do not create content (that is ORGAN-II, Poiesis) and do not sell products (that is ORGAN-III, Ergon). Instead, ORGAN-IV provides the infrastructure that makes the other organs composable: routing rules, governance protocols, capability registries, and workflow coordination.

`a-i--skills` embodies this philosophy in three ways:

### Composability Through Standardization

Every skill in the catalog follows an identical structural contract: a `SKILL.md` with required `name` and `description` frontmatter fields, optional metadata for complexity, prerequisites, triggers, inputs, outputs, and side effects. This standardization means any orchestration layer -- whether a human selecting skills manually, an agent reasoning about which skills to activate, or a CI pipeline validating skill quality -- can interact with every skill through the same interface.

The `complements` field explicitly declares which skills pair well together, enabling multi-skill workflows. The `includes` field creates bundles -- meta-skills that compose multiple skills into a single installable unit. The `triggers` field provides activation conditions (file-type matching, user intent detection, project context detection) that allow agents to autonomously select relevant skills without explicit human instruction.

### Registry as Governance

The `generate_registry.py` script compiles all skill frontmatter into a single `skills-registry.json` file -- a machine-readable manifest of every skill's name, description, category, collection, path, license, complexity, and relationships. This registry serves as a governance artifact: it is the authoritative enumeration of what skills exist, what they claim to do, and how they relate to each other.

The `validate_skills.py` script enforces invariants that no individual skill can violate: names must match directory names, descriptions must fall within length bounds, complexity values must come from a fixed vocabulary, side-effect declarations must use recognized terms. This is governance through automated enforcement rather than manual review.

### Multi-Runtime Distribution

The `refresh_skill_collections.py` script generates agent-specific bundle directories for Claude Code (`.build/claude/skills/`), Codex (`.build/codex/skills/`), and Gemini CLI (`.build/extensions/gemini/`). Each bundle uses the native discovery mechanism of its target runtime: Claude Code uses a plugin marketplace, Codex uses a `.codex/skills/` directory, Gemini uses extensions. The same source skills are distributed through four different channels without any skill-level modification.

This is orchestration in its purest form: a single source of truth, multiple distribution targets, automated synchronization, and zero manual intervention per skill per runtime.

---

## Technical Architecture

### Directory Structure

```
a-i--skills/
├── skills/                           # 97 example skills, organized by category
│   ├── creative/                     # 13 skills (art, music, design, narrative)
│   ├── data/                         # 6 skills (pipelines, ML, analytics)
│   ├── development/                  # 26 skills (code quality, testing, infra)
│   ├── documentation/                # 4 skills (READMEs, profiles, standards)
│   ├── education/                    # 4 skills (tutoring, curriculum, feedback)
│   ├── integrations/                 # 9 skills (MCP, OAuth, webhooks, SpecStory)
│   ├── knowledge/                    # 6 skills (graphs, architecture, research)
│   ├── professional/                 # 11 skills (branding, CVs, proposals)
│   ├── project-management/           # 4 skills (roadmaps, requirements, orchestration)
│   ├── security/                     # 6 skills (threat modeling, compliance, incident response)
│   ├── specialized/                  # 6 skills (blockchain, gaming, AR, fine-tuning)
│   └── tools/                        # 6 skills (agent swarms, skill creation, meta-tools)
│
├── document-skills/                  # 4 production-grade document skills
│   ├── docx/                         # Word document creation and editing
│   ├── pdf/                          # PDF manipulation and form handling
│   ├── pptx/                         # PowerPoint presentation generation
│   └── xlsx/                         # Excel spreadsheet processing
│
├── scripts/                          # Python tooling
│   ├── validate_skills.py            # Frontmatter and naming validation
│   ├── generate_registry.py          # Build skills-registry.json
│   ├── refresh_skill_collections.py  # Multi-runtime bundle generation
│   ├── skill_health_check.py         # Reference and script validation
│   ├── mcp-skill-server.py           # MCP server for runtime skill discovery
│   ├── validate_generated_dirs.py    # Verify bundle synchronization
│   ├── generate_lockfile.py          # Dependency lockfile generation
│   ├── release.py                    # Release management
│   ├── pr_validation_report.py       # PR validation reporting
│   └── skill_lib.py                  # Shared frontmatter parsing utilities
│
├── docs/                             # Documentation
│   ├── CATEGORIES.md                 # Full skill catalog by category
│   ├── CONTRIBUTING.md               # Contribution guidelines
│   ├── CHANGELOG.md                  # Release history
│   ├── AGENTS.md                     # Agent-specific repository guidelines
│   ├── ROADMAP.md                    # Development roadmap
│   ├── architecture/                 # Repository structure documentation
│   ├── api/                          # Skill spec, federation schema, activation conditions
│   └── guides/                       # Getting started, creating skills, contributing
│
├── .build/                           # Generated multi-runtime bundles
│   ├── claude/skills/                # Claude Code plugin bundle
│   ├── codex/skills/                 # Codex agent bundle
│   ├── direct/                       # Direct-access bundle
│   ├── extensions/gemini/            # Gemini CLI extensions
│   └── skills-registry.json          # Machine-readable skill manifest
│
├── .claude-plugin/                   # Claude Code plugin marketplace metadata
│   └── marketplace.json              # Plugin definitions (2 collections)
│
└── .github/                          # CI/CD and templates
    ├── workflows/validate.yml        # Skill validation on PR
    ├── ISSUE_TEMPLATE/               # Bug report, feature request, new skill
    └── PULL_REQUEST_TEMPLATE.md      # PR template
```

### Skill Anatomy

Every skill follows this structure:

```
skill-name/
├── SKILL.md           # Required: YAML frontmatter + Markdown instructions
├── scripts/           # Optional: executable Python helpers
├── references/        # Optional: supporting documentation
├── assets/            # Optional: templates, fonts, images
└── LICENSE.txt        # Optional: skill-specific license
```

The `SKILL.md` frontmatter schema:

```yaml
---
name: skill-name                      # Required: must match directory name
description: What this skill does.    # Required: 20-600 chars, task-focused
license: MIT                          # Optional: license identifier
complexity: intermediate              # Optional: beginner | intermediate | advanced
time_to_learn: 30min                  # Optional: 5min | 30min | 1hour | multi-hour
prerequisites: [other-skill]          # Optional: skills to learn first
tags: [keyword1, keyword2]            # Optional: discovery keywords
inputs: [source-code]                 # Optional: expected input types
outputs: [test-report]                # Optional: produced output types
side_effects: [creates-files]         # Optional: environment changes
triggers:                             # Optional: activation conditions
  - user-asks-about-testing
  - file-type:*.test.ts
complements: [related-skill]          # Optional: pairs well with
includes: [skill-a, skill-b]          # Optional: bundle composition
tier: core                            # Optional: core | community
---
```

### Activation Conditions

The `triggers` field supports five condition types that enable autonomous skill selection:

| Trigger Type | Syntax | Example |
|-------------|--------|---------|
| User intent | `user-asks-about-<topic>` | `user-asks-about-api-design` |
| Project file | `project-has-<filename>` | `project-has-jest-config-js` |
| File type | `file-type:<glob>` | `file-type:*.test.ts` |
| Command context | `command:<name>` | `command:test` |
| Reasoning context | `context:<label>` | `context:debugging` |

Triggers use OR logic -- any single match makes the skill relevant. Agents treat triggers as advisory hints, not mandatory activations.

### MCP Server

The `mcp-skill-server.py` script provides a Model Context Protocol server for runtime skill discovery:

```bash
pip install mcp
python3 scripts/mcp-skill-server.py
```

The server exposes tools for searching skills by keyword, browsing by category, and planning multi-skill workflows. It loads from `skills-registry.json` when available and falls back to scanning `SKILL.md` files directly.

---

## Installation and Quick Start

### Claude Code (Plugin Marketplace)

```bash
# Register the marketplace
/plugin marketplace add anthropics/skills

# Install example skills
/plugin install example-skills@anthropic-agent-skills

# Install document skills
/plugin install document-skills@anthropic-agent-skills
```

After installation, reference skills naturally in conversation: "Use the PDF skill to extract form fields from invoice.pdf."

### Codex (OpenAI)

```bash
# Clone the repository
git clone https://github.com/organvm-iv-taxis/a-i--skills.git
cd a-i--skills

# Regenerate bundles
python3 scripts/refresh_skill_collections.py

# Skills are available in .build/codex/skills/
```

### Gemini CLI

```bash
# Install example skills extension
gemini extensions install ./.build/extensions/gemini/example-skills

# Install document skills extension
gemini extensions install ./.build/extensions/gemini/document-skills
```

### Claude API

Skills can be uploaded and managed via the [Skills API](https://docs.claude.com/en/api/skills-guide#creating-a-skill). Each skill's `SKILL.md` content is passed directly as the skill definition.

### Local Development

```bash
# Clone
git clone https://github.com/organvm-iv-taxis/a-i--skills.git
cd a-i--skills

# Validate all skills
python3 scripts/validate_skills.py --collection example --unique
python3 scripts/validate_skills.py --collection document --unique

# Generate registry
python3 scripts/generate_registry.py

# Regenerate multi-runtime bundles
python3 scripts/refresh_skill_collections.py

# Verify bundles are in sync
python3 scripts/validate_generated_dirs.py

# Run skill health checks
python3 scripts/skill_health_check.py
```

---

## Skill Catalog

The 101 skills are organized into 12 categories. Each category below lists skill count and representative examples.

### Creative and Content (13 skills)

Generative art, music composition, narrative design, and visual media.

| Skill | Description |
|-------|-------------|
| `algorithmic-art` | Generative art with p5.js, seeded randomness, flow fields |
| `generative-music-composer` | Algorithmic music composition and synthesis |
| `canvas-design` | Visual art in PNG and PDF using design philosophies |
| `three-js-interactive-builder` | Interactive 3D experiences with Three.js |
| `creative-writing-craft` | Creative writing techniques and storytelling craft |
| `interactive-theatre-designer` | Interactive theatrical experience design |
| `movement-notation-systems` | Dance and movement notation systems |

### Development (26 skills)

Code quality, testing, infrastructure, frontend, backend, and tooling.

| Skill | Description |
|-------|-------------|
| `tdd-workflow` | Test-driven development process and methodology |
| `api-design-patterns` | RESTful API design patterns and best practices |
| `mcp-builder` | Model Context Protocol server construction |
| `deployment-cicd` | CI/CD pipeline design and deployment automation |
| `rust-systems-design` | Rust systems programming patterns |
| `webapp-testing` | Web application testing with Playwright |
| `verification-loop` | Comprehensive QA verification workflows |

### Data (6 skills)

Pipelines, machine learning, analytics, and time-series analysis.

| Skill | Description |
|-------|-------------|
| `data-pipeline-architect` | Data pipeline design and orchestration |
| `ml-experiment-tracker` | Machine learning experiment tracking |
| `sql-query-optimizer` | SQL query optimization and performance tuning |
| `time-series-analyst` | Time-series data analysis and forecasting |

### Security (6 skills)

Threat modeling, compliance, incident response, and contract analysis.

| Skill | Description |
|-------|-------------|
| `security-threat-modeler` | Systematic threat modeling and risk assessment |
| `gdpr-compliance-check` | GDPR compliance validation and remediation |
| `incident-response-commander` | Incident response coordination and playbooks |
| `contract-risk-analyzer` | Legal contract risk analysis |

### Professional (11 skills)

Career development, branding, proposals, and business communication.

| Skill | Description |
|-------|-------------|
| `brand-guidelines` | Brand identity and guideline application |
| `cv-resume-builder` | Professional resume and CV generation |
| `grant-proposal-writer` | Grant and proposal writing assistance |
| `portfolio-presentation` | Portfolio design and presentation creation |

### Knowledge (6 skills)

Knowledge graphs, research synthesis, and second-brain architecture.

| Skill | Description |
|-------|-------------|
| `knowledge-graph-builder` | Knowledge graph construction and querying |
| `recursive-systems-architect` | Recursive systems design and governance |
| `research-synthesis-workflow` | Research synthesis and literature review |
| `second-brain-librarian` | Personal knowledge management systems |

### Project Management (4 skills)

Roadmap strategy, requirements design, and orchestration workflows.

| Skill | Description |
|-------|-------------|
| `github-roadmap-strategist` | GitHub-based roadmap planning and execution |
| `product-requirements-designer` | Product requirements document generation |
| `project-orchestration` | Multi-project coordination and tracking |

### Education (4 skills)

Curriculum design, Socratic tutoring, and feedback pedagogy.

### Integrations (9 skills)

MCP patterns, OAuth flows, webhooks, and SpecStory tooling.

### Documentation (4 skills)

GitHub profiles, repository curation, and standards enforcement.

### Specialized (6 skills)

Blockchain, DeFi, game mechanics, AR experiences, and local LLM fine-tuning.

### Tools (6 skills)

Agent swarm orchestration, skill creation, and ontological renaming.

For the complete catalog with descriptions for every skill, see [`docs/CATEGORIES.md`](./docs/CATEGORIES.md).

---

## Skill Specification Format

The skill specification defines the contract between skill authors and consuming agents. Key design decisions:

- **Name-directory coupling.** The `name` frontmatter field must exactly match the containing directory name. This eliminates ambiguity in skill resolution and ensures filesystem paths serve as stable identifiers.

- **Description as discovery surface.** The `description` field (20-600 characters) is the primary mechanism for agent-side skill selection. Descriptions are written as task-focused phrases ("Guide for creating...") rather than agent-focused directives ("Use this to...").

- **Structured side-effect declarations.** The `side_effects` field uses a controlled vocabulary (`creates-files`, `modifies-git`, `runs-commands`, `network-access`, `installs-packages`, `reads-filesystem`) that enables agents to assess risk before activation.

- **Tiered quality model.** The `tier` field distinguishes `core` skills (curated, reviewed, maintained) from `community` skills (contributed, validated but not guaranteed).

Full specification: [`docs/api/skill-spec.md`](./docs/api/skill-spec.md).

---

## Federation Protocol

The federation schema (v1.1, stable) allows any repository to host compatible skills:

```
my-repo/
  skills/
    my-skill/
      SKILL.md          # Required: follows the standard frontmatter schema
      scripts/           # Optional
      references/        # Optional
      assets/            # Optional
```

A federated repository is valid if:

1. It contains one or more directories with `SKILL.md` files.
2. Each `SKILL.md` has valid YAML frontmatter with `name` and `description`.
3. Each `name` matches its containing directory name.
4. All names follow the `^[a-z0-9-]+$` pattern.

Agents discover skills by recursively scanning for `SKILL.md` files -- no central registry consultation required. This makes the protocol fully decentralized: any Git repository, any hosting provider, any organizational structure.

Full specification: [`docs/api/federation-schema.md`](./docs/api/federation-schema.md).

---

## Tooling and Scripts

All tooling lives in `scripts/` and uses only the Python standard library plus the optional `mcp` package for the MCP server.

| Script | Purpose |
|--------|---------|
| `validate_skills.py` | Enforce frontmatter schema, naming conventions, description length, side-effect vocabulary, and broken link detection |
| `generate_registry.py` | Compile all skill frontmatter into `skills-registry.json` |
| `refresh_skill_collections.py` | Generate runtime-specific bundle directories for Claude, Codex, and Gemini |
| `validate_generated_dirs.py` | Verify bundle directories are synchronized with source skills |
| `skill_health_check.py` | Validate internal references and script integrity per skill |
| `mcp-skill-server.py` | MCP server for runtime skill discovery and planning |
| `generate_lockfile.py` | Generate dependency lockfiles for reproducible builds |
| `pr_validation_report.py` | Generate validation reports for pull requests |
| `release.py` | Release management automation |
| `skill_lib.py` | Shared library for YAML frontmatter parsing and skill directory discovery |

### CI/CD Pipeline

The `.github/workflows/validate.yml` workflow runs on every pull request:

1. Validates all skill frontmatter against the schema.
2. Checks for broken internal links and missing references.
3. Verifies generated bundle directories are in sync.
4. Ensures unique skill names across both collections.

---

## Cross-Organ Integration

Within the eight-organ ORGAN system, `a-i--skills` serves as a capability registry that multiple organs consume:

### ORGAN-I (Theoria) provides theoretical foundations

The epistemological and recursive-systems theory developed in [ORGAN-I](https://github.com/organvm-i-theoria) informs the skill specification design. The activation-conditions model (trigger types, OR-logic composition, advisory semantics) draws on the recursive governance patterns formalized in ORGAN-I's theoretical corpus. Skills like `recursive-systems-architect` and `knowledge-architecture` directly encode ORGAN-I concepts into actionable agent instructions.

### ORGAN-III (Ergon) consumes skills for product delivery

Product repositories in [ORGAN-III](https://github.com/organvm-iii-ergon) use skills as development accelerators. The `deployment-cicd`, `testing-patterns`, `api-design-patterns`, and `webapp-testing` skills are directly applicable to ORGAN-III's SaaS, B2B, and B2C codebases. The multi-runtime distribution system ensures ORGAN-III developers can access skills regardless of which AI coding assistant they use.

### ORGAN-IV (Taxis) siblings

Other ORGAN-IV repositories complement `a-i--skills`:

- **[agentic-titan](https://github.com/organvm-iv-taxis/agentic-titan)** -- Multi-agent orchestration framework that can consume skills as capability modules.
- **[petasum-super-petasum](https://github.com/organvm-iv-taxis/petasum-super-petasum)** -- Governance protocol layer that the skill validation pipeline implements.
- **[universal-node-network](https://github.com/organvm-iv-taxis/universal-node-network)** -- Node graph infrastructure that the federation protocol extends into distributed skill networks.

### No back-edges

Following the ORGAN dependency invariant, ORGAN-IV infrastructure is consumed by downstream organs but never depends on them. Skills reference no ORGAN-II or ORGAN-III code. The dependency graph flows strictly: I (theory) informs IV (orchestration) which serves II (creation) and III (commerce).

---

## Related Work

- [Anthropic Agent Skills Blog Post](https://anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) -- Engineering rationale for the skills framework.
- [Claude Skills Documentation](https://support.claude.com/en/articles/12512176-what-are-skills) -- Official user documentation.
- [Model Context Protocol](https://modelcontextprotocol.io/) -- The protocol used by the MCP skill server.
- [Notion Skills for Claude](https://www.notion.so/notiondevs/Notion-Skills-for-Claude-28da4445d27180c7af1df7d8615723d0) -- Partner skill implementation demonstrating federation in practice.

---

## Contributing

Contributions are welcome. See [`docs/CONTRIBUTING.md`](./docs/CONTRIBUTING.md) for the full guide.

The short version:

1. Create a new skill directory under the appropriate category in `skills/`.
2. Write a `SKILL.md` with valid frontmatter (`name`, `description` are required).
3. Run the validation suite:
   ```bash
   python3 scripts/validate_skills.py --collection example --unique
   python3 scripts/refresh_skill_collections.py
   python3 scripts/validate_generated_dirs.py
   ```
4. Submit a pull request with the skill and regenerated bundle directories.

Skill names must be lowercase kebab-case (`^[a-z0-9-]+$`), descriptions must be 20-600 characters and task-focused, and the `name` field must match the directory name exactly.

---

## License

This repository is licensed under the [Apache License 2.0](./LICENSE).

Individual skills may carry their own license declarations in the `license` frontmatter field or a `LICENSE.txt` file within their directory.

The document skills in `document-skills/` are source-available reference implementations, not open source. They are provided for educational and development reference purposes.

---

## Author

**[@4444j99](https://github.com/4444j99)** -- ORGAN system architect and maintainer.

This repository is part of [ORGAN-IV: Taxis](https://github.com/organvm-iv-taxis), the orchestration and governance organ of the [ORGAN system](https://github.com/meta-organvm). For the complete system architecture, see the [meta-organvm](https://github.com/meta-organvm) umbrella organization.
