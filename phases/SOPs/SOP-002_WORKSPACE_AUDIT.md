# SOP-002: Comprehensive Workspace Audit Procedure

## Purpose
Exhaustive procedure for auditing the complete organvm workspace, identifying missing seeds, invalid configurations, and governance gaps across all 115+ repositories.

## Scope
- All repos in `/Users/4jp/Workspace/organvm/`
- All bench repositories
- All contrib repositories
- All meta-organvm repositories

## When to Run
- Weekly (every Sunday 00:00 UTC)
- Before any governance review
- After bulk repo creation
- On demand via `organvm audit workspace`

## Audit Micro-Steps

### Phase 1: Discovery & Enumeration

```
┌─────────────────────────────────────────────────────────────────┐
│ AUDIT MICRO-STEP 2.1.1: REPO DISCOVERY                           │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: glob                                      TIMEOUT: 30s    │
│ PATTERN: */seed.yaml                                DEPTH: ∞       │
│ OUTPUT: Complete repo list with seed.yaml present                 │
│ VALIDATION: All discovered paths must be valid directories      │
└─────────────────────────────────────────────────────────────────┘
```

#### Command Sequence
```bash
# Discovery Phase
cd /Users/4jp/Workspace/organvm

# Primary discovery: all seed.yaml files
organvm audit discover --pattern="*/seed.yaml"

# Secondary discovery: all CLAUDE.md files  
organvm audit discover --pattern="*/CLAUDE.md"

# Tertiary discovery: all .git directories (validates git repos)
organvm audit discover --pattern="*/.git"
```

#### Expected Outputs
- `audit/discovered_repos_<timestamp>.json`
- `audit/discovered_seeds_<timestamp>.json`
- `audit/discovered_claude_md_<timestamp>.json`

---

```
┌─────────────────────────────────────────────────────────────────┐
│ AUDIT MICRO-STEP 2.1.2: MISSING SEED IDENTIFICATION               │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: set_difference                           TIMEOUT: 5s       │
│ INPUT: All repos (via ls) - Repos with seed.yaml                  │
│ OUTPUT: List of repos missing seed.yaml                          │
│ CRITICAL: This is the PRIMARY indicator of seeding debt         │
└─────────────────────────────────────────────────────────────────┘
```

#### Algorithm
```python
def identify_missing_seeds(workspace_path: str) -> list[dict]:
    all_repos = glob(f"{workspace_path}/*/")
    repos_with_seeds = glob(f"{workspace_path}/*/seed.yaml")
    seed_set = {r.split('/')[-2] for r in repos_with_seeds}
    all_set = {r.split('/')[-2] for r in all_repos if not r.startswith('.')}
    
    missing = []
    for repo in all_set - seed_set:
        missing.append({
            "repo": repo,
            "path": f"{workspace_path}/{repo}",
            "severity": "HIGH" if repo not in BENCH_EXCEPTIONS else "LOW",
            "organ": infer_organ_from_path(repo),
            "status": "NO_SEED"
        })
    return missing
```

---

### Phase 2: Seed.yaml Validation

```
┌─────────────────────────────────────────────────────────────────┐
│ AUDIT MICRO-STEP 2.2.1: YAML STRUCTURE VALIDATION                │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: yaml.safe_load                          TIMEOUT: 2s/file  │
│ CHECKS:                                                             │
│   □ Required fields present                                        │
│   □ Field types match expected types                               │
│   □ No circular dependency references                             │
│   □ All referenced repos exist                                    │
└─────────────────────────────────────────────────────────────────┘
```

#### Required Fields (By Status)
| Status | Required Fields |
|--------|-----------------|
| LOCAL | name, description, organ, status |
| CANDIDATE | + org, scale, IRF |
| PUBLIC_PROCESS | + capabilities, primitives |
| GRADUATED | + dependencies, entry_points |

#### Validation Rules
```python
REQUIRED_FIELDS = {
    "LOCAL": ["name", "description", "organ", "status"],
    "CANDIDATE": ["name", "description", "organ", "status", "org", "scale", "IRF"],
    "PUBLIC_PROCESS": ["name", "description", "organ", "status", "org", "scale", "IRF", "capabilities", "primitives"],
    "GRADUATED": ["name", "description", "organ", "status", "org", "scale", "IRF", "capabilities", "primitives", "dependencies", "entry_points"]
}
```

---

```
┌─────────────────────────────────────────────────────────────────┐
│ AUDIT MICRO-STEP 2.2.2: ORGAN CLASSIFICATION VALIDATION          │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: regex match                              TIMEOUT: 1s/file  │
│ CHECK: organ field matches /^[I|VII|III|IV|V|VI|VII|Meta]+$/    │
│ OUTPUT: Invalid organ classifications                              │
└─────────────────────────────────────────────────────────────────┘
```

