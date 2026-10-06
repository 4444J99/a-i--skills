# DIWS — Portfolio Composition Map (v3 deepening)

This is the matrix that PDE's per-product composition matrix could not reach: cross-portfolio composition. It tells you, for every n-way combination of DIWS instances, what composite output the combination yields when run through the operators.

## How to read this map

**Input:** N filled DIWS instances in `proof-instances/` or active-portfolio directory
**Output rows:** combinations from C(N,2), C(N,3), C(N,4) (and beyond if N>5)
**Output columns:** what each operator yields when fired across the combination

## Composition pattern (canonical)

For any combination of K instances {D₁, D₂, ..., D_K}:

| Operator | Composition output | Output artifact path |
|---|---|---|
| 1 (Selfish-altruistic) | Net practitioner-skill increase across the combination | `combinations/<id>/net-skill-delta.md` |
| 2 (Magnetic membrane) | Merged refinery rules + merged contribution charter | `combinations/<id>/merged-membrane.md` |
| 3 (Portfolio Operator) | K-way cross-pollination diagnoses (one per instance pair internal to the combination) + merged tool inventory | `combinations/<id>/cross-pollinations.md` + `combinations/<id>/merged-tools.md` |
| 4 (Reflexive) | Meta-study of the combination as its own thing | `combinations/<id>/combination-meta-study.md` |

The combination-id `<id>` follows the pattern `<sorted-domain-list>-<operator-set>`, e.g. `chess-fitness-portfolio` or `chess-education-wellness-merged-membrane`.

## Pair compositions (C(N,2))

For 4 active instances {chess, wellness, education, design}, 6 pair combinations:

| Pair | Operator-1 yield | Operator-2 yield | Operator-3 yield | Operator-4 yield |
|---|---|---|---|---|
| chess × wellness | shared mind-body discipline pattern | merged refinery (chess archives + wellness primary research) | fitness membership-funnel transplant to chess; chess premium-content transplant to fitness | meta-study: "two-flag-pierce as one practitioner mode" |
| chess × education | shared pedagogy depth (1-on-1 vs cohort) | merged refinery (chess theory journals + education research) | "pedagogy-as-content" cross-flow | meta-study: "teaching-as-game vs teaching-as-instruction" |
| chess × design | shared visual-system / principle thinking | merged refinery (chess aesthetics + design language patterns) | "design-as-strategic-thinking" essay surface | meta-study: "principle-bound creativity" |
| wellness × education | shared transformation-coaching pattern | merged refinery (clinical evidence + education research) | "transformation pedagogy" cross-flow surface | meta-study: "growth as taught vs growth as practiced" |
| wellness × design | shared aesthetic-affect pattern (visual brand ↔ embodied affect) | merged refinery (clinical evidence + design language) | "wellness brand language" cross-flow | meta-study: "design as therapeutic vs design as commercial" |
| education × design | shared curricular structure | merged refinery (education research + design pedagogy) | "design-curriculum" cross-flow | meta-study: "structure-as-medium" |

## Triple compositions (C(N,3))

For 4 active instances, 4 triple combinations:

| Triple | What it computes |
|---|---|
| chess × wellness × education | "Coaching for transformation" — combines chess pedagogy + wellness clinical structure + education theory; unified output: design-language-for-transformation-coaches |
| chess × wellness × design | "Embodied strategy" — combines chess principles + wellness somatic + design aesthetic; unified output: visual-language-for-strategic-embodiment |
| chess × education × design | "Pedagogical visual system" — combines chess teaching + education curriculum + design language; unified output: design-of-learning-environments |
| wellness × education × design | "Transformation curriculum design" — combines wellness coaching + education theory + design language; unified output: pedagogy-of-becoming |

## Quad composition (C(N,4) = 1 with N=4)

| Quad | What it computes |
|---|---|
| chess × wellness × education × design | The full portfolio thesis: **principled transformation through visual pedagogy**. Combines chess (principle-binding), wellness (transformation as core), education (pedagogy as method), design (visual language as carrier). This is the user's own substrate, surfaced. |

## Beyond C(N,4): higher-order combinations as portfolio grows

When N=5 (a pre-active stub becomes confirmed) or N=6+ (future flag-pierces), C(N,K) grows combinatorially. Strategy:

- **Cap reporting at K≤4** by default — beyond K=4 the marginal yield drops without methodological change
- **Cap K=5,6,...** runs at *intentional* triggers (annual portfolio review, major positioning rewrite)
- Use the operator-yields table to *score* each combination's depth before fully writing it up; rank-order, write top 5 each cycle

## Stretching rack at composition scale

The Phase 0.5 stretching rack ([`scripts/portfolio-gap-audit.sh`](../scripts/portfolio-gap-audit.sh)) operates on combinations, not just single instances:

For each combination, the rack reports:
- **Holes** in the combination = stratum cells that are weak in *every* member instance (no transplant rescue available)
- **Fat** in the combination = stratum cells that are over-engineered in *every* member instance (consolidate up)
- **N-way overlap** = stratum cells that are strong in ≥2 instances (promote pattern to meta-engine)

This is how user's portfolio finds its **shared spine** vs **unique skins** — the rack at combination scale tells you which features are spine and which are skin.

## Tool/audience cross-flow matrix (Portfolio Operator push leg, expanded)

For each combination, the Portfolio Operator's push leg (cross-flow #3) yields:

| Combination | Reusable tool surfaced | Cross-pollinatable audience |
|---|---|---|
| chess × wellness | Tier-progression UI (named rank-ladder pattern) | local chess club scene ↔ fitness member circle |
| chess × education | Lichess study system + cohort engine | YouTube chess audience ↔ classroom pilots |
| chess × design | Visual notation system (annotation language) | chess content creators ↔ design Twitter |
| wellness × education | Cohort + member-circle hybrid platform | wellness practitioner newsletter ↔ educator network |
| wellness × design | Visual brand system for practitioners | wellness practitioner clients ↔ design portfolio audiences |
| education × design | Curriculum visual-language template | Educator forums ↔ design education |

## Heist + contribute round-trip at combination scale

Layer 4 ↔ Layer 8 round-trip becomes more powerful when combinations are explicit:

- A heist-target identified in chess (e.g. Naroditsky's annotation methodology) might transplant to wellness (clinical case-study annotation) — and the contribution back goes to BOTH source-domain (improved annotation methodology paper) AND merged-domain (case-study-annotation skill).
- This is how 1 heist becomes 3 contributions at portfolio scale.

## How to use this map operationally

1. After Phase 0 portfolio-audit, list which DIWS instances are populated
2. Generate the C(N,2) + C(N,3) + C(N,4) combinations
3. Run Phase 0.5 stretching rack on each combination
4. Walk the operator-yield columns for each
5. Pick top-5 combinations by yield-density; fully write them up
6. Promote the top-1 combination output to a meta-engine if pattern repeats

## Per-engagement minimum

When a single new domain instantiates (single flag-pierce), at minimum:
- 1 pair composition (this domain × strongest-overlap-existing-domain) gets written up
- All other pair compositions get *yield-scored* (binary: high / low) for follow-up

This guarantees Portfolio Operator push fires even on single-engagement flag-pierces.
