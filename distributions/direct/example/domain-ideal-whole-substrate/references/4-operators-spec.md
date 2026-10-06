# DIWS — 4 Operators Specification

Operators describe how flow happens. They fire **simultaneously** on every flag-pierce per Tenet Protocol — never one without the others.

## Operator 1 — Selfish-altruistic loop (single-engagement)

**Class:** self-cycle, single-engagement scope

**Cycle:**
```
Learn-for-self → Quality-of-product → Service-to-friends →
Friends-elevated → Network-effect → Self-elevated → More-learning
```

**Function:** Locks the user into being a real practitioner rather than a curator. The "selfishness" is the gate — without it, the system curates dead. Friends benefit *because* the user is a real practitioner, not despite it.

**Failure mode:** Curator-mode. User stops learning-for-self, becomes a recommender of others' work, loses the substrate. Detection: stratum-1 ontology stops growing; constellation column dominates over user's own work.

**Fire condition:** Every engagement. User self-checks: am I learning here, or just packaging?

**Diagnostic:**
- ✅ Healthy: user has direct skill increase from this engagement
- ⚠️ Watch: user is helping but not learning (ok short-term, dangerous as default)
- ❌ Curator-mode: user has no skill increase across last 3+ engagements

## Operator 2 — Magnetic membrane (single-domain, two-way)

**Class:** flow-through, single-domain scope

**Direction:**
```
Flag pierces →
  INTERNAL leg (PULL): magnetize all applicable, transmute through user's lens, alchemize toward ideal
  EXTERNAL leg (PUSH): contribute to community
```

**Mechanism:** Two-way membrane. Pull-in = refinery (Stratum 7). Push-out = gift (Stratum 8). Per Tenet Protocol, both directions fire simultaneously.

**Failure mode:** One-way pierce. Either pull-only (extraction without contribution) or push-only (contribution without learning). Both are unsustainable.

**Fire condition:** Every engagement, both directions. Stratum 7 and Stratum 8 must both have non-empty active-cadence sections.

**Diagnostic:**
- ✅ Healthy: every Stratum 7 input has a Stratum 8 counterpart
- ⚠️ Watch: imbalance >3:1 in either direction
- ❌ One-way: 0 entries in one direction

## Operator 3 — Portfolio Operator (cross-portfolio, two-way) — v2 + v2.1

**Class:** flow-across, multi-domain scope

**Direction:**

### Pull leg (v2.1)
Before any layer-1 ontology work begins:
1. Scan `~/Workspace/` for existing engines / skills / primitives matching candidate-domain shape
2. Produce `portfolio-reuse-map.md` (which engine gets skinned, what's domain-specific skin, what's genuinely new)
3. Only enter layers 1-8 after reuse-map is filled

Mechanism: [`scripts/audit-portfolio.sh`](../scripts/audit-portfolio.sh) implements this leg.

### Push leg (v2)
Three cross-flows fire simultaneously on every domain instantiation:

1. **Meta-skill flow** — transferable practices (marketing, community-building, writing/voice, audience cultivation) become first-class objects extractable from any domain. User can have low direct interest in a friend's primary domain but high interest in the meta-skill substrate. Meta-skills amortize across every future flag-pierce.

2. **Domain-pair overlaps** — every flag-pierce creates N-1 publishable conversation surfaces:
   - friend-domain × user-domain
   - friend-domain × every-other-friend-domain
   - Each overlap = essay, video, or joint-product opportunity

3. **Tool/audience cross-flow** — every engagement spawns reusable tools AND audiences:
   - Tools amortize across portfolio nodes (a visual-flow renderer built for one client can re-skin as another client's funnel visualizer; the conversation-corpus pipeline for ChatGPT ingest serves every future capture)
   - Audiences cross-pollinate (an education project borrows a collaborator's relationship audience; a chess-coaching brand borrows a fitness brand's audience)

**Output artifact:** `portfolio-resonance.md` (one per domain instantiation; lists the three cross-flows with concrete entries).

**Failure mode:** Vertical silos. Each domain ships 8 great vertical files but cross-pollination diagnoses are missed (the most valuable artifacts of any session). Without explicit Portfolio Operator firing, cross-flows depend on session-luck.

**Fire condition:** Every engagement. Phase 0 (pull) + Phase 9 (push, after stratum artifacts ship).

**Diagnostic:**
- ✅ Healthy: ≥3 portfolio-pull reuses + ≥3 portfolio-push outputs per engagement
- ⚠️ Watch: pull only OR push only (one-leg failure)
- ❌ Silo: 0 entries on either leg

## Operator 4 — Reflexive Operator (build + study, parallel) — v2.2

**Class:** recursion, build/meta-study co-arising

**Mechanism:**
For every structure built, a meta-system appears around it to study it. Per Tenet Protocol, every build-action triggers its opposing reflection-action simultaneously. The thing and the thing-studied co-arise.

**Output artifact:** `domain-meta-study.md` alongside the 8 stratum artifacts. Contents:
- What was built (mirror of the 8 strata)
- How it was built (process, not product)
- What it reveals about the meta-system (the substrate skill itself)
- What changed in the substrate skill as a result of building this instance

**Recursion direction:**
- Building a chess instance → produces `chess/domain-meta-study.md`
- This study-of-build feeds back into the substrate skill's `references/` (rule changes propagate)
- Substrate skill changes → next instantiation reflects the new rules

**Failure mode:** Build-only. Instance ships but no meta-study; substrate skill never refines from real-world execution. Detection: substrate skill's references/ haven't changed in 3+ instantiations.

**Fire condition:** Every engagement. Phase 9 (parallel with Portfolio Operator push).

**Diagnostic:**
- ✅ Healthy: every domain instantiation has `domain-meta-study.md`; substrate skill refines per instantiation
- ⚠️ Watch: study exists but doesn't propagate back to skill
- ❌ Build-only: no study artifacts; skill stagnates

## Operator interaction rules

Operators do not run in isolation. They interact:

| Operator pair | Interaction |
|---|---|
| 1 ↔ 2 | Selfish-altruistic loop's "Service-to-friends" fires the magnetic membrane's EXTERNAL leg |
| 1 ↔ 3 | Network-effect (operator 1 step 5) is realized by Portfolio Operator's push leg |
| 2 ↔ 3 | Magnetic membrane's INTERNAL leg includes portfolio-pull (operator 3 pull leg) |
| 2 ↔ 4 | Reflexive study draws from both INTERNAL and EXTERNAL membrane outputs |
| 3 ↔ 4 | Portfolio Operator's three cross-flows are themselves reflexive — meta-skill extraction IS the study-of-build |

**All four fire simultaneously on every engagement.** The diagnostic is binary: did all four leave artifacts? If any one is missing, the engagement is incomplete.

## Reading the operator pattern at portfolio scale

When running [`scripts/portfolio-gap-audit.sh`](../scripts/portfolio-gap-audit.sh) (the stretching rack), check each operator across all DIWS instances:

- Are all 4 operators firing in all instances? → balanced portfolio
- Is one operator dominant in some instances and absent in others? → cross-flow opportunity (transplant the dominant pattern)
- Is one operator absent across the whole portfolio? → systemic gap (build the missing operator, not a per-domain fix)

This is what makes the operator framework portfolio-relevant rather than per-domain-only.
