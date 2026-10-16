---
name: vector-search-patterns
description: Implement vector similarity search with embedding generation, index selection, and hybrid retrieval strategies. Covers ChromaDB, pgvector, FAISS, and RAG pipeline design. Triggers on vector search, embeddings, semantic search, or RAG architecture requests.
license: MIT
complexity: advanced
time_to_learn: 30min
tags:
  - vector-search
  - embeddings
  - semantic-search
  - rag
  - chromadb
  - pgvector
governance_phases: [build]
organ_affinity: [organ-i, organ-iii]
triggers: [user-asks-about-vector-search, context:semantic-search, context:rag, context:embeddings, project-has-chromadb, project-has-pgvector]
complements: [postgres-advanced-patterns, data-pipeline-architect, knowledge-graph-builder]
---

# Vector Search Patterns

Implement semantic similarity search for retrieval-augmented generation and intelligent querying.

## Embedding Pipeline

### Generating Embeddings

```python
import httpx

async def get_embeddings(texts: list[str], model: str = "text-embedding-3-small") -> list[list[float]]:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.openai.com/v1/embeddings",
            headers={"Authorization": f"Bearer {api_key}"},
            json={"input": texts, "model": model},
        )
        data = response.json()
        return [item["embedding"] for item in data["data"]]
```

### Chunking Strategies

| Strategy | Use Case | Chunk Size |
|----------|----------|------------|
| Fixed-size | Simple documents | 500-1000 tokens |
| Sentence-based | Articles, essays | 3-5 sentences |
| Paragraph-based | Structured docs | Natural breaks |
| Recursive | Mixed content | Hierarchical split |
| Semantic | Research papers | Topic boundaries |

```python
def chunk_text(text: str, max_tokens: int = 500, overlap: int = 50) -> list[str]:
    sentences = text.split(". ")
    chunks = []
    current = []
    current_len = 0

    for sentence in sentences:
        sentence_len = len(sentence.split())
        if current_len + sentence_len > max_tokens and current:
            chunks.append(". ".join(current) + ".")
            # Keep overlap
            overlap_start = max(0, len(current) - 2)
            current = current[overlap_start:]
            current_len = sum(len(s.split()) for s in current)
        current.append(sentence)
        current_len += sentence_len

    if current:
        chunks.append(". ".join(current) + ".")
    return chunks
```

## Vector Stores

### ChromaDB (Development / Small Scale)

```python
import chromadb

client = chromadb.PersistentClient(path="./chroma_data")
collection = client.get_or_create_collection(
    name="documents",
    metadata={"hnsw:space": "cosine"},
)

# Ingest
collection.add(
    ids=["doc1", "doc2"],
    documents=["First document text", "Second document text"],
    metadatas=[{"source": "wiki"}, {"source": "blog"}],
)

# Query
results = collection.query(
    query_texts=["search query"],
    n_results=5,
    where={"source": "wiki"},  # Metadata filter
)
```

### pgvector (Production / PostgreSQL)

```sql
-- Enable extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create table
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    embedding vector(1536),  -- Match embedding dimension
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create index (IVFFlat for large datasets)
CREATE INDEX ON documents
    USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);  -- sqrt(num_rows) is a good starting point

-- Or HNSW for better recall
CREATE INDEX ON documents
    USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);

-- Similarity search
SELECT id, content, 1 - (embedding <=> $1::vector) AS similarity
FROM documents
ORDER BY embedding <=> $1::vector
LIMIT 10;
```

```python
import asyncpg

async def search(query_embedding: list[float], limit: int = 10) -> list[dict]:
    conn = await asyncpg.connect(dsn)
    rows = await conn.fetch(
        """
        SELECT id, content, 1 - (embedding <=> $1::vector) AS similarity
        FROM documents
        ORDER BY embedding <=> $1::vector
        LIMIT $2
        """,
        str(query_embedding), limit,
    )
    return [dict(row) for row in rows]
```

### FAISS (High-Performance Local)

```python
import faiss
import numpy as np

# Build index
dimension = 1536
index = faiss.IndexFlatIP(dimension)  # Inner product (use with normalized vectors)

# Add vectors
vectors = np.array(embeddings, dtype=np.float32)
faiss.normalize_L2(vectors)
index.add(vectors)

# Search
query = np.array([query_embedding], dtype=np.float32)
faiss.normalize_L2(query)
distances, indices = index.search(query, k=10)
```

## Hybrid Search

Combine vector similarity with keyword search for better recall:

```sql
-- Hybrid: vector + full-text search
WITH vector_results AS (
    SELECT id, content, 1 - (embedding <=> $1::vector) AS vscore
    FROM documents
    ORDER BY embedding <=> $1::vector
    LIMIT 20
),
text_results AS (
    SELECT id, content, ts_rank(tsv, plainto_tsquery($2)) AS tscore
    FROM documents
    WHERE tsv @@ plainto_tsquery($2)
    LIMIT 20
)
SELECT
    COALESCE(v.id, t.id) AS id,
    COALESCE(v.content, t.content) AS content,
    COALESCE(v.vscore, 0) * 0.7 + COALESCE(t.tscore, 0) * 0.3 AS combined_score
FROM vector_results v
FULL OUTER JOIN text_results t ON v.id = t.id
ORDER BY combined_score DESC
LIMIT 10;
```

## RAG Pipeline

```python
async def rag_query(question: str) -> str:
    # 1. Embed the question
    query_embedding = (await get_embeddings([question]))[0]

    # 2. Retrieve relevant chunks
    chunks = await search(query_embedding, limit=5)

    # 3. Build context
    context = "\n\n".join(c["content"] for c in chunks)

    # 4. Generate answer with context
    response = await llm.complete(
        system="Answer based on the provided context. Cite sources.",
        messages=[{
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion: {question}",
        }],
    )
    return response
```

## Index Selection Guide

| Dataset Size | Recommended Index | Recall | Speed |
|-------------|-------------------|--------|-------|
| < 10K | Flat (exact) | 100% | Fast enough |
| 10K - 1M | HNSW | 95-99% | Very fast |
| 1M - 100M | IVFFlat | 90-95% | Fast |
| > 100M | IVF + PQ | 80-90% | Fastest |

## Anti-Patterns

- **Embedding entire documents** — Chunk first, embed chunks
- **No metadata filtering** — Pre-filter with metadata before vector search
- **Ignoring embedding model limits** — Respect max token limits per embedding call
- **Static chunking for all content** — Match chunking strategy to content type
- **No reranking** — Use a cross-encoder reranker for top results in production
- **Storing embeddings without source text** — Always store the original text alongside vectors
