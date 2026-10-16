# BigQuery Cost Analysis Queries

*These queries assume billing export is enabled to BigQuery.*

## Setup

Enable billing export:
1. Go to Billing → Billing export
2. Select BigQuery export
3. Choose/create dataset

Table format: `project.dataset.gcp_billing_export_v1_XXXXXX_XXXXXX_XXXXXX`

---

## Daily Spend Overview

```sql
SELECT
  DATE(usage_start_time) as date,
  SUM(cost) as daily_cost,
  SUM(credits.amount) as credits_applied
FROM `project.dataset.gcp_billing_export_v1_*`
LEFT JOIN UNNEST(credits) as credits
WHERE usage_start_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
GROUP BY 1
ORDER BY 1 DESC
```

---

## Cost by Service

```sql
SELECT
  service.description as service,
  SUM(cost) as total_cost,
  ROUND(SUM(cost) * 100 / SUM(SUM(cost)) OVER(), 2) as percentage
FROM `project.dataset.gcp_billing_export_v1_*`
WHERE usage_start_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
GROUP BY 1
ORDER BY 2 DESC
LIMIT 20
```

---

## Cost by SKU (Detailed)

```sql
SELECT
  service.description as service,
  sku.description as sku,
  SUM(cost) as cost,
  SUM(usage.amount) as usage_amount,
  usage.unit as unit
FROM `project.dataset.gcp_billing_export_v1_*`
WHERE usage_start_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
GROUP BY 1, 2, 5
HAVING SUM(cost) > 1  -- Filter noise
ORDER BY 3 DESC
LIMIT 50
```

---

## Cost by Project

```sql
SELECT
  project.id as project_id,
  project.name as project_name,
  SUM(cost) as total_cost
FROM `project.dataset.gcp_billing_export_v1_*`
WHERE usage_start_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
GROUP BY 1, 2
ORDER BY 3 DESC
```

---

## Cost by Label

```sql
SELECT
  labels.key as label_key,
  labels.value as label_value,
  SUM(cost) as total_cost
FROM `project.dataset.gcp_billing_export_v1_*`,
UNNEST(labels) as labels
WHERE usage_start_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
GROUP BY 1, 2
HAVING SUM(cost) > 0
ORDER BY 3 DESC
```

---

## Compute Engine Analysis

```sql
SELECT
  sku.description,
  REGEXP_EXTRACT(sku.description, r'(e2|n1|n2|c2|m2|a2)') as machine_family,
  SUM(cost) as cost,
  SUM(usage.amount) as usage_hours,
  ROUND(SUM(cost) / NULLIF(SUM(usage.amount), 0), 4) as cost_per_hour
FROM `project.dataset.gcp_billing_export_v1_*`
WHERE service.description = 'Compute Engine'
  AND usage_start_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
  AND sku.description LIKE '%Instance%'
GROUP BY 1, 2
ORDER BY 3 DESC
```

---

## Storage Costs Breakdown

```sql
SELECT
  service.description as service,
  CASE 
    WHEN sku.description LIKE '%Standard%' THEN 'Standard'
    WHEN sku.description LIKE '%Nearline%' THEN 'Nearline'
    WHEN sku.description LIKE '%Coldline%' THEN 'Coldline'
    WHEN sku.description LIKE '%Archive%' THEN 'Archive'
    ELSE 'Other'
  END as storage_class,
  SUM(cost) as cost,
  SUM(usage.amount) as gb_months
FROM `project.dataset.gcp_billing_export_v1_*`
WHERE service.description = 'Cloud Storage'
  AND usage_start_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
GROUP BY 1, 2
ORDER BY 3 DESC
```

---

## Network Egress Costs

```sql
SELECT
  service.description,
  sku.description,
  SUM(cost) as cost,
  SUM(usage.amount) as gb_transferred
FROM `project.dataset.gcp_billing_export_v1_*`
WHERE (sku.description LIKE '%Egress%' OR sku.description LIKE '%Network%')
  AND usage_start_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
GROUP BY 1, 2
HAVING SUM(cost) > 0.1
ORDER BY 3 DESC
```

---

## Credits Analysis

```sql
SELECT
  credits.name as credit_type,
  SUM(credits.amount) as credit_amount,
  MIN(usage_start_time) as first_used,
  MAX(usage_start_time) as last_used
FROM `project.dataset.gcp_billing_export_v1_*`,
UNNEST(credits) as credits
WHERE credits.amount < 0  -- Credits are negative
GROUP BY 1
ORDER BY 2
```

---

## Monthly Trend

```sql
SELECT
  FORMAT_TIMESTAMP('%Y-%m', usage_start_time) as month,
  SUM(cost) as gross_cost,
  SUM(credits.amount) as credits,
  SUM(cost) + IFNULL(SUM(credits.amount), 0) as net_cost
FROM `project.dataset.gcp_billing_export_v1_*`
LEFT JOIN UNNEST(credits) as credits
WHERE usage_start_time >= TIMESTAMP('2024-01-01')
GROUP BY 1
ORDER BY 1
```

---

## Anomaly Detection (Day-over-Day)

```sql
WITH daily_costs AS (
  SELECT
    DATE(usage_start_time) as date,
    SUM(cost) as daily_cost
  FROM `project.dataset.gcp_billing_export_v1_*`
  WHERE usage_start_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
  GROUP BY 1
),
with_avg AS (
  SELECT
    *,
    AVG(daily_cost) OVER (ORDER BY date ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING) as avg_7day
  FROM daily_costs
)
SELECT
  date,
  daily_cost,
  avg_7day,
  ROUND((daily_cost - avg_7day) / NULLIF(avg_7day, 0) * 100, 1) as pct_change
FROM with_avg
WHERE ABS((daily_cost - avg_7day) / NULLIF(avg_7day, 0)) > 0.5  -- >50% change
ORDER BY date DESC
```

---

## Forecast Remaining Credits

```sql
WITH credit_data AS (
  SELECT
    DATE(usage_start_time) as date,
    SUM(credits.amount) * -1 as credits_used
  FROM `project.dataset.gcp_billing_export_v1_*`,
  UNNEST(credits) as credits
  WHERE credits.amount < 0
    AND usage_start_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
  GROUP BY 1
),
stats AS (
  SELECT
    AVG(credits_used) as avg_daily_burn,
    SUM(credits_used) as total_used_30d
  FROM credit_data
)
SELECT
  avg_daily_burn,
  total_used_30d,
  -- Replace YOUR_TOTAL_CREDITS with your actual credit amount
  (YOUR_TOTAL_CREDITS - total_used_30d) as estimated_remaining,
  (YOUR_TOTAL_CREDITS - total_used_30d) / NULLIF(avg_daily_burn, 0) as days_remaining
FROM stats
```
