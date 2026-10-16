---
name: error-handling-logging-patterns
description: Implement structured logging, error hierarchies, and observability patterns for production systems. Covers structured JSON logging, error classification, correlation IDs, and alerting integration. Triggers on logging architecture, error handling strategy, or observability requests.
license: MIT
complexity: intermediate
time_to_learn: 30min
tags:
  - logging
  - error-handling
  - observability
  - structured-logging
  - monitoring
governance_phases: [build, prove]
organ_affinity: [all]
triggers: [user-asks-about-logging, user-asks-about-error-handling, context:observability, context:debugging, context:monitoring]
complements: [resilience-patterns, backend-implementation-patterns, configuration-management]
---

# Error Handling & Logging Patterns

Build systems that are debuggable in production through structured logging and intentional error handling.

## Error Hierarchy Design

### Custom Exception Classes

```python
class AppError(Exception):
    """Base error for the application."""
    def __init__(self, message: str, code: str = "INTERNAL_ERROR", status: int = 500):
        self.message = message
        self.code = code
        self.status = status
        super().__init__(message)

class NotFoundError(AppError):
    def __init__(self, entity: str, id: str):
        super().__init__(f"{entity} '{id}' not found", code="NOT_FOUND", status=404)

class ValidationError(AppError):
    def __init__(self, field: str, reason: str):
        super().__init__(f"Invalid {field}: {reason}", code="VALIDATION_ERROR", status=400)

class ExternalServiceError(AppError):
    def __init__(self, service: str, detail: str):
        super().__init__(f"{service} error: {detail}", code="EXTERNAL_ERROR", status=502)
```

### Error Classification

| Category | Retry? | Log Level | Alert? |
|----------|--------|-----------|--------|
| Validation error | No | WARNING | No |
| Not found | No | INFO | No |
| Auth failure | No | WARNING | Rate-based |
| Transient external | Yes | WARNING | After retries |
| Persistent external | No | ERROR | Yes |
| Internal bug | No | CRITICAL | Immediate |

## Structured Logging

### Setup with structlog

```python
import structlog
import logging

def configure_logging(log_level: str = "INFO", json_output: bool = True):
    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
    ]

    if json_output:
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer())

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, log_level.upper())
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
    )

log = structlog.get_logger()
```

### Contextual Logging

```python
import structlog
from contextvars import ContextVar

request_id_var: ContextVar[str] = ContextVar("request_id", default="")

# Bind context per request
structlog.contextvars.bind_contextvars(
    request_id=request_id,
    user_id=user.id,
    organ="IV",
)

# All subsequent log calls include this context
log.info("processing_request", path="/api/skills", method="GET")
# Output: {"event": "processing_request", "request_id": "abc-123", "user_id": "u42", "path": "/api/skills", ...}
```

### Log Levels by Purpose

| Level | Purpose | Example |
|-------|---------|---------|
| DEBUG | Detailed flow tracing | Query parameters, cache hits |
| INFO | Business events | User created, skill activated |
| WARNING | Recoverable issues | Retry attempt, deprecated usage |
| ERROR | Failures needing attention | External service down, data inconsistency |
| CRITICAL | System-level failures | Database unreachable, out of memory |

## Request Middleware

### FastAPI Correlation IDs

```python
import uuid
from starlette.middleware.base import BaseHTTPMiddleware

class CorrelationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        structlog.contextvars.bind_contextvars(request_id=request_id)

        log.info("request_started",
            method=request.method,
            path=request.url.path,
        )

        try:
            response = await call_next(request)
            log.info("request_completed",
                status=response.status_code,
            )
            response.headers["X-Request-ID"] = request_id
            return response
        except Exception as e:
            log.error("request_failed", error=str(e), exc_info=True)
            raise
        finally:
            structlog.contextvars.unbind_contextvars("request_id")
```

### Error Response Handler

```python
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    log.warning("app_error", code=exc.code, message=exc.message)
    return JSONResponse(
        status_code=exc.status,
        content={"error": {"code": exc.code, "message": exc.message}},
    )

@app.exception_handler(Exception)
async def unhandled_error_handler(request: Request, exc: Exception):
    log.error("unhandled_error", error=str(exc), exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": {"code": "INTERNAL_ERROR", "message": "An unexpected error occurred"}},
    )
```

## Logging Patterns

### Operation Logging

```python
async def process_skill(skill_id: str):
    log.info("skill_processing_started", skill_id=skill_id)
    try:
        result = await validate_skill(skill_id)
        log.info("skill_processing_completed", skill_id=skill_id, status=result.status)
        return result
    except ValidationError as e:
        log.warning("skill_validation_failed", skill_id=skill_id, error=e.message)
        raise
    except Exception as e:
        log.error("skill_processing_failed", skill_id=skill_id, error=str(e), exc_info=True)
        raise
```

### Sensitive Data Filtering

```python
SENSITIVE_KEYS = {"password", "token", "secret", "api_key", "authorization"}

def sanitize_log_data(data: dict) -> dict:
    return {
        k: "***REDACTED***" if k.lower() in SENSITIVE_KEYS else v
        for k, v in data.items()
    }
```

### Performance Logging

```python
import time
from contextlib import contextmanager

@contextmanager
def log_duration(operation: str, **extra):
    start = time.perf_counter()
    try:
        yield
    finally:
        duration_ms = (time.perf_counter() - start) * 1000
        log.info(f"{operation}_duration", duration_ms=round(duration_ms, 2), **extra)
```

## Log Aggregation Integration

### JSON Format for Ingestion

```json
{
  "timestamp": "2026-03-20T10:58:00Z",
  "level": "info",
  "event": "request_completed",
  "request_id": "abc-123",
  "method": "GET",
  "path": "/api/skills",
  "status": 200,
  "duration_ms": 42.5,
  "service": "a-i--skills",
  "organ": "IV"
}
```

### Common Fields

Always include: `timestamp`, `level`, `event`, `service`, `request_id`. Optionally: `user_id`, `organ`, `duration_ms`, `error`.

## Anti-Patterns

- **Logging PII or secrets** — Always filter sensitive fields before logging
- **String interpolation in log calls** — Use structured fields: `log.info("x", user=id)` not `log.info(f"user {id}")`
- **Catching and silencing exceptions** — Log or re-raise; never `except: pass`
- **Inconsistent log levels** — Define team conventions and stick to them
- **No correlation IDs** — Impossible to trace requests across services without them
- **Logging in tight loops** — Rate-limit or sample high-frequency events