#### Valid Organ Values
```
ORGAN_I = "I"      # Knowledge/Ontology (26 repos)
ORGAN_II = "II"    # Creative/Content (32 repos)  
ORGAN_III = "III"  # Publishing/Distribution (32 repos)
ORGAN_IV = "IV"    # Orchestration/Agents (22 repos)
ORGAN_V = "V"      # Operations/Tools (6 repos)
ORGAN_VI = "VI"    # Community/Governance (6 repos)
ORGAN_VII = "VII"  # Governance/Law (6 repos)
META_ORG = "Meta"  # Meta-organvm (13 repos)
```

---

```
┌─────────────────────────────────────────────────────────────────┐
│ AUDIT MICRO-STEP 2.2.3: SCALE CLASSIFICATION VALIDATION          │
├────────────────��────────────────────────────────────────────────┤
│ TOOL: set membership                          TIMEOUT: 1s/file   │
│ CHECK: scale field is one of: [σ_E, σ_O, σ_P]                   │
│ OUTPUT: Invalid scale classifications                             │
└─────────────────────────────────────────────────────────────────┘
```

#### Scale Definitions
| Scale | Symbol | Definition |
|-------|--------|------------|
| Emergent | σ_E | Experimental, single-user, rapid iteration |
| Operational | σ_O | Production-capable, multi-user, stable |
| Public | σ_P | Public-facing, high-scale, hardened |

---

### Phase 3: CLAUDE.md Validation

```
┌─────────────────────────────────────────────────────────────────┐
│ AUDIT MICRO-STEP 2.3.1: PRESENCE VALIDATION                      │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: path.exists                             TIMEOUT: 1s       │
│ CHECK: CLAUDE.md exists in repo root                             │
│ OUTPUT: Repos missing CLAUDE.md                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### Exceptions
- External contrib repos (different structure)
- Archived repos (marked NO_SEED)
- Bench repos (seeding not required)

---

```
┌─────────────────────────────────────────────────────────────────┐
│ AUDIT MICRO-STEP 2.3.2: SECTION VALIDATION                      │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: regex search                           TIMEOUT: 2s/file   │
│ REQUIRED SECTIONS:                                                │
│   □ ## Identity                                                  │
│   □ ## Architecture                                              │
│   □ ## Commands                                                  │
│   □ ## Development                                               │
│   □ ## Dependencies                                              │
│ OPTIONAL SECTIONS:                                               │
│   □ ## Key Constraints                                           │
│   □ ## Structure                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

### Phase 4: Dependency Graph Validation

```
┌─────────────────────────────────────────────────────────────────┐
│ AUDIT MICRO-STEP 2.4.1: DEPENDENCY EXTRACTION                    │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: yaml.deep_load                      TIMEOUT: 5s          │
│ OUTPUT: Full dependency graph                                   │
│ FORMAT: DOT for graphviz, JSON for API                          │
└─────────────────────────────────────────────────────────────────┘
```

#### Dependency Graph Schema
```python
DependencyNode = {
    "repo": str,              # e.g., "organvm-iv-taxis/agent--claude-smith"
    "depends_on": list[str],  # list of repo names
    "depended_by": list[str],# inverted index
    "type": "implicit" | "explicit" | "workflow"
}
```

---

```
┌─────────────────────────────────────────────────────────────────┐
│ AUDIT MICRO-STEP 2.4.2: CIRCULAR DEPENDENCY DETECTION            │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: dfs_cycle_detection                TIMEOUT: O(V+E)      │
│ CHECK: No cycles in dependency graph                           │
│ OUTPUT: Any circular dependencies found                       │
└─────────────────────────────────────────────────────────────────┘
```

#### Algorithm
```python
def detect_cycles(graph: dict[str, list[str]]) -> list[list[str]]:
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {node: WHITE for node in graph}
    parent = {node: None for node in graph}
    cycles = []
    
    def dfs(node: str) -> bool:
        color[node] = GRAY
        for neighbor in graph.get(node, []):
            if color.get(neighbor, WHITE) == GRAY:
                # Found cycle
                cycle = [neighbor, node]
                curr = parent[node]
                while curr != neighbor:
                    cycle.append(curr)
                    curr = parent[curr]
                cycles.append(cycle)
                return True
            elif color.get(neighbor, WHITE) == WHITE:
                parent[neighbor] = node
                if dfs(neighbor):
                    return True
        color[node] = BLACK
        return False
    
    for node in graph:
        if color[node] == WHITE:
            dfs(node)
    return cycles
```

