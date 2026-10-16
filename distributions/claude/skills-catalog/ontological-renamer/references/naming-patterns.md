# Naming Patterns

Common compound naming patterns and their applications.

## Pattern Categories

### 1. Domain-Function Pattern

`[domain]-[function]`

Describes what area and what it does.

```
code-analyzer      → Analyzes code
data-transformer   → Transforms data
api-gateway        → Gates API access
log-aggregator     → Aggregates logs
```

### 2. Actor-Action Pattern

`[actor]-[action]`

Describes who and what they do.

```
agent-builder      → Builds agents
user-authenticator → Authenticates users
task-scheduler     → Schedules tasks
event-dispatcher   → Dispatches events
```

### 3. Container-Contents Pattern

`[container]--[contents]`

Describes the vessel and what it holds.

```
vault--credentials     → Vault containing credentials
archive--documents     → Archive of documents
registry--components   → Registry of components
cache--responses       → Cache of responses
```

### 4. Metaphor-Domain Pattern

`[metaphor]--[domain]`

Uses evocative imagery for the domain.

```
forge--authentication  → Auth system as a forge
lighthouse--monitoring → Monitoring as a lighthouse
fabric--microservices  → Microservices as fabric
compass--navigation    → Navigation as a compass
```

### 5. Process-Product Pattern

`[process]--[product]`

Describes the transformation.

```
compile--bytecode      → Compilation to bytecode
render--html           → Rendering to HTML
parse--ast             → Parsing to AST
serialize--json        → Serialization to JSON
```

## Compound Word Formations

### Noun + Noun

Two nouns combined to create a new concept.

```
skill-bundle       → Bundle made of skills
knowledge-base     → Base of knowledge
code-forge         → Forge for code
data-lake          → Lake of data
```

### Adjective + Noun

Modifier describing the noun.

```
smart-agent        → Agent that is smart
fast-cache         → Cache that is fast
secure-vault       → Vault that is secure
distributed-mesh   → Mesh that is distributed
```

### Verb + Noun

Action applied to a thing.

```
build-system       → System for building
deploy-pipeline    → Pipeline for deploying
test-harness       → Harness for testing
watch-tower        → Tower for watching
```

### Noun + Verb (Gerund)

Thing performing action.

```
code-scanning      → Code that scans
log-shipping       → Logs being shipped
event-sourcing     → Events being sourced
load-balancing     → Load being balanced
```

## Multi-Word Patterns

### Three-Word Compounds

```
[domain]-[function]-[type]
api-rate-limiter           → Limits API rates
user-session-manager       → Manages user sessions
file-upload-handler        → Handles file uploads

[actor]-[action]-[target]
agent-task-executor        → Agent executes tasks
client-request-builder     → Client builds requests
server-response-formatter  → Server formats responses
```

### Four-Word Compounds (with --)

```
[left-compound]--[right-compound]
skill-bundle--agent-powers
agent-toolkit--knowledge-base
code-quality--analysis-engine
data-pipeline--transform-hub
```

## Pattern Selection Guide

| Use Case | Pattern | Example |
|----------|---------|---------|
| Library/Framework | Domain-Function | `http-client` |
| Service/System | Metaphor-Domain | `lighthouse--monitoring` |
| Tool/Utility | Actor-Action | `code-formatter` |
| Data Store | Container-Contents | `vault--secrets` |
| Transformation | Process-Product | `compile--native` |

## Metaphor Categories

### Construction Metaphors

```
forge      → Creation with heat/pressure
factory    → Mass production
builder    → Piece-by-piece assembly
architect  → Design and planning
scaffold   → Temporary support structure
```

### Container Metaphors

```
vault      → Secure storage
archive    → Long-term storage
cache      → Quick-access storage
pool       → Shared resources
reservoir  → Large capacity storage
```

### Nature Metaphors

```
stream     → Continuous flow
lake       → Data at rest
forest     → Complex hierarchy
mesh       → Interconnected network
web        → Linked structure
```

### Navigation Metaphors

```
compass    → Direction finding
lighthouse → Guidance beacon
map        → Overview/layout
route      → Path planning
gateway    → Entry point
```

### Weaving Metaphors

```
fabric     → Interconnected whole
weave      → Combining threads
loom       → Creating fabric
thread     → Single path
tapestry   → Complex combined work
```

## Pattern Combinations

### Layered Patterns

```
[metaphor]-[domain]--[function]-[type]

forge-auth--token-generator
├── forge-auth (metaphor applied to domain)
└── token-generator (what it produces)

vault-secrets--access-controller
├── vault-secrets (container with contents)
└── access-controller (function)
```

### Nested Patterns

```
[[noun-noun]-[verb]]--[[noun]-[noun]]

code-quality-analyzer--issue-tracker
├── code-quality-analyzer (thing that analyzes code quality)
└── issue-tracker (tracks the issues found)
```

## Common Pitfalls

### Redundant Patterns

```
❌ system-system       → Redundant
✓  system-core        → Better

❌ manager-controller  → Too similar
✓  session-controller → More specific
```

### Unclear Patterns

```
❌ thing-doer         → Too vague
✓  request-handler   → Specific

❌ data-stuff         → Meaningless
✓  data-transformer  → Clear purpose
```

### Inconsistent Patterns

```
❌ api_client-serverHandler  → Mixed conventions
✓  api-client--server-handler → Consistent
```

## Validation Checklist

- [ ] Pattern is recognizable
- [ ] Components are specific, not vague
- [ ] Relationship between parts is clear
- [ ] No redundant information
- [ ] Consistent separator usage
- [ ] Appropriate length (2-5 words)
- [ ] Domain appropriate vocabulary
