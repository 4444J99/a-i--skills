#!/usr/bin/env bash
# audit-citations.sh
# Citation audit for artifact-resurfacing Phase 1 (Detect).
#
# Given a target file (CLAUDE.md, MEMORY.md, etc.), extract candidate file-path
# citations and check each against the filesystem. Emit one JSONL record per
# citation to stdout.
#
# Record schema:
#   { "cited": "<path-as-cited>",
#     "kind": "path" | "plan" | "id" | "url",
#     "exists": true | false,
#     "found_at": "<resolved-path-or-empty>",
#     "status": "present" | "stale" | "missing" | "unknown" }
#
# Discovery only. Never edits the target file. Run output is consumed by
# Phase 2 (Classify) in the SKILL.md protocol.
#
# Usage:
#   bash audit-citations.sh <path-to-target-file>
#
# Exits non-zero on argument error; exits 0 even when findings are stale (the
# findings are the deliverable, not the exit code).

set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "usage: $(basename "$0") <path-to-target-file>" >&2
  exit 2
fi

target="$1"
if [[ ! -f "$target" ]]; then
  echo "error: target file not found: $target" >&2
  exit 3
fi

emit() {
  local cited="$1" kind="$2" exists="$3" found_at="$4" status="$5"
  # Hand-rolled JSONL with field escaping for embedded quotes and backslashes.
  cited_esc=$(printf '%s' "$cited" | sed 's/\\/\\\\/g; s/"/\\"/g')
  found_esc=$(printf '%s' "$found_at" | sed 's/\\/\\\\/g; s/"/\\"/g')
  printf '{"cited":"%s","kind":"%s","exists":%s,"found_at":"%s","status":"%s"}\n' \
    "$cited_esc" "$kind" "$exists" "$found_esc" "$status"
}

# Extract path-like tokens from the target file. Heuristics:
#   - Tokens starting with ~/, /, or ./
#   - Tokens ending in .md, .yaml, .yml, .json, .py, .sh, .ts, .tsx, .js, .tex
#   - Tokens that look like a unix path with at least one slash
# We use grep -oE to surface candidates; classification follows.

candidates=$(grep -oE '(~|\.{1,2}|/)[A-Za-z0-9_./@:+-]+\.(md|yaml|yml|json|py|sh|ts|tsx|js|tex|txt|html)' "$target" 2>/dev/null | sort -u || true)

# Also surface bare directory paths (no extension) that look anchored.
dir_candidates=$(grep -oE '(~|\.{1,2}|/)[A-Za-z0-9_./@:+-]+/' "$target" 2>/dev/null | sort -u || true)

# Process file-with-extension candidates.
while IFS= read -r citation; do
  [[ -z "$citation" ]] && continue
  # Expand ~ to $HOME.
  expanded="${citation/#~/$HOME}"

  if [[ -e "$expanded" ]]; then
    emit "$citation" "path" "true" "$expanded" "present"
    continue
  fi

  # Attempt to find by basename across canonical roots.
  basename=$(basename "$expanded")
  found=$(find "$HOME/Workspace" "$HOME/Code" "$HOME/.claude" -maxdepth 6 -name "$basename" 2>/dev/null | head -1 || true)
  if [[ -n "$found" ]]; then
    emit "$citation" "path" "false" "$found" "stale"
  else
    emit "$citation" "path" "false" "" "missing"
  fi
done <<< "$candidates"

# Process directory candidates (trailing slash).
while IFS= read -r citation; do
  [[ -z "$citation" ]] && continue
  expanded="${citation/#~/$HOME}"
  expanded="${expanded%/}"

  if [[ -d "$expanded" ]]; then
    emit "$citation" "path" "true" "$expanded" "present"
    continue
  fi

  # For directories, look up by last segment.
  last_seg=$(basename "$expanded")
  found=$(find "$HOME/Workspace" "$HOME/Code" -maxdepth 5 -type d -name "$last_seg" 2>/dev/null | head -1 || true)
  if [[ -n "$found" ]]; then
    emit "$citation" "path" "false" "$found" "stale"
  else
    emit "$citation" "path" "false" "" "missing"
  fi
done <<< "$dir_candidates"
