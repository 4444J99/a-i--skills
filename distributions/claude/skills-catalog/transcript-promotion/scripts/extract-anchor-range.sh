#!/usr/bin/env bash
# extract-anchor-range.sh — verbatim slice of assistant text between two anchors.
#
# Phase 1 of the transcript-promotion protocol. The JSONL transcript is the canonical
# source; this script extracts a verbatim slice without re-authoring. Anchors are
# verified to exist before slicing (Universal Rule #12: memory is hypothesis).
#
# Usage:
#   extract-anchor-range.sh \
#     --jsonl <path-to-jsonl> \
#     --start-anchor <regex> \
#     [--end-anchor <regex>] \
#     --output <path>
#
# If --end-anchor is omitted, the slice runs to EOF of the assistant-text stream.

set -euo pipefail

JSONL=""
START_ANCHOR=""
END_ANCHOR=""
OUTPUT=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --jsonl)        JSONL="$2"; shift 2 ;;
    --start-anchor) START_ANCHOR="$2"; shift 2 ;;
    --end-anchor)   END_ANCHOR="$2"; shift 2 ;;
    --output)       OUTPUT="$2"; shift 2 ;;
    *) echo "unknown flag: $1" >&2; exit 2 ;;
  esac
done

[[ -z "$JSONL" || -z "$START_ANCHOR" || -z "$OUTPUT" ]] && {
  echo "missing required flag (--jsonl, --start-anchor, --output)" >&2
  exit 2
}
[[ -f "$JSONL" ]] || { echo "JSONL not found: $JSONL" >&2; exit 1; }

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

ASSISTANT_TEXT="$WORK/assistant_text.md"
jq -r 'select(.type=="assistant") | .message.content[]? | select(.type=="text") | .text' "$JSONL" > "$ASSISTANT_TEXT"

# Verify anchors exist before slicing — Universal Rule #12.
START_LINE="$(grep -n -E "$START_ANCHOR" "$ASSISTANT_TEXT" | head -1 | cut -d: -f1 || true)"
[[ -z "$START_LINE" ]] && {
  echo "start anchor not found in transcript: $START_ANCHOR" >&2
  echo "candidate headings nearby:" >&2
  grep -nE "^#|^##|^###" "$ASSISTANT_TEXT" | head -20 >&2
  exit 1
}

if [[ -n "$END_ANCHOR" ]]; then
  # End anchor must appear AFTER start anchor.
  END_LINE="$(awk -v s="$START_LINE" -v re="$END_ANCHOR" 'NR>s && $0 ~ re { print NR; exit }' "$ASSISTANT_TEXT")"
  [[ -z "$END_LINE" ]] && {
    echo "end anchor not found after start anchor: $END_ANCHOR" >&2
    exit 1
  }
  # Slice [START_LINE, END_LINE-1] inclusive.
  END_LINE=$((END_LINE - 1))
else
  END_LINE="$(wc -l < "$ASSISTANT_TEXT" | tr -d ' ')"
fi

sed -n "${START_LINE},${END_LINE}p" "$ASSISTANT_TEXT" > "$OUTPUT"

LINES_EXTRACTED=$((END_LINE - START_LINE + 1))
echo "extracted $LINES_EXTRACTED lines [$START_LINE..$END_LINE] from $JSONL" >&2
echo "output: $OUTPUT" >&2
