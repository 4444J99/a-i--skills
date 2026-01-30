# Orchestration Patterns

## Airflow DAG Patterns

### Basic DAG Structure

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'email_on_failure': True,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'etl_daily_sales',
    default_args=default_args,
    description='Daily sales ETL pipeline',
    schedule_interval='0 6 * * *',  # 6 AM daily
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['etl', 'sales'],
) as dag:

    start = EmptyOperator(task_id='start')

    extract = PythonOperator(
        task_id='extract_sales_data',
        python_callable=extract_sales,
    )

    transform = PythonOperator(
        task_id='transform_sales_data',
        python_callable=transform_sales,
    )

    load = PythonOperator(
        task_id='load_to_warehouse',
        python_callable=load_warehouse,
    )

    end = EmptyOperator(task_id='end')

    start >> extract >> transform >> load >> end
```

### Parallel Processing Pattern

```python
with DAG('parallel_etl', ...) as dag:

    start = EmptyOperator(task_id='start')

    # Parallel extraction from multiple sources
    extract_crm = PythonOperator(
        task_id='extract_crm',
        python_callable=extract_crm_data,
    )

    extract_erp = PythonOperator(
        task_id='extract_erp',
        python_callable=extract_erp_data,
    )

    extract_web = PythonOperator(
        task_id='extract_web',
        python_callable=extract_web_data,
    )

    # Wait for all extractions
    merge = PythonOperator(
        task_id='merge_data',
        python_callable=merge_sources,
    )

    # Set up parallel branches
    start >> [extract_crm, extract_erp, extract_web] >> merge
```

### Dynamic DAG Generation

```python
def create_table_etl_dag(table_name):
    dag = DAG(
        f'etl_{table_name}',
        schedule_interval='@daily',
        default_args=default_args,
    )

    with dag:
        extract = PythonOperator(
            task_id='extract',
            python_callable=extract_table,
            op_kwargs={'table': table_name},
        )

        load = PythonOperator(
            task_id='load',
            python_callable=load_table,
            op_kwargs={'table': table_name},
        )

        extract >> load

    return dag

# Generate DAGs for each table
tables = ['users', 'orders', 'products', 'inventory']
for table in tables:
    globals()[f'etl_{table}'] = create_table_etl_dag(table)
```

## Dagster Patterns

### Asset-Based Pipeline

```python
from dagster import asset, AssetExecutionContext, Definitions
import pandas as pd

@asset
def raw_sales_data() -> pd.DataFrame:
    """Extract raw sales data from source"""
    return pd.read_sql("SELECT * FROM sales", connection)

@asset
def cleaned_sales_data(raw_sales_data: pd.DataFrame) -> pd.DataFrame:
    """Clean and validate sales data"""
    df = raw_sales_data.copy()
    df = df.dropna(subset=['amount', 'date'])
    df['date'] = pd.to_datetime(df['date'])
    return df

@asset
def daily_sales_summary(cleaned_sales_data: pd.DataFrame) -> pd.DataFrame:
    """Aggregate to daily summary"""
    return cleaned_sales_data.groupby('date').agg({
        'amount': 'sum',
        'order_id': 'count'
    }).reset_index()

defs = Definitions(
    assets=[raw_sales_data, cleaned_sales_data, daily_sales_summary]
)
```

### Partitioned Assets

```python
from dagster import asset, DailyPartitionsDefinition

daily_partitions = DailyPartitionsDefinition(start_date="2024-01-01")

@asset(partitions_def=daily_partitions)
def daily_events(context: AssetExecutionContext) -> pd.DataFrame:
    partition_date = context.partition_key
    return fetch_events_for_date(partition_date)
```

## Prefect Patterns

### Flow with Retries

```python
from prefect import flow, task
from prefect.tasks import task_input_hash
from datetime import timedelta

@task(
    retries=3,
    retry_delay_seconds=60,
    cache_key_fn=task_input_hash,
    cache_expiration=timedelta(hours=1)
)
def extract_data(source: str) -> dict:
    return fetch_from_api(source)

@task
def transform_data(data: dict) -> dict:
    return process(data)

@task
def load_data(data: dict) -> None:
    write_to_warehouse(data)

@flow(name="ETL Pipeline")
def etl_pipeline(source: str):
    raw = extract_data(source)
    transformed = transform_data(raw)
    load_data(transformed)
```

## dbt Patterns

### Incremental Model

```sql
-- models/staging/stg_orders.sql
{{
    config(
        materialized='incremental',
        unique_key='order_id',
        incremental_strategy='merge'
    )
}}

SELECT
    order_id,
    customer_id,
    order_date,
    total_amount,
    updated_at
FROM {{ source('raw', 'orders') }}

{% if is_incremental() %}
WHERE updated_at > (SELECT MAX(updated_at) FROM {{ this }})
{% endif %}
```

### Model with Tests

```yaml
# models/schema.yml
version: 2

models:
  - name: stg_orders
    description: Staged orders with cleaning applied
    columns:
      - name: order_id
        tests:
          - unique
          - not_null
      - name: total_amount
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0
```
