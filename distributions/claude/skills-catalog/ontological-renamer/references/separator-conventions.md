# Separator Conventions

Detailed rules for using hyphens in ontological naming.

## Separator Types

| Separator | Symbol | Use Case |
|-----------|--------|----------|
| Single Hyphen | `-` | Compound words, close concepts |
| Double Hyphen | `--` | Conceptual distance, categories |
| Underscore | `_` | Avoid (use hyphen instead) |
| CamelCase | `N/A` | Only for code, not naming |

## Single Hyphen Rules

### Rule 1: Compound Nouns

Join two nouns that form a single concept.

```
skill-bundle      "a bundle of skills"
knowledge-base    "a base of knowledge"
code-forge        "a forge for code"
data-lake         "a lake of data"
```

### Rule 2: Adjective-Noun

Modifier attached to the thing it describes.

```
smart-agent       "an agent that is smart"
fast-cache        "a cache that is fast"
secure-vault      "a vault that is secure"
lightweight-lib   "a library that is lightweight"
```

### Rule 3: Verb-Object (Compound Action)

Action and what it acts upon, as a unit.

```
build-tool        "tool that builds"
test-runner       "runner of tests"
code-generator    "generator of code"
log-shipper       "shipper of logs"
```

### Rule 4: Noun-Verb (Gerund)

Thing performing ongoing action.

```
load-balancing    "balancing of load"
event-sourcing    "sourcing from events"
rate-limiting     "limiting of rate"
cache-warming     "warming of cache"
```

### Test: Magnetic Proximity

If the words "want" to be together (removing one breaks the meaning), use single hyphen.

```
skill-bundle → "skill" alone or "bundle" alone loses meaning
            → Single hyphen ✓

agent-powered → "agent" modifies "powered"
             → Single hyphen ✓
```

## Double Hyphen Rules

### Rule 1: Category Separation

Separating domain/category from instance/implementation.

```
dev-tools--linter
├── dev-tools    (category)
└── linter       (specific tool)

auth-system--jwt-handler
├── auth-system  (system type)
└── jwt-handler  (implementation)
```

### Rule 2: What vs How

Separating what something is from how it works.

```
storage--distributed-cache
├── storage     (what it provides)
└── distributed-cache (how it does it)

messaging--event-queue
├── messaging   (what it does)
└── event-queue (mechanism)
```

### Rule 3: Container vs Contents

Clear separation between vessel and payload.

```
vault--credentials
├── vault       (container)
└── credentials (contents)

registry--microservices
├── registry    (container)
└── microservices (contents)
```

### Rule 4: Interface vs Implementation

Separating abstraction from concrete.

```
database--postgres-adapter
├── database   (interface/concept)
└── postgres-adapter (implementation)

cache--redis-backend
├── cache      (abstraction)
└── redis-backend (concrete)
```

### Test: Conceptual Distance

If words represent different "levels" or "layers", use double hyphen.

```
frontend--react-components
├── frontend (layer)
└── react-components (technology choice)
→ Double hyphen ✓

skill-codex--agent-mastery
├── skill-codex (what it is)
└── agent-mastery (what it provides)
→ Double hyphen ✓
```

## Decision Matrix

| Relationship | Examples | Separator |
|--------------|----------|-----------|
| Adjective + Noun | `fast-cache`, `secure-vault` | `-` |
| Noun + Noun (compound) | `skill-bundle`, `code-forge` | `-` |
| Verb + Object | `test-runner`, `log-shipper` | `-` |
| Noun + Gerund | `load-balancing`, `rate-limiting` | `-` |
| Category + Instance | `tools--linter`, `db--postgres` | `--` |
| Container + Contents | `vault--secrets`, `cache--data` | `--` |
| What + How | `storage--redis`, `auth--oauth` | `--` |
| Concept + Implementation | `api--rest-handler` | `--` |

## Combined Usage

### Pattern: `[compound]-[word]--[compound]-[word]`

```
agent-skill--knowledge-forge
├── agent-skill (compound: skills for agents)
├── --          (separates what from how)
└── knowledge-forge (compound: forge of knowledge)
```

### Pattern: `[single]--[compound]-[compound]`

```
cache--memory-store-manager
├── cache   (what)
├── --      (separation)
└── memory-store-manager (how: compound)
```

### Pattern: `[compound]--[single]`

```
api-gateway--auth
├── api-gateway (compound)
├── --          (separation)
└── auth        (focused function)
```

## Common Mistakes

### Mistake 1: Inconsistent Separators

```
❌ skill_bundle--agent-mastery   (mixing _ and -)
✓  skill-bundle--agent-mastery  (consistent)
```

### Mistake 2: Wrong Level of Separation

```
❌ skill--bundle   (too distant for compound)
✓  skill-bundle   (compound noun)

❌ api-gateway-auth-handler   (missing category break)
✓  api-gateway--auth-handler (category separated)
```

### Mistake 3: Unnecessary Double Hyphen

```
❌ fast--cache   (adjective doesn't need distance)
✓  fast-cache   (simple modifier)

❌ test--runner  (compound verb-object)
✓  test-runner  (stays together)
```

### Mistake 4: Missing Double Hyphen

```
❌ vault-secrets-manager   (unclear structure)
✓  vault--secrets-manager (clear: vault containing secrets-manager)

❌ frontend-react-app   (all same level?)
✓  frontend--react-app  (layer separated from tech)
```

## Validation Checklist

When naming, verify:

- [ ] Single hyphens join magnetically close concepts
- [ ] Double hyphens separate conceptual levels
- [ ] No mixing of underscore and hyphen
- [ ] Structure reads naturally left-to-right
- [ ] Each segment is meaningful alone
- [ ] Total length is reasonable (2-5 words)

## Quick Reference

```
Close concepts (compound):     word-word
Different levels (separation): word--word
Combined:                      word-word--word-word
```
