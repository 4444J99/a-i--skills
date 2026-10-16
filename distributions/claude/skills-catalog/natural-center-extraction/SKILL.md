---
name: natural-center-extraction
description: Apply narratological scoring to a text, transcript, or recording transcript — rating contiguous spans for pathos, logos, ethos, kairos, and density — then extract the single highest-scoring contiguous block as the work's Natural Center, with a scoring table and justification. Triggers on "find the natural center", "extract the most dramatic moment", "what's the strongest passage", or pulling the peak block from a long artifact for a short, excerpt, or trailer.
license: MIT
complexity: intermediate
time_to_learn: 30min
tags:
  - narratology
  - content-scoring
  - excerpt-extraction
  - rhetoric
  - editing
  - distribution
governance_phases: [build, prove]
organ_affinity: [organ-ii, organ-v, organ-vii]
inputs:
  - source artifact (essay, transcript, session log, script, recording transcript)
  - target length for the extracted block (e.g. 60-second short, pull-quote, abstract)
outputs:
  - the Natural Center block (verbatim, contiguous, source-spanned)
  - five-axis scoring table for all candidate blocks
  - justification paragraph
side_effects:
  - reads-filesystem
  - creates-files
triggers: [user-asks-for-natural-center, context:extract-peak-moment, context:best-passage, context:short-form-excerpt]
complements: [narratological-algorithms, script-analysis-dramaturgical, content-distribution, essay-to-distribution-pack]
---

# Natural Center Extraction

Every sufficiently long artifact has a passage where its energies converge — the block a reader quotes, a trailer cuts to, an editor pulls. This skill finds that block by scoring rather than vibes, and returns it verbatim with the evidence for why it wins.

## Why this exists

Excerpt selection is usually done by skimming, which favors openings and recency. Algorithmic scoring over *all* contiguous candidates surfaces centers that skimming misses — the buried turn in hour two of a transcript, the paragraph where argument and feeling finally coincide. The output feeds distribution work (shorts, pull-quotes, abstracts) with a defensible selection rather than a taste call.

## The five axes

| Axis | What it measures | High-scoring signals |
|------|------------------|---------------------|
| **pathos** | felt intensity | stakes made personal; vulnerability; register shifts; concrete sensory detail |
| **logos** | argumentative force | a claim *completed* in-block (setup → turn → consequence); evidence meeting assertion |
| **ethos** | voice authority | the speaker most distinctly themselves; earned credibility on display; coinages dense |
| **kairos** | timeliness/pivot | the moment the piece turns; before/after asymmetry; decision points; reversals |
| **density** | compression | ideas-per-sentence; no warm-up or wind-down inside the block; every line load-bearing |

Each axis scored 0–10 per candidate block. Axes are scored independently *then* combined — a block must not be pre-selected because one axis shouts.

## Workflow

### 1. Normalize and segment
- Normalize the source to numbered units (paragraphs for prose; speaker-turns for transcripts; beats for scripts).
- Generate candidate blocks: all contiguous runs whose length fits the target ±30% (sliding window). For long sources, pre-filter with a cheap density pass to a candidate set of 15–40 blocks before full scoring.

### 2. Score every candidate
- Score each block on all five axes with one-line evidence per axis ("kairos 9: the 'and then I stopped' reversal lands mid-block").
- **Contiguity is a hard constraint**: no stitching, no elisions, no `[...]`. The Natural Center is found, not assembled.
- Compute the composite. Default: equal weights. Named intents shift weights — trailer/short → pathos+kairos ×1.5; abstract → logos+density ×1.5; bio/about → ethos ×1.5. State the weighting used.

### 3. Break ties structurally
When composites tie (within ~5%):
- Prefer the block that *survives decontextualization* — read it cold; does it work without the surrounding pages?
- Prefer complete arcs (in-block setup and payoff) over blocks that borrow setup from outside.
- Prefer the later block when scores tie exactly — late convergence usually means the whole work feeds it.

### 4. Emit the result

```markdown
# Natural Center — {source} ({date})
**Block:** units {n}–{m} ({word-count}w, target {t})  |  **Weighting:** {profile}

> {the block, verbatim, contiguous}

## Scoring table
| Block | pathos | logos | ethos | kairos | density | Σ |
|-------|--------|-------|-------|--------|---------|---|
| u12–u15 | 7 | 9 | 6 | 9 | 8 | 39 |  ← NATURAL CENTER
| u03–u06 | 8 | 5 | 7 | 4 | 6 | 30 |
| …top 5 candidates… |

## Justification
{one paragraph: why this block; which axes carried it; what the runner-up
lacked; per-axis evidence lines for the winner}
```

- Always include the runner-up comparison — the justification is only credible against a named alternative.
- Record the source span precisely so downstream cuts (video timestamps, page cites) can locate it.

### 5. Optional: multi-center mode
For serialized distribution (a thread, a cut-down series), re-run with the winner's span masked to find secondary centers. Label them C2, C3 — never promote a secondary to "the" center; the hierarchy is part of the finding.

## Anti-patterns

- **Stitching a better block than the author wrote.** Ellipses disqualify the result; contiguity is the constraint that keeps the method honest.
- **Scoring only the passages that caught your eye.** The method's value is exhaustive candidate coverage; eye-catching passages are the skim bias this skill exists to defeat.
- **One axis masquerading as five.** If the winner leads every axis, re-check the scoring — axes are designed to disagree; convergence is the *finding*, not the default.
- **Ignoring the target length.** A brilliant 900-word block is a failed extraction when the ask was a 60-second short; fit is part of the score.
- **Editing the block "lightly" on output.** Verbatim means verbatim; cleanup belongs to the downstream format pass, clearly marked as derivative.
