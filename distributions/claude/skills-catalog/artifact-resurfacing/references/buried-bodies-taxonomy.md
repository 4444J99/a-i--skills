# Buried-Bodies Taxonomy

The four classes of drift that this skill resurfaces, each with worked examples drawn from the genesis session (2026-05-17). Read alongside `../SKILL.md` Phase 2 (Classify).

The taxonomy is **mutually exclusive at the level of action**. A finding may be ambiguous between two classes during detection (`Phase 1`); classification (`Phase 2`) resolves the ambiguity by escalation to the conductor rather than by guess.

## Class 1 — Stale-citation

**Definition**: The artifact named by a citation exists on disk, but the path in the citation points at a different location.

**Detection signal**: `test -f <cited-path>` returns false; `find / -name "<basename-of-cited-path>"` returns one or more hits at a different prefix.

**Why it accumulates**: Repos move between organs. Workspaces split. A skill is developed under `~/Workspace/meta-organvm/<repo>/`, later canonicalized at `~/Code/organvm/<repo>/`, but the constitutional docs (`CLAUDE.md`, `MEMORY.md`) that cite it lag behind. Each new session that consults the stale CLAUDE.md inherits the wrong location.

**Polish action**: emit a unified diff via `scripts/propose-citation-fix.py`. The diff rewrites the citation's prefix while preserving filename. The conductor reviews and applies.

**Worked example (genesis)**: Pipeline `CLAUDE.md` "Academic & Institutional Context" section cited:

```
meta-organvm/praxis-perpetua/research/dissertation-institutional-authority/
```

`test -d ~/Workspace/meta-organvm/praxis-perpetua/research/dissertation-institutional-authority/` returned false. The path resolved at `~/Code/organvm/praxis-perpetua/research/dissertation-institutional-authority/` (13 dissertation chapters, all present). The polish: rewrite the prefix from `meta-organvm/` to `~/Code/organvm/`. The conductor authorizes the diff; the skill emits but does not apply it.

**Anti-pattern to avoid**: rewriting the citation in the same session that surfaced the drift, without explicit conductor authorization. Discovery ≠ remediation. The conductor may have a reason the old path is still relevant (a migration in progress, a stub being preserved for reference).

## Class 2 — Missing-but-probably-never-written

**Definition**: A citation names an artifact that has never been created. No on-disk version exists; no commit history references it; no cross-scope memory contains a draft.

**Detection signal**: `find /Users/4jp -name "<basename>*"` returns nothing; `grep -r "<artifact-keyword>" ~/.claude/projects/*/memory/*.md` returns nothing; `git log --all --grep="<keyword>"` across plausible repos returns nothing.

**Why it accumulates**: A planning document or a CLAUDE.md is written in *prospective* mode — naming an artifact that is intended to be written but has not yet been written. The intention is sound; the planning notation outpaces the execution. The citation persists across compactions and becomes load-bearing in later memory.

**Polish action**: do NOT reconstruct the artifact. Emit an annotation diff that marks the citation as planned-but-unwritten with a date stamp. Optionally, propose an IRF row capturing the writing-task.

**Worked example (genesis)**: Pipeline `CLAUDE.md` cited three 2026-03-15 papers:

```
organvm-v-logos/public-process/research/2026-03-15-ai-as-psychometrician.md
meta-organvm/praxis-perpetua/research/2026-03-15-institutional-immune-system.md
meta-organvm/praxis-perpetua/research/2026-03-15-self-governing-institution-of-checks.md
```

`find /Users/4jp -name "*psychometrician*" -o -name "*institutional-immune-system*" -o -name "*self-governing-institution*" 2>/dev/null | grep -v node_modules` returned zero hits. Cross-scope memory grep returned zero hits. The papers were planned in CLAUDE.md but never written.

The polish proposed:

```diff
- - Journal paper (Doc A): `organvm-v-logos/public-process/research/2026-03-15-ai-as-psychometrician.md`
+ - Journal paper (Doc A): `organvm-v-logos/public-process/research/2026-03-15-ai-as-psychometrician.md` (planned — not yet written as of 2026-05-17; tracked in IRF-LOG-NNN)
```

Plus an IRF row proposal for each unwritten paper. Conductor authorizes both edits.

**Anti-pattern to avoid**: writing the missing paper in the same session, without conductor go-ahead. Reconstruction is a separate research task, not a polish.

## Class 3 — Missing-but-lost

**Definition**: A citation names an artifact whose creation history exists (in a session transcript, an old commit, a cross-scope memory file), but the artifact itself is not present at any known path.

**Detection signal**: `find` for the basename returns nothing on the standard tree, BUT cross-scope memory or git history contains evidence of the artifact's prior existence.

**Why it accumulates**: Files are written into a directory that is later moved or deleted. A session writes a draft, the workstream pivots, the draft is removed without updating the citing CLAUDE.md. The artifact was real; the artifact is gone; the citation persists.

