---
name: corpus-persona-extraction
description: Ingest a corpus of session logs (JSONL transcripts, chat exports) and extract a persona profile — vocabulary frequency, unique idioms and coinages, structural analogies — then synthesize an ideal_yearning and archetypal_pattern and append the result to a {persona_id}.lexicon.yaml. Triggers on "extract persona", "build a lexicon", "map the domain language", or any request to process conversation logs into a voice/vocabulary model.
license: MIT
complexity: advanced
time_to_learn: 1hour
tags:
  - corpus-linguistics
  - persona
  - lexicon
  - voice-modeling
  - session-mining
  - vocabulary
governance_phases: [build]
organ_affinity: [organ-i, organ-ii, organ-v]
inputs:
  - corpus of session files (JSONL, markdown exports, or message-atom extracts)
  - persona_id (which voice to extract — usually the human operator)
  - existing {persona_id}.lexicon.yaml if one exists (append, never overwrite)
outputs:
  - updated {persona_id}.lexicon.yaml with dated extraction block
  - extraction report (counts, new coinages, drift vs prior blocks)
side_effects:
  - reads-filesystem
  - creates-files
triggers: [user-asks-to-extract-persona, context:build-lexicon, context:domain-language-mapping, context:voice-model]
complements: [voice-enforcement, conversation-content-pipeline, knowledge-architecture, second-brain-librarian]
---

# Corpus Persona-Extraction

Distill *how a specific voice thinks and speaks* from a pile of session logs, and persist it as a machine-usable lexicon that downstream agents can write against.

## Why this exists

Agents that work with a long-running human collaborator keep re-learning the same voice from scratch: the coinages, the load-bearing metaphors, the sentence shapes that mean "yes, proceed" versus "you've missed the point." A lexicon file makes that knowledge durable and composable — voice-enforcement gates can score against it, drafting skills can imitate it, and translation layers (persona storefronts) can project from it.

## Core doctrine

- **User coinages outrank standard vocabulary.** When the corpus shows an idiosyncratic term for a concept ("vacuum", "organ", "cartridge", "liturgy"), the lexicon records the coinage as primary and the standard term as gloss — never the reverse.
- **Append-only.** Each extraction run adds a dated block. Prior blocks are evidence of drift, not errors to clean up.
- **Separate speakers ruthlessly.** A transcript interleaves human, assistant, and tool text. Only the persona's own turns feed frequency analysis; assistant paraphrase contaminates the signal.

## Workflow

### 1. Assemble and filter the corpus
- Gather session files; record provenance (paths, date range, message counts) in the extraction header.
- Parse each format to (speaker, timestamp, text) tuples; keep only `speaker == persona_id` turns.
- Strip quoted/pasted material (code blocks, tool output, copied text) — the persona's *own* prose only.
- **Redact before analysis**: run the corpus through secret/PII patterns first; a lexicon must be shareable.

### 2. Vocabulary frequency
- Tokenize; compute frequency ranks for unigrams/bigrams/trigrams.
- Diff against a general-English baseline: the interesting set is terms whose corpus rank vastly exceeds baseline rank (keyness), not raw frequency.
- Bucket results: domain terms (shared with field), **coinages** (absent from baseline entirely), and inflections (standard words used in non-standard senses).

### 3. Idioms and structural analogies
- Idioms: recurring multiword expressions with stable meaning ("fix bases, not outputs", "the soul persists").
- Structural analogies: the source domains the persona habitually maps from — music, anatomy, liturgy, architecture. Record each as `analogy: {source_domain} → {target_domain}` with 2-3 verbatim examples.
- Register markers: profanity patterns, emphasis habits (caps, em-dashes), sentence-length distribution, imperative density.

### 4. Synthesize ideal_yearning and archetypal_pattern
These two fields are the lexicon's soul — short synthesized statements, each grounded in ≥3 verbatim quotes:
- **`ideal_yearning`** — what the persona is reaching toward across all sessions; the recurring wish underneath the tasks. Written as one sentence in the persona's own idiom.
- **`archetypal_pattern`** — the recurring role/shape the persona enacts (e.g. "the conductor who builds the orchestra rather than playing the instrument"). One sentence plus the evidence quotes.

These are *hypotheses*, marked with extraction date and confidence — later blocks may revise them.

### 5. Append to the lexicon

```yaml
# {persona_id}.lexicon.yaml — append block, never rewrite
- extraction:
    date: 2026-06-07
    corpus: {files: 128, persona_turns: 1432, date_range: [2026-04-17, 2026-06-07]}
    redaction: {patterns_run: true, hits_scrubbed: 0}
  vocabulary:
    coinages:
      - term: vacuum
        gloss: "an absence that is unrepresented anywhere durable; never a resting state"
        examples: ["N/A is a vacuum", "vacuum field burn"]
    domain_terms: [...]
    inflections: [...]
  idioms:
    - phrase: "fix bases, not outputs"
      meaning: "modify the source/template/pipeline, never the rendered artifact"
  analogies:
    - source: liturgy/theology
      target: configuration management
      examples: ["Tier-0 Liturgy", "the Reliquary", "testament"]
  register:
    profanity: "affection-marker, not hostility"
    emphasis: ["em-dash chains", "bold imperatives"]
  ideal_yearning: "…"   # one sentence, persona's idiom, ≥3 quote citations
  archetypal_pattern: "…"
```

### 6. Report
Emit a short extraction report: new coinages since last block, terms that dropped out (candidate drift), and any revision to yearning/pattern with the evidence that forced it. Commit lexicon + report together.

## Anti-patterns

- **Extracting from assistant turns.** The most common contamination; the lexicon ends up describing the model, not the persona.
- **Overwriting prior blocks.** Drift between blocks is the most valuable longitudinal signal; preserve it.
- **Unredacted lexicons.** Verbatim example quotes can carry credentials/PII from the source sessions; redact at extraction time, not later.
- **Synthesizing yearning from one loud session.** Require cross-session recurrence (≥3 sessions) before a theme reaches the yearning/pattern fields.
