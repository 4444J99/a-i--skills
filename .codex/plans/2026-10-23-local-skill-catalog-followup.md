# Local catalog review follow-up

Continue the user-assigned PR46 corrections on the existing branch after
published head b4a767a860f6a6769419d79f48aa74f4834afcc4.

1. Reproduce aggregate catalogs incorrectly sharing the package-file read
   bound and an inaccessible source aborting the entire inventory.
2. Enforce a separate aggregate bound during staged publication and reads;
   retain successful sources when another root is inaccessible.
3. Document runtime-only pruning and the catalog limit, and add dated current
   evidence while preserving historical counts and private-inventory results.
4. Verify the focused suite, obtain independent review, then publish a normal
   fast-forward against the observed branch head. Approval, hosted checks,
   the normal merge rail, and host activation remain separate gates.

Regression evidence: three new test cases fail on the published implementation.
After correction all 38 focused tests pass on Linux / Python 3.12. No source
stores, private runtime inventories, or activation targets are modified.
