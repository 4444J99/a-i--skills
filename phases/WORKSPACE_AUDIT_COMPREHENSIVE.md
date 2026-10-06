# FULL WORKSPACE AUDIT — COMPREHENSIVE
## organvm Ecosystem — 2026-04-26

---

## VERIFIED STATISTICS

| Metric | Count |
|---|---|
| **Total directories** | 120 |
| **With seed.yaml** | 104 |
| **With CLAUDE.md** | ~90 |
| **Missing both** | 16 |

---

## ORGAN DISTRIBUTION

| Organ | Count | Notes |
|---|---|---|
| **IV** (Agents) | 36 | Largest - MCP servers, agent frameworks |
| **I** (Theoria) | 15 | Knowledge, atoms, linguistics |
| **II** (Ergon) | 7 | Creative, artistic |
| **III** (Kerygma) | 8 | Content, distribution |
| **V** ( Praxis) | 6 | Operations, execution |
| **VI** (Koinonia) | 5 | Community |
| **VII** (Krypteia) | 5 | Governance |
| **Meta** | 8 | Meta-organizational |
| **THEORIA** | 1 | mesh |
| **SOVEREIGN** | 1 | sovereign systems |
| **PERSONAL** | 1 | personal workspace |
| **NO_SEED** | 16 | Need seeding |

---

## REPOS WITH SEED.YAML (104)

```
ORGAN-I (Theoria) — Knowledge Systems
├── atomic-substrata — Atoms, primitives
├── auto-revision-epistemic-engine — Epistemic revision
├── call-function--ontological — Ontological function calling
├── cognitive-archaelogy-tribunal — Cognitive archaeology
├── linguistic-atomization-framework — Language atomization
├── mesh — Universal reference mesh (5 primitives)
├── narratological-algorithmic-lenses — Narrative algorithms
├── reading-observatory — Reading tracking
├── recursive-engine--generative-entity — Recursive entity engine
├── schema-definitions — Schema library
├── universal-node-network — Node network
├── .github-org — GitHub org config

ORGAN-II (Ergon) — Creative Systems
├── a-mavs-olevm — ???
├── alchemical-synthesizer — Alchemical synthesis
├── chthon-oneiros — Oneiros system
├── classroom-rpg-aetheria — RPG classroom
├── materia-collider — Materia collisions
├── sema-metra--alchemica-mundi — Alchemical semiotics

ORGAN-III (Kerygma) — Content/Distribution
├── content-engine--asset-amplifier — Content amplification
├── commerce--meta — Commerce metadata
├── essay-pipeline — Essay pipeline
├── distribution-strategy — Distribution strategy
├── social-automation — Social automation
├── peer-audited--behavioral-blockchain — Behavioral blockchain

ORGAN-IV (Organon) — Agent Systems
├── agent--claude-smith — Claude Smith agent
├── agentic-titan — Agentic Titan
├── collective-persona-operations — Persona collective
├── contrib--* — 25+ MCP/contrib repos
├── growth-auditor — Growth auditing
├── kerygma-pipeline — Kerygma pipeline
├── kerygma-profiles — Kerygma profiles
├── tool-interaction-design — Tool interaction

ORGAN-V (Praxis) — Operations
├── analytics-engine — Analytics
├── announcement-templates — Announcements
├── carrier-wave--zeitgeist-thesis — Zeitgeist carrier
├── krypto-velamen — Crypto veil
├── public-record-data-scrapper — Public records
├── system-dashboard — System dashboard

ORGAN-VI (Koinonia) — Community
├── adaptive-personal-syllabus — Adaptive syllabus
├── community-hub — Community hub
├── ivi374ivi027-05 — ???
├── k6-contrib — K6 contributions
├── reading-group-curriculum — Reading group

ORGAN-VII (Krypteia) — Governance
├── aerarium--res-publica — Public res
├── custodian-securitatis — Security
├── cvrsvs-honorvm — Honor
├── public-process — Public process
├── rules-system-bound — Rules system
├── scale-threshold-emergence — Scale emergence
├── styx-behavioral-art — Styx behavioral
├── styx-behavioral-economics-theory — Styx economics
├── system-governance-framework — Governance framework

META
├── organvm-engine — Engine
├── organvm-mcp-server — MCP server
├── organvm-corpvs-testamentvm — Corpvs Testamentvm
├── organvm-ontologia — Ontology
├── praxis-perpetua — Perpetual praxis
├── organvm-organizational — Org tools

SPECIAL
├── [client repo — redacted]
├── sovereign--ground — Ground
├── [client repo — redacted]
├── stakeholder-portal — Stakeholder portal
├── studium-generale — General study

BENCH (archived/inactive)
├── matter-collider/bench/* — 50+ bench repos

---

## REPOS WITHOUT SEED.YAML (16)

These need seeding:

```
agentkit — ???
blender-mcp — Blender MCP
fastmcp — Fast MCP
gemini-cli-blender-extension — Gemini Blender
openai-agents-contrib — OpenAI agents
post-flood — Post-flood archive
python-sdk — Python SDK
[client repo — redacted] — *** WAITING FOR SPEC ***
system-system--system--monad — Monad system
tmp_organvm-i-theoria.github.io — Temp github.io
... (10 more)
```

---

## INCOMPLETE REPOS (NO CLAUDE.MD)

```
contrib--a2aproject-a2a-python
contrib--anthropics-anthropic-sdk-python
contrib--camel-ai-camel
contrib--coinbase-agentkit
contrib--dapr-dapr
contrib--databricks-dbt-databricks
contrib--datadog-guarddog
contrib--modelcontextprotocol-python-sdk
contrib--prefecthq-fastmcp
contrib--tadata-org-fastapi-mcp
```

---

## KEY REPOS FOR PHASES

### Phase 1: Content Deliverables
| Repo | Purpose |
|---|---|
| essay-pipeline | Content pipeline |
| distribution-strategy | Distribution |
| social-automation | Social |
| stakeholder-portal | Client portal |

### Phase 2: Architecture
| Repo | Purpose |
|---|---|
| schema-definitions | Schema library |
| mesh | Reference mesh |
| linguistic-atomization-framework | Language atoms |
| narratological-algorithmic-lenses | Narrative lenses |

### Phase 3: Execution
| Repo | Purpose |
|---|---|
| organvm-engine | Core engine |
| organvm-mcp-server | MCP integration |
| tool-interaction-design | Tool design |

### Phase 4: Rigor
| Repo | Purpose |
|---|---|
| analytics-engine | Analytics |
| growth-auditor | Growth tracking |
| system-dashboard | Dashboards |

---

## DEPENDENCY GRAPH (Partial)

```
schema-definitions
  ↑
  ├── mesh (uses schemas)
  ├── linguistic-atomization-framework (uses schemas)
  └── tool-interaction-design (uses schemas)

