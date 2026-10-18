# Closeout corrective review dispositions

Owner: https://github.com/4444J99/limen/issues/2995
Implementation: a-i--skills PR52; parent reviewed head cd598b9e.
This record accompanies the substantive corrective implementation, not a CI-note loop.

All 19 remote review findings are accepted after source inspection. Duplicate
findings share their implementation and regressions.

| Finding | Disposition and evidence |
| --- | --- |
| Addendum after publication | Fixed: write summary addendum before publication/readback. |
| Overlay pre-push terminal claim | Fixed: pre-push preparation only; final check follows remote readback. |
| Quiet-session bypass | Fixed: measured ownership and repository predicate still required. |
| Inherited Git location variables (helper and fixture) | Fixed: scrub repository/index/object variables in every child environment; redirect regression. |
| Directory-target symlink (two reviews) | Fixed: hash link itself; direct and sibling guards exclude symlinks. |
| Bare worktree anchor | Fixed: no working-tree status for bare records; linked-worktree fixture. |
| Malformed obligation/response (two reviews) | Fixed: validate object shape and return structured unmeasured results. |
| Bounded subprocess wording | Fixed: forbid persistent/detached processes; allow bounded checker subprocesses. |
| Index-hidden content | Fixed: fingerprint assume-unchanged/skip-worktree entries without changing flags. |
| Ignored artifacts | Fixed: content-bound ignored-path inventory; changed content invalidates ownership. |
| Non-checked-out branch commits | Fixed: enumerate local branch refs and deduplicate commit obligations. |
| GitHub host mismatch | Fixed: every API read explicitly targets github.com. |
| Non-UTF8 Git paths | Fixed: filesystem decoding and escaped JSON hashing; raw Git-path regression on APFS. |
| Self remote | Fixed: reject filesystem remote resolving to the same common Git store. |
| Remote credentials | Fixed: strip userinfo/query/fragment from projected URLs and repository identities. |
| Repeated shared owner reads | Fixed: scope-bound cache per pass; refresh before the second pass. |

Fresh independent review additionally found executable Git filter/diff programs
and landed retained branches. Both accepted: active clean/process attributes and
gitlinks return UNMEASURED before status; cached diffs disable ext-diff/textconv.
Unused filter configuration remains measurable. Every nondefault retained local
branch remains an obligation even at a landed/base-equal tip. Three new witnesses
failed before these fixes. A final gitlink regression guards recursive status.

PR50 round-two substantive commit 84c9cf87 was compared directly. Its scoped
instruction discovery, Session Review heading, publication/handoff ordering,
effects metadata, generic-copy identity, concrete ORGANVM opt-in, remote/default
and squash evidence, quiet-session rule, overlay homing and transcript owner
requirements are implemented here. Its declared checker and retired plan-root
deferrals are implemented by this repair. CI receipts are removed from the
closeout changelog entry. Receipt-only commits are not replayed. Original refs,
PR48/50 and every Claude checkout remain preserved.

Limits: PR census covers open same-repository heads with a local branch; declare
remote-only/fork PR obligations explicitly. Filters/submodules remain visibly
unmeasured until separately scoped observation is available. This helper proves
ownership only; it never grants Limen session release or deletion authority.
Installation and native discovery remain under #2995/#2999 after merge.
