# DIWS — Engine Taxonomy (3 tiers)

Per v2.2: every engine in the portfolio sits in exactly one of three tiers. This taxonomy governs Phase 0 portfolio-audit and decides whether a discovered pattern gets re-skinned (Tier 1), promoted to cross-domain primitive (Tier 2), or installed-into-every-engagement (Tier 3).

## Tier 1 — Domain engines

**Scope:** re-skin within the same or adjacent domain. The engine's pattern is bound to a domain class.

**Example portfolio engines (illustrative):**

| Engine | Origin | Domain class | Re-skin candidates |
|---|---|---|---|
| 4-level membership funnel mechanism | fitness engagement | Membership / progression-tier | Chess coaching tiers, wellness coaching memberships |
| Visual-flow renderer (e.g. a spiral/flow SVG component) | wellness-brand engagement | Visual-flow brand / aesthetic-affect | Other visual-flow brands, meditation aids, generative art |
| Landing-engine (Astro+SSG persona templates) | shared across engagements | Persona-arch landing pages | All future client landing pages |
| 75-person Constellation file | PRT-046 | Peer-research foundation | Every domain (chess, wellness, education, design, voodoo) |

**Re-skinning protocol:**
1. Phase 0 portfolio-audit identifies a Tier 1 candidate
2. Configuration / theming layer separates from logic layer (if not already done)
3. New skin = new YAML/CSS/parameter file
4. Logic engine version bumps minor (1.x.0 → 1.x.1)
5. Original engine docs add new skin to known-instances list

**Promotion criteria (Tier 1 → Tier 2):**
- Pattern fires across ≥3 domain classes (not just adjacent ones)
- Logic separates cleanly from any single domain's vocabulary
- ≥2 unrelated portfolio nodes benefit independently

## Tier 2 — Meta-engines

**Scope:** cross-domain pattern. The engine works regardless of domain class but works on *domain content* — it doesn't run independently of any domain.

**Example portfolio engines (illustrative):**

| Engine | Origin | What it does | Cross-domain instances |
|---|---|---|---|
| Cross-pollination diagnosis | PRT-045 | Surfaces n-way mechanism asymmetries between 2+ domain instances | e.g. chess ↔ fitness; chess ↔ education, etc. |
| Product Domain Engine (PDE) | a-i--skills (cf92479) | 5-phase × 4-mode formalization of product-tied-to-domain | Used across chess, wellness; pending for education, design |
| Bridge Content templates | PRT-040 | Weekly signature-technique + monthly rivalry-episode creator cadence | Originated in one creator engagement; transplantable to any creator domain |
| Discord rituals (Welcome Wed / Loot Drop Fri / Quest Log Sun) | PRT-041 | Tier-gated community engagement cadence | Originated in one creator engagement; transplantable to all gated communities |
| Portfolio-gap-audit (the stretching rack) | DIWS Phase 0.5 | Holes/fat diagnosis at portfolio scale | All multi-instance portfolios |

**Promotion criteria (Tier 2 → Tier 3):**
- Engine runs even when no specific domain content is loaded
- Engine is part of consultant identity (what's brought TO the engagement, not what's built FOR it)
- ≥3 unrelated portfolio nodes consume identically (no skinning needed)

## Tier 3 — Consultant engines

**Scope:** every engagement regardless of domain. The engine *is* part of consultant identity — what's brought TO the engagement beyond the engagement itself.

**Example portfolio engines (real):**

| Engine | Origin | What it does | Why Tier 3 |
|---|---|---|---|
| Knowledge base | personal infra | Persistent structured notes across all engagements | Used by every engagement; not skinnable, just shared |
| Application pipeline | 4444J99/application-pipeline | Job/grant/opportunity tracking infrastructure | Cross-engagement personal infrastructure |
| Plan-mode discipline | dotfiles + CLAUDE.md | Dated plan files, never-overwrite, sculpture rule | Used in every session regardless of project |
| IRF / MEMORY / chezmoi rescue protocols | personal infra | Local→remote sync, triple-reference, vacuum tracking | Used across every project |
| Conversation-corpus pipeline | corpus engine | ChatGPT / Claude / Copilot / Gemini ingest + dedup | Personal capture infrastructure |
| chatgpt_exporter_to_bundle converter | corpus engine | Bridges per-conv exports to bundle format | Personal capture infrastructure |
| 5 organvm CLIs (sessions audit / subatomic decompose / memory triangulate / relay draft / atoms pipeline verify) | DIWS Stream Τ | Cross-session governance enforcement | Used by every session |

**Identity:** Tier 3 engines get installed into client projects as *embedded deliverables* (rule 5: fix bases not outputs — install the engine, don't ship its output once). When a client hires the user, they get the relevant domain engine (Tier 1, e.g. a visual-flow renderer) AND inherit the conversation-corpus pipeline (Tier 3) running in their project.

## Engine extraction (mode `engine-extract`)

When an instance reveals a generalizable pattern, promote up the tier ladder:

```
ad-hoc pattern → Tier 1 (domain engine) → Tier 2 (meta-engine) → Tier 3 (consultant engine)
```

Promotion is **only via user authorization**. The substrate skill detects candidate promotions but flags them; the user decides.

**Detection rules (substrate skill):**
- Pattern fires identically in ≥2 instances → flag for Tier 1 status
- Pattern fires across ≥3 unrelated domain classes → flag for Tier 2 status
- Pattern is part of consultant identity (works without any specific domain content) → flag for Tier 3 status

## Tier-load distribution per engagement

Target ratio (per v2.1 engine + skin pattern):

| Source | Engagement-level contribution |
|---|---|
| Tier 3 (consultant engines) | 30–50% — installed as default infrastructure |
| Tier 2 (meta-engines) | 20–30% — applied per engagement context |
| Tier 1 (domain engines, re-skinned) | 20–30% — pulled in via Phase 0 audit |
| Genuine new code (skin only) | 10–20% — what neither engine nor pattern can express |

Engagements with >40% genuine new code = Phase 0 audit was incomplete OR the engagement is in a genuinely new domain class (rare; flag for Tier 1 promotion candidate).

Engagements with <10% genuine new code = engagement is pure assembly; this is fine for repeat-pattern work but should not become the default (every engagement should grow the engine fleet a little).

## Anti-pattern: ignoring the taxonomy

**Failure mode 1 — "domain-only thinking":** every engagement scratch-builds because the consultant doesn't recognize their own consultant-engines. Output: 100% new code, low margins, slow ramp.

**Failure mode 2 — "over-promotion":** engineer promotes a Tier 1 pattern to Tier 2 prematurely, ends up with a brittle abstraction. Detection: promoted engine has ≤2 actual cross-domain consumers after 6+ months.

**Failure mode 3 — "consultant identity bloat":** Tier 3 engines proliferate, slowing every new engagement's setup. Detection: ratio of setup-time to value-add-time exceeds 30%.

## Cross-references

- DIWS Phase 0 ([`scripts/audit-portfolio.sh`](../scripts/audit-portfolio.sh)) — produces engine inventory categorized by tier
- DIWS Phase 0.5 ([`scripts/portfolio-gap-audit.sh`](../scripts/portfolio-gap-audit.sh)) — uses engine taxonomy to identify promotion candidates
- Plan v2.2 — original spec (`~/.claude/plans/2026-04-25-domain-ideal-whole-substrate-design.md` lines 330-340)
