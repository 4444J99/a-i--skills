# Pipeline Templates

## Batch ETL Pipeline

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Extract   │───▶│   Stage     │───▶│  Transform  │───▶│    Load     │
│   (Source)  │    │   (Raw)     │    │  (Clean)    │    │   (Target)  │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                  │                  │                  │
       ▼                  ▼                  ▼                  ▼
   Incremental        Landing Zone       Data Quality       Merge/Upsert
   or Full           with Metadata       Validation         or Replace
```

## Change Data Capture (CDC) Pipeline

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Source DB  │───▶│   CDC Tool   │───▶│   Message    │
│   (MySQL)    │    │  (Debezium)  │    │    Queue     │
└──────────────┘    └──────────────┘    └──────────────┘
                                               │
                    ┌──────────────────────────┘
                    │
                    ▼
           ┌──────────────┐    ┌──────────────┐
           │   Stream     │───▶│    Target    │
           │  Processor   │    │     DW       │
           └──────────────┘    └──────────────┘
```

## Data Lake Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Data Lake                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐           │
│  │   Bronze    │──▶│   Silver    │──▶│    Gold     │           │
│  │   (Raw)     │   │  (Cleaned)  │   │ (Business)  │           │
│  └─────────────┘   └─────────────┘   └─────────────┘           │
│                                                                 │
│  - Original format  - Standardized    - Aggregated             │
│  - Append-only      - Deduplicated    - Joined                  │
│  - All history      - Validated       - Business logic          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Reverse ETL Pipeline

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│    Data     │───▶│   Sync      │───▶│   SaaS      │
│  Warehouse  │    │   Tool      │    │   Tools     │
│  (Source)   │    │ (Census/    │    │ (Salesforce,│
│             │    │  Hightouch) │    │  HubSpot)   │
└─────────────┘    └─────────────┘    └─────────────┘
```

## Pipeline Configuration Template

```yaml
# pipeline_config.yaml
pipeline:
  name: sales_etl
  version: "1.0"
  schedule: "0 6 * * *"  # 6 AM daily
  owner: data-team@company.com

source:
  type: postgres
  connection: ${POSTGRES_CONNECTION_STRING}
  table: sales
  incremental_key: updated_at

staging:
  type: s3
  bucket: data-lake-staging
  path: sales/{{ ds }}/

transformations:
  - name: clean_nulls
    type: fill_null
    columns:
      - name: region
        value: "Unknown"
  - name: validate_amounts
    type: filter
    condition: "amount >= 0"
  - name: add_metadata
    type: add_columns
    columns:
      - name: _loaded_at
        value: "{{ ts }}"

destination:
  type: snowflake
  database: analytics
  schema: sales
  table: fact_sales
  write_mode: merge
  merge_keys: [sale_id]

quality_checks:
  - type: row_count
    min: 1000
  - type: null_check
    columns: [sale_id, amount]
    max_null_pct: 0
  - type: freshness
    column: sale_date
    max_age_hours: 48

alerts:
  on_failure:
    - slack: "#data-alerts"
    - email: oncall@company.com
```