---

### Phase 5: Governance State Validation

```
┌─────────────────────────────────────────────────────────────────┐
│ AUDIT MICRO-STEP 2.5.1: STATE MACHINE VALIDATION                 │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: state_transition_check                   TIMEOUT: 3s       │
│ VALID TRANSITIONS:                                                │
│   □ LOCAL → CANDIDATE                                            │
│   □ CANDIDATE → PUBLIC_PROCESS                                    │
│   □ PUBLIC_PROCESS → GRADUATED                                   │
│   □ GRADUATED → GRADUATED (terminal)                             │
│ INVALID TRANSITIONS:                                            │
│   □ Any skip (LOCAL → PUBLIC_PROCESS)                           │
│   □ Any backward                                                 │
└───────────────────────────────────────────────────���─���───────────┘
```

#### State Transition Matrix
```
        │LOCAL│CANDIDATE│PUBLIC_PROCESS│GRADUATED│
────────┼─────┼─────────┼─────────────┼─────────┤
LOCAL   │ ─  │  VALID  │   INVALID   │ INVALID │
CANDIDATE│INVALID│  ─   │   VALID    │ INVALID │
PUBLIC_ │INVALID│INVALID│     ─     │ VALID   │
PROCESS │       │        │            │         │
GRADUATED│INVALID│INVALID│  INVALID  │   ─    │
```

---

### Phase 6: IRF Registry Validation

```
┌─────────────────────────────────────────────────────────────────┐
│ AUDIT MICRO-STEP 2.6.1: IRF FORMAT VALIDATION                   │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: regex ^IRF-[A-Z]{3}-[0-9]{3}$        TIMEOUT: 1s          │
│ OUTPUT: Invalid IRF formats                                     │
└─────────────────────────────────────────────────────────────────┘
```

#### IRF Schema
```
IRF-XXX-NNN
   │    │
   │    └── Sequence number (001-999)
   └─────── Organ prefix (THE, KER, PUB, TAX, OPS, COM, GOV)
```

#### Organ-IRF Mapping
| Organ | IRF Prefix | Range |
|-------|-----------|-------|
| I - Theoria | THE | THE-001 to THE-999 |
| II - Kerygma | KER | KER-001 to KER-999 |
| III - Publica | PUB | PUB-001 to PUB-999 |
| IV - Taxis | TAX | TAX-001 to TAX-999 |
| V - Ops | OPS | OPS-001 to OPS-999 |
| VI - Koinonia | COM | COM-001 to COM-999 |
| VII - Kerygma | GOV | GOV-001 to GOV-999 |
| Meta | META | META-001 to META-999 |

---

### Phase 7: Report Generation

```
┌─────────────────────────────────────────────────────────────────┐
│ AUDIT MICRO-STEP 2.7.1: SUMMARY REPORT                            │
├─────────────────────────────────────────────────────────────────┤
│ OUTPUT FORMAT: Markdown + JSON                                   │
│ SECTIONS:                                                      │
│   1. Executive Summary                                        │
│   2. Repo Statistics                                          │
│   3. Missing Seeds (by severity)                               │
│   4. Invalid Configurations                                   │
│   5. Dependency Graph Status                                 │
│   6. Governance State Distribution                           │
│   7. Action Items                                             │
└─────────────────────────────────────────────────────────────────┘
```

#### Report Template
```markdown
# Workspace Audit Report

**Generated**: {{timestamp}}
**Auditor**: organvm-IV-taxis/agent--claude-smith
**Scope**: {{repo_count}} repositories

## Executive Summary

| Metric | Count | Change |
|--------|-------|--------|
| Total Repos | {{total}} | ±{{delta}} |
| With Seed | {{seeded}} | ±{{delta}} |
| Missing Seed | {{unseeded}} | ±{{delta}} |
| Invalid Config | {{invalid}} | ±{{delta}} |

## Severity Breakdown

### CRITICAL
{{#each critical}}
- [{{repo}}]({{path}}) - {{issue}}
{{/each}}

### HIGH
{{#each high}}
- [{{repo}}]({{path}}) - {{issue}}
{{/each}}

### MEDIUM
{{#each medium}}
- [{{repo}}]({{path}}) - {{issue}}
{{/each}}

## Action Items

{{#each actions}}
- [ ] {{issue}} (Owner: {{owner}}, Due: {{due}})
{{/each}}
```

---

## Automated Execution

