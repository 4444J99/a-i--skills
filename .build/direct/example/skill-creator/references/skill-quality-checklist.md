# Skill Quality Checklist

Pre-packaging validation checklist for skill authors.

## Metadata Validation

### Frontmatter Required Fields

- [ ] `name` field present and matches directory name exactly
- [ ] `name` uses lowercase letters and hyphens only (e.g., `my-skill-name`)
- [ ] `description` field present and non-empty
- [ ] `license` field present (e.g., `MIT`, `Apache-2.0`, or path to LICENSE file)

### Description Quality

- [ ] Description starts with what the skill does (verb or noun phrase)
- [ ] Description explains when the skill should be triggered
- [ ] Description uses third-person language ("This skill..." not "Use this skill...")
- [ ] Description is specific enough to distinguish from similar skills
- [ ] Description is concise (under 200 characters preferred)

**Good Examples:**

```yaml
description: Generate PDF documents with precise bounding box layouts. This skill should be used when users need programmatic PDF creation with pixel-perfect positioning.

description: Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends Claude's capabilities.
```

**Poor Examples:**

```yaml
# Too vague - doesn't explain when to use
description: Helps with documents.

# Uses second person
description: Use this skill when you need to work with images.

# Too generic - could match too many requests
description: General purpose utility skill.
```

## SKILL.md Content

### Structure

- [ ] Begins with YAML frontmatter delimited by `---`
- [ ] Contains markdown content after frontmatter
- [ ] Organized with clear headings (##, ###)
- [ ] No duplicate information between SKILL.md and references

### Writing Style

- [ ] Uses imperative/infinitive form ("To accomplish X, do Y")
- [ ] Avoids second person ("you should...")
- [ ] Objective, instructional language throughout
- [ ] Procedural steps are numbered or clearly sequenced

### Content Completeness

- [ ] Explains the skill's purpose in opening section
- [ ] Documents when and how to use each bundled resource
- [ ] Provides workflow guidance for common tasks
- [ ] Includes any required setup or prerequisites

## Bundled Resources

### Scripts (`scripts/`)

- [ ] Each script has a clear, descriptive filename
- [ ] Scripts are executable (correct shebang line)
- [ ] Scripts handle errors gracefully
- [ ] Scripts are referenced in SKILL.md with usage instructions
- [ ] No hardcoded paths or credentials
- [ ] Dependencies are documented

**Script Naming Convention:**

```
verb_noun.py       # rotate_pdf.py, validate_skill.py
noun_verb.sh       # image_resize.sh (also acceptable)
```

### References (`references/`)

- [ ] Each reference file has a focused topic
- [ ] Reference files are markdown format
- [ ] Content is not duplicated in SKILL.md
- [ ] Large files (>10k words) have search guidance in SKILL.md
- [ ] Information is organized for quick lookup (tables, lists, code blocks)

### Assets (`assets/`)

- [ ] Assets are organized in logical subdirectories if numerous
- [ ] Template files have clear placeholder markers
- [ ] Image assets are optimized for size
- [ ] Binary files are necessary (not just convenience)
- [ ] Assets are referenced with correct relative paths

## Progressive Disclosure

### Context Efficiency

- [ ] SKILL.md stays under 5,000 words
- [ ] Detailed reference material moved to `references/`
- [ ] Reusable code in `scripts/` rather than inline
- [ ] Templates in `assets/` rather than SKILL.md

### Information Hierarchy

| Level | Content | Load Timing |
|-------|---------|-------------|
| 1. Metadata | name + description | Always loaded |
| 2. SKILL.md | Core workflows, procedures | When skill triggers |
| 3. Resources | Details, templates, code | As needed by Claude |

## Common Issues

### Metadata Problems

| Issue | Fix |
|-------|-----|
| Name mismatch | Rename directory or update frontmatter |
| Missing description | Add task-focused description |
| Vague description | Be specific about trigger conditions |

### Content Problems

| Issue | Fix |
|-------|-----|
| Too long SKILL.md | Move details to references |
| Duplicate info | Keep in one place only |
| Missing workflows | Add step-by-step procedures |
| Inline code blocks | Extract to scripts |

### Resource Problems

| Issue | Fix |
|-------|-----|
| Unused resources | Delete or document their purpose |
| Missing documentation | Add usage notes in SKILL.md |
| Broken paths | Verify relative path accuracy |

## Final Validation

Run the packaging script to perform automated validation:

```bash
scripts/package_skill.py <path/to/skill-folder>
```

The script validates:

1. YAML frontmatter format
2. Required fields presence
3. Naming conventions
4. Directory structure
5. Resource organization

Fix any reported errors before distribution.

## Distribution Readiness

- [ ] All checklist items above are satisfied
- [ ] Skill tested on representative use cases
- [ ] Documentation reviewed for clarity
- [ ] Packaging script runs without errors
- [ ] Zip file created successfully
