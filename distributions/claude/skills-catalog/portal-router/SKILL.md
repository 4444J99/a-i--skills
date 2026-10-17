---
name: portal-router
description: Resolve and load any agent capability across the whole fleet from one place. Given an intent, finds the matching skill, command, or agent across Claude, Codex, Gemini, .agents, a-i--skills, OpenCode, and OpenClaw — then loads it through a single portal. Use for cross-agent skill discovery, "which agent has a skill for X", capability routing, or "find a skill that does Y" when capabilities are spread across multiple agent ecosystems.
license: MIT
governance_phases: [frame, build]
governance_norm_group: repo-hygiene
organ_affinity: [organ-iv]
triggers: [cross-agent-skill-discovery, capability-routing, find-a-skill, which-agent-has, portal-resolve]
complements: [agent-swarm-orchestrator, multi-agent-workforce-planner, cross-agent-handoff]
---

# portal-router — cross-agent capability resolution

When capabilities are spread across many agent ecosystems (Claude, Codex, Gemini,
OpenCode, OpenClaw, a shared `.agents` pool, a skills distribution), the expensive
question is no longer "how do I do X" but **"which of my agents already has a skill
for X, and how do I load it?"** `portal-router` answers that from one place.

It treats every ecosystem as a capability source, normalizes their heterogeneous
unit shapes into one record, ranks matches against an intent, and loads the chosen
unit. It is the skill an orchestrator reaches for *before* authoring a new skill —
to check whether the fleet already owns the capability.

## When to use

- "Which agent has a skill for PDF extraction / k8s / data cleaning?"
- "Find me a capability that does Y" — across all agents, not just the current one.
- Before forging a new skill: confirm the fleet doesn't already have one.
- Routing a task to whichever agent owns the right tool.

## The load-path

The reference implementation is the operator's `~/_arms/arm` portal (the `_arms`
cross-agent skill ecosystem). It exposes:

```sh
arm find <query…>        # rank capabilities across ALL ecosystems by relevance
arm list [ecosystem]     # the portal index (computed live; never stale)
arm show <eco> <name>    # LOAD one capability through the portal (prints its body)
arm status               # portal health
```

Example — find a capability regardless of which agent owns it, then load it:

```sh
arm find pdf extraction
arm show claude pdf-processing      # capability loaded through the portal into context
```

## How it resolves (the engine)

`references/resolve.py` (stdlib-only Python — no dependencies) is the portable
engine. It:

1. Discovers every ecosystem's skill home (following symlinks — `find -L` /
   `followlinks=True`; the mirror entries are symlinks, and without following them
   the portal reads as empty — the single load-bearing detail).
2. Normalizes heterogeneous units — Claude/Codex/Gemini `SKILL.md` dirs with YAML
   frontmatter, OpenCode flat command `.md` (name = filename), a-i--skills
   `*.skill`/category dirs — into one `{ecosystem, type, name, description, path,
   invoke}` record.
3. Ranks matches (name > triggers > description > path) and, on `show`, prints the
   unit plus the exact invoke hint for that agent's own loader.

Point it at any directory of ecosystems (default `~/_arms/mirror/` + `~/_arms/skills/`)
and it indexes them live. The index is computed each call from the sources, so it
can never drift from reality — there is no stored index to stale.

## Honest about reach

For same-agent units (e.g. Claude loading a Claude `SKILL.md`), `show` is a real
context-load. For other agents it prints the unit and the precise invoke hint for
*that* agent's loader — the portal routes you to the door; each agent still opens
its own. Cross-agent *execution* is the orchestrator's job (see `agent-swarm-orchestrator`);
`portal-router` is the discovery-and-routing layer beneath it.
