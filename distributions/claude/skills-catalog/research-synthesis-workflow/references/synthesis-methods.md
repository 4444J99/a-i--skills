# Research Synthesis Methods

## Thematic Analysis

### Process

1. **Familiarization**: Read through all material
2. **Coding**: Label meaningful segments
3. **Theme Search**: Group codes into themes
4. **Theme Review**: Refine and validate themes
5. **Theme Definition**: Name and describe themes
6. **Writing**: Present with evidence

### Coding Example

```markdown
## Raw Note
"Vector databases show 3-5x performance improvement
over PostgreSQL for similarity search at scale"

## Codes Applied
- [performance] - quantitative comparison
- [vector-db] - technology category
- [scale] - scalability context
- [benchmark] - empirical evidence

## Theme Assignment
→ "Performance characteristics" theme
→ "Technology selection criteria" theme
```

### Theme Development

```
Level 1 (Codes):        Level 2 (Sub-themes):    Level 3 (Themes):

[latency]           ─┐
[throughput]        ─┼── Query Performance    ─┐
[batch-speed]       ─┘                         │
                                               ├── PERFORMANCE
[memory-usage]      ─┐                         │
[disk-footprint]    ─┼── Resource Usage       ─┘
[cpu-utilization]   ─┘

[setup-complexity]  ─┐
[maintenance]       ─┼── Operations           ─┐
[monitoring]        ─┘                         │
                                               ├── OPERATIONS
[pricing]           ─┐                         │
[hidden-costs]      ─┼── Economics            ─┘
[scaling-costs]     ─┘
```

## Framework Synthesis

### Building Comparison Frameworks

```markdown
## Decision Framework: [Topic]

### Dimensions Identified
From synthesis, key decision factors are:
1. [Dimension 1]: Description
2. [Dimension 2]: Description
3. [Dimension 3]: Description

### Option Comparison

| Option | Dim 1 | Dim 2 | Dim 3 | Best For |
|--------|-------|-------|-------|----------|
| A      | +++   | +     | ++    | Use case |
| B      | +     | +++   | ++    | Use case |
| C      | ++    | ++    | +++   | Use case |

### Decision Tree
1. If [condition] → Option A
2. Else if [condition] → Option B
3. Else → Option C
```

## Narrative Synthesis

### Structure

1. **Introduction**: Research question, scope
2. **Search Strategy**: How sources found
3. **Findings by Theme**: Organized presentation
4. **Discussion**: Integration, implications
5. **Limitations**: Gaps, uncertainties
6. **Conclusions**: Key takeaways

### Writing Patterns

**Presenting Agreement:**
"Multiple sources (A, B, C) converge on..."
"The literature consistently shows..."
"There is broad consensus that..."

**Presenting Disagreement:**
"However, some authors (D, E) argue..."
"In contrast, [Source] finds..."
"This is disputed by..."

**Synthesizing:**
"Taken together, these findings suggest..."
"When considering both views..."
"The balance of evidence indicates..."

## Meta-Analysis (Quantitative)

### Effect Size Calculation

```python
import numpy as np
from scipy import stats

def cohens_d(group1, group2):
    """Calculate Cohen's d effect size"""
    n1, n2 = len(group1), len(group2)
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    pooled_std = np.sqrt(((n1-1)*var1 + (n2-1)*var2) / (n1+n2-2))
    return (np.mean(group1) - np.mean(group2)) / pooled_std

# Interpretation
# |d| < 0.2: Small effect
# 0.2 <= |d| < 0.8: Medium effect
# |d| >= 0.8: Large effect
```

### Combining Studies

```python
def weighted_mean_effect(effects, variances):
    """Fixed-effects meta-analysis"""
    weights = 1 / np.array(variances)
    weighted_effect = np.sum(effects * weights) / np.sum(weights)
    combined_variance = 1 / np.sum(weights)
    return weighted_effect, np.sqrt(combined_variance)
```

## Contradiction Resolution

### Matrix for Tracking Disagreements

| Topic | Position A | Position B | Source A | Source B | Resolution |
|-------|-----------|-----------|----------|----------|------------|
| X     | Claim     | Counter   | [Ref]    | [Ref]    | Analysis   |

### Resolution Strategies

1. **Methodological Differences**
   - Were different methods used?
   - Different sample sizes/populations?

2. **Contextual Differences**
   - Different time periods?
   - Different domains/industries?

3. **Definitional Differences**
   - Are they defining terms differently?
   - Different scope of claims?

4. **Evidence Quality**
   - Which has stronger evidence?
   - More rigorous methodology?

5. **Possible Integration**
   - Can both be true in different contexts?
   - Is there a synthesis that reconciles?

## Gap Analysis

### Identifying Gaps

Questions to ask:
- What questions remain unanswered?
- What aspects weren't studied?
- What populations weren't included?
- What contexts weren't examined?
- What methods weren't tried?

### Gap Documentation

```markdown
## Research Gap: [Topic]

**Current State:**
What is known...

**Gap Description:**
What is unknown or unstudied...

**Why It Matters:**
Implications of the gap...

**Potential Approaches:**
How the gap could be addressed...

**Sources Noting This Gap:**
References that acknowledge this limitation...
```
