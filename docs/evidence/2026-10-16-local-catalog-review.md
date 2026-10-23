# Local catalog review validation

## Current validation - 23 October 2026

Validation: 38 focused unittest cases pass on Linux / CPython 3.12.14. This
includes the five previously open race, overlap, alias and preview findings,
plus separate aggregate-catalog limits and per-source permission failures.
The latter regressions failed against published head
`b4a767a860f6a6769419d79f48aa74f4834afcc4` before the follow-up correction.

The aggregate catalog bound is enforced before staged publication and by both
readers. An inaccessible root preserves successfully captured source packages
and reports incomplete coverage. The usage guide now distinguishes runtime
pruning from ordinary collection roots. The earlier 23-test planning record
is unchanged.

The private 715-object inventory was not available or reverified in this
continuation. Its older result below remains dated historical evidence.
Hosted checks on each new commit and eligible approving review are separate
gates; this local result does not assert merge or runtime activation.

## Historical validation - 16 October 2026

All published findings on the original implementation were checked against the
current code. Corrections cover inert index values, bounded enumeration, typed
input, atomic snapshot publication, explicit collection roots and blank paths,
coverage-aware search, complete link event assertions, failed-object cleanup,
occurrence references, metadata/package consistency, actual-byte limits, and
review-event path search.

Validation: 28 focused unittest cases pass, including injected publication/copy
failures, source metadata churn, malformed inputs, package byte accounting, and
review-only path discovery. The existing private 715-object snapshot was also
independently rehashed with no failures or orphan objects; incomplete source
coverage remains explicitly false for overall verification.

The PR requires independent approving review under the existing branch rule.
There is no self-approval, rule change, or administrative bypass. A prior exact
head submission was deferred for missing lifecycle classification; delivery
classification has since been added. Source corrections change the head, which
will receive its one normal submission. Landing remains distinct from runtime
installation and retirement acceptance.
