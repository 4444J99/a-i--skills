# Workflow Integration: Time Series Analyst

This document describes how `time-series-analyst` integrates with other skills in the Data Science & Analytics ecosystem.

## Related Skills

| Skill | Relationship | When to Invoke |
|-------|--------------|----------------|
| `data-pipeline-architect` | **Upstream** | Design time-partitioned pipelines |
| `ml-experiment-tracker` | **Complementary** | Track forecasting experiments |
| `systemic-product-analyst` | **Complementary** | Temporal product patterns |
| `sql-query-optimizer` | **Upstream** | Optimize time-range queries |
| `data-storytelling-analyst` | **Downstream** | Visualize temporal patterns |

## Prerequisites

Before invoking `time-series-analyst`, ensure:

1. **Time data available** - Regular interval observations
2. **Granularity defined** - Hourly, daily, weekly, etc.
3. **History depth known** - How much historical data

## Handoff Patterns

### From: data-pipeline-architect

**Trigger:** Time series data pipeline ready.

**What to receive:**
- Timestamp handling approach
- Aggregation intervals
- Gap handling strategy

**Integration points:**
- Validate time series continuity
- Handle missing values
- Align to consistent intervals

### To: ml-experiment-tracker

**Trigger:** Forecasting models need tracking.

**What to hand off:**
- Temporal features engineered
- Seasonality components
- Training/validation split approach

**Expected output from tracker:**
- Tracked forecast experiments
- Model comparison metrics
- Production model selection

### To: systemic-product-analyst

**Trigger:** Temporal patterns inform product analysis.

**What to hand off:**
- Trend analysis results
- Seasonality patterns
- Anomaly detection outputs

**Expected output from product:**
- Product behavior correlations
- Event impact analysis
- Trend-adjusted metrics

### To: data-storytelling-analyst

**Trigger:** Temporal insights ready for visualization.

**What to hand off:**
- Trend decompositions
- Forecasts with intervals
- Pattern highlights

**Expected output from storytelling:**
- Time series visualizations
- Forecast dashboards
- Trend comparison charts

## Workflow Sequence

```
┌─────────────────────────────────────────────────────────────┐
│                    Time Series Analysis Flow                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. DATA-PIPELINE-ARCHITECT: Prepare time series data      │
│           │                                                 │
│           ▼                                                 │
│  2. SQL-QUERY-OPTIMIZER: Optimize time-range queries       │
│           │                                                 │
│           ▼                                                 │
│  3. TIME-SERIES-ANALYST: Analyze patterns                  │
│           │                                                 │
│           ├──────────────────────────────────────┐          │
│           ▼                                      ▼          │
│  4a. ML-EXPERIMENT-TRACKER   4b. SYSTEMIC-PRODUCT-ANALYST  │
│      (forecasting)               (temporal insights)       │
│           │                                      │          │
│           └──────────────────────────────────────┘          │
│                          │                                  │
│                          ▼                                  │
│  5. DATA-STORYTELLING-ANALYST: Visualize results           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Integration Checklist

Before completing time series analysis, verify:

- [ ] Data frequency is consistent
- [ ] Missing values handled appropriately
- [ ] Seasonality components identified
- [ ] Trend direction established
- [ ] Outliers detected and addressed
- [ ] Stationarity assessed
- [ ] Appropriate model family selected
- [ ] Cross-validation uses time-aware splits

## Common Scenarios

### Demand Forecasting

1. **Data Pipeline Architect:** Historical sales pipeline
2. **Time Series Analyst:** Decomposition and patterns
3. **ML Experiment Tracker:** Track forecast models
4. **Data Storytelling Analyst:** Forecast dashboard

### Anomaly Detection

1. **Data Pipeline Architect:** Real-time metrics stream
2. **Time Series Analyst:** Baseline and deviation analysis
3. **Systemic Product Analyst:** Root cause investigation

### Seasonal Planning

1. **Time Series Analyst:** Identify seasonal patterns
2. **Systemic Product Analyst:** Product impact analysis
3. **Data Storytelling Analyst:** Planning presentation

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Random train/test split | Data leakage | Use time-based splits |
| Ignoring seasonality | Poor forecasts | Decompose and model seasonality |
| No stationarity check | Invalid model assumptions | Test and transform if needed |
| Single point forecasts | False precision | Use prediction intervals |

## Related Resources

- [Data Science Skills Ecosystem Map](../../../docs/guides/data-science-skills-ecosystem.md)
