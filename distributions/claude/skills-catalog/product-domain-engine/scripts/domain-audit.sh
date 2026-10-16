#!/usr/bin/env bash
# domain-audit.sh — score a repository against the four rhetorical modes
#
# Usage:  domain-audit.sh /path/to/repo [--json]
# Output: scores + dominant mode + composition gaps
#
# Scoring is intentionally crude — it detects *presence* of mode signals,
# not their quality. A high score means "the surface area exists"; a human
# still has to judge whether the surface is dense or hollow.

# NOTE: pipefail intentionally not set — grep -v on empty input returns 1,
# which would kill the script on every directory that lacks a given category
# of files. This is a metrics script; partial counts are fine.
set -eu

REPO="${1:-.}"
FORMAT="text"
[[ "${2:-}" == "--json" ]] && FORMAT="json"

if [[ ! -d "$REPO" ]]; then
    echo "ERROR: $REPO is not a directory" >&2
    exit 1
fi

REPO=$(cd "$REPO" && pwd)
NAME=$(basename "$REPO")

# ─── LOGOS — internal skeleton ──────────────────────────────────
# Signals: types, tests, schemas, internal architecture, seed contract
logos_score=0
logos_evidence=()

if [[ -d "$REPO/src" ]] || [[ -d "$REPO/lib" ]]; then
    logos_score=$((logos_score + 1))
    logos_evidence+=("src/ or lib/ present")
fi

test_count=$(find "$REPO" -type f \
    \( -name "*.test.ts" -o -name "*.test.js" -o -name "*.test.tsx" \
    -o -name "*_test.py" -o -name "test_*.py" \
    -o -name "*.spec.ts" -o -name "*.spec.js" \) 2>/dev/null \
    | grep -v node_modules | wc -l | tr -d ' ')

if [[ $test_count -gt 0 ]]; then
    logos_score=$((logos_score + 1))
    logos_evidence+=("$test_count test files")
fi
if [[ $test_count -gt 100 ]]; then
    logos_score=$((logos_score + 1))
    logos_evidence+=("dense test coverage (>100)")
fi

if [[ -f "$REPO/seed.yaml" ]]; then
    logos_score=$((logos_score + 1))
    logos_evidence+=("seed.yaml present")
fi

# Type definitions / schemas
schema_count=$(find "$REPO" -type f \
    \( -name "*.d.ts" -o -name "schema*.json" -o -name "schema*.yaml" \
    -o -name "types.ts" -o -name "models.py" \) 2>/dev/null \
    | grep -v node_modules | wc -l | tr -d ' ')
if [[ $schema_count -gt 0 ]]; then
    logos_score=$((logos_score + 1))
    logos_evidence+=("$schema_count type/schema files")
fi

# ─── ETHOS — external credibility ───────────────────────────────
# Signals: research, citations, deployment, flagship README, CI
ethos_score=0
ethos_evidence=()

readme_lines=0
if [[ -f "$REPO/README.md" ]]; then
    readme_lines=$(wc -l < "$REPO/README.md" | tr -d ' ')
    if [[ $readme_lines -gt 50 ]]; then
        ethos_score=$((ethos_score + 1))
        ethos_evidence+=("README ($readme_lines lines)")
    fi
    if [[ $readme_lines -gt 200 ]]; then
        ethos_score=$((ethos_score + 1))
        ethos_evidence+=("flagship-grade README")
    fi
fi

if [[ -d "$REPO/research" ]] || [[ -d "$REPO/docs/research" ]]; then
    ethos_score=$((ethos_score + 1))
    ethos_evidence+=("research/ directory")
fi

if [[ -f "$REPO/PROVENANCE.yaml" ]] || [[ -f "$REPO/reference/PROVENANCE.yaml" ]]; then
    ethos_score=$((ethos_score + 1))
    ethos_evidence+=("PROVENANCE.yaml")
fi

if [[ -d "$REPO/.github/workflows" ]]; then
    workflow_count=$(find "$REPO/.github/workflows" -type f \
        \( -name "*.yml" -o -name "*.yaml" \) 2>/dev/null | wc -l | tr -d ' ')
    if [[ $workflow_count -gt 0 ]]; then
        ethos_score=$((ethos_score + 1))
        ethos_evidence+=("$workflow_count CI workflows")
    fi
