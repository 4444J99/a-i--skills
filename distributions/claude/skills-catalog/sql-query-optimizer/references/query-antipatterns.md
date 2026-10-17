# SQL Query Anti-Patterns

Common performance killers and how to fix them.

## SELECT Anti-Patterns

### SELECT *

**Problem**: Fetches all columns, wastes bandwidth, prevents covering indexes.

```sql
-- Bad
SELECT * FROM orders WHERE user_id = 123;

-- Good
SELECT order_id, total, status FROM orders WHERE user_id = 123;
```

### SELECT DISTINCT as a Band-Aid

**Problem**: Often hides a JOIN problem or missing WHERE clause.

```sql
-- Bad: covering up duplicate rows from bad join
SELECT DISTINCT u.name FROM users u
JOIN orders o ON u.id = o.user_id;

-- Good: fix the root cause
SELECT u.name FROM users u
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.user_id = u.id);
```

## WHERE Clause Anti-Patterns

### Functions on Indexed Columns

**Problem**: Prevents index usage.

```sql
-- Bad: index on created_at not used
SELECT * FROM orders WHERE YEAR(created_at) = 2024;

-- Good: sargable predicate
SELECT * FROM orders
WHERE created_at >= '2024-01-01' AND created_at < '2025-01-01';
```

```sql
-- Bad: index on email not used
SELECT * FROM users WHERE LOWER(email) = 'user@example.com';

-- Good: use expression index or store normalized
CREATE INDEX idx_email_lower ON users(LOWER(email));
SELECT * FROM users WHERE LOWER(email) = 'user@example.com';
```

### Leading Wildcards

**Problem**: Can't use index.

```sql
-- Bad: full table scan
SELECT * FROM products WHERE name LIKE '%phone%';

-- Better: trailing wildcard uses index
SELECT * FROM products WHERE name LIKE 'phone%';

-- Best for search: use full-text search
SELECT * FROM products
WHERE to_tsvector('english', name) @@ to_tsquery('phone');
```

### OR Conditions

**Problem**: Often causes table scans.

```sql
-- Bad: may not use indexes efficiently
SELECT * FROM orders WHERE status = 'pending' OR status = 'processing';

-- Good: use IN
SELECT * FROM orders WHERE status IN ('pending', 'processing');

-- For different columns, consider UNION
SELECT * FROM users WHERE email = 'x' OR phone = 'y';
-- Could be rewritten as
SELECT * FROM users WHERE email = 'x'
UNION
SELECT * FROM users WHERE phone = 'y';
```

### Implicit Type Conversion

**Problem**: Index can't be used when types don't match.

```sql
-- Bad: user_id is integer, comparing to string
SELECT * FROM orders WHERE user_id = '123';

-- Good: use correct type
SELECT * FROM orders WHERE user_id = 123;
```

### NOT IN with NULLs

**Problem**: Returns no rows if subquery contains NULL.

```sql
-- Dangerous: returns nothing if any inactive user_id is NULL
SELECT * FROM orders WHERE user_id NOT IN (
    SELECT id FROM users WHERE status = 'inactive'
);

-- Safe: NOT EXISTS handles NULLs correctly
SELECT * FROM orders o WHERE NOT EXISTS (
    SELECT 1 FROM users u
    WHERE u.id = o.user_id AND u.status = 'inactive'
);
```

## JOIN Anti-Patterns

### Cartesian Product

**Problem**: Missing join condition multiplies rows.

```sql
-- Bad: returns M × N rows
SELECT * FROM orders, users;

-- Good: explicit join with condition
SELECT * FROM orders o
JOIN users u ON o.user_id = u.id;
```

### Joining on Non-Indexed Columns

**Problem**: Requires nested loop with full scans.

```sql
-- Slow without index
SELECT * FROM orders o
JOIN products p ON o.product_code = p.code;

-- Fix: add index
CREATE INDEX idx_products_code ON products(code);
```

### Excessive Joins

**Problem**: Each join multiplies complexity.

```sql
-- Consider: do you need all these tables?
SELECT * FROM orders o
JOIN users u ON o.user_id = u.id
JOIN addresses a ON u.id = a.user_id
JOIN products p ON o.product_id = p.id
JOIN categories c ON p.category_id = c.id
JOIN vendors v ON p.vendor_id = v.id;

-- Better: only join what you need
-- Or: denormalize for read-heavy workloads
```

## Subquery Anti-Patterns

### Correlated Subquery in SELECT

**Problem**: Executes once per row.

```sql
-- Bad: N+1 queries
SELECT
    o.id,
    (SELECT COUNT(*) FROM order_items WHERE order_id = o.id) as item_count
FROM orders o;

-- Good: single aggregation
SELECT o.id, COALESCE(oi.item_count, 0) as item_count
FROM orders o
LEFT JOIN (
    SELECT order_id, COUNT(*) as item_count
    FROM order_items GROUP BY order_id
) oi ON o.id = oi.order_id;
```

### Subquery Instead of JOIN

**Problem**: Multiple scans instead of one.

```sql
-- Bad: subquery
SELECT * FROM orders
WHERE user_id IN (SELECT id FROM users WHERE status = 'active');

-- Good: join
SELECT o.* FROM orders o
JOIN users u ON o.user_id = u.id
WHERE u.status = 'active';

-- Also good: EXISTS (sometimes faster)
SELECT * FROM orders o
WHERE EXISTS (
    SELECT 1 FROM users u
    WHERE u.id = o.user_id AND u.status = 'active'
);
```

## Aggregation Anti-Patterns

### COUNT(*) vs COUNT(column)

```sql
-- COUNT(*): counts all rows (fast, uses index)
SELECT COUNT(*) FROM orders;

-- COUNT(column): counts non-NULL values only (may be slower)
SELECT COUNT(shipped_date) FROM orders;

-- Know the difference!
```

### HAVING Instead of WHERE

**Problem**: Filters after aggregation instead of before.

```sql
-- Bad: aggregates all, then filters
SELECT user_id, SUM(total) FROM orders
GROUP BY user_id
HAVING user_id > 100;

-- Good: filters first
SELECT user_id, SUM(total) FROM orders
WHERE user_id > 100
GROUP BY user_id;
```

## LIMIT Anti-Patterns

### OFFSET for Pagination

**Problem**: Scans and discards rows.

```sql
-- Bad: scans 10000 rows, returns 10
SELECT * FROM orders ORDER BY created_at DESC LIMIT 10 OFFSET 10000;

-- Good: keyset pagination
SELECT * FROM orders
WHERE created_at < '2024-01-15 10:30:00'
ORDER BY created_at DESC
LIMIT 10;
```

## Quick Reference

| Anti-Pattern | Detection | Fix |
|--------------|-----------|-----|
| SELECT * | Query review | Explicit columns |
| Function on column | EXPLAIN shows Seq Scan | Expression index or rewrite |
| Leading wildcard | LIKE '%...' | Full-text search |
| OR conditions | EXPLAIN shows Seq Scan | IN or UNION |
| Correlated subquery | SELECT list subquery | JOIN or window function |
| Large OFFSET | OFFSET > 1000 | Keyset pagination |
| Missing index on FK | Slow JOINs/DELETEs | Add index |
