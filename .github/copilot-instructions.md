# AI Skills Repository - GitHub Copilot Instructions

This repository contains a collection of Claude skills that extend AI agent capabilities. Each skill is self-contained and documented through a `SKILL.md` file with YAML frontmatter.

## Repository Purpose

The AI Skills repository hosts specialized instructions, scripts, and resources for AI agents (Claude, Codex, Gemini CLI). Skills enable agents to perform tasks ranging from creative work to technical documentation and code analysis.

## Key Principles

- **Skill-First Architecture**: Every skill must have a `SKILL.md` file with valid YAML frontmatter
- **Self-Contained Design**: Each skill directory is independent with its own resources
- **Generated Artifacts**: Link directories and collections are committed and maintained by scripts
- **Dual Collections**: Example skills (root) and document skills (document-skills/)

## Code Assistance Guidelines

### When Creating or Modifying Skills

1. **Naming Convention**: Use lowercase kebab-case matching the directory name
2. **Required Frontmatter**:
   ```yaml
   ---
   name: skill-name
   description: Concise task-focused sentence
   ---
   ```
3. **Optional Fields**: `license`, `allowed-tools`, `metadata`
4. **After Changes**: Run `python3 scripts/refresh_skill_collections.py`

### When Writing Python Scripts

- Keep scripts self-contained within skill's `scripts/` directory
- Include simple smoke tests or usage examples
- Reference environment variables for credentials (never commit secrets)

### When Updating Documentation

- Update `README.md` if adding/removing skills from curated lists
- Update `THIRD_PARTY_NOTICES.md` when adding external assets
- Keep examples concise and actionable

### Common Workflows

**Add a new skill:**
```bash
# Create directory and SKILL.md with frontmatter
# Add any scripts or assets
python3 scripts/refresh_skill_collections.py
python3 scripts/validate_skills.py --collection example --unique
```

**Validate changes:**
```bash
python3 scripts/validate_skills.py --collection example --unique
python3 scripts/validate_skills.py --collection document --unique
python3 scripts/validate_generated_dirs.py
```

**Release workflow:**
```bash
python3 scripts/release.py VERSION --change "Description" --commit --tag --push
```

## Directory Structure Context

- `skills/`, `.codex/skills`, `.claude/skills`, `extensions/gemini/*/skills` - Generated bundles
- `collections/` - Auto-generated skill path lists
- `document-skills/` - Reference implementations for complex file formats
- `scripts/` - Maintenance and validation scripts

## Important Constraints

- Only install one collection at a time (avoid duplicate skill names)
- No repo-wide test suite; run per-skill tests when they exist
- Skill `name` must exactly match directory name
- Generated directories are committed artifacts

## Commit Message Style

Use short, imperative messages with PR references:
```
Add accessibility-patterns skill (#42)
Update SKILL.md validation script
Clarify installation steps in README.md (#20)
```
