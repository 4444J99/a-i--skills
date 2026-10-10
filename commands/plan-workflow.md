---
name: plan-workflow
description: Generate a skill chain plan for a high-level goal by analyzing the skills registry for input/output compatibility.
---

# /plan-workflow

Generate an ordered skill chain to accomplish a goal.

## Usage

`/plan-workflow <goal description>`

Example: `/plan-workflow Build a secure REST API with tests and deployment`

## Process

1. Resolve and validate the installed release with `python3 scripts/skills_install.py path` (honors `DOMUS_SKILLS_HOME` or XDG defaults). Read `distributions/skills-registry.json` beneath that exact returned directory to load all skill metadata. If no installation exists, run the documented installer first. Do not read a checkout copy as a fallback.
2. Match the goal against skill descriptions, tags, and triggers
3. Build a dependency chain based on input/output compatibility
4. Include complementary skills that enhance the workflow
5. Present the plan as an ordered list with data flow

## Output Format

```
Goal: <user's goal>

Skill Chain:
1. skill-name (category)
   Inputs: what it needs
   Outputs: what it produces
   Purpose: why it's in the chain

2. skill-name (category)
   ...

Data Flow:
  service-requirements -> [api-design-patterns] -> api-specification
  api-specification -> [backend-implementation-patterns] -> backend-code
  ...

Also Consider:
  - complementary-skill: brief description
```

## Notes

- Plans are suggestions; approve or modify before executing
- Use `/skill-health` to check individual skills before running a chain
- Chains are limited to 8 skills for reviewability
- Prefer core-tier skills when multiple options match
