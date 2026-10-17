# Workflow Integration: Systemic Product Analyst

This document describes how `systemic-product-analyst` integrates with other skills in the Data Science & Analytics ecosystem.

## Related Skills

| Skill | Relationship | When to Invoke |
|-------|--------------|----------------|
| `data-pipeline-architect` | **Upstream** | Set up product event pipelines |
| `sql-query-optimizer` | **Upstream** | Optimize metric queries |
| `time-series-analyst` | **Complementary** | Temporal product patterns |
| `ml-experiment-tracker` | **Complementary** | Model impact measurement |
| `data-storytelling-analyst` | **Downstream** | Present product insights |

## Prerequisites

Before invoking `systemic-product-analyst`, ensure:

1. **Event tracking in place** - User actions captured
2. **Key metrics defined** - Business-relevant KPIs
3. **User identity resolved** - Can track across sessions

## Handoff Patterns

### From: data-pipeline-architect

**Trigger:** Product event pipeline ready.

**What to receive:**
- Event schema definitions
- User identity mapping
- Session reconstruction logic

**Integration points:**
- Define computed metrics
- Build funnel queries
- Create cohort definitions

### From: sql-query-optimizer

**Trigger:** Metric queries optimized.

**What to receive:**
- Optimized aggregation queries
- Materialized view definitions
- Performance benchmarks

**Integration points:**
- Use optimized queries for analysis
- Set up metric caching
- Configure dashboard data sources

### To: time-series-analyst

**Trigger:** Need temporal pattern analysis.

**What to hand off:**
- Metric time series
- Event frequency data
- Cohort trends

**Expected output from time-series:**
- Trend analysis
- Seasonality patterns
- Forecasts for planning

### To: ml-experiment-tracker

**Trigger:** Measure model impact on product.

**What to hand off:**
- A/B test design
- Success metrics
- Treatment/control segments

**Expected output from tracker:**
- Experiment tracking setup
- Statistical significance analysis
- Model attribution

### To: data-storytelling-analyst

**Trigger:** Insights ready for stakeholders.

**What to hand off:**
- Key findings
- Metric trends
- Recommendations

**Expected output from storytelling:**
- Executive dashboard
- Insight presentations
- Actionable visualizations

## Workflow Sequence

```
┌─────────────────────────────────────────────────────────────┐
│                    Product Analysis Flow                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. DATA-PIPELINE-ARCHITECT: Set up event tracking         │
│           │                                                 │
│           ▼                                                 │
│  2. SQL-QUERY-OPTIMIZER: Optimize metric queries           │
│           │                                                 │
│           ▼                                                 │
│  3. SYSTEMIC-PRODUCT-ANALYST: Analyze product behavior     │
│           │                                                 │
│           ├──────────────────────────────────────┐          │
│           ▼                                      ▼          │
│  4a. TIME-SERIES-ANALYST      4b. ML-EXPERIMENT-TRACKER    │
│      (trend analysis)             (A/B tests)              │
│           │                                      │          │
│           └──────────────────────────────────────┘          │
│                          │                                  │
│                          ▼                                  │
│  5. DATA-STORYTELLING-ANALYST: Present insights            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Integration Checklist

Before completing product analysis, verify:

- [ ] Metrics accurately reflect business goals
- [ ] Funnel definitions are complete
- [ ] Cohort logic is consistent
- [ ] Segment definitions are mutually exclusive
- [ ] Statistical methods appropriate
- [ ] Confounding variables considered
- [ ] Recommendations are actionable
- [ ] Data freshness sufficient for decisions

## Common Scenarios

### Funnel Analysis

1. **Data Pipeline Architect:** Event tracking for funnel steps
2. **SQL Query Optimizer:** Fast funnel queries
3. **Systemic Product Analyst:** Funnel analysis and drops
4. **Data Storytelling Analyst:** Funnel visualization

### A/B Test Analysis

1. **Systemic Product Analyst:** Test design
2. **ML Experiment Tracker:** Track variants
3. **Systemic Product Analyst:** Statistical analysis
4. **Data Storytelling Analyst:** Results presentation

### Retention Analysis

1. **Data Pipeline Architect:** User activity pipeline
2. **Systemic Product Analyst:** Cohort retention analysis
3. **Time Series Analyst:** Retention trend analysis
4. **Data Storytelling Analyst:** Retention curves

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Vanity metrics | No actionable insights | Focus on leading indicators |
| P-hacking | False positives | Pre-register hypotheses |
| No segmentation | Missed nuances | Always segment key findings |
| Correlation = causation | Wrong conclusions | Use experimental methods |

## Related Resources

- [Data Science Skills Ecosystem Map](../../../docs/guides/data-science-skills-ecosystem.md)
