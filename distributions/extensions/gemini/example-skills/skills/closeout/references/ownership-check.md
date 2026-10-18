# Measured ownership check

The bundled `scripts/closeout_check.py` is the single fallback checker. It does not
replace repository predicates or Limen's session-release procedure. It never emits
the terminal closeout statement or claims task completion/deletion eligibility.

Use a projection of the session's existing owner records as input. Do not establish
another task registry. Preserve the native session identity and actual repository
roots. An opening base must be a full commit hash proven in a live published
baseline branch; `base_ref` defaults to the remote's measured default branch.

```json
{
  "schema": "closeout.evidence.v1",
  "session_id": "native-session-id",
  "scopes": [
    {"id": "code", "root": "/actual/repository", "base": "FULL_OPENING_COMMIT_HASH"}
  ],
  "non_file_obligations": [],
  "owners": {}
}
```

Supply `remote` explicitly if there are multiple remotes without a usable tracking
remote. The helper discovers the real default using live `git ls-remote --symref`.
Missing upstreams are reported explicitly and never treated as proof of publication.
A feature-branch opening base may name its published `base_ref: refs/heads/topic`.

Run `inventory --evidence PATH` to obtain current item IDs and content fingerprints.
Inventory exit 0 means collection succeeded; it does **not** prove ownership. Include
inline deliverables, promised actions and other non-file obligations in
`non_file_obligations`, each with `id`, `scope`, and substantive `description`.
All observed commits, files, stashes and retained worktrees need owners or evidenced
exclusions. Sibling worktree dirty content is fingerprinted without adopting it.

Map each item ID in `owners` to an evidence reference and its current `fingerprint`:

- `git-record`: `ref` is an existing published branch ref; `path` is a JSON record
  in that branch's actual durable owner. The exact live remote tip is read, and its
  content is read from the matching immutable local Git object. Fetch before
  checking if that object is unavailable; the checker never fetches or writes Git.
- `github-issue` or `github-pr`: `number` identifies the open owner on this scope's
  actual GitHub repository. Authenticated `gh api` reads its body. Include a JSON
  record/list between `<!-- closeout-owner`, a newline, and a newline plus `-->`.
- `landed`: valid for a commit item. Verify ancestry to the live default tip.
  For a squash landing, include `pull_request`: authenticated repository-qualified
  PR metadata must show merged, its commit list must contain the original commit,
  and the landed commit must be on the measured remote default.

A durable record (or one entry in a JSON list) has this shape:

```json
{
  "binding": {
    "session_id": "native-session-id",
    "repository": "github.com/owner/repository",
    "item_id": "exact inventory item ID",
    "fingerprint": "exact inventory fingerprint"
  },
  "disposition": "owned",
  "owner": "existing tracker or plan owner",
  "next_action": "concrete next action or acceptance predicate"
}
```

For a remote evidenced exclusion, set the reference and record disposition to
`excluded`, with `rationale` and a different `source_session`. Also provide
`source_evidence`, a supported remote reference to that session's owned record
bound to this same repository, item and fingerprint. A source-session label alone
is insufficient. Spoken blockers, unpublished handoffs and caller success flags
do not establish ownership.

Run `check --evidence PATH --twice`. Exit 0 means every measured obligation is owned;
1 means dangling/stale ownership; 2 means incomplete measurement (including missing,
unsupported or inaccessible evidence). Two passes must have identical inventory,
input evidence and remote readback fingerprints, with `passes: [0, 0]` and
`stable: true`. Repository session predicates remain additional authority.

Publish and read back any newly changed handoff before this final check. Retain
unchanged code-verification receipts; successful inventory is never verification.
The helper disables optional Git index writes and local replace/graft effects.
All subprocess reads have a 30-second timeout. Evidence input is an observation
projection, and must itself be homed if the session produced it as an artifact.
