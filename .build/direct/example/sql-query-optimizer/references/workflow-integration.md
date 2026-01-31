# Workflow Integration: SQL Query Optimizer

This document describes how `sql-query-optimizer` integrates with other skills in the Data Science & Analytics ecosystem.

## Related Skills

| Skill | Relationship | When to Invoke |
|-------|--------------|----------------|
| `data-pipeline-architect` | **Upstream** | Understand source schemas and volumes |
| `ml-experiment-tracker` | **Downstream** | Optimize training data queries |
| `systemic-product-analyst` | **Downstream** | Optimize metric aggregations |
| `time-series-analyst` | **Complementary** | Time-based partitioning strategies |
| `data-storytelling-analyst` | **Downstream** | Optimize dashboard queries |

## Prerequisites

Before invoking `sql-query-optimizer`, ensure:

1. **Schema documented** - Table structures and relationships
2. **Query patterns known** - Common access patterns
3. **Performance baselines** - Current query times

## Handoff Patterns

### From: data-pipeline-architect

**Trigger:** Pipeline queries need optimization.

**What to receive:**
- Schema definitions
- Data volumes and growth
- Transformation requirements

**Integration points:**
- Optimize materialized view definitions
- Add appropriate indexes
- Design partitioning scheme

### To: ml-experiment-tracker

**Trigger:** Feature extraction queries optimized.

**What to hand off:**
- Optimized feature queries
- Query execution plans
- Performance benchmarks

**Expected output from tracker:**
- Data loading integration
- Query caching strategy
- Versioned query definitions

### To: systemic-product-analyst

**Trigger:** Metric queries ready.

**What to hand off:**
- Optimized aggregation queries
- Materialized view definitions
- Index recommendations

**Expected output from product:**
- Metric SQL implementations
- Dashboard query patterns
- Caching layer usage

### To: time-series-analyst

**Trigger:** Time-based queries need optimization.

**What to hand off:**
- Time range query patterns
- Aggregation window definitions
- Current indexing on time columns

**Expected output from time-series:**
- Optimal time partitioning
- Window function patterns
- Pre-aggregation recommendations

## Workflow Sequence

```
┌─────────────────────────────────────────────────────────────┐
│                    Query Optimization Flow                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. DATA-PIPELINE-ARCHITECT: Provide schema context        │
│           │                                                 │
│           ▼                                                 │
│  2. SQL-QUERY-OPTIMIZER: Analyze and optimize              │
│           │                                                 │
│           ├──────────────────────────────────────┐          │
│           ▼                                      ▼          │
│  3a. ML-EXPERIMENT-TRACKER   3b. SYSTEMIC-PRODUCT-ANALYST  │
│      (feature queries)           (metric queries)          │
│           │                                      │          │
│           └──────────────────────────────────────┘          │
│                          │                                  │
│                          ▼                                  │
│  4. DATA-STORYTELLING-ANALYST: Dashboard queries           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Integration Checklist

Before completing query optimization, verify:

- [ ] EXPLAIN plans analyzed
- [ ] Indexes cover common queries
- [ ] Partitioning aligned with access patterns
- [ ] Materialized views for expensive aggregations
- [ ] Query statistics collected
- [ ] Slow query log reviewed
- [ ] Connection pooling configured
- [ ] Query timeout limits set

## Common Scenarios

### Dashboard Query Optimization

1. **Data Pipeline Architect:** Provide data model
2. **SQL Query Optimizer:** Optimize aggregations
3. **Data Storytelling Analyst:** Fast dashboard queries

### Feature Store Queries

1. **SQL Query Optimizer:** Optimize feature extraction
2. **ML Experiment Tracker:** Integrate optimized queries
3. **Time Series Analyst:** Time-windowed features

### Product Metrics

1. **Data Pipeline Architect:** Event schema
2. **SQL Query Optimizer:** Metric query optimization
3. **Systemic Product Analyst:** Analysis on optimized data

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Over-indexing | Write performance degradation | Index only necessary columns |
| SELECT * | Unnecessary data transfer | Select only needed columns |
| No query cache | Repeated expensive queries | Use materialized views |
| Missing EXPLAIN | Blind optimization | Always analyze query plans |

## Related Resources

- [Data Science Skills Ecosystem Map](../../../docs/guides/data-science-skills-ecosystem.md)
