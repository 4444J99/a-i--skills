---
name: personalized-storefront-render
description: Translate internal markdown artifacts (pitch decks, business plans, research) into per-persona client-facing storefront surfaces in the client's domain language with ELI5/TLDR layers. Sits above Product Domain Engine and 8-Strata Domain Ideal-Whole; invokes voice-enforcement against persona-specific voice_constitution. Triggers on requests for client-facing surfaces, persona-tuned translation, ELI5/TLDR projections, or storefront-style client deliverables. Render is scaffold-and-curate (never auto-publish) to protect client trust.
license: MIT
---

# Personalized Storefront Render — Substrate Skill

> Translate internal artifacts into client-facing surfaces in the client's domain language. Substrate, not bespoke build.

## When to invoke

- User asks for "a client-facing version of X" / "translate this for <client>" / "ELI5 / TLDR of <internal doc>".
- User wants every internal artifact (or a class of them) to project to a client storefront.
- A new client is being onboarded and needs a personalized read-surface for ongoing work.
- A specific artifact is tagged with `audiences:` frontmatter and the storefront has not been regenerated.

## When NOT to invoke

- The artifact is governance/SOP/internal-only with no client surface (`audiences: [internal]` or unmtagged).
- The work is bespoke creative direction for a specific deliverable (use the relevant domain skill — e.g. a creator brand's bridge-content templates or a practitioner brand's lineage substrate).
- The client surface already exists and is hand-curated outside this substrate (do not ingest after-the-fact; respect the existing artifact).

## Architecture (4 layers)

```
LAYER 0 — PERSONA CORPUS  (~/Documents/personas/)
  {id}.md          ← prose source-of-truth (untouched by this skill)
  {id}.lexicon.yaml ← machine-readable translation table (this skill consumes)

LAYER 1 — INTERNAL ARTIFACTS  (per client repo, /docs/**)
  Existing artifacts, optionally extended with YAML frontmatter:
  audiences[], tldr, strata, client_render_mode

LAYER 2 — TRANSLATION ENGINE  (this skill)
  Composes:
    Product Domain Engine (Phase 4 logos→pathos rendering)
    8-Strata Domain Ideal-Whole (gap-map / coverage detection)
    voice-enforcement (constitution check vs persona register)
    lexicon-substitution (forbidden-terms removal, analogy mapping, ELI5/TLDR shaping)
  Output: docs/storefront/_generated/<artifact>.<persona>.client.md
   then:  docs/storefront/_curated/<artifact>.<persona>.client.md  (after human ratify)

LAYER 3 — DEPLOY SURFACE  (per-repo, per-stack adapter)
  Next.js repos:  /storefront/[...slug] → <client>.<domain> (link-gated)
  Astro repos:    /storefront/[...slug] → <client>.<domain> (link-gated)
  Future:         static adapter ships plain HTML
```

## Commands (CLI surface)

The skill is callable from any agent; the operator-facing form is the `organvm storefront` subcommand:

| Command | Purpose |
|---|---|
| `organvm storefront sync --repo <path>` | Walk source.globs, read audiences frontmatter, render per-persona drafts to `_generated/`. Idempotent. |
| `organvm storefront audit [--persona <id>] [--unmtagged]` | Report: lexicons stale (>90d behind prose), unmtagged client-relevant artifacts, orphan curated files (no source), forbidden-term hits in any draft. |
| `organvm storefront ratify <artifact-slug> [--persona <id>]` | Move `_generated/...client.md` → `_curated/...client.md` after human read. Records voice-scorer score in artifact metadata. |
| `organvm storefront status` | One-line: `<n> drafts unratified · <m> internal artifacts changed since last sync · <k> forbidden-term hits`. |
| `organvm storefront feedback add --persona <id> --note "..."` | Append client feedback to `~/Documents/personas/{id}.feedback.md` and create an `IRF.STO-FEEDBACK-*` item. |

Invocation by agents: prefer the skill protocol (this document) over re-implementing; call the CLI for actual rendering.

## Composition contract (what this skill does NOT duplicate)

This skill is a conductor. It **invokes** existing skills/tools rather than re-implementing them:

- **Product Domain Engine** — Phase 4 (rhetorical-mode rendering) is invoked for the logos→pathos transform when audience.register requires it.
- **domain-ideal-whole-substrate** — the 8-strata `internal-magnet` rules are read to determine which source globs are eligible for client projection. The `gap-map` stratum surfaces audit findings.
- **voice-enforcement** — the persona's `voice_constitution` field names a rule pack that voice-scorer uses to score every draft pre-ratify.
- **stranger-test-protocol** — the verification step "fresh agent identifies the persona's domain language without invoking PDE/ontology terms" comes from this protocol.

**Do not** re-implement what these skills already do. Substrate failure modes flow downstream from substrate violations.

## Substrate refuses to render orphans

Every storefront-rendered artifact MUST trace `bridge_to:` lineage to a real internal artifact. The substrate refuses to emit `_generated/*.client.md` for any input where:

- No source file exists at the path implied by the artifact frontmatter, OR
- `bridge_to:` references a domain handle not present in the persona's lexicon, OR
- `audiences[].id` references a persona without a `{id}.lexicon.yaml` file in `~/Documents/personas/`.

This rule prevents personalization theatre — making something *sound like* the persona without saying anything they would actually care about. Density-of-real-content is the gravity.

## Lifecycle (Universal Rule #6 — everything is a loop)

```
internal artifact created/updated
  → audiences frontmatter present? if no → skip (default [internal])
  → operator runs `organvm storefront sync` (on demand, no daemon — Universal Rule #55)
  → render pipeline emits _generated/<artifact>.<persona>.client.md per audience entry
  → voice-scorer scores draft against persona.voice_constitution
  → IRF auto-issues STO-DRAFT-* item per unratified draft
  → operator reads + ratifies → _curated/
  → repo-native build (npm run build for Next.js, etc.) ships /storefront/* routes
  → client receives URL; reads in their language
  → client feedback enters via mailto + `storefront feedback add` → STO-FEEDBACK-* IRF items
  → next sync regenerates from updated source + lexicon
```

No daemons. No LaunchAgents. Pre-push git hook in opt-in repos may warn (exit 0) when client-relevant files changed without a regenerate; the warning surfaces the exact `storefront sync` command to run.

## Phased rollout (substrate maturity)

| Slice | Scope |
|---|---|
| 1 — First client storefront (Next.js) | Schema, first persona lexicon, repo `storefront.config.yaml`, frontmatter on 1+ canonical artifact, hand-curated drafts |
| 2 — Second client storefront (Astro) | Astro adapter, second persona lexicon, repo config, frontmatter on a handful of artifacts |
| 3 — Full substrate | Auto-draft generator, pre-push hook, IRF wiring, mailto backfeed, static adapter, `audit --unmtagged` baseline |

## References

- **Plan**: `~/.claude/plans/2026-04-25-personalized-client-storefront-substrate.md`
- **Schema**: `~/Workspace/organvm/schema-definitions/schemas/storefront-v1.schema.json`
- **Canonical example**: `~/Workspace/organvm/schema-definitions/examples/storefront-frontmatter-<persona>.yaml`
- **Persona lexicon**: `~/Documents/personas/<persona-id>.lexicon.yaml`
- **Repo opt-in**: `<client-repo>/storefront.config.yaml`
- **Sibling skills**: `product-domain-engine` (PDE Phase 4 invocation), `domain-ideal-whole-substrate` (8-strata gap-map), `voice-enforcement` (per-persona constitution checks)
