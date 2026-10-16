---
name: resilience-patterns
description: Build fault-tolerant systems with circuit breakers, retries with backoff, bulkheads, timeouts, and graceful degradation. Covers distributed system failure modes and recovery strategies. Triggers on reliability engineering, fault tolerance, or distributed system resilience requests.
license: MIT
complexity: advanced
time_to_learn: 30min
tags:
  - resilience
  - fault-tolerance
  - circuit-breaker
  - retry
  - distributed-systems
governance_phases: [build]
organ_affinity: [organ-iii, organ-vii]
triggers: [user-asks-about-resilience, context:distributed-systems, context:fault-tolerance, context:reliability, context:error-recovery]
complements: [redis-patterns, backend-implementation-patterns, error-handling-logging-patterns]
---

# Resilience Patterns

Build systems that survive partial failures and degrade gracefully.

## Core Patterns

### Retry with Exponential Backoff

```python
import asyncio
import random
from functools import wraps

def retry(max_attempts: int = 3, base_delay: float = 1.0, max_delay: float = 30.0):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    delay = min(base_delay * (2 ** attempt) + random.uniform(0, 1), max_delay)
                    await asyncio.sleep(delay)
        return wrapper
    return decorator

@retry(max_attempts=3, base_delay=1.0)
async def fetch_data(url: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
```

### Circuit Breaker

```python
import time
from enum import Enum

class CircuitState(Enum):
    CLOSED = "closed"       # Normal operation
    OPEN = "open"           # Failing, reject requests
    HALF_OPEN = "half_open" # Testing recovery

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, recovery_timeout: float = 30.0):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = 0.0

    async def call(self, func, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitOpenError(f"Circuit open, retry after {self.recovery_timeout}s")

        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise

    def _on_success(self):
        self.failure_count = 0
        self.state = CircuitState.CLOSED

    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
```

### Timeout

```python
async def with_timeout(coro, seconds: float):
    try:
        return await asyncio.wait_for(coro, timeout=seconds)
    except asyncio.TimeoutError:
        raise TimeoutError(f"Operation timed out after {seconds}s")
```

### Bulkhead (Resource Isolation)

```python
class Bulkhead:
    """Limit concurrent access to a resource."""
    def __init__(self, max_concurrent: int = 10):
        self.semaphore = asyncio.Semaphore(max_concurrent)

    async def execute(self, func, *args, **kwargs):
        async with self.semaphore:
            return await func(*args, **kwargs)

# Isolate different downstream services
payment_bulkhead = Bulkhead(max_concurrent=5)
inventory_bulkhead = Bulkhead(max_concurrent=20)
```

### Fallback

```python
async def get_user_profile(user_id: str) -> dict:
    try:
        return await primary_service.get_profile(user_id)
    except ServiceUnavailable:
        try:
            return await cache.get_profile(user_id)  # Stale cache fallback
        except CacheMiss:
            return {"user_id": user_id, "name": "Unknown", "_fallback": True}
```

## Composition

Chain patterns for defense in depth:

```
Request → Timeout → Bulkhead → Circuit Breaker → Retry → Service Call
```

```python
class ResilientClient:
    def __init__(self):
        self.circuit = CircuitBreaker(failure_threshold=5)
        self.bulkhead = Bulkhead(max_concurrent=10)

    @retry(max_attempts=3, base_delay=0.5)
    async def call(self, url: str) -> dict:
        return await with_timeout(
            self.bulkhead.execute(
                self.circuit.call, self._do_request, url
            ),
            seconds=15
        )

    async def _do_request(self, url: str) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=5)
            response.raise_for_status()
            return response.json()
```

## Queue-Based Load Leveling

```python
import asyncio
from collections import deque

class RateLimiter:
    def __init__(self, rate: int, per: float = 1.0):
        self.rate = rate
        self.per = per
        self.tokens = rate
        self.last_refill = time.time()
        self.lock = asyncio.Lock()

    async def acquire(self):
        async with self.lock:
            now = time.time()
            elapsed = now - self.last_refill
            self.tokens = min(self.rate, self.tokens + elapsed * (self.rate / self.per))
            self.last_refill = now
            if self.tokens >= 1:
                self.tokens -= 1
                return True
            return False
```

## Health Check Patterns

```python
from enum import Enum

class HealthStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"

async def health_check() -> dict:
    checks = {
        "database": check_database(),
        "cache": check_cache(),
        "external_api": check_external_api(),
    }
    results = {}
    for name, check in checks.items():
        try:
            await asyncio.wait_for(check, timeout=5)
            results[name] = HealthStatus.HEALTHY
        except Exception:
            results[name] = HealthStatus.UNHEALTHY

    overall = (
        HealthStatus.HEALTHY if all(v == HealthStatus.HEALTHY for v in results.values())
        else HealthStatus.DEGRADED if any(v == HealthStatus.HEALTHY for v in results.values())
        else HealthStatus.UNHEALTHY
    )
    return {"status": overall.value, "checks": {k: v.value for k, v in results.items()}}
```

## Failure Mode Analysis

| Failure Mode | Pattern | Recovery |
|-------------|---------|----------|
| Transient network error | Retry with backoff | Automatic |
| Service down | Circuit breaker | Automatic after recovery |
| Service overloaded | Bulkhead + rate limit | Shed load |
| Slow response | Timeout | Fail fast |
| Cascade failure | Circuit breaker + bulkhead | Isolate blast radius |
| Data corruption | Idempotent operations | Safe retry |

## Idempotency

```python
async def process_payment(idempotency_key: str, amount: float):
    existing = await db.get_by_idempotency_key(idempotency_key)
    if existing:
        return existing  # Already processed

    result = await payment_gateway.charge(amount)
    await db.store(idempotency_key=idempotency_key, result=result)
    return result
```

## Anti-Patterns

- **Retry without backoff** — Creates thundering herd on recovering services
- **Retry on non-transient errors** — 400 errors will never succeed on retry
- **No timeout** — Hanging requests consume resources indefinitely
- **Cascading retries** — Each layer retrying multiplies total attempts exponentially
- **Circuit breaker too sensitive** — Single failure shouldn't trip the circuit
- **Ignoring partial failures** — Assume any external call can fail
