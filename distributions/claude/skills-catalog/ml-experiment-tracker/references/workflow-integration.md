# Workflow Integration: ML Experiment Tracker

This document describes how `ml-experiment-tracker` integrates with other skills in the Data Science & Analytics ecosystem.

## Related Skills

| Skill | Relationship | When to Invoke |
|-------|--------------|----------------|
| `data-pipeline-architect` | **Upstream** | Receive training data pipelines |
| `sql-query-optimizer` | **Upstream** | Optimize feature extraction queries |
| `time-series-analyst` | **Complementary** | Track forecasting experiments |
| `data-storytelling-analyst` | **Downstream** | Present experiment results |
| `systemic-product-analyst` | **Downstream** | Model impact on product metrics |

## Prerequisites

Before invoking `ml-experiment-tracker`, ensure:

1. **Training data available** - Clean, accessible datasets
2. **Problem defined** - Classification, regression, forecasting
3. **Success metrics clear** - What defines a good model

## Handoff Patterns

### From: data-pipeline-architect

**Trigger:** Training data pipeline ready.

**What to receive:**
- Feature table locations
- Label data sources
- Data versioning approach

**Integration points:**
- Register data sources
- Track data versions with experiments
- Configure data loading

### From: sql-query-optimizer

**Trigger:** Feature queries optimized.

**What to receive:**
- Optimized feature extraction SQL
- Performance benchmarks
- Caching recommendations

**Integration points:**
- Use optimized queries in pipelines
- Track query versions
- Monitor data loading time

### To: time-series-analyst

**Trigger:** Forecasting experiments need time expertise.

**What to hand off:**
- Historical model performance
- Feature importance for time features
- Prediction intervals

**Expected output from time-series:**
- Temporal feature engineering
- Seasonality adjustments
- Forecast validation approach

### To: data-storytelling-analyst

**Trigger:** Experiment results ready to present.

**What to hand off:**
- Model comparison metrics
- Learning curves
- Feature importance rankings

**Expected output from storytelling:**
- Model comparison visualizations
- Business-friendly explanations
- Executive summary

### To: systemic-product-analyst

**Trigger:** Model deployed, need impact tracking.

**What to hand off:**
- Deployed model version
- Prediction endpoints
- Expected impact metrics

**Expected output from product:**
- A/B test design
- Impact measurement
- Metric tracking setup

## Workflow Sequence

```
┌─────────────────────────────────────────────────────────────┐
│                    ML Experiment Lifecycle                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. DATA-PIPELINE-ARCHITECT: Prepare training data         │
│           │                                                 │
│           ▼                                                 │
│  2. SQL-QUERY-OPTIMIZER: Optimize feature queries          │
│           │                                                 │
│           ▼                                                 │
│  3. ML-EXPERIMENT-TRACKER: Run experiments                 │
│           │                                                 │
│           ├──────────────────────────────────────┐          │
│           ▼                                      ▼          │
│  4a. TIME-SERIES-ANALYST      4b. DATA-STORYTELLING        │
│      (if forecasting)             (present results)        │
│           │                                      │          │
│           └──────────────────────────────────────┘          │
│                          │                                  │
│                          ▼                                  │
│  5. SYSTEMIC-PRODUCT-ANALYST: Measure production impact    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Integration Checklist

Before completing experiment tracking, verify:

- [ ] All hyperparameters logged
- [ ] Data version tracked
- [ ] Model artifacts saved
- [ ] Metrics recorded consistently
- [ ] Code version linked
- [ ] Environment captured
- [ ] Reproducible training script
- [ ] Baseline comparison included

## Common Scenarios

### Model Development

1. **Data Pipeline Architect:** Feature pipeline ready
2. **SQL Query Optimizer:** Fast feature extraction
3. **ML Experiment Tracker:** Run and compare experiments
4. **Data Storytelling Analyst:** Present best model

### Forecasting Project

1. **Time Series Analyst:** Temporal features designed
2. **ML Experiment Tracker:** Track forecast models
3. **Data Storytelling Analyst:** Forecast visualization

### A/B Test Model Launch

1. **ML Experiment Tracker:** Champion model selected
2. **Systemic Product Analyst:** A/B test design
3. **ML Experiment Tracker:** Production monitoring

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| No baseline | Can't judge improvement | Always track baseline model |
| Missing hyperparameters | Can't reproduce | Log all parameters |
| No data versioning | Training-serving skew | Version all datasets |
| Overfitting validation | Poor generalization | Proper holdout strategy |

## Related Resources

- [Data Science Skills Ecosystem Map](../../../docs/guides/data-science-skills-ecosystem.md)
