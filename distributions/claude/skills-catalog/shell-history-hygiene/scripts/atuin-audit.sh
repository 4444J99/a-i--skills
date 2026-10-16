#!/usr/bin/env bash
# atuin-audit.sh — dry-run hygiene audit for atuin shell history.
#
# Produces two dated preview artifacts alongside this script and prints a
# headline summary. Never applies changes — apply commands are echoed at the
# end for the human to copy-paste after inspecting the previews.
#
# Usage:
#   ./atuin-audit.sh                # dedup --before defaults to today
#   ./atuin-audit.sh 2026-05-01     # dedup --before <date>
#
# Replaces the one-liner shape `atuin ... | tee cmd > file.txt` which:
#   - wrote two identical files (cmd and file.txt),
#   - swallowed the dedup output from the terminal,
#   - left a junk file named `cmd` in cwd.

set -euo pipefail

STAMP="$(date +%F)"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BEFORE="${1:-$STAMP}"
PRUNE_OUT="$HERE/atuin-prune-preview-$STAMP.txt"
DEDUP_OUT="$HERE/atuin-dedup-preview-$STAMP.txt"

if ! command -v atuin >/dev/null 2>&1; then
  echo "error: atuin not on PATH" >&2
  exit 1
fi

echo "=== atuin stats today ==="
atuin stats today
echo

echo "=== prune preview -> $PRUNE_OUT ==="
atuin history prune --dry-run | tee "$PRUNE_OUT"
PRUNE_N="$(awk '/^Found [0-9]+ entries to prune\./{print $2; exit}' "$PRUNE_OUT")"
PRUNE_N="${PRUNE_N:-0}"
echo

echo "=== dedup preview (before $BEFORE, dupkeep 1) -> $DEDUP_OUT ==="
atuin history dedup --dry-run --before "$BEFORE" --dupkeep 1 > "$DEDUP_OUT"
DEDUP_N="$(awk '/^Found [0-9]+ duplicates to delete\./{print $2; exit}' "$DEDUP_OUT")"
DEDUP_N="${DEDUP_N:-0}"
DEDUP_LINES="$(wc -l < "$DEDUP_OUT" | tr -d ' ')"
echo "$DEDUP_N duplicates flagged ($DEDUP_LINES lines in preview, multi-line commands expand)"
echo

cat <<EOF
=== summary ===
  prune entries:    $PRUNE_N
  dedup duplicates: $DEDUP_N

=== to apply (only after inspecting previews) ===
  atuin history prune
  atuin history dedup --before "$BEFORE" --dupkeep 1
EOF
