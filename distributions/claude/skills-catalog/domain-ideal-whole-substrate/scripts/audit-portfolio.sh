#!/usr/bin/env bash
# DIWS Phase 0 — Portfolio audit (PULL leg of Portfolio Operator)
#
# Globs ~/Workspace/ for existing engines, classifies into 3-tier taxonomy:
#   Tier 1 (domain engines): re-skinnable within similar domain
#   Tier 2 (meta-engines): cross-domain pattern
#   Tier 3 (consultant engines): every engagement regardless of domain
#
# Outputs portfolio-reuse-map.md to CWD (or --output path).
#
# Usage:
#   bash audit-portfolio.sh                              # default: scan ~/Workspace, output to ./portfolio-reuse-map.md
#   bash audit-portfolio.sh --workspace /custom/path     # custom scan root
#   bash audit-portfolio.sh --output /path/to/out.md     # custom output path
#   bash audit-portfolio.sh --domain chess               # bias scoring toward a candidate domain
#
# Exit codes:
#   0 — success
#   1 — invalid arguments
#   2 — workspace not found

set -euo pipefail

WORKSPACE="${HOME}/Workspace"
OUTPUT="./portfolio-reuse-map.md"
CANDIDATE_DOMAIN=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --workspace)
      WORKSPACE="$2"
      shift 2
      ;;
    --output)
      OUTPUT="$2"
      shift 2
      ;;
    --domain)
      CANDIDATE_DOMAIN="$2"
      shift 2
      ;;
    --help|-h)
      sed -n 's/^# \{0,1\}//p' "$0" | head -20
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      exit 1
      ;;
  esac
done

if [[ ! -d "$WORKSPACE" ]]; then
  echo "ERROR: Workspace not found: $WORKSPACE" >&2
  exit 2
fi

# Engine signature patterns — these are the actual engines DIWS knows about.
# Each pattern: regex (matches path or filename) | tier | name | known reuse-classes
declare -a ENGINE_SIGNATURES=(
  # Tier 1 — Domain engines
  "spiral\.ts|1|spiral-renderer|visual-flow-brand,meditation-aid,generative-art"
  "membership.*funnel|tier.*funnel|1|four-level-funnel|membership-progression-tier"
  "landing-engine|persona-template|1|landing-engine|persona-arch-landing-pages"

  # Tier 2 — Meta-engines
  "cross-pollination|prt-045|2|cross-pollination-diagnosis|n-way-mechanism-asymmetry"
  "constellation\.yaml|75-person|prt-046|2|peer-research-foundation|every-domain"
  "product-domain-engine|2|pde-skill|product-tied-to-domain"
  "bridge-content|jutsu|boss-battle|prt-040|2|bridge-content-templates|creator-cadence"
  "discord-rituals|prt-041|2|discord-rituals|tier-gated-communities"
  "modular-synthesis-philosophy|2|msp-skill|portfolio-routing"

  # Tier 3 — Consultant engines
  "knowledge-base|3|knowledge-base|persistent-cross-engagement-notes"
  "application-pipeline|3|application-pipeline|opportunity-tracking"
  "chezmoi.*claude|claude.*chezmoi|3|plan-mode-discipline|every-session"
  "INST-INDEX-RERUM-FACIENDARUM|3|irf-protocol|cross-engagement-governance"
  "MEMORY\.md|3|memory-protocol|cross-session-context"
  "conversation-corpus|3|corpus-pipeline|capture-infrastructure"
  "chatgpt_exporter_to_bundle|3|chatgpt-converter|capture-infrastructure"
  "organvm-corpvs-testamentvm|3|governance-corpus|cross-engagement-governance"
)

# Scan workspace
echo "DIWS Phase 0 — Portfolio audit"
echo "Workspace: $WORKSPACE"
[[ -n "$CANDIDATE_DOMAIN" ]] && echo "Candidate domain: $CANDIDATE_DOMAIN"
echo "Scanning..."

declare -A FOUND_TIER1
declare -A FOUND_TIER2
declare -A FOUND_TIER3

# Use find for paths, not git — supports non-git artifacts
ALL_PATHS=$(find "$WORKSPACE" -maxdepth 6 \( \
    -name "spiral.ts" -o \
    -name "*funnel*" -o \
    -name "*landing-engine*" -o \
    -name "*persona-template*" -o \
    -name "*cross-pollination*" -o \
    -name "constellation*.yaml" -o \
    -name "INST-INDEX-RERUM-FACIENDARUM*" -o \
    -name "MEMORY.md" -o \
    -name "*conversation-corpus*" -o \
    -name "chatgpt_exporter_to_bundle*" -o \
    -name "SKILL.md" \
  \) -type f 2>/dev/null || true)

# Always include known skill paths
SKILL_PATHS=$(find "$WORKSPACE" -maxdepth 5 -path "*/a-i--skills/skills/*/SKILL.md" -type f 2>/dev/null || true)

ALL_PATHS="$ALL_PATHS"$'\n'"$SKILL_PATHS"

