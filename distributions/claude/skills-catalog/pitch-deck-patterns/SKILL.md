---
name: pitch-deck-patterns
description: Create compelling pitch decks for startups, projects, and internal proposals. Covers narrative structure, slide design principles, data visualization, and audience-specific adaptation. Triggers on pitch deck creation, presentation design, or fundraising deck requests.
license: MIT
complexity: intermediate
time_to_learn: 30min
tags:
  - pitch-deck
  - presentations
  - storytelling
  - fundraising
  - proposals
governance_phases: [shape]
organ_affinity: [all]
triggers: [user-asks-about-pitch-deck, context:presentation, context:fundraising, context:proposal]
complements: [portfolio-presentation, workshop-presentation-design, content-distribution]
---

# Pitch Deck Patterns

Build presentations that communicate vision, demonstrate value, and compel action.

## Narrative Structures

### The Classic 10-Slide Pitch

| Slide | Purpose | Time |
|-------|---------|------|
| 1. **Title** | Name, tagline, contact | 15s |
| 2. **Problem** | Pain point with evidence | 1min |
| 3. **Solution** | How you solve it | 1min |
| 4. **Demo/Product** | Show, don't tell | 2min |
| 5. **Market** | TAM/SAM/SOM, growth | 1min |
| 6. **Business Model** | How you make money | 1min |
| 7. **Traction** | Metrics, milestones, users | 1min |
| 8. **Team** | Why this team wins | 30s |
| 9. **Ask** | What you need, what they get | 30s |
| 10. **Contact** | CTA, next steps | 15s |

### The Problem-First Arc

```
Hook → Pain → Failed Solutions → Your Insight → Product → Evidence → Vision → Ask
```

Best for: Markets where the problem is well-known but solutions are bad.

### The Vision-First Arc

```
Vision → Why Now → How → Product → Traction → Team → Ask
```

Best for: Category-creating products where the vision is the differentiator.

### The Traction-First Arc

```
Results → How We Did It → The Market → The Team → What's Next → Ask
```

Best for: Growth-stage pitches where numbers speak louder than vision.

## Slide Design Principles

### One Idea Per Slide

```
BAD: Slide with 5 bullet points, a chart, and a screenshot
GOOD: One clear statement + one supporting visual
```

### The 3-Second Rule

A viewer should grasp the slide's point within 3 seconds. If they can't, simplify.

### Visual Hierarchy

```
1. Headline (largest, boldest)     → The claim
2. Key visual (chart/screenshot)   → The evidence
3. Supporting text (smallest)      → The context
```

### Data Visualization

| Data Type | Best Chart | Avoid |
|-----------|-----------|-------|
| Trend over time | Line chart | Pie chart |
| Comparison | Bar chart | 3D chart |
| Part of whole | Stacked bar, treemap | Pie chart (>5 segments) |
| Relationship | Scatter plot | Table |
| Single metric | Large number | Any chart |

### The Big Number Slide

```
┌─────────────────────────────┐
│                             │
│         47%                 │
│   reduction in deploy time  │
│                             │
│   (from 45min to 24min)     │
│                             │
└─────────────────────────────┘
```

## Content Patterns

### Problem Slide

**Formula:** Specific pain + Quantified impact + Who feels it

```
"Engineering teams waste 15 hours/week on manual deployment tasks.
For a 50-person team, that's $1.2M/year in lost productivity."
```

### Solution Slide

**Formula:** What it does + How it's different + Key benefit

```
"One-click deployment pipelines that integrate with your existing
CI/CD stack. No migration needed — install and deploy in 5 minutes."
```

### Market Slide

**TAM/SAM/SOM Framework:**
- **TAM** (Total Addressable Market): Everyone who could use it
- **SAM** (Serviceable Addressable Market): Your reachable segment
- **SOM** (Serviceable Obtainable Market): What you'll capture in 2-3 years

### Traction Slide

Show growth trajectory, not just current numbers:

```
Month 1: 50 users
Month 3: 500 users
Month 6: 5,000 users
Month 12: 50,000 users (projected)
```

### Team Slide

Focus on: **Why this team?** Not resume bullets, but relevant achievements.

```
"Previously built and sold DevToolCo (acquired by BigCorp).
15 years combined experience in CI/CD infrastructure.
Early engineers at [credible company]."
```

## Audience Adaptation

| Audience | Emphasize | De-emphasize |
|----------|-----------|-------------|
| Investors | Market, traction, team | Technical details |
| Technical | Architecture, scalability | Business model |
| Executives | ROI, risk, timeline | Implementation details |
| Internal | Impact, resources needed | Market analysis |

## Delivery Tips

### Timing

- **5 minutes:** Problem + Solution + Demo + Ask
- **10 minutes:** Full 10-slide deck
- **20 minutes:** Deck + deep-dive on 2-3 slides + Q&A
- **30 minutes:** Full deck + demo + extensive Q&A

### Opening Hooks

- **Startling statistic:** "90% of deployments fail on first attempt"
- **Story:** "Last month, our team lost 3 days to a broken deploy..."
- **Question:** "How many hours does your team spend on deployments?"
- **Demonstration:** Start with the product, then explain the context

## Anti-Patterns

- **Wall of text** — If it's readable as a document, it's not a presentation
- **Feature list** — Benefits, not features; outcomes, not capabilities
- **Vanity metrics** — "10M downloads" without engagement or revenue context
- **Missing the ask** — Always end with a clear, specific call to action
- **One-size-fits-all** — Adapt emphasis for each audience
- **Demo disasters** — Pre-record demos or have a screenshot fallback
