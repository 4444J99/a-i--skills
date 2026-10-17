# Genesis Case Study — 2026-05-17 — Praxis-Perpetua Resurfacing

The session that built this skill. Read alongside `../SKILL.md` to see the four-phase protocol applied to its own birth.

## Session shape

- **Working directory**: `/Users/4jp/Workspace/4444J99/application-pipeline`
- **Branch**: `main`
- **Phase**: RESEARCH-DELIVERED → SKILL-BUILT
- **Conductor request 1 (plan mode, prior turn)**: "Where on my local drive is the grading, auditing, norming, so forth institution we developed?"
- **Conductor request 2 (plan mode, this turn)**: "Find all plans, transcripts, sessions, everything associated with this domain."
- **Conductor request 3 (closeout)**: "/closeout"
- **Conductor request 4 (handoff)**: "/cross-agent-handoff"
- **Conductor request 5 (skill creation)**: "take the meta process — sunken buried bodies for resurfacing — polishing, future fixed"

This is the request that named the skill.

## Phase 1 — Detect

The inventory plan at `~/.claude/plans/where-on-my-local-enchanted-meerkat.md` enumerated the institutional-authority domain across nine sections (A through I). The detection step surfaced four classes of drift:

### Finding 1.1 — Stale citation: praxis-perpetua workspace path

Pipeline `CLAUDE.md` "Academic & Institutional Context" section cited:

```
meta-organvm/praxis-perpetua/research/dissertation-institutional-authority/
```

Verification:

```bash
test -d ~/Workspace/meta-organvm/praxis-perpetua/research/dissertation-institutional-authority/
# returns false

ls ~/Workspace/meta-organvm/praxis-perpetua/
# AGENTS.md, CLAUDE.md, GEMINI.md, sessions/ — a 4-file stub

ls ~/Code/organvm/praxis-perpetua/research/dissertation-institutional-authority/ | wc -l
# 13 — the dissertation is there
```

**Class**: stale-citation. Polishable.

### Finding 1.2 — Cross-scope stale citation

Pipeline-scope `MEMORY.md` (`~/.claude/projects/-Users-4jp-Workspace-4444J99-application-pipeline/memory/MEMORY.md`) inherits the same wrong path via the "Academic & Institutional Context" block.

**Class**: stale-citation (second instance — same drift, different scope). The pattern crosses the ≥2-scope threshold for Phase 4 compound-pattern codification.

### Finding 1.3 — Three missing-but-probably-never-written papers

Pipeline `CLAUDE.md` cited:

```
organvm-v-logos/public-process/research/2026-03-15-ai-as-psychometrician.md
meta-organvm/praxis-perpetua/research/2026-03-15-institutional-immune-system.md
meta-organvm/praxis-perpetua/research/2026-03-15-self-governing-institution-of-checks.md
```

Verification:

```bash
find /Users/4jp -name "*psychometrician*" \
  -o -name "*institutional-immune-system*" \
  -o -name "*self-governing-institution*" \
  2>/dev/null | grep -v node_modules
# zero hits

grep -rl "psychometrician\|institutional-immune-system\|self-governing-institution" \
  ~/.claude/projects/*/memory/*.md 2>/dev/null
# zero hits in cross-scope memory
```

Deep-search would continue into `prompt-corpus/` (356 files) and `content-pipeline/` (386 files) in praxis-perpetua. The genesis session deferred deep-search as out-of-scope. Pending that search, the working classification is **missing-but-probably-never-written** — the papers were planned in CLAUDE.md but never written.

**Class**: missing-but-probably-never-written (provisional, pending deep-corpus search).

### Finding 1.4 — Orphan plans

The inventory found 21 active + 18 archived plans in `~/.claude/plans/` matching domain keywords. Of those, the plan `where-on-my-local-enchanted-meerkat.md` (created mid-session) lacks DONE-NNN / IRF-XXX-NNN markers.

**Class**: orphan-plan (provisional). The session's `/closeout` reclassified it as **DELIVERED-RESEARCH** — a class that does not require a closure ID because the document IS the deliverable. Per the composition-with-closeout protocol, the closeout's classification wins.

## Phase 2 — Classify

Summary table (the four-column finding output):

| artifact | cited-at | status | candidate-action |
|---|---|---|---|
| `meta-organvm/praxis-perpetua/research/dissertation-institutional-authority/` | pipeline `CLAUDE.md` + pipeline-scope `MEMORY.md` | stale | rewrite prefix to `~/Code/organvm/praxis-perpetua/` |
| `2026-03-15-ai-as-psychometrician.md` | pipeline `CLAUDE.md` | missing-probably-never-written | annotate as planned; propose IRF row |
| `2026-03-15-institutional-immune-system.md` | pipeline `CLAUDE.md` | missing-probably-never-written | annotate as planned; propose IRF row |
| `2026-03-15-self-governing-institution-of-checks.md` | pipeline `CLAUDE.md` | missing-probably-never-written | annotate as planned; propose IRF row |
| `where-on-my-local-enchanted-meerkat.md` | (the plan itself) | orphan | hand to closeout → reclassified DELIVERED-RESEARCH |

## Phase 3 — Polish (proposed, deferred to conductor)

The genesis session did NOT apply any polish actions — discovery ≠ remediation. All five findings were surfaced as proposed actions in the closeout doc (`~/.claude/plans/closeout-2026-05-17-plugin-surface-reconciliation.md`) and handoff doc (`~/.claude/plans/2026-05-17-handoff-plugin-surface-reconciliation.md`).

Sample proposal that would be emitted by `scripts/propose-citation-fix.py`:

