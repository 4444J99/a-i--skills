# Repository Structure

This document explains the organization of the AI Skills repository.

## Directory Layout

```
ai-skills/
├── README.md                          # Main documentation
├── CONTRIBUTING.md                    # Contribution guidelines
├── CATEGORIES.md                      # Skill categorization
├── CHANGELOG.md                       # Version history
├── LICENSE                           # Apache 2.0 license
├── THIRD_PARTY_NOTICES.md           # Third-party attributions
│
├── .github/                          # GitHub-specific files
│   ├── workflows/                    # CI/CD workflows
│   │   └── validate.yml             # Skill validation on PR
│   ├── ISSUE_TEMPLATE/              # Issue templates
│   │   ├── bug_report.md
│   │   ├── feature_request.md
│   │   └── new_skill.md
│   ├── PULL_REQUEST_TEMPLATE.md     # PR template
│   ├── copilot-instructions.md      # Copilot-specific guidance
│   └── instructions/                # Additional instructions
│
├── docs/                            # Documentation
│   ├── architecture/                # Architecture docs
│   │   ├── repository-structure.md  # This file
│   │   └── skill-format.md          # Skill format specification
│   ├── guides/                      # User guides
│   │   ├── getting-started.md       # Getting started guide
│   │   ├── creating-skills.md       # How to create skills
│   │   └── contributing.md          # Detailed contribution guide
│   └── api/                         # API/Specification docs
│       └── skill-spec.md            # Detailed skill spec
│
├── collections/                     # Generated and categorized collections
│   ├── example-skills.txt           # All example skills
│   ├── by-category/                 # Skills by category
│   │   ├── creative.txt
│   │   ├── professional.txt
│   │   ├── development.txt
│   │   └── ...
│   ├── by-purpose/                  # Skills by purpose
│   │   ├── code-quality.txt
│   │   ├── testing.txt
│   │   └── ...
│   └── by-complexity/               # Skills by complexity level
│       ├── beginner.txt
│       ├── intermediate.txt
│       └── advanced.txt
│
├── scripts/                         # Maintenance scripts
│   ├── refresh_skill_collections.py # Regenerate collections
│   ├── validate_skills.py           # Validate skill format
│   ├── validate_generated_dirs.py   # Validate generated dirs
│   └── release.py                   # Release management
│
├── [85 skill directories]           # Individual skills at root
│   ├── skill-name/
│   │   ├── SKILL.md                 # Required: skill definition
│   │   ├── LICENSE.txt              # Optional: specific license
│   │   ├── README.md                # Optional: additional docs
│   │   ├── scripts/                 # Optional: helper scripts
│   │   ├── assets/                  # Optional: templates, configs
│   │   └── references/              # Optional: reference docs
│
├── .claude/                         # Generated: Claude agent bundle
│   └── skills/                      # Symlinks to all skills
├── .codex/                          # Generated: Codex agent bundle
│   └── skills/                      # Symlinks to all skills
├── .claude-plugin/                  # Plugin metadata
│   └── marketplace.json             # Plugin marketplace config
├── extensions/                      # Generated: Gemini extensions
│   └── gemini/
│       └── example-skills/
└── skills/                          # Generated: links to example skills
```

## Generated vs Source Files

### Source Files (Manually Maintained)
- Individual skill directories at repository root
- Documentation in `docs/`
- Scripts in `scripts/`
- GitHub templates in `.github/`
- Root-level markdown files

### Generated Files (Auto-Generated)
These are created by `scripts/refresh_skill_collections.py`:
- `.claude/skills/*` - Claude agent skill links
- `.codex/skills/*` - Codex agent skill links
- `extensions/gemini/*/skills/*` - Gemini extension skills
- `skills/*` - Example skill links
- `collections/*.txt` - Collection files

**Important**: Always run `python3 scripts/refresh_skill_collections.py` after modifying skills!

## Why Flat Structure?

The repository uses a flat structure (skills at root) for several reasons:

1. **Backward Compatibility**: Existing installations expect flat structure
2. **Simplicity**: Easy to navigate and find skills
3. **Tool Compatibility**: Works with multiple agent systems
4. **Convention**: Follows patterns from major skill repositories

## Virtual Organization

Instead of physical directories, skills are organized virtually through:

1. **Categories**: Skills grouped by domain (see `CATEGORIES.md`)
2. **Collections**: Text files listing related skills (see `collections/`)
3. **Metadata**: YAML frontmatter in `SKILL.md` for programmatic access

This approach provides organization without breaking compatibility.

## Adding New Skills

1. Create directory at repository root: `new-skill-name/`
2. Add `SKILL.md` with valid frontmatter
3. Run `python3 scripts/refresh_skill_collections.py`
4. Skills are automatically categorized via metadata

## Updating Generated Files

After any skill modification:

```bash
# Regenerate all collections and agent bundles
python3 scripts/refresh_skill_collections.py

# Validate changes
python3 scripts/validate_skills.py --collection example --unique
python3 scripts/validate_generated_dirs.py
```

## Collection System

### By Category (`collections/by-category/`)
Groups skills by domain: creative, professional, development, etc.

### By Purpose (`collections/by-purpose/`)
Groups skills by use case: code-quality, testing, security, etc.

### By Complexity (`collections/by-complexity/`)
Groups skills by difficulty: beginner, intermediate, advanced

## References

- See `docs/guides/creating-skills.md` for skill creation guide
- See `docs/api/skill-spec.md` for skill format specification
- See `CONTRIBUTING.md` for contribution workflow
