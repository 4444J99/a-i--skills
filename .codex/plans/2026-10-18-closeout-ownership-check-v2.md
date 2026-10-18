# Repository-agnostic closeout repair v2

Owner: https://github.com/4444J99/limen/issues/2995
Related: a-i--skills#50 and domus-genoma-private#505.

Implement one bundled read-only Python inventory/check helper with native session and repository/content binding, authenticated remote ownership readback, fail-closed missing evidence, and 0/1/2 outcomes. Preserve the generic core plus repository overlays, Limen delegation, and the existing ORGANVM ritual. Repair overlay discovery, actual remote/default handling, pre-push preparation, companion durable owners, and effects metadata. Test edge cases and regenerate distributions.

Domus owns template/fallback/discovery #2999; Limen owns plan-checker #2997. Reopen #2998 without claiming new billing diagnosis. Publish isolated repair branches, obey exact-head merge policy, install only merged source using existing rollback-capable installer, and apply Domus through chezmoi. Report merged/live/observed separately.

Isolation: reuse inactive clean Codex consolidation checkout on new fix/closeout-ownership-check-20261018; original PR46 branch retained. No Claude checkout or branch is written. No original artifacts or native state are deleted.

Verification: inventory/check regressions, overlay detection, non-origin/missing upstream/squash evidence, skill/link validation, generated output and installation tests; unchanged successful ownership check twice. Runtime and installation acceptance remain separate from branch tests.
