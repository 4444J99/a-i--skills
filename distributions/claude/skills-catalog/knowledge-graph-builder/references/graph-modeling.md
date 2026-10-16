# Graph Data Modeling

## Design Principles

### Nodes vs Properties

**Use nodes when:**
- The concept has its own identity
- You need to connect it to other things
- You want to query it directly

**Use properties when:**
- It's a simple attribute
- No need to connect it elsewhere
- Won't query by this alone

### Relationship Direction

```
Always model direction based on domain semantics:

(Person)-[:WORKS_AT]->(Company)     ✓ Clear direction
(Person)-[:KNOWS]->(Person)         ✓ Can query either way
(Person)<-[:EMPLOYS]-(Company)      ✓ Alternative, equally valid
```

### Relationship vs Node

**Use relationship when:**
- It's a direct connection between two things
- Properties are about the connection itself

**Use intermediate node when:**
- Connection has complex attributes
- Need to connect the connection to other things
- Multiple relationships would duplicate data

```cypher
-- Simple relationship
(Person)-[:BOUGHT {date, price}]->(Product)

-- Intermediate node for complex case
(Person)-[:PLACED]->(Order)-[:CONTAINS]->(Product)
                         \-[:SHIPPED_TO]->(Address)
```

## Common Patterns

### Hierarchies

```cypher
-- Organization hierarchy
(Employee)-[:REPORTS_TO]->(Manager)-[:REPORTS_TO]->(Director)

-- Category tree
(SubCategory)-[:CHILD_OF]->(Category)-[:CHILD_OF]->(RootCategory)

-- Query any level
MATCH (e:Employee)-[:REPORTS_TO*]->(ceo:Employee {role: 'CEO'})
RETURN e.name
```

### Versioning

```cypher
-- Create version relationship
(Document)-[:HAS_VERSION]->(DocumentVersion {
    version: 2,
    created_at: datetime(),
    content: "..."
})

-- Point to current version
(Document)-[:CURRENT_VERSION]->(DocumentVersion)

-- Query history
MATCH (d:Document)-[:HAS_VERSION]->(v:DocumentVersion)
RETURN v ORDER BY v.created_at
```

### Temporal Data

```cypher
-- State changes over time
(Person)-[:HAS_STATE {
    valid_from: date('2020-01-01'),
    valid_to: date('2020-12-31')
}]->(PersonState {status: 'employed'})

-- Query state at point in time
MATCH (p:Person)-[r:HAS_STATE]->(s:PersonState)
WHERE r.valid_from <= date('2020-06-15')
  AND (r.valid_to IS NULL OR r.valid_to >= date('2020-06-15'))
RETURN p, s
```

### Authorization Model

```cypher
-- Role-based access
(User)-[:HAS_ROLE]->(Role)-[:CAN_ACCESS]->(Resource)
(Role)-[:INHERITS]->(Role)

-- Check access
MATCH (u:User {id: $userId})-[:HAS_ROLE*1..3]->(r:Role)-[:CAN_ACCESS]->(res:Resource {id: $resourceId})
RETURN count(*) > 0 as hasAccess
```

### Event Sourcing

```cypher
-- Events as nodes
(Entity)-[:HAD_EVENT]->(Event {
    type: 'StatusChanged',
    timestamp: datetime(),
    data: {old: 'pending', new: 'active'}
})

-- Chain events
(Event1)-[:FOLLOWED_BY]->(Event2)-[:FOLLOWED_BY]->(Event3)
```

## Anti-Patterns

### Dense Nodes

```cypher
-- Bad: Too many relationships on one node
(PopularUser)-[:FOLLOWED_BY]->(millions of followers)

-- Better: Shard with intermediate nodes
(PopularUser)-[:HAS_FOLLOWER_GROUP]->(FollowerGroup)-[:CONTAINS]->(Follower)
```

### Property Arrays for Relationships

```cypher
-- Bad: Storing related IDs as array property
(Person {friend_ids: [1, 2, 3, 4]})

-- Good: Use relationships
(Person)-[:FRIENDS_WITH]->(Person)
```

### Generic Relationship Types

```cypher
-- Bad: Generic relationship
(a)-[:RELATED_TO {type: 'knows'}]->(b)

-- Good: Specific relationship
(a)-[:KNOWS]->(b)
```

## Schema Constraints

```cypher
-- Unique constraint
CREATE CONSTRAINT person_email_unique
FOR (p:Person) REQUIRE p.email IS UNIQUE

-- Node key (composite unique)
CREATE CONSTRAINT order_item_key
FOR (oi:OrderItem) REQUIRE (oi.order_id, oi.product_id) IS NODE KEY

-- Property existence
CREATE CONSTRAINT person_name_exists
FOR (p:Person) REQUIRE p.name IS NOT NULL
```
