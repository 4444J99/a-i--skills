#!/usr/bin/env bash
# DIWS Phase 0.5 — Portfolio gap audit (THE STRETCHING RACK)
#
# Operates across N concurrent DIWS instances simultaneously to surface
# holes (under-developed) and fat (over-engineered) at portfolio scale.
#
# For each axis (8 strata + 4 operators), reports:
#   - Holes — under-developed in 1+ instances; transplantable from siblings
#   - Fat — over-engineered in 1+ instances; consolidatable into shared engine
#   - N-way overlap — concept present in ≥2 instances; promotion candidate
#
# Outputs holes-fat-report.md to CWD (or --output path).
#
# Usage:
#   bash portfolio-gap-audit.sh --instances voodoo,<your-instance>
#   bash portfolio-gap-audit.sh --instances-dir ./proof-instances/
#   bash portfolio-gap-audit.sh --output /path/to/report.md
#
# Exit codes:
#   0 — success (report generated)
#   1 — invalid arguments
#   2 — instance(s) not found
#   3 — no instances to audit

set -euo pipefail

INSTANCES_LIST=""
INSTANCES_DIR=""
OUTPUT="./holes-fat-report.md"
DIWS_ROOT="${DIWS_ROOT:-${HOME}/Workspace/a-i--skills/skills/project-management/domain-ideal-whole-substrate}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --instances)
      INSTANCES_LIST="$2"
      shift 2
      ;;
    --instances-dir)
      INSTANCES_DIR="$2"
      shift 2
      ;;
    --output)
      OUTPUT="$2"
      shift 2
      ;;
    --diws-root)
      DIWS_ROOT="$2"
      shift 2
      ;;
    --help|-h)
      sed -n 's/^# \{0,1\}//p' "$0" | head -25
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      exit 1
      ;;
  esac
done

# Resolve instances
declare -a INSTANCES=()
declare -A INSTANCE_PATHS

if [[ -n "$INSTANCES_LIST" ]]; then
  IFS=',' read -ra INSTANCE_NAMES <<< "$INSTANCES_LIST"
  for name in "${INSTANCE_NAMES[@]}"; do
    name=$(echo "$name" | xargs)  # trim
    path="$DIWS_ROOT/proof-instances/$name"
    if [[ ! -d "$path" ]]; then
      echo "ERROR: Instance not found: $path" >&2
      exit 2
    fi
    INSTANCES+=("$name")
    INSTANCE_PATHS[$name]="$path"
  done
elif [[ -n "$INSTANCES_DIR" ]]; then
  if [[ ! -d "$INSTANCES_DIR" ]]; then
    echo "ERROR: Instances directory not found: $INSTANCES_DIR" >&2
    exit 2
  fi
  for path in "$INSTANCES_DIR"/*/; do
    [[ -d "$path" ]] || continue
    name=$(basename "$path")
    INSTANCES+=("$name")
    INSTANCE_PATHS[$name]="$path"
  done
else
  # Default: scan DIWS proof-instances
  if [[ -d "$DIWS_ROOT/proof-instances" ]]; then
    for path in "$DIWS_ROOT/proof-instances"/*/; do
      [[ -d "$path" ]] || continue
      name=$(basename "$path")
      INSTANCES+=("$name")
      INSTANCE_PATHS[$name]="$path"
    done
  fi
fi