fi

# Citations / source lists
sources_count=$(find "$REPO" -type f \
    \( -name "sources*.md" -o -name "bibliography*.md" -o -name "references*.md" \) 2>/dev/null \
    | grep -v node_modules | wc -l | tr -d ' ')
if [[ $sources_count -gt 0 ]]; then
    ethos_score=$((ethos_score + 1))
    ethos_evidence+=("$sources_count source/bibliography files")
fi

# ─── PATHOS — narrative / community surface ─────────────────────
# Signals: brand, voice, naming, narrative, landing page, community
pathos_score=0
pathos_evidence=()

if [[ -d "$REPO/brand" ]] || [[ -d "$REPO/docs/brand" ]]; then
    pathos_score=$((pathos_score + 1))
    pathos_evidence+=("brand/ directory")
fi

if [[ -f "$REPO/brand/voice.md" ]] || [[ -f "$REPO/docs/brand/voice.md" ]]; then
    pathos_score=$((pathos_score + 1))
    pathos_evidence+=("voice.md")
fi

# Landing page detection (Next.js, Astro, plain HTML)
landing_present=0
[[ -f "$REPO/src/app/page.tsx" ]] && landing_present=1
[[ -f "$REPO/src/app/page.jsx" ]] && landing_present=1
[[ -f "$REPO/src/pages/index.astro" ]] && landing_present=1
[[ -f "$REPO/src/pages/index.tsx" ]] && landing_present=1
[[ -f "$REPO/index.html" ]] && landing_present=1
if [[ $landing_present -eq 1 ]]; then
    pathos_score=$((pathos_score + 1))
    pathos_evidence+=("landing page present")
fi

# Narrative / story content
narrative_count=$(find "$REPO" -type f \
    \( -name "narrative*.md" -o -name "origin*.md" -o -name "story*.md" \
    -o -name "manifesto*.md" -o -name "naming*.md" \) 2>/dev/null \
    | grep -v node_modules | wc -l | tr -d ' ')
if [[ $narrative_count -gt 0 ]]; then
    pathos_score=$((pathos_score + 1))
    pathos_evidence+=("$narrative_count narrative files")
fi

# Community surface
if [[ -f "$REPO/docs/community.md" ]] || [[ -d "$REPO/community" ]]; then
    pathos_score=$((pathos_score + 1))
    pathos_evidence+=("community surface")
fi

# ─── KAIROS — timing / strategic readiness ──────────────────────
# Signals: roadmap, launch plan, recent commits, release tags
kairos_score=0
kairos_evidence=()

if [[ -f "$REPO/ROADMAP.md" ]] || [[ -f "$REPO/docs/ROADMAP.md" ]]; then
    kairos_score=$((kairos_score + 1))
    kairos_evidence+=("ROADMAP.md")
fi

if [[ -f "$REPO/docs/launch-plan.md" ]] || [[ -f "$REPO/LAUNCH.md" ]]; then
    kairos_score=$((kairos_score + 1))
    kairos_evidence+=("launch plan")
fi

# Commit recency — active project = healthy kairos
if [[ -d "$REPO/.git" ]]; then
    last_commit_ts=$(git -C "$REPO" log -1 --format=%ct 2>/dev/null || echo 0)
    if [[ $last_commit_ts -gt 0 ]]; then
        days_since=$((($(date +%s) - last_commit_ts) / 86400))
        if [[ $days_since -lt 7 ]]; then
            kairos_score=$((kairos_score + 1))
            kairos_evidence+=("active (commit $days_since days ago)")
        elif [[ $days_since -lt 30 ]]; then
            kairos_evidence+=("recent (commit $days_since days ago)")
        fi
    fi

    # Tag count (release cadence)
    tag_count=$(git -C "$REPO" tag 2>/dev/null | wc -l | tr -d ' ')
    if [[ $tag_count -gt 0 ]]; then
        kairos_score=$((kairos_score + 1))
        kairos_evidence+=("$tag_count release tags")
    fi
fi

# ─── Determine dominant mode ────────────────────────────────────
max=$logos_score
dominant="logos"

if [[ $ethos_score -gt $max ]]; then
    max=$ethos_score
    dominant="ethos"
fi
if [[ $pathos_score -gt $max ]]; then
    max=$pathos_score
    dominant="pathos"
