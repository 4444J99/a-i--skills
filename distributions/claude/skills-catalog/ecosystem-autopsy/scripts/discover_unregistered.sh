#!/usr/bin/env bash
# discover_unregistered.sh — list git repositories on disk that are NOT
# present in `organvm ecosystem list` output.
#
# Usage:
#   bash discover_unregistered.sh PATH [PATH ...]
#
# Output: one absolute path per line, sorted, deduplicated.
#
# This is the one piece of net-new value over the canonical
# `organvm ecosystem list`: it surfaces git repos the registry does not
# yet know about. Everything else this skill needs already exists in the
# `organvm` CLI — see ../SKILL.md "Authority boundary".

set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "usage: $0 PATH [PATH ...]" >&2
  exit 2
fi

if ! command -v organvm >/dev/null 2>&1; then
  echo "error: organvm CLI not on PATH — cannot determine registered set" >&2
  exit 3
fi

registered_repos="$(mktemp)"
trap 'rm -f "$registered_repos"' EXIT

organvm ecosystem list 2>/dev/null \
  | awk '{print $1}' \
  | grep -v '^$' \
  | sort -u > "$registered_repos"

for path in "$@"; do
  if [[ ! -d "$path" ]]; then
    echo "skip: $path is not a directory" >&2
    continue
  fi

  find "$path" -type d -name .git -not -path '*/node_modules/*' -not -path '*/.venv/*' 2>/dev/null \
    | while read -r git_dir; do
        repo_root="$(dirname "$git_dir")"
        repo_name="$(basename "$repo_root")"
        if ! grep -Fxq "$repo_name" "$registered_repos"; then
          printf '%s\n' "$repo_root"
        fi
      done
done | sort -u