if [[ ${#INSTANCES[@]} -eq 0 ]]; then
  echo "ERROR: No instances to audit. Use --instances or --instances-dir." >&2
  exit 3
fi

echo "DIWS Phase 0.5 — Portfolio gap audit (stretching rack)"
echo "Auditing instances: ${INSTANCES[*]}"
echo

# 8 strata + 4 operators = 12 axes
declare -a AXES=(
  "1-ontology|domain-ontology.md"
  "2-lineage|domain-lineage.md"
  "3-constellation|domain-constellation.yaml"
  "4-gap-map|domain-gap-map.md"
  "5-agent-fleet|domain-agent-fleet.yaml"
  "6-production-stack|domain-production-stack.md"
  "7-internal-magnet|domain-attractor.md"
  "8-external-contribution|domain-contribution-charter.md"
  "OP1-selfish-altruistic|domain-meta-study.md"
  "OP2-magnetic-membrane|portfolio-resonance.md"
  "OP3-portfolio-operator|portfolio-resonance.md"
  "OP4-reflexive|domain-meta-study.md"
)

# Score each axis × instance: 0 (missing), 1 (stub <500B), 2 (partial 500-2000B), 3 (full >2000B)
declare -A SCORES

for axis_entry in "${AXES[@]}"; do
  axis_id=$(echo "$axis_entry" | cut -d'|' -f1)
  expected_file=$(echo "$axis_entry" | cut -d'|' -f2)

  for instance in "${INSTANCES[@]}"; do
    file="${INSTANCE_PATHS[$instance]}/$expected_file"
    score=0
    if [[ -f "$file" ]]; then
      size=$(wc -c < "$file" | tr -d ' ')
      if (( size >= 2000 )); then
        score=3
      elif (( size >= 500 )); then
        score=2
      elif (( size > 0 )); then
        score=1
      fi
    fi
    SCORES["${axis_id}|${instance}"]=$score
  done
done

# Generate report
{
  echo "# Portfolio Holes/Fat Report (Stretching Rack)"
  echo
  echo "**Generated:** $(date '+%Y-%m-%d %H:%M:%S')"
  echo "**Generator:** DIWS Phase 0.5 (\`portfolio-gap-audit.sh\`)"
  echo "**Instances audited:** ${INSTANCES[*]}"
  echo
  echo "## Score legend"
  echo
  echo "- **0** = missing (no file)"
  echo "- **1** = stub (<500 bytes — placeholder only)"
  echo "- **2** = partial (500–2000 bytes — some content, gaps remain)"
  echo "- **3** = full (>2000 bytes — substantive)"
  echo
  echo "## Per-axis × per-instance scores"
  echo
  printf "| Axis "
  for instance in "${INSTANCES[@]}"; do
    printf "| %s " "$instance"
  done
  printf "|\n"
  printf "|------"
  for instance in "${INSTANCES[@]}"; do
    printf "|------"
  done
  printf "|\n"

  for axis_entry in "${AXES[@]}"; do
    axis_id=$(echo "$axis_entry" | cut -d'|' -f1)
    printf "| %s " "$axis_id"
    for instance in "${INSTANCES[@]}"; do
      printf "| %s " "${SCORES[${axis_id}|${instance}]}"
    done
    printf "|\n"
  done

  echo
  echo "## HOLES — under-developed dimensions (transplant candidates)"
  echo
  echo "An axis is a **hole** in an instance if score ≤1 AND ≥1 sibling instance has score ≥2 (transplant available)."
  echo

  HOLE_COUNT=0
  for axis_entry in "${AXES[@]}"; do
    axis_id=$(echo "$axis_entry" | cut -d'|' -f1)

    # Find max sibling score
    max_score=0
    max_donor=""
    for instance in "${INSTANCES[@]}"; do
      s="${SCORES[${axis_id}|${instance}]}"
      if (( s > max_score )); then
        max_score=$s
        max_donor=$instance
      fi
    done

    # Find instances that need transplant
    if (( max_score >= 2 )); then
      for instance in "${INSTANCES[@]}"; do
        s="${SCORES[${axis_id}|${instance}]}"
        if (( s <= 1 )) && [[ "$instance" != "$max_donor" ]]; then
          echo "- **${axis_id}** in \`${instance}\` (score $s) ← transplant candidate from \`${max_donor}\` (score $max_score)"
          HOLE_COUNT=$((HOLE_COUNT + 1))
        fi
      done
    fi
  done

  if (( HOLE_COUNT == 0 )); then
    echo "_No transplant-eligible holes detected. Either portfolio is uniformly developed or uniformly underdeveloped._"
  fi

  echo
  echo "## FAT — over-engineered axes (consolidation candidates)"
  echo
  echo "An axis is **fat** in the portfolio if ≥2 instances score 3 AND the axis represents work that could consolidate to a shared engine."
  echo

  FAT_COUNT=0
  for axis_entry in "${AXES[@]}"; do
    axis_id=$(echo "$axis_entry" | cut -d'|' -f1)
    full_count=0
    full_instances=()
    for instance in "${INSTANCES[@]}"; do
      s="${SCORES[${axis_id}|${instance}]}"
      if (( s == 3 )); then
        full_count=$((full_count + 1))
        full_instances+=("$instance")
      fi
    done
    if (( full_count >= 2 )); then
      echo "- **${axis_id}** is fully developed in $full_count instances: ${full_instances[*]}"
      echo "  - Consolidation candidate → promote to shared engine (Tier 2 meta-engine candidate)"
      FAT_COUNT=$((FAT_COUNT + 1))
    fi
  done

  if (( FAT_COUNT == 0 )); then
    echo "_No fat-cell consolidation candidates yet. Portfolio is differentiated; revisit when ≥2 instances reach full score on the same axis._"
  fi

  echo
  echo "## N-WAY OVERLAP — promotion candidates"
  echo
  echo "Concepts present in ≥3 instances at score ≥2 are candidates for Tier 2 (meta-engine) or Tier 3 (consultant-engine) promotion."
  echo

  PROMO_COUNT=0
  for axis_entry in "${AXES[@]}"; do
    axis_id=$(echo "$axis_entry" | cut -d'|' -f1)
    high_count=0
    for instance in "${INSTANCES[@]}"; do
      s="${SCORES[${axis_id}|${instance}]}"
      if (( s >= 2 )); then
        high_count=$((high_count + 1))
      fi
    done
    if (( high_count >= 3 )); then
      echo "- **${axis_id}** present in $high_count instances at score ≥2"
      echo "  - Promotion candidate → flag for engine-extract mode review"
      PROMO_COUNT=$((PROMO_COUNT + 1))
    fi
  done

  if (( PROMO_COUNT == 0 )); then
    echo "_No N-way overlap detected yet. Portfolio is too narrow or instances too sparse._"
  fi

  echo
  echo "## SUMMARY"
  echo
  echo "- Instances audited: ${#INSTANCES[@]}"
  echo "- Axes scored: ${#AXES[@]}"
  echo "- Holes (transplant candidates): $HOLE_COUNT"
  echo "- Fat axes (consolidation candidates): $FAT_COUNT"
  echo "- N-way overlap (promotion candidates): $PROMO_COUNT"
  echo
  echo "## Action items"
  echo
  echo "Review each hole/fat/promotion entry above and decide:"
  echo "- [ ] Schedule transplant work for under-developed axes"
  echo "- [ ] Authorize consolidation of over-engineered cells (Tier 2 promotion via \`mode engine-extract\`)"
  echo "- [ ] Approve N-way overlap promotions (Tier 2 → Tier 3 candidates)"
  echo
  echo "---"
  echo
  echo "_Generated by DIWS Phase 0.5 portfolio-gap-audit (the stretching rack). To refresh, re-run \`portfolio-gap-audit.sh\`. To audit a different instance set, pass \`--instances <list>\` or \`--instances-dir <path>\`._"

} > "$OUTPUT"

# Summary to stdout
echo "Holes detected (transplant candidates): $HOLE_COUNT"
echo "Fat axes (consolidation candidates): $FAT_COUNT"
echo "N-way overlap (promotion candidates): $PROMO_COUNT"
echo
echo "Output written to: $OUTPUT"
