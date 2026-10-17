# Index Strategy Guide

When and how to create indexes for optimal query performance.

## Index Types

### B-Tree (Default)

Best for:
- Equality comparisons (`=`)
- Range queries (`<`, `>`, `BETWEEN`)
- Sorting (`ORDER BY`)
- Prefix matching (`LIKE 'abc%'`)

```sql
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_orders_date ON orders(order_date);
```

### Hash

Best for:
- Exact equality only
- Very fast for `=` comparisons

```sql
-- PostgreSQL
CREATE INDEX idx_users_id_hash ON users USING HASH (id);
```

Limitations:
- No range queries
- No sorting
- No partial matching

### GIN (Generalized Inverted Index)

Best for:
- Array containment
- Full-text search
- JSONB queries

```sql
-- Array
CREATE INDEX idx_posts_tags ON posts USING GIN (tags);

-- Full-text
CREATE INDEX idx_articles_body ON articles USING GIN (to_tsvector('english', body));

-- JSONB
CREATE INDEX idx_data_json ON data USING GIN (attributes jsonb_path_ops);
```

### GiST (Generalized Search Tree)

Best for:
- Geometric data
- Range types
- Full-text (alternative to GIN)

```sql
CREATE INDEX idx_places_location ON places USING GIST (location);
CREATE INDEX idx_events_duration ON events USING GIST (time_range);
```

## Index Design Patterns

### Single Column

```sql
-- Most common: filter columns
CREATE INDEX idx_users_status ON users(status);

-- Foreign keys (often overlooked)
CREATE INDEX idx_orders_user_id ON orders(user_id);
```

### Composite (Multi-Column)

Column order matters! Place:
1. Equality columns first
2. Range columns last

```sql
-- Good: filters by status (=), then date range
CREATE INDEX idx_orders_status_date ON orders(status, order_date);

-- Query uses both columns
SELECT * FROM orders WHERE status = 'pending' AND order_date > '2024-01-01';

-- Query uses only first column (still works!)
SELECT * FROM orders WHERE status = 'pending';

-- Query uses only second column (index NOT used efficiently)
SELECT * FROM orders WHERE order_date > '2024-01-01';
```

### Covering Index

Include columns needed by SELECT to avoid table lookup:

```sql
-- PostgreSQL
CREATE INDEX idx_orders_covering ON orders(user_id) INCLUDE (total, status);

-- Query satisfied entirely by index
SELECT total, status FROM orders WHERE user_id = 123;
```

### Partial Index

Index subset of rows:

```sql
-- Only index active users
CREATE INDEX idx_active_users ON users(email) WHERE status = 'active';

-- Only index recent orders
CREATE INDEX idx_recent_orders ON orders(user_id)
WHERE order_date > '2024-01-01';
```

### Expression Index

Index on computed value:

```sql
-- Index lowercase email
CREATE INDEX idx_users_email_lower ON users(LOWER(email));

-- Query must use same expression
SELECT * FROM users WHERE LOWER(email) = 'user@example.com';

-- Index year from date
CREATE INDEX idx_orders_year ON orders(EXTRACT(YEAR FROM order_date));
```

## When to Index

### Always Index

- Primary keys (automatic)
- Foreign keys
- Columns in `WHERE` clauses (frequently queried)
- Columns in `JOIN` conditions
- Columns in `ORDER BY` (if sorting is slow)

### Consider Indexing

- Columns with high selectivity (many unique values)
- Columns used in `GROUP BY`
- Columns in `DISTINCT` queries

### Avoid Indexing

- Small tables (<1000 rows)
- Columns with low selectivity (few unique values like boolean)
- Columns rarely queried
- Tables with heavy write load (indexes slow writes)

## Index Performance Impact

### Read Operations

| Operation | Without Index | With Index |
|-----------|---------------|------------|
| Equality lookup | O(n) scan | O(log n) |
| Range scan | O(n) scan | O(log n + k) |
| Sort | O(n log n) | O(n) or O(1) |

### Write Operations

| Operation | Impact |
|-----------|--------|
| INSERT | Slower (index maintenance) |
| UPDATE | Slower if indexed column changes |
| DELETE | Slower (index cleanup) |

**Rule of thumb**: Each index adds ~10-20% overhead to writes.

## Maintenance

### Check Index Usage (PostgreSQL)

```sql
SELECT
    schemaname,
    relname AS table,
    indexrelname AS index,
    idx_scan AS times_used,
    pg_size_pretty(pg_relation_size(indexrelid)) AS size
FROM pg_stat_user_indexes
ORDER BY idx_scan ASC;
```

### Find Unused Indexes

```sql
SELECT
    indexrelname,
    idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0
AND schemaname = 'public';
```

### Rebuild Bloated Indexes

```sql
-- PostgreSQL
REINDEX INDEX idx_name;

-- Or rebuild concurrently (no lock)
REINDEX INDEX CONCURRENTLY idx_name;
```

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Too many indexes | Slow writes, storage bloat | Remove unused |
| Wrong column order | Composite index not used | Put equality columns first |
| Indexing low-cardinality | No benefit | Remove or use partial |
| Missing FK indexes | Slow joins/deletes | Add indexes on FKs |
| Functions on columns | Index not used | Use expression index |

## Quick Checklist

Before creating an index:

- [ ] Is this column frequently queried?
- [ ] Does the column have good selectivity?
- [ ] Is the table large enough to benefit?
- [ ] Can existing indexes be extended instead?
- [ ] Is write performance acceptable with new index?
