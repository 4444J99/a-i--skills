# Changelog

All notable changes to this repository are documented in this file.
This project follows semantic versioning.

## [1.2.0] - 2026-02-06
### Added
- 7 new optional frontmatter fields: `inputs`, `outputs`, `side_effects`, `triggers`, `complements`, `includes`, `tier`
- Federation schema spec (`docs/api/federation-schema.md`) for third-party skill repositories (v1.1)
- Activation conditions spec (`docs/api/activation-conditions.md`) with 5 trigger types
- Machine-readable skills registry (`scripts/generate_registry.py` → `.build/skills-registry.json`)
- Skill bundles: `fullstack-starter-pack` and `security-essentials-pack`
- MCP skill server (`scripts/mcp-skill-server.py`) with 7 tools (search, info, complement, suggest, plan, categories, bundles)
- PR validation bot (`.github/workflows/pr-comment.yml` + `scripts/pr_validation_report.py`)
- Skill health checks (`scripts/skill_health_check.py`) and `/skill-health` command
- Skill override system via `SKILLS_CUSTOM_DIR` environment variable
- Lockfile for reproducibility (`scripts/generate_lockfile.py` → `.build/skills-lock.json`)
- Core vs community quality tiers with stricter validation for core-tier skills
- Skill planner agent (`agents/skill-planner.md`) for AI-driven skill composition
- `/plan-workflow` command for generating ordered skill chains
- Tier lists: `.build/collections/core-skills.txt` and `community-skills.txt`
- Guides: skill overrides, core vs community

### Changed
- `validate_skills.py`: validates new fields, cross-references includes/complements, stricter core-tier checks
- `refresh_skill_collections.py`: generates tier lists, registry JSON, and lockfile
- `validate_generated_dirs.py`: checks registry and lockfile existence
- 5 exemplar skills updated with new semantic fields (mcp-builder, tdd-workflow, api-design-patterns, canvas-design, security-threat-modeler)
- Skill count: 95 → 101

### Fixed
- Broken references across 16 skills (28 missing reference files added)
- MCP server cache staleness via mtime-based invalidation
- Volatile fields (`generated_at`, `git_commit`) in lockfile/registry causing CI freshness failures
- Skill count discrepancies in CATEGORIES.md
- Duplicate CI workflows consolidated
- Link checker false positives from fenced code blocks
- Missing shebangs on 10 standalone CLI scripts (specstory-guard, pdf)
- Health check false positives for `__init__.py` and test files

## [1.1.0] - 2026-01-30
### Added
- Multi-agent distribution bundles for Claude Code, Codex, and Gemini CLI (copy-based skill directories).
- Validation tooling and CI workflow to keep skill metadata and collections in sync.
- Contributor guidance for collections, install flows, and release steps.

### Changed
- Marketplace and Gemini extension versions to 1.1.0.
- Release workflow to include regenerated bundles and committed artifacts.

## [1.1.1] - 2026-01-30
### Changed
- Link to `CHANGELOG.md` from `README.md`.
- Bump marketplace and Gemini extension versions to 1.1.1.
