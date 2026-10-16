# Composition with artifact-resurfacing

The two skills sit on opposite sides of the same entropy regime: drift between content
that exists and citations that point at it.

## The two motions

| Motion | Skill | When |
|---|---|---|
| Content exists; citation absent → mint citation | `transcript-promotion` | substantive deliverable lives only in JSONL |
| Citation exists; content absent → reconcile citation | `artifact-resurfacing` | `CLAUDE.md`/memory points at a path that returns no hits |

They are inverses. Together they cover the four cells of the citation-vs-content
matrix:

|   | content present | content absent |
|---|---|---|
| **citation present** | *the normal case — nothing to do* | `artifact-resurfacing` (stale-citation / missing-but-lost) |
| **citation absent** | `transcript-promotion` (lift content into plan + cite) | *not a drift problem — there's nothing to track* |

## Why they live as separate skills

The motions look symmetric but their *protocols* are not:

- `transcript-promotion` is **forward-only** for routine plan files (no constitutional
  doc edits; extract-verbatim is deterministic; chezmoi propagation is deterministic).
- `artifact-resurfacing` is **propose-not-apply** across the board (constitutional doc
  edits require conductor authorization; citation rewrites need taxonomic classification
  before action).

The risk profiles differ enough that conflating them would force the more-cautious
protocol on a class of operations that doesn't need it. Splitting keeps each skill's
defaults appropriate to its risk surface.

## When promotion creates citations that later go stale

A promoted plan file is cited from:
- Other plan files (`[[other-plan]]` style links)
- Memory entries (`[[memory-name]]` links)
- `CLAUDE.md` (at any scope)
- Future transcripts (the next session may reference the slug)

Over time, paths move. Repos restructure. The chezmoi runtime ↔ source mapping shifts.
When that happens, the citations to the promoted file become stale — exactly the regime
`artifact-resurfacing` handles.

Pattern: every promotion is a future drift candidate. The series register in
`engine-log-series.md` is the canonical-path anchor that `artifact-resurfacing`'s
Phase 4 (codify) recommends. If the file moves, update one row in the register; all
downstream citations can re-resolve through it.

## When resurfacing reveals promotion candidates

The inverse also happens. `artifact-resurfacing` Phase 1 (detect) sometimes surfaces
"missing-but-lost" classifications where the content exists in a transcript that's
older than memory's reach. The deep-search command set in `artifact-resurfacing` Phase 3
includes grepping `~/.claude/projects/*/memory/`, but it doesn't grep the `.jsonl`
transcripts directly. When a missing-but-lost search returns "transcript has it, no plan
file mirrors it," the right next move is `transcript-promotion`, not citation-removal.

## Sequence for the combined motion

```
artifact-resurfacing Phase 1 — detect
  └─ finding: "CLAUDE.md cites ~/Workspace/foo.md (no such file)"
       └─ Phase 2 — classify
            └─ search hits: transcript has the content under that name
                 └─ reclassify: not missing-but-lost; promotion-candidate
                      └─ hand off to transcript-promotion
                           └─ promotion runs; plan file created at the cited path
                                └─ artifact-resurfacing finding closes as "promoted"
```

The two skills compose cleanly. The composition is documented in this file rather than
hard-wired into either skill, so each remains independently invokable.