for path in $ALL_PATHS; do
  [[ -z "$path" ]] && continue

  for sig in "${ENGINE_SIGNATURES[@]}"; do
    pattern=$(echo "$sig" | cut -d'|' -f1)
    tier=$(echo "$sig" | cut -d'|' -f2)
    name=$(echo "$sig" | cut -d'|' -f3)
    classes=$(echo "$sig" | cut -d'|' -f4)

    # Match path against pattern (case-insensitive)
    if echo "$path" | grep -iqE "$pattern"; then
      case "$tier" in
        1) FOUND_TIER1["$name"]="$path|$classes" ;;
        2) FOUND_TIER2["$name"]="$path|$classes" ;;
        3) FOUND_TIER3["$name"]="$path|$classes" ;;
      esac
    fi
  done
done

# Generate report
{
  echo "# Portfolio Reuse Map"
  echo
  echo "**Generated:** $(date '+%Y-%m-%d %H:%M:%S')"
  echo "**Workspace scanned:** \`$WORKSPACE\`"
  [[ -n "$CANDIDATE_DOMAIN" ]] && echo "**Candidate domain:** $CANDIDATE_DOMAIN"
  echo "**Generator:** DIWS Phase 0 (\`audit-portfolio.sh\`)"
  echo
  echo "## Tier 1 — Domain engines (re-skinnable within similar domain)"
  echo
  if [[ ${#FOUND_TIER1[@]} -eq 0 ]]; then
    echo "_No Tier 1 engines detected. This is unusual; check workspace path._"
  else
    echo "| Engine | Path | Re-skin classes |"
    echo "|---|---|---|"
    for name in "${!FOUND_TIER1[@]}"; do
      entry="${FOUND_TIER1[$name]}"
      path=$(echo "$entry" | cut -d'|' -f1)
      classes=$(echo "$entry" | cut -d'|' -f2)
      echo "| \`$name\` | \`$path\` | $classes |"
    done
  fi

  echo
  echo "## Tier 2 — Meta-engines (cross-domain pattern)"
  echo
  if [[ ${#FOUND_TIER2[@]} -eq 0 ]]; then
    echo "_No Tier 2 engines detected._"
  else
    echo "| Engine | Path | Reuse classes |"
    echo "|---|---|---|"
    for name in "${!FOUND_TIER2[@]}"; do
      entry="${FOUND_TIER2[$name]}"
      path=$(echo "$entry" | cut -d'|' -f1)
      classes=$(echo "$entry" | cut -d'|' -f2)
      echo "| \`$name\` | \`$path\` | $classes |"
    done
  fi

  echo
  echo "## Tier 3 — Consultant engines (every engagement)"
  echo
  if [[ ${#FOUND_TIER3[@]} -eq 0 ]]; then
    echo "_No Tier 3 engines detected._"
  else
    echo "| Engine | Path | Reuse classes |"
    echo "|---|---|---|"
    for name in "${!FOUND_TIER3[@]}"; do
      entry="${FOUND_TIER3[$name]}"
      path=$(echo "$entry" | cut -d'|' -f1)
      classes=$(echo "$entry" | cut -d'|' -f2)
      echo "| \`$name\` | \`$path\` | $classes |"
    done
  fi

  echo
  echo "## Reuse decisions (TO FILL)"
  echo
  echo "Per Engine + Skin pattern, target ratio: 60–80% engine + 20–40% skin."
  echo
  if [[ -n "$CANDIDATE_DOMAIN" ]]; then
    echo "For candidate domain **$CANDIDATE_DOMAIN**, decide for each detected engine:"
  else
    echo "For each candidate domain, decide for each detected engine:"
  fi
  echo
  echo "- [ ] **Re-skin** (use the engine, parameterize for this domain)"
  echo "- [ ] **Skip** (engine doesn't apply to this domain)"
  echo "- [ ] **Promote** (this engine fires across more domains than originally tagged → flag for tier-up)"
  echo "- [ ] **Invent** (new engine needed; document gap and add to substrate skill backlog)"
  echo
  echo "## Genuine new code (estimate)"
  echo
  echo "Engagements with >40% genuine new code = Phase 0 audit was incomplete OR the engagement is in a genuinely new domain class."
  echo "Engagements with <10% genuine new code = pure assembly; engagement should still grow the engine fleet a little."
  echo
  echo "**Estimated for this candidate domain:** _TBD — fill after reuse decisions are made_"
  echo
  echo "---"
  echo
  echo "_Generated by DIWS Phase 0 portfolio-audit. To refresh, re-run \`audit-portfolio.sh\`. To run the stretching rack across N concurrent instances, see \`portfolio-gap-audit.sh\`._"

} > "$OUTPUT"

# Summary to stdout
echo
echo "Engines detected:"
echo "  Tier 1: ${#FOUND_TIER1[@]}"
echo "  Tier 2: ${#FOUND_TIER2[@]}"
echo "  Tier 3: ${#FOUND_TIER3[@]}"
echo
echo "Output written to: $OUTPUT"
