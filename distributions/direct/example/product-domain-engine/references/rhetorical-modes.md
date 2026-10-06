# The Four Rhetorical Modes

Classical rhetoric distinguishes four modes of persuasion. Each names a *register* — a register being an independent class of output, not a stylistic choice within one channel. The Product Domain Engine uses these four modes as a coordinate system: every product output has a position on all four axes simultaneously.

## Logos (λόγος) — the internal skeleton

**The question it answers:** *what is structurally true?*

**Internal/external:** strictly internal. Logos is the architecture — types, proofs, algorithms, schemas, tests — that makes the system coherent. It rarely faces the audience directly. Its function is to make ethos and pathos *possible*. Without logos underneath, ethos is hollow assertion and pathos is manipulation.

**Generation method:** engineering. Type definitions, algorithm implementations, test suites, formal models, financial models, system architecture. The output is *executable*, not communicable.

**Outputs (kept internal):**

- Type definitions and interfaces
- Algorithm implementations
- Data schemas and pipelines
- Test suites (internal validation)
- Financial models
- System architecture documents
- API contracts (internal-facing)

**The principle:** logos is what you build, not what you show. A customer does not consume types. They consume the credibility (ethos) or feeling (pathos) that types make possible.

## Ethos (ἦθος) — the credibility / authority register

**The question it answers:** *why should this be trusted?*

**Internal/external:** external-facing, but generated *through* logos. Ethos is the projection of logos into the audience's perception of trustworthiness. Audiences do not read the proofs. They see that proofs *exist* and trust the source.

**Generation method:** academic density. The mechanism is the *production* of scholarly-grade research, formal proofs, and quantifiable evidence. The depth of the research is the raw material that ethos is forged from.

**Concrete outputs (external-facing, ethos-functional):**

- Academic studies and research papers → signals depth
- Test counts and CI badges (`2,055 tests passing`) → signals reliability
- Portfolio README with provenance → signals professionalism
- Peer-reviewed source lists (30–80 sources per pillar) → signals rigor
- Deployment URLs and uptime metrics (`it's live`) → signals operational reality
- Case studies with measurable outcomes → signals results
- Trademark filings and legal standing → signals legitimacy
- `PROVENANCE.yaml` with SHA-256 chain → signals integrity

**The principle:** "we have 2,055 tests" is a logos *fact* but its function for the audience is ethos. The customer is not running the tests. They are inferring "this system is serious" from the test count.

**Audience:** sponsors, employers, investors, potential clients, collaborators, the market.

## Pathos (πάθος) — the emotional / narrative register

**The question it answers:** *why does this matter to a human?*

**Internal/external:** external-facing, generated through *social and media production*. Pathos creates the feeling of "I'm part of this" and "this is for me." Audiences do not analyze the narrative structure. They *feel* it.

**Generation method:** social/media volume. YouTube videos, Discord community, email sequences, landing pages, brand voice, naming systems, physical objects. The authenticity and volume of the media is the raw material.

**Concrete outputs (external-facing, pathos-functional):**

- YouTube content (the evergreen library) → creates connection
- Shorts / Reels / TikTok → creates discovery
- Landing pages (conversion-optimized) → creates desire
- Pitch decks → creates vision
- Discord community → creates belonging
- Email sequences → creates relationship
- Brand voice and visual identity → creates recognition
- Naming systems (a named rank ladder) → creates identity
- Physical objects (chess pieces, merch) → creates tangibility
- Origin / underdog story → creates emotional investment

