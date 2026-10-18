## Description

Successful Git inventory commands could previously produce a terminal closeout claim while unfinished work lacked durable owners. Add one bundled, read-only Python ownership checker with inventory/check operations and 0/1/2 outcomes. Repository predicates, including Limen's, retain session-release authority.

This branch includes PR #50 head 62214d3 plus its repair; #50's branch and Claude checkouts are preserved. Refs #50 and 4444J99/limen#2995. Companion Domus entry: 4444J99/domus-genoma-private#505.

## Type of Change

- [x] Bug fix in existing skill
- [x] Enhancement to existing skill
- [x] Documentation update

## Changes Made

- Bind files, commits, stashes, retained worktrees and declared non-file obligations to native session, repository identity and exact content.
- Read back pushed Git records and authenticated GitHub issue/PR records; reject unknown/stale ownership, unpublished handoffs, unsupported evidence and source-session labels without a source owner record.
- Prove the opening base against a live published branch. Support actual non-origin remotes, missing upstreams and repository-qualified squash landings.
- Disable Git optional index writes and replace/graft effects. Compare inventory, input and remote readback fingerprints across two fresh checks.
- Preserve .codex discovery and customized overlays; exclude documentation/bundled ORGANVM examples. Repair both companion durable-owner workflows and effects metadata.
- Regenerate all runtime distributions, metadata and executable modes.

## Testing

- Final helper regression file: 15 passed, including genuine local bare-remote readback, unpublished bases/handoffs, changed sibling worktrees, exclusions, squash evidence and local Git replacement attacks.
- Helper plus installation tests: 39 passed in 161 seconds.
- Skill/link validation: 167 passed.
- Generated-output validation: passed; Ruff and git diff --check passed.
- Fresh read-only review: accepted and fixed all five important findings (base provenance, sibling content, changed remote readback, exclusion provenance, Git replace refs).

## Checklist

- [x] Scope and review completed; documentation and examples updated.
- [x] Scripts executable, no secrets in source.
- [x] Generated directories included.
- [x] Limen canonical protocol remains unchanged.

## Delivery evidence

Plan published before implementation: fd38ddb. Implementation: 798005c.
Installed runtime remains unchanged until merged source is admitted through the existing installer. A native OpenCode API read returned an empty list and reported its working directory instead of the requested directory; this is not discovery acceptance (owner 4444J99/limen#2999).
