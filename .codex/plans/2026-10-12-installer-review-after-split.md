# Installer review repair after the Domus split

Date: 2026-10-12
Owner: 4444J99; execution: Codex
Scope: existing a-i--skills PR #43; coordinated private Domus PR #414.

## Accepted prerequisites

Limen registry PR #2854 is merged. Private routing PR #424 is merged at
c040244d1d5fa0b80dede6dc4d1d51ef963af49c. Public domus-genoma remains curated;
the original private repository is domus-genoma-private.

## Implementation

- Implement the advertised path command with clean stdout and validated release identity.
- Restore both current and previous after caught activation or rollback errors,
  including errors occurring after a pointer replacement.
- Preserve inventory checks on every MCP cache hit; run semantic validators only
  on a cache miss and invalidate cache on release changes.
- Apply one cache-exclusion policy to copied sources, generated bundles and locks.
- Carry explicit marketplace skipping through final generated-output validation.
- Resolve planner commands from the installed prefix, not the working directory.
- Pin existing workflow action versions to verified immutable commits and disable
  checkout credential persistence.

## Verification and acceptance

Use a private custody-staging copy of the standalone package as a source fixture,
replace differing runtime files with exact PR-head source, and verify remaining
canonical inputs against the GitHub tree. No new disposable Git checkout is made.
Run focused regressions, then the existing full suite with a 450-second deadline.
Existing real-catalog cases cover install, successful update and removal, failed
generation preservation, guarded rollback, and source-free package installation.

Submit one repaired exact head through the normal merge rail. Do not override
review rules, wait synchronously for CI, activate native consumers before the
accepted pair is available, delete retained data, or rewrite history.
Keep the original archive, interrupted prefix and dirty shared checkout intact.
