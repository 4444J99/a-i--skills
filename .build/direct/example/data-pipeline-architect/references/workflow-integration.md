# Workflow Integration: Data Pipeline Architect

This document describes how `data-pipeline-architect` integrates with other skills in the Data Science & Analytics ecosystem.

## Related Skills

| Skill | Relationship | When to Invoke |
|-------|--------------|----------------|
| `sql-query-optimizer` | **Downstream** | Optimize transformation queries |
| `time-series-analyst` | **Downstream** | Design time-partitioned pipelines |
| `ml-experiment-tracker` | **Downstream** | Provide training data pipelines |
| `systemic-product-analyst` | **Downstream** | Set up product metrics pipelines |
| `data-storytelling-analyst` | **Downstream** | Pipeline health dashboards |

## Prerequisites

Before invoking `data-pipeline-architect`, ensure:

1. **Data sources identified** - Databases, APIs, files
2. **Target destination known** - Warehouse, lake, feature store
3. **Freshness requirements clear** - Real-time, hourly, daily

## Handoff Patterns

### To: sql-query-optimizer

**Trigger:** Transformation queries need optimization.

**What to hand off:**
- Schema definitions
- Data volumes and distributions
- Query patterns for transformations

**Expected output from optimizer:**
- Optimized transformation queries
- Indexing recommendations
- Partitioning strategies

### To: time-series-analyst

**Trigger:** Time-series data needs proper handling.

**What to hand off:**
- Timestamp column specifications
- Time granularity requirements
- Historical data availability

**Expected output from time-series:**
- Time partitioning recommendations
- Aggregation window definitions
- Gap handling strategies

### To: ml-experiment-tracker

**Trigger:** ML team needs training data.

**What to hand off:**
- Feature table locations
- Label data sources
- Data versioning approach

**Expected output from tracker:**
- Data loading patterns
- Version tagging requirements
- Reproducibility constraints

### To: systemic-product-analyst

**Trigger:** Product metrics need data foundation.

**What to hand off:**
- Event schema definitions
- User identity mappings
- Session reconstruction logic

**Expected output from product:**
- Metric definitions to compute
- Aggregation requirements
- Funnel specifications

## Workflow Sequence

```
┌─────────────────────────────────────────────────────────────┐
│                    Data Pipeline Design                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. DATA-PIPELINE-ARCHITECT: Design ETL/ELT pipeline       │
│           │                                                 │
│           ├──────────────────────────────────────┐          │
│           ▼                                      ▼          │
│  2a. SQL-QUERY-OPTIMIZER      2b. TIME-SERIES-ANALYST      │
│      (transformation queries)     (time partitioning)      │
│           │                                      │          │
│           └──────────────────────────────────────┘          │
│                          │                                  │
│           ┌──────────────┼──────────────┐                   │
│           ▼              ▼              ▼                   │
│  3a. ML-EXPERIMENT   3b. PRODUCT    3c. STORYTELLING       │
│      (training data)    (metrics)       (monitoring)       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Integration Checklist

Before completing pipeline design, verify:

- [ ] Source connections tested
- [ ] Schema evolution handled
- [ ] Idempotent transformations
- [ ] Error handling and dead-letter queues
- [ ] Backfill strategy defined
- [ ] Monitoring and alerting configured
- [ ] Data quality checks in place
- [ ] Documentation complete

## Common Scenarios

### Event Streaming Pipeline

1. **Data Pipeline Architect:** Design Kafka→Warehouse flow
2. **SQL Query Optimizer:** Optimize aggregation queries
3. **Systemic Product Analyst:** Define event metrics
4. **Data Storytelling Analyst:** Real-time dashboards

### ML Feature Pipeline

1. **Data Pipeline Architect:** Feature computation DAG
2. **SQL Query Optimizer:** Feature query optimization
3. **ML Experiment Tracker:** Feature versioning
4. **Time Series Analyst:** Temporal feature handling

### Data Warehouse Migration

1. **Data Pipeline Architect:** Design new pipeline
2. **SQL Query Optimizer:** Migrate and optimize queries
3. **Data Storytelling Analyst:** Migration progress dashboard

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| No idempotency | Duplicate data on reruns | Make all operations idempotent |
| Hardcoded schemas | Breaks on source changes | Schema-on-read or evolution |
| No backfill | Historical gaps | Design backfill from day one |
| Missing monitoring | Silent failures | Pipeline observability |

## Related Resources

- [Data Science Skills Ecosystem Map](../../../docs/guides/data-science-skills-ecosystem.md)
