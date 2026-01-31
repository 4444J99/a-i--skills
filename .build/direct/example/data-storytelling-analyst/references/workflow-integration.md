# Workflow Integration: Data Storytelling Analyst

This document describes how `data-storytelling-analyst` integrates with other skills in the Data Science & Analytics ecosystem.

## Related Skills

| Skill | Relationship | When to Invoke |
|-------|--------------|----------------|
| `ml-experiment-tracker` | **Upstream** | Receive model results to visualize |
| `systemic-product-analyst` | **Upstream** | Receive product insights to present |
| `time-series-analyst` | **Upstream** | Receive temporal patterns to visualize |
| `sql-query-optimizer` | **Upstream** | Ensure dashboard queries are fast |
| `data-pipeline-architect` | **Upstream** | Pipeline health monitoring visuals |

## Prerequisites

Before invoking `data-storytelling-analyst`, ensure:

1. **Analysis complete** - Insights ready to communicate
2. **Audience identified** - Executive, technical, stakeholder
3. **Key message clear** - What action should result

## Handoff Patterns

### From: ml-experiment-tracker

**Trigger:** Experiment results ready for presentation.

**What to receive:**
- Model comparison metrics
- Feature importance rankings
- Performance over time

**Integration points:**
- Create experiment comparison charts
- Build feature importance visuals
- Design model performance dashboards

### From: systemic-product-analyst

**Trigger:** Product insights ready for stakeholders.

**What to receive:**
- Funnel analysis results
- Cohort behavior patterns
- Key metric trends

**Integration points:**
- Create executive dashboards
- Build funnel visualizations
- Design metric tracking charts

### From: time-series-analyst

**Trigger:** Temporal insights need visualization.

**What to receive:**
- Trend decompositions
- Seasonality patterns
- Forecasts with confidence intervals

**Integration points:**
- Design time-series charts
- Create forecast visualizations
- Build trend comparison views

### From: sql-query-optimizer

**Trigger:** Dashboard queries need to be fast.

**What to receive:**
- Optimized dashboard queries
- Query performance benchmarks
- Caching recommendations

**Integration points:**
- Integrate optimized queries
- Configure refresh strategies
- Set up query caching

## Workflow Sequence

```
┌─────────────────────────────────────────────────────────────┐
│                    Data Storytelling Flow                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. UPSTREAM ANALYSIS SKILLS: Complete analysis            │
│           │                                                 │
│           ├─────────────┬─────────────┬─────────────┐       │
│           ▼             ▼             ▼             ▼       │
│      ML-TRACKER    PRODUCT-ANALYST  TIME-SERIES  PIPELINE  │
│           │             │             │             │       │
│           └─────────────┴─────────────┴─────────────┘       │
│                          │                                  │
│                          ▼                                  │
│  2. SQL-QUERY-OPTIMIZER: Optimize visualization queries    │
│           │                                                 │
│           ▼                                                 │
│  3. DATA-STORYTELLING-ANALYST: Create visualizations       │
│           │                                                 │
│           ▼                                                 │
│  4. Present to stakeholders with narrative                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Integration Checklist

Before completing data storytelling, verify:

- [ ] Key message is clear and actionable
- [ ] Visualizations match audience level
- [ ] Color choices are accessible
- [ ] Axes and labels are clear
- [ ] Interactive elements work smoothly
- [ ] Dashboard loads quickly
- [ ] Mobile view considered
- [ ] Narrative flows logically

## Common Scenarios

### Executive Dashboard

1. **Systemic Product Analyst:** Key metrics identified
2. **SQL Query Optimizer:** Fast aggregation queries
3. **Data Storytelling Analyst:** Clean, high-level dashboard

### ML Results Presentation

1. **ML Experiment Tracker:** Best model selected
2. **Data Storytelling Analyst:** Model explanation visuals
3. **Data Storytelling Analyst:** Business impact narrative

### Forecasting Report

1. **Time Series Analyst:** Forecast models complete
2. **Data Storytelling Analyst:** Forecast visualization
3. **Data Storytelling Analyst:** Scenario comparisons

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Data dump | No story, overwhelming | Focus on key insights |
| Poor color choices | Accessibility issues | Use colorblind-safe palettes |
| Too many charts | Decision paralysis | Curate ruthlessly |
| Missing context | Numbers without meaning | Add benchmarks, comparisons |

## Related Resources

- [Data Science Skills Ecosystem Map](../../../docs/guides/data-science-skills-ecosystem.md)
