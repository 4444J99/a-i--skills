# Skill Format Instructions

## SKILL.md File Structure

Every skill must have a `SKILL.md` file as its entry point.

### Required YAML Frontmatter

```yaml
---
name: my-skill-name
description: Clear, task-focused description of what the skill does
---
```

### Optional YAML Fields

```yaml
---
name: my-skill-name
description: What the skill does and when to use it
license: Apache-2.0
allowed-tools:
  - bash
  - edit
  - view
metadata:
  author: Your Name
  version: 1.0.0
  category: development
---
```

## Naming Rules

- **Skill name**: Lowercase, hyphen-separated (kebab-case)
- **Must match directory name** exactly
- Pattern: `[a-z0-9]+(-[a-z0-9]+)*`
- Examples: `algorithmic-art`, `mcp-builder`, `web-artifacts-builder`

## Description Guidelines

- Write as a complete sentence
- Focus on the task or capability
- Be concise but informative
- Good: "Create generative art using p5.js with seeded randomness and particle systems"
- Bad: "Art skill" or "This skill helps you make art and stuff"

## Markdown Body

After the frontmatter, write clear instructions:

1. **Purpose**: What the skill does
2. **Usage**: How an agent should use it
3. **Examples**: Concrete use cases
4. **Resources**: Links to scripts, templates, or references

Keep examples concise and actionable. Prefer ASCII content unless the domain requires otherwise.

## Template Example

```markdown
---
name: template-skill
description: A basic template for creating new skills
---

# Template Skill

This skill provides a starting point for creating new skills.

## Usage

Use this skill when you need to create a new skill from scratch.

## Instructions

1. Copy this template directory
2. Rename to your skill name (kebab-case)
3. Update the frontmatter
4. Add your instructions
5. (Optional) Add scripts and resources

## Examples

**Creating a simple skill:**
- Copy template-skill to my-new-skill
- Edit SKILL.md with your content
- Run refresh script

**Adding scripts:**
- Create scripts/ subdirectory
- Add Python/bash scripts
- Document usage in SKILL.md
```

## Validation

Your skill will be validated by `scripts/validate_skills.py`:

- ✅ SKILL.md exists
- ✅ Valid YAML frontmatter
- ✅ Required fields present (name, description)
- ✅ Name matches directory name
- ✅ Name uses valid characters
- ✅ No duplicate names in collection
