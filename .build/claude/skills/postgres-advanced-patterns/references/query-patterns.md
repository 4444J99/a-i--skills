# PostgreSQL Query Patterns

Advanced query patterns for PostgreSQL.

## Common Table Expressions (CTEs)

### Recursive CTE (Hierarchies)

```sql
-- Organization hierarchy
WITH RECURSIVE org_tree AS (
    -- Base case: top-level
    SELECT id, name, manager_id, 1 as level
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- Recursive case
    SELECT e.id, e.name, e.manager_id, t.level + 1
    FROM employees e
    JOIN org_tree t ON e.manager_id = t.id
)
SELECT * FROM org_tree ORDER BY level, name;
```

### Multiple CTEs

```sql
WITH
active_users AS (
    SELECT * FROM users WHERE status = 'active'
),
recent_orders AS (
    SELECT * FROM orders WHERE created_at > NOW() - INTERVAL '30 days'
),
user_order_summary AS (
    SELECT
        u.id,
        u.name,
        COUNT(o.id) as order_count,
        SUM(o.total) as total_spent
    FROM active_users u
    LEFT JOIN recent_orders o ON u.id = o.user_id
    GROUP BY u.id, u.name
)
SELECT * FROM user_order_summary ORDER BY total_spent DESC;
```

## Window Functions

### Row Numbering

```sql
-- Rank users by total purchases
SELECT
    name,
    total_purchases,
    ROW_NUMBER() OVER (ORDER BY total_purchases DESC) as rank,
    RANK() OVER (ORDER BY total_purchases DESC) as rank_with_ties,
    DENSE_RANK() OVER (ORDER BY total_purchases DESC) as dense_rank
FROM users;
```

### Running Totals

```sql
SELECT
    date,
    amount,
    SUM(amount) OVER (ORDER BY date) as running_total,
    AVG(amount) OVER (
        ORDER BY date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) as moving_avg_7day
FROM sales;
```

### Partitioned Windows

```sql
-- Rank within each category
SELECT
    category,
    product_name,
    sales,
    RANK() OVER (PARTITION BY category ORDER BY sales DESC) as category_rank
FROM products;
```

### Lead/Lag

```sql
-- Compare to previous/next row
SELECT
    date,
    revenue,
    LAG(revenue) OVER (ORDER BY date) as prev_day_revenue,
    revenue - LAG(revenue) OVER (ORDER BY date) as day_over_day_change,
    LEAD(revenue) OVER (ORDER BY date) as next_day_revenue
FROM daily_revenue;
```

## JSON Operations

### JSON Extraction

```sql
-- Extract from JSON
SELECT
    data->>'name' as name,                    -- Text extraction
    data->'address'->>'city' as city,         -- Nested extraction
    (data->>'age')::int as age,               -- Cast to type
    data->'tags' as tags                      -- Keep as JSON
FROM users;
```

### JSON Aggregation

```sql
-- Build JSON from rows
SELECT json_agg(
    json_build_object(
        'id', id,
        'name', name,
        'email', email
    )
) as users
FROM users WHERE status = 'active';
```

### JSONB Contains

```sql
-- Query JSONB fields
SELECT * FROM products
WHERE attributes @> '{"color": "red"}';  -- Contains

SELECT * FROM products
WHERE attributes ? 'color';  -- Has key

SELECT * FROM products
WHERE attributes ?| ARRAY['color', 'size'];  -- Has any key
```

## Array Operations

```sql
-- Array contains
SELECT * FROM posts WHERE 'javascript' = ANY(tags);

-- Array overlap
SELECT * FROM posts WHERE tags && ARRAY['javascript', 'typescript'];

-- Array aggregation
SELECT
    user_id,
    ARRAY_AGG(DISTINCT tag ORDER BY tag) as all_tags
FROM post_tags
GROUP BY user_id;

-- Unnest array
SELECT id, UNNEST(tags) as tag FROM posts;
```

## Upsert Patterns

### ON CONFLICT

```sql
-- Insert or update
INSERT INTO users (email, name, updated_at)
VALUES ('user@example.com', 'John', NOW())
ON CONFLICT (email)
DO UPDATE SET
    name = EXCLUDED.name,
    updated_at = NOW();

-- Insert or ignore
INSERT INTO users (email, name)
VALUES ('user@example.com', 'John')
ON CONFLICT (email) DO NOTHING;
```

## Conditional Aggregation

```sql
SELECT
    DATE_TRUNC('month', created_at) as month,
    COUNT(*) as total_orders,
    COUNT(*) FILTER (WHERE status = 'completed') as completed,
    COUNT(*) FILTER (WHERE status = 'cancelled') as cancelled,
    SUM(total) FILTER (WHERE status = 'completed') as revenue
FROM orders
GROUP BY DATE_TRUNC('month', created_at)
ORDER BY month;
```

## Lateral Joins

```sql
-- Get top 3 posts per user
SELECT u.name, p.title, p.created_at
FROM users u
CROSS JOIN LATERAL (
    SELECT title, created_at
    FROM posts
    WHERE user_id = u.id
    ORDER BY created_at DESC
    LIMIT 3
) p;
```

## Full-Text Search

```sql
-- Create search index
CREATE INDEX posts_search_idx ON posts
USING GIN (to_tsvector('english', title || ' ' || content));

-- Search query
SELECT title, ts_rank(
    to_tsvector('english', title || ' ' || content),
    plainto_tsquery('english', 'search terms')
) as rank
FROM posts
WHERE to_tsvector('english', title || ' ' || content)
    @@ plainto_tsquery('english', 'search terms')
ORDER BY rank DESC;
```

## Date/Time Patterns

```sql
-- Generate date series
SELECT generate_series(
    '2024-01-01'::date,
    '2024-12-31'::date,
    '1 day'::interval
) as date;

-- Group by time bucket
SELECT
    DATE_TRUNC('hour', created_at) as hour,
    COUNT(*) as count
FROM events
GROUP BY DATE_TRUNC('hour', created_at);

-- Time zone conversion
SELECT
    created_at AT TIME ZONE 'UTC' AT TIME ZONE 'America/New_York' as eastern_time
FROM orders;
```

## Performance Tips

| Pattern | Optimization |
|---------|--------------|
| `LIMIT` on subqueries | Reduces rows early |
| `EXISTS` vs `IN` | EXISTS often faster for correlated |
| `DISTINCT ON` | Faster than GROUP BY for first per group |
| Partial indexes | Index only relevant rows |
| `EXPLAIN ANALYZE` | Always check query plan |
