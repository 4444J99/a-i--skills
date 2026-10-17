# The Composition Matrix

Every product output is a specific blend of the four rhetorical modes. The blend ratio determines what the output *is*. Selecting the right output for a given mode-pattern is the central craft of Phase 4 (EXPRESS).

The matrix below distinguishes **internal mass** (how much of each mode the output structurally contains) from **external function** (which mode the audience experiences).

## Symbol Key

- ■■■ — heavy presence
- ■■  — moderate presence
- ■   — light presence
- —   — absent
- *ext* — external function (what the audience experiences), distinct from internal mass

## Full Matrix

| Output | Logos (mass) | Ethos | Pathos | Kairos | Generation |
|--------|:------------:|:-----:|:------:|:------:|------------|
| Technical spec | ■■■ | — | — | — | Engineering |
| Type definitions | ■■■ | — | — | — | Engineering |
| Test suite | ■■■ | ■■ ext | — | — | TDD, CI/CD |
| Algorithm doc | ■■■ | ■ ext | — | — | Engineering + writing |
| Data schema | ■■■ | ■ ext | — | — | Engineering |
| Academic study | ■■■ | ■■■ ext | — | ■ | $RESEARCH_ATLAS, canonical papers |
| Research atlas | ■■■ | ■■■ ext | — | ■ | $RESEARCH_ATLAS_V3 |
| Source list (peer-reviewed) | ■■■ | ■■■ ext | — | — | Bibliographic scholarship |
| Financial model | ■■■ | ■■ ext | — | ■ | Unit economics research |
| Methodological pillars | ■■■ | ■■ ext | — | — | Pillar pattern ($PILLAR_*) |
| Flagship README | ■■ | ■■■ ext | ■ | — | Documentation craft |
| Standard README | ■ | ■■ ext | — | — | Documentation craft |
| Sales one-pager | ■ | ■■ ext | ■■ ext | ■ | Sales-engineering split |
| Pitch deck (10–12 slides) | ■ | ■■ ext | ■■ ext | ■ | Narrative + evidence |
| Course content | ■■ | ■■ ext | ■■ ext | ■ | Educational design |
| Experiment design pack | ■■■ | ■■ ext | — | — | Hypothesis design + tests |
| Live ROS (research op system) | ■■■ | ■■ ext | — | ■ | Engineering + research integration |
| Landing page (conversion) | ■ | ■ ext | ■■■ ext | ■■ | Content strategy + design |
| YouTube content | ■ | — | ■■■ ext | ■■ | Narrative frameworks, hooks |
| Shorts / Reels | — | — | ■■■ ext | ■■■ | Hook architecture |
| Discord community | — | — | ■■■ ext | ■ | Community design, identity |
| Email sequence | — | — | ■■ ext | ■■ | Relationship craft |
| Brand voice doc | — | — | ■■■ ext | — | Brand-guidelines skill |
| Naming system | ■ | — | ■■■ ext | — | Naming craft |
| Visual identity | — | — | ■■■ ext | — | Brand-guidelines skill |
| Origin / underdog story | — | ■ ext | ■■■ ext | ■ | Narrative writing |
| Physical product | — | — | ■■■ ext | ■ | Brand embodiment |
| Deployment URL | ■■ | ■■■ ext | — | ■ | DevOps |
| CI badges | ■■ | ■■■ ext | — | — | DevOps |
| `PROVENANCE.yaml` | ■■ | ■■■ ext | — | — | SHA-256 chain |
| Trademark filing | ■ | ■■ ext | ■ ext | ■■ | Legal |
| Roadmap | ■ | ■ | — | ■■■ | Strategic planning |
| Launch announcement | — | ■ ext | ■■ ext | ■■■ | Distribution timing |
| Seasonal calendar | — | — | ■ | ■■■ | Distribution timing |
| Competitive window map | ■ | ■ | — | ■■■ | Market analysis |
| Hold-vs-ship memo | ■ | ■ | — | ■■■ | Strategic decision |

## Reading The Matrix

### The internal/external distinction

A test suite is **logos-mass** internally (it is a structured truth-checker) but its **external function** is ethos — the audience does not run the tests; they read "2,055 tests passing" and trust the source. The matrix records both.

This distinction matters because:

1. **You build for internal mass.** Engineering effort goes into making the test suite real.
2. **You communicate for external function.** Marketing effort goes into making the test count *visible* (badges, README callouts, deployment dashboards).

A test suite that exists but is invisible is logos-mass without ethos-function. A test count claimed but not real is ethos-function without logos-mass — that's the marketing-without-product failure.

### Why the matrix is asymmetric

Some outputs are pure logos with no external function (technical specs, type definitions). They are *internal* artifacts that make the system possible. They serve no audience directly.

Other outputs are pure pathos with negligible logos (Discord community, brand voice docs). They are *expressive* artifacts that exist only to create connection. They have no internal function beyond their external one.

The interesting outputs are the **blends**: pitch deck (pathos+ethos), course content (pathos+ethos+logos), landing page (pathos+kairos+ethos), academic study (logos+ethos). These are the artifacts where the engine's craft is visible.

## Mode-Pattern → Output Recommendation

When `domain-audit.sh` reveals an under-developed mode, the next pass should produce outputs that strengthen it:

| Weak mode | Recommended next outputs |
|-----------|--------------------------|
| Logos | Test suite, type definitions, algorithm docs, schema, formalized PRD |
| Ethos | Flagship README, research atlas, source list, deployment URL with metrics, PROVENANCE chain |
| Pathos | Brand voice doc, naming system, landing page, origin story, Discord, YouTube cadence |
| Kairos | ROADMAP, launch plan, seasonal calendar, competitive window map, kairos-gated decisions in roadmap |

## Output Sequencing By Stage

For a *new* domain, ship outputs in this order to balance the modes early:

1. **Foundation pass:** seed.yaml + Natural Center statement + agent census *(logos)*
2. **Density pass:** flagship README + research atlas (light) + test scaffold *(logos+ethos)*
3. **Expression pass:** brand voice + landing page draft + naming system *(pathos)*
4. **Strategic pass:** ROADMAP + launch plan + competitive window *(kairos)*
5. **Loop:** re-audit, identify weakest mode, produce one strengthening output

For a *deployed* domain, the order reverses — kairos first (is the moment right?), then a targeted pass on whichever mode is weakest, never re-doing what density already provides.

## Anti-Patterns

| Anti-pattern | What goes wrong |
|--------------|-----------------|
| Pathos-only launch | Brand exists, product doesn't. Audience tries to use the thing and bounces. |
| Logos-only launch | Real product, no audience. Density without expression = invisibility. |
| Ethos-without-logos | Claims of rigor without underlying tests/research. Eventually exposed. |
| Pathos-without-ethos | Emotional connection without trustworthy substance = manipulation. |
| Logos+Ethos without kairos | Right product, wrong moment. Burns the launch energy too early. |
| All-mode-balanced too early | Spread effort thin; nothing reaches density. Pick a leading mode. |

## The Lead-Mode Principle

**Each domain leads with one dominant mode** — determined by domain nature, not preference:

- B2B utility → leads with **logos+ethos** (density creates gravity)
- Theoretical / academic → leads with **logos** (depth is the product)
- Entertainment / community → leads with **pathos** (connection is the product)
- Time-sensitive / seasonal → leads with **kairos** (moment is the product)

The other modes are not absent — they are *supporting*. The lead mode receives the disproportionate engineering investment in early passes.
