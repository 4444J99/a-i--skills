# Core vs Community Tiers

Skills are organized into two quality tiers, following a pattern similar to LangChain's `langchain-core` / `langchain-community` split. Tiers set expectations for quality, completeness, and maintenance.

## Tiers

### Core

Core skills are curated and maintained by the repository team. They meet a higher quality bar and are recommended as starting points.

**Requirements for core tier:**

- `complexity` field set (`beginner`, `intermediate`, or `advanced`)
- `time_to_learn` field set (`5min`, `30min`, `1hour`, or `multi-hour`)
- `tags` field with at least one keyword
- `triggers` field with at least one activation condition
- Description between 20 and 600 characters
- All referenced files (`references/`, `assets/`) must exist

**Example frontmatter:**

```yaml
---
name: tdd-workflow
description: Guide test-driven development with red-green-refactor cycles, test doubles, and coverage strategies.
license: MIT
tier: core
complexity: intermediate
time_to_learn: 30min
tags: [testing, tdd, workflow, development]
triggers: [test-driven, tdd, write tests first]
---
```

### Community

Community skills are contributed by the community and pass standard validation. They may not have all optional fields populated.

**Requirements for community tier:**

- Valid `name` matching directory name
- `description` between 20 and 600 characters
- Valid frontmatter format

Community is the default tier. Skills without an explicit `tier` field are treated as community.

## The `tier` Field

Add the `tier` field to your skill's YAML frontmatter:

```yaml
---
name: my-skill
description: What this skill does.
license: MIT
tier: community
---
```

Valid values are `core` and `community`. The validator rejects any other value.

## Validation

The validator applies stricter rules to core skills. Running:

```bash
python3 scripts/validate_skills.py --collection example --unique
```

For core-tier skills, the validator checks that `complexity`, `time_to_learn`, `tags`, and `triggers` are all present and valid. Community skills only need to pass the standard checks.

## Promotion Path

Community skills can be promoted to core after review:

1. **Fill in required fields.** Add `complexity`, `time_to_learn`, `tags`, and `triggers` to the frontmatter.
2. **Verify references.** Ensure all referenced files exist and links are valid (`--check-links`).
3. **Set the tier.** Change `tier: community` to `tier: core`.
4. **Open a pull request.** The reviewer will confirm the skill meets core quality standards.
5. **Pass validation.** The CI pipeline applies core-tier rules automatically.

## How Tiers Appear

- **Search results:** Core skills are prioritized when multiple skills match a query.
- **Registry listings:** Core skills are marked with a `[core]` badge.
- **Documentation:** The categories page groups skills by tier within each category.

## Summary

| Aspect | Core | Community |
|--------|------|-----------|
| `tier` value | `core` | `community` (or omitted) |
| Required fields | name, description, complexity, time_to_learn, tags, triggers* | name, description |
| Maintained by | Repository team | Contributors |
| Promotion | N/A | Submit PR with all required fields |
| Validation | Strict | Standard |

\* Bundle skills (those with an `includes` field) are exempt from the `triggers` requirement.

## See Also

- [Skill Specification](../api/skill-spec.md) -- All frontmatter fields
- [Creating Skills](creating-skills.md) -- How to write a new skill
- [Skill Overrides](skill-overrides.md) -- Custom skill override system
