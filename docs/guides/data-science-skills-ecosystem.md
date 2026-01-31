# Data Science & Analytics Skills Ecosystem

This guide maps the relationships between data science and analytics-focused skills in this repository and provides workflow guidance for using them together effectively.

## Skill Overview

| Skill | Category | Focus Area |
|-------|----------|------------|
| [`data-pipeline-architect`](../../skills/data/data-pipeline-architect/) | data | ETL/ELT orchestration and data flow |
| [`sql-query-optimizer`](../../skills/data/sql-query-optimizer/) | data | Query performance and optimization |
| [`data-storytelling-analyst`](../../skills/data/data-storytelling-analyst/) | data | Visualization and narrative |
| [`ml-experiment-tracker`](../../skills/data/ml-experiment-tracker/) | data | Model development lifecycle |
| [`time-series-analyst`](../../skills/data/time-series-analyst/) | data | Temporal pattern analysis |
| [`systemic-product-analyst`](../../skills/data/systemic-product-analyst/) | data | Product metrics and system analysis |

## Ecosystem Diagram

```mermaid
flowchart TB
    subgraph Ingest["Data Ingestion"]
        DPA[data-pipeline-architect]
    end

    subgraph Process["Processing Layer"]
        SQO[sql-query-optimizer]
        TSA[time-series-analyst]
    end

    subgraph Model["Modeling Layer"]
        MET[ml-experiment-tracker]
    end

    subgraph Analyze["Analysis Layer"]
        SPA[systemic-product-analyst]
        DSA[data-storytelling-analyst]
    end

    DPA -->|"Data flows to"| SQO
    DPA -->|"Time data to"| TSA
    SQO -->|"Optimized queries for"| MET
    SQO -->|"Aggregations for"| SPA
    TSA -->|"Patterns inform"| MET
    TSA -->|"Trends for"| SPA
    MET -->|"Results to"| DSA
    SPA -->|"Insights to"| DSA
    DPA -.->|"Metrics pipeline"| SPA
    MET -.->|"Predictions to"| TSA

    style DPA fill:#e3f2fd
    style SQO fill:#e8f5e9
    style TSA fill:#e8f5e9
    style MET fill:#fff3e0
    style SPA fill:#f3e5f5
    style DSA fill:#f3e5f5
```

## Workflow Scenarios

### Scenario 1: ML Pipeline

**Goal:** Build an end-to-end machine learning pipeline from data to insights.

```mermaid
sequenceDiagram
    participant DS as Data Scientist
    participant DPA as data-pipeline-architect
    participant SQO as sql-query-optimizer
    participant MET as ml-experiment-tracker
    participant TSA as time-series-analyst
    participant DSA as data-storytelling-analyst

    DS->>DPA: 1. Design data ingestion
    DPA-->>DS: ETL pipeline, data catalog
    DS->>SQO: 2. Optimize feature queries
    SQO-->>DS: Indexed, partitioned queries
    DS->>MET: 3. Run experiments
    MET-->>DS: Model versions, metrics
    DS->>TSA: 4. Analyze temporal patterns
    TSA-->>DS: Seasonality, trends
    DS->>DSA: 5. Present findings
    DSA-->>DS: Dashboard, narrative
```

**Skill Sequence:**
1. **`data-pipeline-architect`** - Design data ingestion and transformation
2. **`sql-query-optimizer`** - Optimize feature extraction queries
3. **`ml-experiment-tracker`** - Track model experiments
4. **`time-series-analyst`** - Analyze temporal aspects
5. **`data-storytelling-analyst`** - Present results

### Scenario 2: Product Analytics

**Goal:** Build product analytics from data pipeline to executive dashboard.

```mermaid
sequenceDiagram
    participant PM as Product Manager
    participant DPA as data-pipeline-architect
    participant SQO as sql-query-optimizer
    participant SPA as systemic-product-analyst
    participant DSA as data-storytelling-analyst

    PM->>DPA: 1. Set up event tracking
    DPA-->>PM: Event pipeline, schema
    PM->>SQO: 2. Build metric queries
    SQO-->>PM: Optimized aggregations
    PM->>SPA: 3. Analyze product metrics
    SPA-->>PM: Funnels, cohorts, trends
    PM->>DSA: 4. Create executive report
    DSA-->>PM: Dashboard, presentation
```

**Skill Sequence:**
1. **`data-pipeline-architect`** - Set up event data pipeline
2. **`sql-query-optimizer`** - Optimize metric calculations
3. **`systemic-product-analyst`** - Deep dive on product behavior
4. **`data-storytelling-analyst`** - Communicate insights

### Scenario 3: Forecasting Project

**Goal:** Build forecasting models with proper tracking and communication.

