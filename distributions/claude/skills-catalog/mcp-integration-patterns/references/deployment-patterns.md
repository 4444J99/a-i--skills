# MCP Server Deployment Patterns

## Local Development

### stdio Transport (Default)

Configure in Claude Desktop:

```json
// ~/Library/Application Support/Claude/claude_desktop_config.json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["-m", "my_mcp_server"],
      "env": {
        "DATABASE_URL": "postgresql://localhost/mydb"
      }
    }
  }
}
```

### Using uv (Python)

```json
{
  "mcpServers": {
    "my-server": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/server", "python", "-m", "my_server"]
    }
  }
}
```

### Using npx (Node.js)

```json
{
  "mcpServers": {
    "my-server": {
      "command": "npx",
      "args": ["-y", "@myorg/my-mcp-server"]
    }
  }
}
```

## Remote Deployment

### HTTP/SSE Transport

```python
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

sse = SseServerTransport("/messages")

async def handle_sse(request):
    async with sse.connect_sse(
        request.scope, request.receive, request._send
    ) as streams:
        await server.run(streams[0], streams[1])

app = Starlette(
    routes=[
        Route("/sse", endpoint=handle_sse),
        Route("/messages", endpoint=sse.handle_post_message, methods=["POST"])
    ],
    middleware=[
        Middleware(CORSMiddleware, allow_origins=["*"])
    ]
)

# Run with: uvicorn main:app --host 0.0.0.0 --port 8000
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-m", "my_mcp_server"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  mcp-server:
    build: .
    environment:
      - DATABASE_URL=postgresql://db/mydb
      - API_KEY=${API_KEY}
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=mydb
```

## Security

### Environment Variables

Never hardcode secrets:

```python
import os

API_KEY = os.environ.get("API_KEY")  # allow-secret
if not API_KEY:
    raise ValueError("API_KEY environment variable required")

DATABASE_URL = os.environ.get("DATABASE_URL")
```

### Input Validation

```python
from pydantic import BaseModel, validator

class QueryInput(BaseModel):
    sql: str
    limit: int = 100

    @validator('sql')
    def validate_sql(cls, v):
        dangerous = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'TRUNCATE']
        v_upper = v.upper()
        for d in dangerous:
            if d in v_upper:
                raise ValueError(f"Dangerous operation: {d}")
        return v

    @validator('limit')
    def validate_limit(cls, v):
        if v < 1 or v > 1000:
            raise ValueError("Limit must be 1-1000")
        return v

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "query":
        validated = QueryInput(**arguments)
        # Use validated.sql, validated.limit
```

### Rate Limiting

```python
from datetime import datetime, timedelta
from collections import defaultdict

class RateLimiter:
    def __init__(self, max_requests=100, window_seconds=60):
        self.max_requests = max_requests
        self.window = timedelta(seconds=window_seconds)
        self.requests = defaultdict(list)

    def check(self, client_id: str = "default"):
        now = datetime.now()
        cutoff = now - self.window

        # Clean old requests
        self.requests[client_id] = [
            t for t in self.requests[client_id] if t > cutoff
        ]

        if len(self.requests[client_id]) >= self.max_requests:
            raise RateLimitError("Too many requests")

        self.requests[client_id].append(now)

rate_limiter = RateLimiter()

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    rate_limiter.check()
    # ... process
```

## Logging & Monitoring

### Structured Logging

```python
import logging
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module
        }
        if hasattr(record, 'tool_name'):
            log_data['tool'] = record.tool_name
        if hasattr(record, 'duration_ms'):
            log_data['duration_ms'] = record.duration_ms
        return json.dumps(log_data)

handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger = logging.getLogger("mcp")
logger.addHandler(handler)
logger.setLevel(logging.INFO)

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    start = time.time()
    try:
        result = await process_tool(name, arguments)
        duration = (time.time() - start) * 1000
        logger.info("Tool call completed",
                    extra={'tool_name': name, 'duration_ms': duration})
        return result
    except Exception as e:
        logger.error(f"Tool call failed: {e}",
                     extra={'tool_name': name})
        raise
```

### Health Check Endpoint

```python
from starlette.responses import JSONResponse

async def health_check(request):
    checks = {
        "database": await check_database(),
        "api": await check_external_api()
    }
    all_healthy = all(checks.values())
    return JSONResponse(
        {"status": "healthy" if all_healthy else "unhealthy", "checks": checks},
        status_code=200 if all_healthy else 503
    )

app = Starlette(routes=[
    Route("/health", endpoint=health_check),
    # ... other routes
])
```

## Testing

### Unit Tests

```python
import pytest
from mcp.client import Client

@pytest.fixture
async def mcp_client():
    # Start server in subprocess
    process = await asyncio.create_subprocess_exec(
        "python", "-m", "my_mcp_server",
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE
    )

    client = Client()
    await client.connect(process.stdout, process.stdin)
    yield client

    process.terminate()

@pytest.mark.asyncio
async def test_list_tools(mcp_client):
    tools = await mcp_client.list_tools()
    assert len(tools) > 0
    assert any(t.name == "query" for t in tools)

@pytest.mark.asyncio
async def test_call_tool(mcp_client):
    result = await mcp_client.call_tool("query", {"sql": "SELECT 1"})
    assert not result.isError
    assert result.content
```

### Integration Tests

```python
@pytest.mark.integration
async def test_database_query():
    """Test actual database query"""
    result = await call_tool("query", {"sql": "SELECT * FROM users LIMIT 1"})
    assert "user" in result.content[0].text.lower()
```

## Configuration

### Config File

```yaml
# config.yaml
server:
  name: my-mcp-server
  version: 1.0.0

database:
  url: ${DATABASE_URL}
  pool_size: 10

security:
  allowed_tables:
    - users
    - orders
  rate_limit:
    requests: 100
    window_seconds: 60

logging:
  level: INFO
  format: json
```

```python
import yaml
import os

def load_config():
    with open("config.yaml") as f:
        config = yaml.safe_load(f)

    # Expand environment variables
    def expand_vars(obj):
        if isinstance(obj, str):
            return os.path.expandvars(obj)
        elif isinstance(obj, dict):
            return {k: expand_vars(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [expand_vars(v) for v in obj]
        return obj

    return expand_vars(config)
```