### Cron Configuration
```yaml
# .github/workflows/audit.yaml
name: Weekly Workspace Audit
on:
  schedule:
    - cron: '0 0 * * 0'  # Sunday 00:00 UTC
  workflow_dispatch:

jobs:
  audit:
    runs-on: macOS-latest
    steps:
      - uses: actions/checkout@v4
        with:
          path: organvm
      
      - name: Run Complete Audit
        run: |
          cd organvm/a-i--skills/phases
          python3 audit_workspace.py --output=audit/report
      
      - name: Commit Report
        run: |
          git add audit/
          git commit -m "chore: weekly workspace audit"
      
      - name: Upload Report
        uses: actions/upload-artifact@v4
        with:
          name: audit-report
          path: audit/report_*.md
```

---

## Manual Execution

### Full Audit Command
```bash
organvm audit workspace \
  --output=audit/full_audit_$(date +%Y%m%d) \
  --format=markdown \
  --include-dependencies=true \
  --include-governance=true \
  --severity-threshold=LOW
```

### Quick Audit Command
```bash
organvm audit workspace --quick
```

### Targeted Audit Command
```bash
organvm audit workspace --organ=IV --status=LOCAL
```

---

## Verification

### Self-Verification Commands
```bash
# Verify audit script exists and is executable
test -x /Users/4jp/Workspace/organvm/a-i--skills/phases/audit_workspace.py

# Verify YAML output is valid
python3 -c "import yaml; yaml.safe_load(open('audit/latest.yaml'))"

# Verify report has minimum sections
grep -q "## Executive Summary" audit/latest.md
grep -q "## Action Items" audit/latest.md
```

---

## Owner
- **Responsible**: organvm-IV-taxis/agent--claude-smith
- **Oversight**: organvm-corpvs-testamentvm
- **Escalation**: organvm-vii-kerygma/system-governance-framework

---

## Exceptions

### Bench Repositories
The following are exceptions and should never be flagged:
- `bench--*` repositories (experimental, stateless)
- `contrib--*` repositories (external, different structure)
- `.archived--*` repositories (archived, no seeding required)

### Known Issues
- Client repos awaiting a spec: pending spec creation (names redacted)
- Repos in CONTRIBUTING state may have incomplete fields

---

## Appendix A: Audit Cog Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                  AUDIT COG MATRIX                            │
├──────────────────────────────────────────────────────────────────┤
│ COG  │ NAME                    │ MICROS │ DEPENDENCY     │
├──────────────────────────────────────────────────────────────────┤
│ 2.1  │ Discovery               │ 2.1.1 │ glob           │
│      │                        │ 2.1.2 │ set_diff       │
│      │                        │ 2.1.3 │ git_ls        │
├──────────────────────────────────────────────────────────────────┤
│ 2.2  │ Seed Validation        │ 2.2.1 │ yaml_parse    │
│      │                        │ 2.2.2 │ regex_match  │
│      │                        │ 2.2.3 │ set_member  │
├──────────────────────────────────────────────────────────────────┤
│ 2.3  │ CLAUDE.md Validation   │ 2.3.1 │ path_exists  │
│      │                        │ 2.3.2 │ regex_find  │
├──────────────────────────────────────────────────────────────────┤
│ 2.4  │ Dependency Graph     │ 2.4.1 │ yaml_deep   │
│      │                        │ 2.4.2 │ dfs_cycle   │
├──────────────────────────────────────────────────────────────────┤
│ 2.5  │ Governance State     │ 2.5.1 │ state_check │
│      │                        │ 2.5.2 │ trans_mat  │
├──────────────────────────────────────────────────────────────────┤
│ 2.6  │ IRF Registry        │ 2.6.1 │ regex       │
│      │                        │ 2.6.2 │ irf_range  │
├──────────────────────────────────────────────────────────────────┤
│ 2.7  │ Report Generation  │ 2.7.1 │ jinja2      │
│      │                        │ 2.7.2 │ json_dump  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Appendix B: Performance Targets

| Audit Phase | Target Time | Max Time |
|------------|------------|----------|
| Discovery | 5s | 30s |
| Seed Validation | 30s | 2min |
| CLAUDE.md Validation | 10s | 1min |
| Dependency Graph | 5s | 30s |
| Governance State | 5s | 30s |
| IRF Registry | 3s | 15s |
| Report Generation | 3s | 15s |
| **TOTAL** | **61s** | **5min** |

---

## Appendix C: Severity Classification

| Severity | Definition | SLA |
|---------|------------|-----|
| CRITICAL | Repo cannot function | 24h |
| HIGH | Major functionality missing | 7d |
| MEDIUM | Non-blocking issue | 30d |
| LOW | Cosmetic or enhancement | 90d |

---

*Last updated: 2026-04-26*
*Version: 2.1.0*
*SOP-002: Comprehensive Workspace Audit Procedure*