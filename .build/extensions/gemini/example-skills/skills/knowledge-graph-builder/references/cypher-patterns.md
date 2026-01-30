# Cypher Query Patterns

## Pattern Matching

### Basic Patterns

```cypher
-- Single node
MATCH (n:Person) RETURN n

-- Node with properties
MATCH (n:Person {name: 'Alice'}) RETURN n

-- Relationship
MATCH (a:Person)-[:KNOWS]->(b:Person) RETURN a, b

-- Undirected relationship
MATCH (a:Person)-[:KNOWS]-(b:Person) RETURN a, b

-- Multiple relationships
MATCH (a:Person)-[:KNOWS]->(b:Person)-[:WORKS_AT]->(c:Company)
RETURN a, b, c
```

### Variable-Length Paths

```cypher
-- Exactly 2 hops
MATCH (a)-[:KNOWS*2]->(b) RETURN a, b

-- 1 to 3 hops
MATCH (a)-[:KNOWS*1..3]->(b) RETURN a, b

-- Any number of hops (expensive!)
MATCH (a)-[:KNOWS*]->(b) RETURN a, b

-- Zero or more hops
MATCH (a)-[:KNOWS*0..]->(b) RETURN a, b
```

### Named Paths

```cypher
-- Capture path for analysis
MATCH path = (a:Person)-[:KNOWS*1..5]->(b:Person)
WHERE a.name = 'Alice' AND b.name = 'Bob'
RETURN path, length(path) as hops
```

## Aggregations

```cypher
-- Count
MATCH (p:Person)-[:WORKS_AT]->(c:Company)
RETURN c.name, count(p) as employee_count

-- Collect into list
MATCH (p:Person)-[:HAS_SKILL]->(s:Skill)
RETURN p.name, collect(s.name) as skills

-- Multiple aggregations
MATCH (p:Person)-[:WORKED_ON]->(proj:Project)
RETURN p.name,
       count(proj) as project_count,
       sum(proj.budget) as total_budget,
       avg(proj.duration) as avg_duration
```

## Subqueries

### CALL Subquery

```cypher
-- Correlated subquery
MATCH (c:Company)
CALL {
    WITH c
    MATCH (c)<-[:WORKS_AT]-(e:Person)
    RETURN count(e) as employees
}
RETURN c.name, employees
ORDER BY employees DESC

-- UNION in subquery
MATCH (p:Person {name: 'Alice'})
CALL {
    WITH p
    MATCH (p)-[:KNOWS]->(friend)
    RETURN friend
    UNION
    MATCH (p)-[:WORKS_WITH]->(colleague)
    RETURN colleague as friend
}
RETURN DISTINCT friend.name
```

### EXISTS Subquery

```cypher
-- Filter with existence check
MATCH (p:Person)
WHERE EXISTS {
    MATCH (p)-[:MANAGES]->(team:Team)
    WHERE team.size > 5
}
RETURN p.name
```

## APOC Procedures

### Batch Processing

```cypher
-- Process in batches
CALL apoc.periodic.iterate(
    "MATCH (n:Person) WHERE n.processed IS NULL RETURN n",
    "SET n.processed = true, n.processedAt = datetime()",
    {batchSize: 1000, parallel: true}
)
```

### Path Expansion

```cypher
-- Configurable path expansion
MATCH (start:Person {name: 'Alice'})
CALL apoc.path.expandConfig(start, {
    relationshipFilter: "KNOWS|WORKS_WITH",
    minLevel: 1,
    maxLevel: 3,
    uniqueness: "NODE_GLOBAL"
}) YIELD path
RETURN path
```

### Data Import

```cypher
-- Load from JSON
CALL apoc.load.json('https://api.example.com/users')
YIELD value
MERGE (p:Person {id: value.id})
SET p.name = value.name, p.email = value.email

-- Load from CSV
LOAD CSV WITH HEADERS FROM 'file:///users.csv' AS row
MERGE (p:Person {id: row.id})
SET p.name = row.name
```

## Performance Patterns

### Use Indexes

```cypher
-- Create index for frequent lookups
CREATE INDEX person_name_idx FOR (p:Person) ON (p.name)

-- Composite index
CREATE INDEX person_name_email_idx FOR (p:Person) ON (p.name, p.email)

-- Full-text index
CREATE FULLTEXT INDEX person_bio_idx FOR (p:Person) ON EACH [p.bio]

-- Use index hint
MATCH (p:Person)
USING INDEX p:Person(name)
WHERE p.name = 'Alice'
RETURN p
```

### Profile Queries

```cypher
-- See execution plan
EXPLAIN MATCH (p:Person)-[:KNOWS]->(f) RETURN p, f

-- Execute and see actual performance
PROFILE MATCH (p:Person)-[:KNOWS]->(f) RETURN p, f
```

### Avoid Cartesian Products

```cypher
-- Bad: Creates cartesian product
MATCH (a:Person), (b:Company)
WHERE a.company_id = b.id
RETURN a, b

-- Good: Use relationship
MATCH (a:Person)-[:WORKS_AT]->(b:Company)
RETURN a, b
```
