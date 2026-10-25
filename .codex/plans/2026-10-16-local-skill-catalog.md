# Local skill consolidation

Request: make Claude Insights available and amalgamate/housekeep local agent skills.

The current catalog authority is `4444J99/a-i--skills`, based on main commit
`9badcce43805ea43141c1997eea10a133607f61e`. Local runtime stores, plugin caches,
synced copies, project-owned skills, and inactive worktree variants require a
separate private machine inventory; they must not be imported wholesale into the
public distribution.

Implementation:

1. Inventory explicit local roots, aliases, missing paths, and complete packages.
2. Build a new content-addressed snapshot with one verified copy per distinct
   eligible package, all source occurrences, and visible review-only entries.
3. Test duplicate identity, resource variants, link handling, overlap refusal,
   and post-copy integrity with isolated fixtures.
4. Publish only generic tooling and documentation here. Preserve machine evidence
   privately. Keep live activation distinct from source publication.

Insights discovery: Claude `/insights` is built in. An existing `vendor-insights`
skill and implementation in the owning runtime repository can be catalogued with
their required working directory; an additional report engine is unnecessary.

Live cutover owner: the host configuration owner, with writable access to agent
runtime roots and its managed source. The current session can read those roots
but cannot modify them. Acceptance for a later cutover: dependency-complete
source selection, supported consumer activation, effective-path readback,
rollback custody, and no removal of distinct skills or vendor-managed state.

No automatic source deletion, permissions change, plugin uninstall, or scheduling
is part of this implementation.
