#!/usr/bin/env bash
# find-orphan-plans.sh
# Orphan-plan scan for artifact-resurfacing Phase 1 (Detect).
#
# Walk a glob of plan files (default: ~/.claude/plans/*.md) and check each for
# closure markers: DONE-NNN, IRF-XXX-NNN, or DELIVERED-RESEARCH annotations.
# Emit one JSONL record per plan to stdout.
#
# Record schema:
#   { "path": "<plan-path>",
#     "mtime": "<ISO-8601>",
#     "has_done_ref": true | false,
#     "has_irf_ref": true | false,
#     "has_delivered_research_marker": true | false,
#     "candidate_class": "executed" | "in_progress" | "delivered_research" | "orphan" }
#
# Discovery only. Never moves plan files. Closure classification is handed off
# to `closeout` per composition rules.
#
# Usage:
#   bash find-orphan-plans.sh [glob]
#
# Examples:
#   bash find-orphan-plans.sh
#   bash find-orphan-plans.sh '~/.claude/plans/2026-*.md'
#   bash find-orphan-plans.sh '~/Workspace/4444J99/application-pipeline/.claude/plans/*.md'

set -euo pipefail

glob="${1:-$HOME/.claude/plans/*.md}"
# Expand ~ in the glob if present.
glob="${glob/#~/$HOME}"

shopt -s nullglob
plans=( $glob )
shopt -u nullglob

if [[ ${#plans[@]} -eq 0 ]]; then
  echo "info: no plans matched glob: $glob" >&2
  exit 0
fi

for plan in "${plans[@]}"; do
  # Skip directories that may match (e.g., archive/).
  [[ -d "$plan" ]] && continue

  has_done="false"
  has_irf="false"
  has_delivered="false"

  if grep -qE 'DONE-[0-9]{3,}' "$plan" 2>/dev/null; then
    has_done="true"
  fi

  if grep -qE 'IRF-[A-Z]{3}-[0-9]{3}' "$plan" 2>/dev/null; then
    has_irf="true"
  fi

  if grep -qiE 'DELIVERED[-_ ]RESEARCH|DELIVERED:[[:space:]]*research' "$plan" 2>/dev/null; then
    has_delivered="true"
  fi

  if [[ "$has_done" == "true" ]]; then
    klass="executed"
  elif [[ "$has_irf" == "true" ]]; then
    klass="in_progress"
  elif [[ "$has_delivered" == "true" ]]; then
    klass="delivered_research"
  else
    klass="orphan"
  fi

  # mtime in ISO-8601 (portable across BSD/Linux date).
  if mtime=$(stat -f '%Sm' -t '%Y-%m-%dT%H:%M:%SZ' "$plan" 2>/dev/null); then
    :  # macOS BSD stat
  else
    mtime=$(stat -c '%y' "$plan" 2>/dev/null | head -c 19 | tr ' ' 'T' || echo "")
  fi

  path_esc=$(printf '%s' "$plan" | sed 's/\\/\\\\/g; s/"/\\"/g')
  printf '{"path":"%s","mtime":"%s","has_done_ref":%s,"has_irf_ref":%s,"has_delivered_research_marker":%s,"candidate_class":"%s"}\n' \
    "$path_esc" "$mtime" "$has_done" "$has_irf" "$has_delivered" "$klass"
done
