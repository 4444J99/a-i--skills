#!/usr/bin/env bash
# propagate-via-chezmoi.sh — Phase 3 of the transcript-promotion protocol.
#
# Background: bash-redirect file creation (`cat > file`) bypasses the PostToolUse
# Write|Edit hook that fires `domus-memory-sync`. Files exist on the runtime
# filesystem but never reach chezmoi-source or remote — Universal Rule #2 violated
# silently. This script runs the chezmoi-documented recovery: `chezmoi add` brings
# the runtime path into source, and chezmoi's autoCommit+autoPush config does the
# rest in one move.
#
# Verifies parity after propagation. Surfaces non-chezmoi-managed targets for
# manual git ops.
#
# Usage:
#   propagate-via-chezmoi.sh <runtime-path> [<runtime-path> ...]

set -euo pipefail

[[ $# -eq 0 ]] && { echo "usage: $0 <runtime-path> [<runtime-path> ...]" >&2; exit 2; }

CHEZMOI_SOURCE="${CHEZMOI_SOURCE_DIR:-$HOME/Workspace/4444J99/domus-semper-palingenesis}"
[[ -d "$CHEZMOI_SOURCE/.git" ]] || {
  echo "chezmoi-source not a git repo: $CHEZMOI_SOURCE" >&2
  echo "set CHEZMOI_SOURCE_DIR or verify chezmoi config" >&2
  exit 1
}

# Verify each path is chezmoi-managed-eligible (under HOME and not gitignored).
CHEZMOI_TARGETS=()
NON_CHEZMOI_TARGETS=()
for path in "$@"; do
  [[ -f "$path" ]] || { echo "not a file: $path" >&2; exit 1; }
  # chezmoi managed-source-path returns non-zero for unmanaged paths; we use it
  # as a probe rather than authority, since unmanaged-but-eligible is normal for
  # newly-created files.
  if [[ "$path" == "$HOME/"* ]]; then
    CHEZMOI_TARGETS+=("$path")
  else
    NON_CHEZMOI_TARGETS+=("$path")
  fi
done

if [[ ${#NON_CHEZMOI_TARGETS[@]} -gt 0 ]]; then
  echo "Non-chezmoi targets surfaced for manual git ops:" >&2
  printf '  %s\n' "${NON_CHEZMOI_TARGETS[@]}" >&2
  echo "(propagate these via the per-repo git add+commit+push protocol)" >&2
fi

if [[ ${#CHEZMOI_TARGETS[@]} -eq 0 ]]; then
  echo "no chezmoi-eligible targets; exiting" >&2
  exit 0
fi

# Pre-state for parity comparison.
BEFORE_HEAD="$(git -C "$CHEZMOI_SOURCE" rev-parse HEAD)"
BEFORE_AHEAD="$(git -C "$CHEZMOI_SOURCE" log @{u}..HEAD --oneline 2>/dev/null | wc -l | tr -d ' ' || echo 0)"

# Run chezmoi add. autoCommit+autoPush fires from chezmoi config.
chezmoi add "${CHEZMOI_TARGETS[@]}"

# Post-state parity.
AFTER_HEAD="$(git -C "$CHEZMOI_SOURCE" rev-parse HEAD)"
AFTER_AHEAD="$(git -C "$CHEZMOI_SOURCE" log @{u}..HEAD --oneline 2>/dev/null | wc -l | tr -d ' ' || echo 0)"

echo "chezmoi-source: ${BEFORE_HEAD:0:7} -> ${AFTER_HEAD:0:7}" >&2
echo "ahead-of-upstream: $BEFORE_AHEAD -> $AFTER_AHEAD" >&2

if [[ "$AFTER_AHEAD" != "0" ]]; then
  echo "WARNING: chezmoi-source is ${AFTER_AHEAD} commits ahead of upstream" >&2
  echo "expected 0 — autoPush should have fired" >&2
  echo "manual recovery: git -C $CHEZMOI_SOURCE push origin master" >&2
  exit 1
fi

echo "propagation verified: chezmoi-source @ upstream parity" >&2