fi
if [[ $kairos_score -gt $max ]]; then
    max=$kairos_score
    dominant="kairos"
fi

# Detect balanced state (no clear leader)
total=$((logos_score + ethos_score + pathos_score + kairos_score))
if [[ $total -gt 0 ]]; then
    avg=$((total / 4))
    spread=$((max - avg))
    if [[ $spread -le 1 ]]; then
        dominant="balanced"
    fi
fi

# ─── Composition gaps ───────────────────────────────────────────
gaps=()
[[ $logos_score -eq 0 ]] && gaps+=("LOGOS: no internal skeleton (no src/, no tests, no seed.yaml)")
[[ $ethos_score -eq 0 ]] && gaps+=("ETHOS: no credibility surface (no flagship README, no research, no CI)")
[[ $pathos_score -eq 0 ]] && gaps+=("PATHOS: no narrative surface (no brand/, no landing page, no story)")
[[ $kairos_score -eq 0 ]] && gaps+=("KAIROS: no timing surface (no ROADMAP, no recent activity, no releases)")

if [[ $logos_score -gt 0 ]] && [[ $ethos_score -eq 0 ]] && [[ $pathos_score -eq 0 ]]; then
    gaps+=("LOGOS exists but no rhetorical expression — formalization is invisible to audience")
fi
if [[ $pathos_score -gt 0 ]] && [[ $logos_score -eq 0 ]]; then
    gaps+=("PATHOS without LOGOS — narrative without underlying truth (manipulation risk)")
fi

# ─── Output ─────────────────────────────────────────────────────
if [[ "$FORMAT" == "json" ]]; then
    cat <<EOF
{
  "domain": "$NAME",
  "path": "$REPO",
  "scores": {
    "logos": $logos_score,
    "ethos": $ethos_score,
    "pathos": $pathos_score,
    "kairos": $kairos_score
  },
  "dominant_mode": "$dominant",
  "metrics": {
    "test_files": $test_count,
    "readme_lines": $readme_lines,
    "schema_files": $schema_count
  },
  "evidence": {
    "logos": $(printf '%s\n' "${logos_evidence[@]:-}" | jq -R . | jq -s .),
    "ethos": $(printf '%s\n' "${ethos_evidence[@]:-}" | jq -R . | jq -s .),
    "pathos": $(printf '%s\n' "${pathos_evidence[@]:-}" | jq -R . | jq -s .),
    "kairos": $(printf '%s\n' "${kairos_evidence[@]:-}" | jq -R . | jq -s .)
  },
  "composition_gaps": $(printf '%s\n' "${gaps[@]:-}" | jq -R . | jq -s .)
}
EOF
else
    echo "═══════════════════════════════════════════════════════════"
    echo "  DOMAIN AUDIT: $NAME"
    echo "  Path: $REPO"
    echo "═══════════════════════════════════════════════════════════"
    echo
    printf "  LOGOS   %s/5  — internal skeleton\n" "$logos_score"
    for e in "${logos_evidence[@]:-}"; do [[ -n "$e" ]] && printf "          • %s\n" "$e"; done
    echo
    printf "  ETHOS   %s/6  — credibility (external function)\n" "$ethos_score"
    for e in "${ethos_evidence[@]:-}"; do [[ -n "$e" ]] && printf "          • %s\n" "$e"; done
    echo
    printf "  PATHOS  %s/5  — narrative (external function)\n" "$pathos_score"
    for e in "${pathos_evidence[@]:-}"; do [[ -n "$e" ]] && printf "          • %s\n" "$e"; done
    echo
    printf "  KAIROS  %s/4  — timing (strategic)\n" "$kairos_score"
    for e in "${kairos_evidence[@]:-}"; do [[ -n "$e" ]] && printf "          • %s\n" "$e"; done
    echo
    echo "  ───────────────────────────────────────────────────────"
    printf "  DOMINANT MODE: %s\n" "$dominant"
    echo
    if [[ ${#gaps[@]} -gt 0 ]]; then
        echo "  COMPOSITION GAPS:"
        for g in "${gaps[@]}"; do
            printf "    ⚠  %s\n" "$g"
        done
    else
        echo "  ✓ No critical mode-absences detected."
    fi
    echo
fi
