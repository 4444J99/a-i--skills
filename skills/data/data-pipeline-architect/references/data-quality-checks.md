# Data Quality Checks

## Quality Dimensions

| Dimension | Description | Example Check |
|-----------|-------------|---------------|
| Completeness | No missing required data | NULL count < threshold |
| Uniqueness | No duplicates where expected | Primary key uniqueness |
| Validity | Values in expected ranges | Age between 0-150 |
| Consistency | Data agrees across sources | Sum matches between tables |
| Timeliness | Data is fresh enough | Max timestamp within SLA |
| Accuracy | Data reflects reality | Spot check against source |

## Great Expectations Patterns

### Expectation Suite

```python
import great_expectations as gx

context = gx.get_context()

# Create expectation suite
suite = context.add_expectation_suite("orders_suite")

# Add expectations
validator = context.get_validator(
    batch_request=batch_request,
    expectation_suite_name="orders_suite"
)

# Completeness
validator.expect_column_values_to_not_be_null("order_id")
validator.expect_column_values_to_not_be_null("customer_id")

# Uniqueness
validator.expect_column_values_to_be_unique("order_id")

# Validity
validator.expect_column_values_to_be_between(
    "total_amount", min_value=0, max_value=1000000
)
validator.expect_column_values_to_be_in_set(
    "status", ["pending", "processing", "completed", "cancelled"]
)

# Format
validator.expect_column_values_to_match_regex(
    "email", r"^[\w\.-]+@[\w\.-]+\.\w+$"
)

# Referential integrity
validator.expect_column_values_to_be_in_set(
    "customer_id", valid_customer_ids
)

# Save suite
validator.save_expectation_suite()
```

### Running Checkpoints

```python
checkpoint = context.add_or_update_checkpoint(
    name="orders_checkpoint",
    validations=[
        {
            "batch_request": batch_request,
            "expectation_suite_name": "orders_suite"
        }
    ],
    action_list=[
        {
            "name": "store_validation_result",
            "action": {"class_name": "StoreValidationResultAction"}
        },
        {
            "name": "update_data_docs",
            "action": {"class_name": "UpdateDataDocsAction"}
        },
        {
            "name": "send_slack_notification",
            "action": {
                "class_name": "SlackNotificationAction",
                "slack_webhook": "${SLACK_WEBHOOK}",
                "notify_on": "failure"
            }
        }
    ]
)

result = checkpoint.run()
```

## SQL-Based Checks

### Row Count Comparison

```sql
-- Check row counts match between source and target
WITH source_count AS (
    SELECT COUNT(*) as cnt FROM source_table
),
target_count AS (
    SELECT COUNT(*) as cnt FROM target_table
)
SELECT
    CASE
        WHEN s.cnt = t.cnt THEN 'PASS'
        ELSE 'FAIL: Source=' || s.cnt || ', Target=' || t.cnt
    END as result
FROM source_count s, target_count t;
```

### Null Percentage Check

```sql
-- Alert if null percentage exceeds threshold
SELECT
    column_name,
    null_count,
    total_count,
    (null_count * 100.0 / total_count) as null_percentage
FROM (
    SELECT
        'email' as column_name,
        SUM(CASE WHEN email IS NULL THEN 1 ELSE 0 END) as null_count,
        COUNT(*) as total_count
    FROM users
)
WHERE (null_count * 100.0 / total_count) > 5;  -- 5% threshold
```

### Freshness Check

```sql
-- Ensure data is recent
SELECT
    CASE
        WHEN MAX(updated_at) > NOW() - INTERVAL '1 hour'
        THEN 'FRESH'
        ELSE 'STALE: Last update ' ||
             EXTRACT(EPOCH FROM NOW() - MAX(updated_at))/3600 ||
             ' hours ago'
    END as freshness_status
FROM orders;
```

### Duplicate Detection

```sql
-- Find duplicates
SELECT
    order_id,
    COUNT(*) as duplicate_count
FROM orders
GROUP BY order_id
HAVING COUNT(*) > 1;
```

## Metric Thresholds

| Check Type | Warning | Critical |
|------------|---------|----------|
| Null percentage | > 5% | > 10% |
| Duplicate rate | > 0.1% | > 1% |
| Row count change | > ±20% | > ±50% |
| Freshness (hourly) | > 2 hours | > 4 hours |
| Freshness (daily) | > 26 hours | > 48 hours |