organvm-engine
  ↑
  ├── organvm-mcp-server
  ├── tool-interaction-design
  └── content-engine--asset-amplifier

peer-audited--behavioral-blockchain
  ↑
  └── stakeholder-portal

growth-auditor
  ↑
  └── analytics-engine
```

---

## PRIORITY SEEDING (16 repos)

| Priority | Repo | Why |
|---|---|---|
| P0 | [client repo — redacted] | Waiting for spec |
| P1 | agentkit | Active agent framework |
| P1 | fastmcp | Fast MCP server |
| P2 | python-sdk | SDK coverage |
| P2 | openai-agents-contrib | OpenAI agents |
| P3 | blender-mcp | Blender integration |
| P3 | gemini-cli-blender-extension | Gemini extension |

---

## FILE STRUCTURE SUMMARY

```
organvm/
├── .atoms/              # Atoms definitions
├── .claude/             # Claude config
├── .github/             # GitHub config
├── a-i--skills/         # Skills repo (WE ARE HERE)
├── organvm-engine/      # Core engine
├── organvm-corpvs-testamentvm/ # IRF, Omega
├── schema-definitions/  # Schemas
├── mesh/               # Reference mesh
├── tool-interaction-design/ # Tool design
├── [client repos — redacted]
└── [100+ more repos]
```

---

*Generated by audit_workspace.py — 2026-04-26*