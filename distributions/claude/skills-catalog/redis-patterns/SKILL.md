---
name: redis-patterns
description: Use Redis effectively for caching, pub/sub messaging, rate limiting, distributed locks, and session storage. Covers data structure selection, expiration strategies, and cluster patterns. Triggers on Redis usage, caching architecture, or pub/sub messaging requests.
license: MIT
complexity: intermediate
time_to_learn: 30min
tags:
  - redis
  - caching
  - pub-sub
  - distributed-systems
  - rate-limiting
governance_phases: [build]
organ_affinity: [organ-iii, organ-iv]
triggers: [user-asks-about-redis, project-has-redis-config, context:caching, context:pub-sub, context:rate-limiting]
complements: [resilience-patterns, backend-implementation-patterns, fastapi-patterns]
---

# Redis Patterns

Effective patterns for caching, messaging, and distributed coordination with Redis.

## Data Structure Selection

| Need | Structure | Example |
|------|-----------|---------|
| Simple cache | String | `SET user:123 '{"name":"Jo"}'` |
| Object fields | Hash | `HSET user:123 name Jo email jo@x.com` |
| Unique collection | Set | `SADD online_users user:123 user:456` |
| Ranked items | Sorted Set | `ZADD leaderboard 100 user:123` |
| Message queue | List | `LPUSH tasks '{"type":"email"}'` |
| Recent items | List (capped) | `LPUSH + LTRIM` |
| Real-time messaging | Pub/Sub | `PUBLISH events '{"type":"deploy"}'` |
| Event log | Stream | `XADD events * type deploy organ IV` |

## Caching Patterns

### Cache-Aside (Lazy Loading)

```python
import redis
import json

r = redis.Redis(decode_responses=True)

async def get_user(user_id: str) -> dict:
    cache_key = f"user:{user_id}"
    cached = r.get(cache_key)
    if cached:
        return json.loads(cached)

    user = await db.fetch_user(user_id)
    r.setex(cache_key, 3600, json.dumps(user))  # TTL: 1 hour
    return user
```

### Write-Through

```python
async def update_user(user_id: str, data: dict) -> dict:
    user = await db.update_user(user_id, data)
    r.setex(f"user:{user_id}", 3600, json.dumps(user))
    return user
```

### Cache Invalidation

```python
def invalidate_user(user_id: str):
    r.delete(f"user:{user_id}")

def invalidate_user_pattern(user_id: str):
    # Invalidate all related keys
    for key in r.scan_iter(f"user:{user_id}:*"):
        r.delete(key)
```

### Stampede Prevention

```python
import time

def get_with_lock(key: str, ttl: int, fetch_fn):
    value = r.get(key)
    if value:
        return json.loads(value)

    lock_key = f"lock:{key}"
    if r.set(lock_key, "1", nx=True, ex=10):  # 10s lock
        try:
            value = fetch_fn()
            r.setex(key, ttl, json.dumps(value))
            return value
        finally:
            r.delete(lock_key)
    else:
        # Wait for other process to populate
        time.sleep(0.1)
        return get_with_lock(key, ttl, fetch_fn)
```

## Pub/Sub Patterns

### Basic Publisher/Subscriber

```python
# Publisher
def publish_event(channel: str, event: dict):
    r.publish(channel, json.dumps(event))

# Subscriber
def subscribe_events(channel: str):
    pubsub = r.pubsub()
    pubsub.subscribe(channel)
    for message in pubsub.listen():
        if message["type"] == "message":
            event = json.loads(message["data"])
            handle_event(event)
```

### Redis Streams (Durable Messaging)

```python
# Producer
r.xadd("events", {"type": "deploy", "organ": "IV", "repo": "a-i--skills"})

# Consumer group
r.xgroup_create("events", "workers", id="0", mkstream=True)

# Consumer
while True:
    messages = r.xreadgroup("workers", "worker-1", {"events": ">"}, count=10, block=5000)
    for stream, entries in messages:
        for msg_id, data in entries:
            process(data)
            r.xack("events", "workers", msg_id)
```

## Rate Limiting

### Sliding Window

```python
def is_rate_limited(user_id: str, limit: int = 100, window: int = 60) -> bool:
    key = f"rate:{user_id}"
    now = time.time()
    pipe = r.pipeline()
    pipe.zremrangebyscore(key, 0, now - window)
    pipe.zadd(key, {str(now): now})
    pipe.zcard(key)
    pipe.expire(key, window)
    results = pipe.execute()
    return results[2] > limit
```

### Token Bucket

```python
def acquire_token(key: str, rate: int, capacity: int) -> bool:
    lua_script = """
    local tokens = tonumber(redis.call('get', KEYS[1]) or ARGV[2])
    local last = tonumber(redis.call('get', KEYS[2]) or ARGV[3])
    local now = tonumber(ARGV[3])
    local elapsed = now - last
    tokens = math.min(tonumber(ARGV[2]), tokens + elapsed * tonumber(ARGV[1]))
    if tokens >= 1 then
        redis.call('set', KEYS[1], tokens - 1)
        redis.call('set', KEYS[2], now)
        return 1
    end
    return 0
    """
    return bool(r.eval(lua_script, 2, f"{key}:tokens", f"{key}:ts", rate, capacity, time.time()))
```

## Distributed Locks

```python
import uuid

def acquire_lock(name: str, timeout: int = 10) -> str | None:
    token = str(uuid.uuid4())  # allow-secret
    if r.set(f"lock:{name}", token, nx=True, ex=timeout):
        return token  # allow-secret
    return None

def release_lock(name: str, token: str) -> bool:  # allow-secret
    lua = """
    if redis.call('get', KEYS[1]) == ARGV[1] then
        return redis.call('del', KEYS[1])
    end
    return 0
    """
    return bool(r.eval(lua, 1, f"lock:{name}", token))
```

## Session Storage

```python
def store_session(session_id: str, data: dict, ttl: int = 86400):
    r.hset(f"session:{session_id}", mapping=data)
    r.expire(f"session:{session_id}", ttl)

def get_session(session_id: str) -> dict | None:
    data = r.hgetall(f"session:{session_id}")
    return data if data else None

def extend_session(session_id: str, ttl: int = 86400):
    r.expire(f"session:{session_id}", ttl)
```

## Key Naming Conventions

```
{entity}:{id}                    → user:123
{entity}:{id}:{field}            → user:123:preferences
{scope}:{entity}:{id}            → organ-iv:repo:a-i--skills
{function}:{entity}:{id}         → cache:user:123, lock:deploy:iv
```

## Performance Patterns

### Pipelining

```python
pipe = r.pipeline()
for user_id in user_ids:
    pipe.get(f"user:{user_id}")
results = pipe.execute()
```

### Lua Scripts for Atomicity

Use Lua when multiple operations must be atomic. Redis executes Lua scripts as a single atomic operation.

### Memory Management

```python
# Set maxmemory policy
# allkeys-lru: Evict least recently used keys (good for caches)
# volatile-lru: Evict only keys with TTL set
# noeviction: Return errors when memory is full (good for queues)
```

## Anti-Patterns

- **Using Redis as primary database** — Redis is volatile by default; use it as cache or coordination layer
- **Unbounded key growth** — Always set TTLs or implement cleanup
- **Large values** — Keep values under 100KB; use references for larger data
- **Blocking on KEYS command** — Use SCAN for production iteration
- **Missing error handling** — Always handle ConnectionError and TimeoutError