```mermaid
sequenceDiagram
    participant An as Analyst
    participant DPA as data-pipeline-architect
    participant TSA as time-series-analyst
    participant MET as ml-experiment-tracker
    participant DSA as data-storytelling-analyst

    An->>DPA: 1. Prepare historical data
    DPA-->>An: Clean time-series pipeline
    An->>TSA: 2. Analyze patterns
    TSA-->>An: Seasonality, trends, cycles
    An->>MET: 3. Track forecast models
    MET-->>An: Model comparison, metrics
    An->>DSA: 4. Visualize forecasts
    DSA-->>An: Interactive forecast charts
```

**Skill Sequence:**
1. **`data-pipeline-architect`** - Prepare historical data pipeline
2. **`time-series-analyst`** - Identify patterns and features
3. **`ml-experiment-tracker`** - Track forecasting experiments
4. **`data-storytelling-analyst`** - Visualize forecasts

## Decision Tree: Which Skill to Use?

```mermaid
flowchart TD
    Start([What do you need?]) --> Q1{Stage of work?}

    Q1 -->|Data preparation| Q2{What aspect?}
    Q2 -->|Pipeline/ETL| DPA[data-pipeline-architect]
    Q2 -->|Query speed| SQO[sql-query-optimizer]

    Q1 -->|Analysis| Q3{What type?}
    Q3 -->|Time patterns| TSA[time-series-analyst]
    Q3 -->|Product metrics| SPA[systemic-product-analyst]
    Q3 -->|ML modeling| MET[ml-experiment-tracker]

    Q1 -->|Communication| DSA[data-storytelling-analyst]

    Q1 -->|End-to-end| Q4{Primary goal?}
    Q4 -->|ML model| MET
    Q4 -->|Product insights| SPA
    Q4 -->|Forecasting| TSA

    style DPA fill:#e3f2fd
    style SQO fill:#e8f5e9
    style TSA fill:#e8f5e9
    style MET fill:#fff3e0
    style SPA fill:#f3e5f5
    style DSA fill:#f3e5f5
```

## Cross-Reference Matrix

This matrix shows when each skill might invoke or reference another:

| Primary Skill | Invokes | For |
|---------------|---------|-----|
| `data-pipeline-architect` | `sql-query-optimizer` | Optimizing transformation queries |
| `data-pipeline-architect` | `time-series-analyst` | Time-partitioning strategies |
| `sql-query-optimizer` | `data-pipeline-architect` | Understanding source schemas |
| `sql-query-optimizer` | `ml-experiment-tracker` | Feature query optimization |
| `time-series-analyst` | `data-pipeline-architect` | Time series data requirements |
| `time-series-analyst` | `ml-experiment-tracker` | Forecasting model tracking |
| `ml-experiment-tracker` | `sql-query-optimizer` | Training data queries |
| `ml-experiment-tracker` | `data-storytelling-analyst` | Experiment result visualization |
| `systemic-product-analyst` | `sql-query-optimizer` | Metric query optimization |
| `systemic-product-analyst` | `data-storytelling-analyst` | Insight presentation |
| `data-storytelling-analyst` | All skills | Receiving analysis results |

## Common Handoff Patterns

### Pipeline Architect → SQL Optimizer
When data pipelines are designed, optimize queries:
- Schema is finalized
- Data volumes are known
- Query patterns identified

### SQL Optimizer → ML Experiment Tracker
When feature queries are optimized, track experiments:
- Feature extraction queries ready
- Training data accessible
- Reproducible data loading

### Time Series → ML Experiments
When temporal patterns are identified, track forecasting:
- Seasonality components known
- Feature engineering complete
- Baseline models defined

### Product Analyst → Storytelling
When analysis is complete, communicate:
- Key metrics identified
- Insights synthesized
- Recommendations ready

## Best Practices

### Sequential vs. Parallel Usage
- **Sequential:** ML pipeline (pipeline → optimizer → experiments → story)
- **Parallel:** Time-series + product analyst can analyze simultaneously

### Avoiding Overlap
- **Data concerns:** `data-pipeline-architect` owns ETL/ELT
- **Query concerns:** `sql-query-optimizer` owns query performance
- **Temporal concerns:** `time-series-analyst` owns time patterns
- **Model concerns:** `ml-experiment-tracker` owns model lifecycle
- **Product concerns:** `systemic-product-analyst` owns product metrics
- **Communication concerns:** `data-storytelling-analyst` owns visualization

### When to Combine Skills
Some tasks benefit from multiple skills in one session:
- **Full ML project:** pipeline + optimizer + experiments + storytelling
- **Product deep dive:** pipeline + product analyst + storytelling
- **Forecasting:** pipeline + time-series + experiments + storytelling

## Related Resources

- [Creating Skills Guide](./creating-skills.md)
- [Skill Specification](../api/skill-spec.md)
- [Getting Started](./getting-started.md)