**Polish action**: emit deep-search commands first (`prompt-corpus/`, `content-pipeline/`, `~/.claude/projects/*/memory/`, all sibling scopes). If the search returns hits, the finding **reclassifies as stale-citation** and runs the citation-fix proposer. If the search exhausts and returns zero, the finding **reclassifies as missing-but-probably-never-written** and the annotation proposer runs. The class is transitional; it resolves into one of the other two.

**Worked example (hypothetical, not from genesis)**: A CLAUDE.md cites `docs/architecture/2026-03-01-system-overview.md`. The file does not exist at that path. A grep across `~/Code/organvm/praxis-perpetua/prompt-corpus/` finds a session transcript referencing the file's content; another grep against `~/.claude/projects/*/memory/` finds a project-memory describing the file. The artifact exists somewhere — it was real. Deep search continues until either the file is found (→ stale-citation) or all corpora are exhausted (→ missing-never-written).

**Anti-pattern to avoid**: declaring a missing-but-lost artifact "lost" after a single `find` against the home tree. The 742-file praxis-perpetua `prompt-corpus/` + `content-pipeline/` corpus is exactly the kind of deep directory that needs explicit search before declaring loss.

## Class 4 — Orphan-plan

**Definition**: A plan file in `~/.claude/plans/` (or repo-local `.claude/plans/`) lacks any closure marker (no `DONE-NNN`, no `IRF-XXX-NNN`, no `DELIVERED-RESEARCH` annotation), and is older than the most recent session.

**Detection signal**: `grep -l "DONE-\|IRF-" <plan-file>` returns nothing; mtime is older than the current session's start.

**Why it accumulates**: Plans are authored frequently (one per planning session). Plans are closed rarely (a closure ritual exists in `closeout` but is not always invoked). The closeout SKILL.md cites a 90.4% global orphan rate.

**Polish action**: do NOT classify here. Hand the plan path to `closeout`'s classifier with a request to label it (EXECUTED / IN-PROGRESS / ABANDONED / DELIVERED-RESEARCH). The conductor confirms the label. This skill does not assign closure marks; it surfaces orphans for closeout to process.

**Worked example (genesis)**: The plan file `~/.claude/plans/where-on-my-local-enchanted-meerkat.md` lacks DONE-NNN / IRF-XXX-NNN markers. The genesis session's closeout classified it as **DELIVERED-RESEARCH** (a class that does not require a closure ID — the document IS the deliverable). This skill would have surfaced it as orphan-candidate; closeout's classifier resolved it.

**Anti-pattern to avoid**: bulk-classifying orphans as ABANDONED and moving them to `~/.claude/plans/abandoned/`. Memory rule #53: atoms are permanent, only the human closes. Plans-as-artifacts inherit the same discipline.

## Class boundaries — escalation rules

When a finding ambiguates between two classes, escalate to the conductor with the evidence rather than guessing:

| Ambiguity | Escalation |
|---|---|
| Stale-citation vs missing-lost (path doesn't exist, but `find` shows multiple plausible candidates) | Surface candidates; ask which is canonical |
| Missing-lost vs probably-never-written (deep search returns ambiguous hits — old session transcript mentions the title but not the content) | Surface the transcript reference; ask whether the artifact was ever written or only planned |
| Orphan-plan vs DELIVERED-RESEARCH (plan has no closure mark but its content reads as a delivered research artifact) | Surface plan + content excerpt; ask which classification applies |

Escalation is cheap. False classification corrupts the polish-log and future runs of this skill, which compounds.

## Why the taxonomy is exactly four classes

The four classes correspond to a 2×2 matrix:

|  | Artifact exists on disk | Artifact does not exist on disk |
|---|---|---|
| **Citation references a path** | Class 1 (stale-citation) | Class 2 or 3 (missing-never-written vs missing-lost) |
| **Citation references a closure state** | Class 4 (orphan-plan) | n/a — plans without closure marks default to Class 4 |

Class 3 (missing-lost) is the transitional state — it resolves into either Class 1 (the artifact was found elsewhere) or Class 2 (the artifact was never written). Including it as a distinct class is deliberate: the deep-search step is procedurally distinct from the immediate-classify steps for Classes 1 and 2.

The matrix is not extensible to a third dimension without changing the polish actions. If a future finding doesn't fit the matrix, the matrix needs revision — not a fifth class.

## Compound patterns (Phase 4 codification triggers)

When the same finding appears in multiple locations, the codification leg of the protocol fires:

- **Same stale-citation in ≥2 scopes** — autogen footer propagation. Update the workspace `CLAUDE.md` autogen block to assert the canonical path; the next `organvm refresh` re-writes it across sibling scopes.
- **Same missing-never-written across ≥3 sessions** — IRF row promotion. The drift is no longer ad-hoc; it's a known unwritten artifact and deserves a ledger entry.
- **Same orphan-plan class in ≥5 plans** — closeout SKILL.md update. The class is common enough to warrant auto-recognition.
- **Cross-scope memory drift for the same domain** — workspace-scope `reference_<topic>_canonical_path.md`. One memory entry queryable from all sibling scopes via the cross-scope grep pattern documented in `~/CLAUDE.md`.

Codification is what turns this skill from a one-shot polish into a system that learns from its own findings.