```diff
--- a/Users/4jp/Workspace/4444J99/application-pipeline/CLAUDE.md
+++ b/Users/4jp/Workspace/4444J99/application-pipeline/CLAUDE.md
@@ -300,5 +300,5 @@
-- Authority dissertation: `meta-organvm/praxis-perpetua/research/dissertation-institutional-authority/`
-- Supporting docs: `meta-organvm/praxis-perpetua/research/2026-03-15-institutional-immune-system.md`, `2026-03-15-self-governing-institution-of-checks.md`
-- Journal paper (Doc A): `organvm-v-logos/public-process/research/2026-03-15-ai-as-psychometrician.md`
+- Authority dissertation: `~/Code/organvm/praxis-perpetua/research/dissertation-institutional-authority/`
+- Supporting docs: `~/Code/organvm/praxis-perpetua/research/2026-03-15-institutional-immune-system.md` (planned — not yet written as of 2026-05-17), `2026-03-15-self-governing-institution-of-checks.md` (planned — not yet written as of 2026-05-17)
+- Journal paper (Doc A): `organvm-v-logos/public-process/research/2026-03-15-ai-as-psychometrician.md` (planned — not yet written as of 2026-05-17)
```

The conductor sees this diff and decides:

- Apply the stale-path correction immediately (the dissertation IS at the new path; correction is uncontroversial)
- Apply the annotation for the three missing papers, OR initiate a separate research task to write them
- Either decision becomes a polish-log entry

## Phase 4 — Codify (proposed)

Compound-pattern triggers fired by this session's findings:

- **Same stale-citation in ≥2 scopes** (Finding 1.1 + 1.2): propose updating workspace `CLAUDE.md` autogen footer to assert the canonical `~/Code/organvm/praxis-perpetua/` path. Verification: the workspace `CLAUDE.md` autogen footer already cites `/Users/4jp/Code/organvm/praxis-perpetua/library` correctly (line 222 of `~/Workspace/CLAUDE.md`). The autogen knows the truth; only the body lags. The codification is to *re-derive* the body's references from the autogen source rather than to write the body manually.

- **Cross-scope memory drift**: propose writing a `reference_praxis_perpetua_canonical_path.md` memory at the workspace scope (`~/.claude/projects/-Users-4jp-Workspace/memory/`) so all 107 sibling scopes can grep-find the canonical path via the cross-scope grep pattern documented in `~/CLAUDE.md`.

Proposed IRF rows (NOT yet written to `INST-INDEX-RERUM-FACIENDARUM.md`):

```yaml
- id: IRF-DOM-NNN  # next available
  title: "Pipeline CLAUDE.md + MEMORY.md cite stale praxis-perpetua workspace path"
  status: open
  domain: DOM
  surfaced_by: artifact-resurfacing
  resurfacing_session: 2026-05-17-plugin-surface-reconciliation
  action_required: Apply citation-fix diff to ~/Workspace/4444J99/application-pipeline/CLAUDE.md and pipeline-scope MEMORY.md
  authorization_required_from: conductor

- id: IRF-LOG-NNN  # next available
  title: "Three 2026-03-15 papers cited in pipeline CLAUDE.md never written"
  status: open
  domain: LOG
  surfaced_by: artifact-resurfacing
  resurfacing_session: 2026-05-17-plugin-surface-reconciliation
  action_required: Either annotate citations as planned-but-unwritten, or initiate writing
  authorization_required_from: conductor
```

## What this case study demonstrates

1. **Discovery ≠ remediation, applied recursively.** The session that built the skill is itself a worked example of the skill's discipline. Five findings; zero auto-applied edits; all surfaced as proposals.

2. **Composition with closeout works.** Closeout's plan classifier handled Finding 1.4 (orphan-plan → DELIVERED-RESEARCH). Artifact-resurfacing did not duplicate the closure decision.

3. **The four-class taxonomy holds.** Every finding from the genesis session fit cleanly into one of the four classes. No class-5 escape hatch was needed.

4. **Codification flows from compound patterns.** Findings 1.1 and 1.2 are the same drift in two scopes — that's exactly the trigger for Phase 4's autogen-footer propagation rule. The compound-pattern rule earned its keep on the skill's first run.

5. **The plan file is itself an example.** `~/.claude/plans/where-on-my-local-enchanted-meerkat.md` Phase 2 contains the plan-of-record for this skill. It is both the skill's blueprint AND a Finding 1.4 orphan candidate AND (via closeout) a DELIVERED-RESEARCH artifact. The plan is a kind of artifact that this skill exists to handle.

## What this case study deferred

- Deep-search of `prompt-corpus/` (356 files) and `content-pipeline/` (386 files) in praxis-perpetua for the three missing papers. Tracked as a follow-up in the handoff doc. The deep-search would reclassify the three papers from Class 2 (missing-never-written) to either Class 1 (stale-citation, if drafts exist) or confirm Class 2.

- Writing the canonical-path memory at the workspace scope. The proposal is recorded; the write requires conductor authorization.

- Applying any of the proposed diffs. All deferred to next session per the closeout's universal-format block: "Authorized actions remaining: 0 — no auth was given for any of the flagged follow-ups."

## Reading order

To re-enter this case study cold, read in this order:

1. `~/.claude/plans/2026-05-17-handoff-plugin-surface-reconciliation.md` — what the next agent needs to know
2. `~/.claude/plans/where-on-my-local-enchanted-meerkat.md` — the inventory + skill plan
3. `~/.claude/plans/closeout-2026-05-17-plugin-surface-reconciliation.md` — the closeout summary
4. `~/Code/organvm/a-i--skills/skills/tools/artifact-resurfacing/SKILL.md` — the protocol that codifies the lesson
5. This file — the worked example proving the protocol against its own genesis
