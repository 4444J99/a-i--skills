#!/usr/bin/env bash
set -euo pipefail

# Domain Ideal-Whole Substrate Audit
# Checks for the presence and validity of the 8 strata.

DOMAIN_DIR=${1:-"."}

echo "Auditing Domain Substrate in: $DOMAIN_DIR"

STRATA=(
  "domain-ontology.md"
  "domain-lineage.md"
  "domain-constellation.yaml"
  "domain-gap-map.md"
  "domain-agent-fleet.yaml"
  "domain-production-stack.md"
  "domain-attractor.md"
  "domain-contribution-charter.md"
)

MISSING=0
for stratum in "${STRATA[@]}"; do
  if [[ ! -f "$DOMAIN_DIR/$stratum" ]]; then
    echo "[MISSING] $stratum"
    MISSING=$((MISSING+1))
  else
    echo "[FOUND]   $stratum"
  fi
done

if [[ $MISSING -eq 0 ]]; then
  echo "Substrate is COMPLETE."
else
  echo "Substrate is INCOMPLETE ($MISSING missing)."
  exit 1
fi
