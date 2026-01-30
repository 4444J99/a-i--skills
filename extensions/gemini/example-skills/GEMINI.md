# Example Skills Extension

This extension exposes the top-level skills from this repository.

## What is included
- Each skill directory is linked under `skills/`.
- Skill instructions live in `SKILL.md` with YAML frontmatter.

## Updating
If skills are added or removed, regenerate the links:

```bash
python3 scripts/refresh_skill_collections.py
```