**The principle:** "I'm 1350 and climbing" is a logos *fact* (a creator's actual rating) but its function for the audience is pathos. They are not auditing the rating. They are projecting themselves into the journey.

**Audience:** customers, community members, followers — the human who encounters the product.

## Kairos (καιρός) — the strategic / timing register

**The question it answers:** *when is the right moment?*

**Internal/external:** strategic — operates at the *meta* level above logos/ethos/pathos. Kairos is the choice of *when* to enter, *when* to hold, *what* the market is ready for now versus in six months.

**Generation method:** market-timing observation. Monitoring zeitgeist waves (the user's "music → film → TV → internet → systems" thesis is a kairos thesis at civilizational scale), competitive windows, seasonal cycles, audience readiness.

**Concrete outputs:**

- Launch timing analysis
- Seasonal content calendars
- Competitive window mapping
- "Wave-riding" assessment: arriving / peaking / fading?
- Hold-versus-ship decisions
- Roadmap with kairos gates ("ship X when Y happens, not before")

**The principle:** kairos is *when* logos becomes ethos becomes pathos. The right truth at the wrong moment lands as noise. The right narrative timed to a rising wave compounds.

**Domain examples:**

- **chess-creator-brand** (anonymized): chess content market is post-pandemic normalized; the "improvement journey" niche is rising; an existing video archive becomes more valuable over time; **kairos is OPEN now for community launch, gated for course products** (the creator needs to reach a target rating first to claim authority).
- **styx**: behavioral economics meets DeFi — both rising; peer accountability trending (BeReal, Strava); **kairos is OPEN**.
- **wellness-practitioner-brand** (anonymized): wellness practitioners over-served on websites, under-served on multi-domain topology; **kairos depends on the client's readiness**, not market.
- **public-record-data-scrapper**: UCC search demand is steady (legal/compliance); **kairos is ALWAYS** for B2B utility — no wave to ride or miss.

## The Relationship Between Modes

Logos generates ethos and pathos as outputs. It does not face the audience directly.

```
LOGOS (internal skeleton)
  │
  ├──→ ETHOS (academic density makes credibility visible)
  │     "We have 2,055 tests"  = logos fact, ethos function
  │     "9 peer-reviewed proofs" = logos fact, ethos function
  │
  └──→ PATHOS (narrative makes emotional connection)
        "I'm 1350 and climbing" = logos fact, pathos function
        "300+ documented games" = logos fact, pathos function (commitment signal)
```

Kairos sits orthogonal — it modulates *when* the logos→ethos and logos→pathos projections are released.

```
        KAIROS (timing modulator)
            │
            ▼
    ┌───────────────┐
    │   LOGOS       │
    │ (skeleton)    │
    └───┬───┬───────┘
        │   │
   ETHOS    PATHOS
   (trust)  (feeling)
```

## Mode Diagnostics

A product can fail in any of four ways:

| Failure mode | Symptom | Remedy |
|--------------|---------|--------|
| LOGOS absent | Brand without substance; promises without infrastructure | Build the formalization first; resist the urge to ship pathos-only |
| ETHOS absent | Real product, but no one trusts it | Produce density: research, tests, public deployment metrics |
| PATHOS absent | Trustworthy product, but no one cares | Produce narrative: voice, naming, community, story |
| KAIROS wrong | Right product, wrong moment | Hold; observe the wave; ship when the curve points up |

**Common pathology:** logos + pathos without ethos. The product is real and felt-as-meaningful, but lacks the credibility scaffolding (research density, test counts, deployments) that converts feeling into trust at scale. Solution: produce ethos density.

**Common pathology #2:** ethos + pathos without logos. The product *seems* trustworthy and meaningful but the underlying structure is missing. This is the marketing-without-product failure. Solution: build the formalization. The clock is ticking — eventually the audience tries to use the thing.

## Detection Heuristics (used by `domain-audit.sh`)

The audit script uses *structural* signals to detect mode presence:

| Mode | Signals detected |
|------|-----------------|
| Logos | `src/`, tests, `seed.yaml`, type definitions, schemas |
| Ethos | flagship README, `research/`, `PROVENANCE.yaml`, CI workflows, source lists |
| Pathos | `brand/`, voice docs, landing page, narrative files, community surface |
| Kairos | `ROADMAP.md`, launch plan, recent commit activity, release tags |

**Limitation:** the script reads structure, not voice. A landing page with strong pathos voice but no `brand/` directory will under-score on pathos. Treat the audit as a *coverage* check, not a quality assessment.
