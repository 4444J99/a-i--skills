# Graph Algorithms

## Neo4j Graph Data Science

### Setup

```cypher
-- Create in-memory graph projection
CALL gds.graph.project(
    'myGraph',
    'Person',
    'KNOWS',
    {
        nodeProperties: ['age', 'score'],
        relationshipProperties: ['weight']
    }
)

-- View projections
CALL gds.graph.list()

-- Drop projection
CALL gds.graph.drop('myGraph')
```

## Centrality Algorithms

### PageRank

Measures importance based on incoming links.

```cypher
-- Stream results
CALL gds.pageRank.stream('myGraph')
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).name AS name, score
ORDER BY score DESC
LIMIT 10

-- Write results to nodes
CALL gds.pageRank.write('myGraph', {
    writeProperty: 'pageRank',
    maxIterations: 20,
    dampingFactor: 0.85
})
```

### Betweenness Centrality

Identifies bridges/brokers in the network.

```cypher
CALL gds.betweenness.stream('myGraph')
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).name AS name, score
ORDER BY score DESC
LIMIT 10
```

### Degree Centrality

Simple connection count.

```cypher
CALL gds.degree.stream('myGraph', {
    orientation: 'UNDIRECTED'
})
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).name AS name, score as connections
ORDER BY connections DESC
```

## Community Detection

### Louvain

Finds densely connected clusters.

```cypher
CALL gds.louvain.stream('myGraph')
YIELD nodeId, communityId
WITH communityId, collect(gds.util.asNode(nodeId).name) AS members
RETURN communityId, size(members) AS size, members
ORDER BY size DESC
```

### Label Propagation

Fast community detection.

```cypher
CALL gds.labelPropagation.stream('myGraph')
YIELD nodeId, communityId
RETURN communityId, count(*) AS size
ORDER BY size DESC
```

### Weakly Connected Components

Find disconnected subgraphs.

```cypher
CALL gds.wcc.stream('myGraph')
YIELD nodeId, componentId
RETURN componentId, count(*) AS size
ORDER BY size DESC
```

## Path Finding

### Shortest Path

```cypher
-- Dijkstra (weighted)
MATCH (source:Person {name: 'Alice'}), (target:Person {name: 'Bob'})
CALL gds.shortestPath.dijkstra.stream('myGraph', {
    sourceNode: source,
    targetNode: target,
    relationshipWeightProperty: 'weight'
})
YIELD path, totalCost
RETURN path, totalCost

-- Unweighted shortest path (native)
MATCH path = shortestPath(
    (a:Person {name: 'Alice'})-[:KNOWS*]-(b:Person {name: 'Bob'})
)
RETURN path, length(path)
```

### All Shortest Paths

```cypher
MATCH paths = allShortestPaths(
    (a:Person {name: 'Alice'})-[:KNOWS*]-(b:Person {name: 'Bob'})
)
RETURN paths
```

### A* (with heuristic)

```cypher
CALL gds.shortestPath.astar.stream('myGraph', {
    sourceNode: source,
    targetNode: target,
    latitudeProperty: 'latitude',
    longitudeProperty: 'longitude',
    relationshipWeightProperty: 'distance'
})
YIELD path, totalCost
RETURN path, totalCost
```

## Similarity Algorithms

### Node Similarity

```cypher
-- Find similar nodes based on neighbors
CALL gds.nodeSimilarity.stream('myGraph')
YIELD node1, node2, similarity
RETURN gds.util.asNode(node1).name AS Person1,
       gds.util.asNode(node2).name AS Person2,
       similarity
ORDER BY similarity DESC
LIMIT 10
```

### K-Nearest Neighbors

```cypher
CALL gds.knn.stream('myGraph', {
    nodeProperties: ['embedding'],
    topK: 5
})
YIELD node1, node2, similarity
RETURN gds.util.asNode(node1).name, gds.util.asNode(node2).name, similarity
```

## Link Prediction

```cypher
-- Common Neighbors
CALL gds.linkprediction.commonNeighbors.stream('myGraph')
YIELD node1, node2, score
RETURN gds.util.asNode(node1).name, gds.util.asNode(node2).name, score
ORDER BY score DESC
LIMIT 10

-- Preferential Attachment
CALL gds.linkprediction.preferentialAttachment.stream('myGraph')
YIELD node1, node2, score
```

## Algorithm Selection Guide

| Use Case | Algorithm |
|----------|-----------|
| Find influencers | PageRank |
| Find bridges | Betweenness |
| Group similar items | Louvain, Label Prop |
| Find path | Dijkstra, A* |
| Recommend connections | Node Similarity |
| Predict links | Common Neighbors |
