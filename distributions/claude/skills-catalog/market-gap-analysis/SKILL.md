---
name: market-gap-analysis
description: Analyze market positioning, identify underserved segments, and map competitive gaps using systematic frameworks. Covers SWOT analysis, competitive landscape mapping, opportunity scoring, and positioning strategy. Triggers on market analysis, competitive research, or gap identification requests.
license: MIT
complexity: intermediate
time_to_learn: 30min
tags:
  - market-analysis
  - competitive-research
  - gap-analysis
  - positioning
  - strategy
governance_phases: [shape]
organ_affinity: [all]
triggers: [user-asks-about-market-analysis, context:competitive-research, context:market-positioning, context:gap-analysis]
complements: [systemic-product-analyst, product-requirements-designer, research-synthesis-workflow]
---

# Market Gap Analysis

Identify underserved markets and competitive positioning opportunities through systematic analysis.

## Analysis Framework

```
Market Scan → Competitor Map → Gap Identification → Opportunity Scoring → Strategy
     │              │                  │                    │              │
     │              │                  │                    │              └─ Positioning
     │              │                  │                    └─ Prioritized gaps
     │              │                  └─ Unserved/underserved areas
     │              └─ Feature/capability matrix
     └─ Total landscape understanding
```

## Market Scanning

### TAM/SAM/SOM Analysis

```markdown
## Market Size

### Total Addressable Market (TAM)
- Market: {broad market definition}
- Size: ${amount} ({year})
- Growth: {CAGR}%
- Source: {citation}

### Serviceable Addressable Market (SAM)
- Segment: {specific segment you can reach}
- Size: ${amount}
- Criteria: {geographic, demographic, or technical constraints}

### Serviceable Obtainable Market (SOM)
- Realistic capture: ${amount} over {timeframe}
- Assumptions: {market share %, conversion rates}
```

### Market Segmentation

| Segment | Size | Growth | Competition | Fit |
|---------|------|--------|-------------|-----|
| Enterprise | $2B | 12% | High | Medium |
| SMB | $800M | 18% | Medium | High |
| Developer tools | $500M | 25% | Low | High |
| Education | $300M | 8% | Low | Medium |

## Competitive Landscape

### Feature Matrix

```markdown
| Capability | Us | Competitor A | Competitor B | Competitor C |
|------------|:--:|:-----------:|:-----------:|:-----------:|
| Core feature 1 | ● | ● | ◐ | ○ |
| Core feature 2 | ● | ○ | ● | ● |
| Feature 3 | ◐ | ● | ○ | ○ |
| Feature 4 | ○ | ○ | ○ | ○ |
| Integration X | ● | ◐ | ● | ○ |

● = Full support  ◐ = Partial  ○ = None
```

### Positioning Map

```
        High Price
            │
    Enterprise │ Premium
    Solutions  │ Tools
            │
Low ────────┼──────── High
Innovation  │         Innovation
            │
    Legacy   │ Open Source /
    Tools    │ Community
            │
        Low Price
```

### Competitor Profiles

```markdown
## {Competitor Name}

**Positioning:** {one-sentence positioning}
**Target:** {primary customer segment}
**Pricing:** {model and range}
**Strengths:** {2-3 key strengths}
**Weaknesses:** {2-3 key weaknesses}
**Recent moves:** {latest product/market changes}
**Threat level:** High / Medium / Low
```

## Gap Identification

### Gap Types

| Gap Type | Description | Signal |
|----------|-------------|--------|
| **Feature gap** | Missing capability | Feature requests, workarounds |
| **Segment gap** | Unserved customer type | Forums, job boards, community |
| **Price gap** | No option at price point | Customer complaints, DIY solutions |
| **Integration gap** | Missing connection | Stack compatibility issues |
| **Quality gap** | Poor existing solutions | Low satisfaction, high churn |
| **Geography gap** | Unserved region | Language/compliance gaps |

### Gap Discovery Methods

```markdown
### Direct Research
- Customer interviews (5-10 per segment)
- Support ticket analysis (top 20 requests)
- Feature request boards (competitor and own)
- App store reviews (1-star and 3-star)

### Indirect Research
- Job postings (what tools are companies hiring for?)
- Stack Overflow questions (what problems remain unsolved?)
- Reddit/community forums (what workarounds exist?)
- Conference talks (what problems are speakers addressing?)
```

## Opportunity Scoring

### ICE Framework

| Opportunity | Impact (1-10) | Confidence (1-10) | Ease (1-10) | Score |
|------------|:-----:|:-----:|:-----:|:-----:|
| Developer API | 9 | 7 | 5 | 7.0 |
| Mobile app | 6 | 8 | 3 | 5.7 |
| Enterprise SSO | 8 | 9 | 7 | 8.0 |
| Free tier | 7 | 6 | 8 | 7.0 |

Score = (Impact + Confidence + Ease) / 3

### RICE Framework

| Opportunity | Reach | Impact | Confidence | Effort | Score |
|------------|:-----:|:------:|:----------:|:------:|:-----:|
| Developer API | 500 | 3 | 80% | 3 months | 400 |
| Mobile app | 2000 | 1 | 60% | 6 months | 200 |

Score = (Reach × Impact × Confidence) / Effort

## Positioning Strategy

### Positioning Statement Template

```
For {target customer}
who {need/problem},
{product name} is a {category}
that {key benefit}.
Unlike {primary competitor},
we {key differentiator}.
```

### Strategic Options

| Strategy | When | Example |
|----------|------|---------|
| **Head-to-head** | Strong differentiator | Better UX than market leader |
| **Niche focus** | Underserved segment | "Built specifically for..." |
| **Blue ocean** | Category creation | New category definition |
| **Platform play** | Ecosystem potential | Extensibility as moat |
| **Price disruption** | Overpriced market | Free/open-source alternative |

## SWOT Analysis

```markdown
| | Positive | Negative |
|---|---------|----------|
| **Internal** | **Strengths** | **Weaknesses** |
| | • {strength 1} | • {weakness 1} |
| | • {strength 2} | • {weakness 2} |
| **External** | **Opportunities** | **Threats** |
| | • {opportunity 1} | • {threat 1} |
| | • {opportunity 2} | • {threat 2} |
```

## Anti-Patterns

- **Analysis paralysis** — Set a time-box; analysis that delays action costs more than imperfect analysis
- **Competitor obsession** — Focus on customer needs, not competitor features
- **Confirmation bias** — Seek disconfirming evidence, not just supporting data
- **Static analysis** — Markets change; revisit quarterly
- **Ignoring indirect competitors** — Spreadsheets, manual processes, and "do nothing" are competitors
- **Feature parity as strategy** — Matching competitors feature-for-feature is not differentiation
