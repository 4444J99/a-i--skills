# MCP Server Implementation Examples

## Database Server

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, Resource
import asyncpg

server = Server("database-server")

# Connection pool
pool = None

async def get_pool():
    global pool
    if pool is None:
        pool = await asyncpg.create_pool(
            host='localhost',
            database='mydb',
            user='user',
            password='password'  # allow-secret
        )
    return pool

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="query",
            description="Execute a SELECT query",
            inputSchema={
                "type": "object",
                "properties": {
                    "sql": {
                        "type": "string",
                        "description": "SELECT SQL query"
                    }
                },
                "required": ["sql"]
            }
        ),
        Tool(
            name="list_tables",
            description="List all tables in database",
            inputSchema={"type": "object", "properties": {}}
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    pool = await get_pool()

    if name == "query":
        sql = arguments["sql"]

        # Safety: only allow SELECT
        if not sql.strip().upper().startswith("SELECT"):
            return [TextContent(
                type="text",
                text="Error: Only SELECT queries allowed"
            )]

        async with pool.acquire() as conn:
            rows = await conn.fetch(sql)

            # Format results
            if not rows:
                return [TextContent(type="text", text="No results")]

            headers = list(rows[0].keys())
            result = " | ".join(headers) + "\n"
            result += "-" * (len(result) - 1) + "\n"
            for row in rows[:100]:  # Limit results
                result += " | ".join(str(row[h]) for h in headers) + "\n"

            return [TextContent(type="text", text=result)]

    elif name == "list_tables":
        async with pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
            """)
            tables = [row['table_name'] for row in rows]
            return [TextContent(
                type="text",
                text="Tables:\n" + "\n".join(f"- {t}" for t in tables)
            )]

@server.list_resources()
async def list_resources():
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
        """)

    return [
        Resource(
            uri=f"db://tables/{row['table_name']}/schema",
            name=f"{row['table_name']} Schema",
            mimeType="text/plain"
        )
        for row in rows
    ]

@server.read_resource()
async def read_resource(uri: str):
    if uri.startswith("db://tables/") and uri.endswith("/schema"):
        table_name = uri.replace("db://tables/", "").replace("/schema", "")

        pool = await get_pool()
        async with pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = $1
            """, table_name)

        schema = f"Table: {table_name}\n\n"
        schema += "Columns:\n"
        for row in rows:
            nullable = "NULL" if row['is_nullable'] == 'YES' else "NOT NULL"
            schema += f"  {row['column_name']}: {row['data_type']} {nullable}\n"

        return schema

async def main():
    async with stdio_server() as (read, write):
        await server.run(read, write)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## File System Server

```python
from mcp.server import Server
from mcp.types import Tool, TextContent, Resource
from pathlib import Path

server = Server("filesystem-server")

# Allowed directories (security)
ALLOWED_PATHS = [Path.home() / "Documents", Path.home() / "Projects"]

def validate_path(path_str: str) -> Path:
    path = Path(path_str).resolve()
    for allowed in ALLOWED_PATHS:
        try:
            path.relative_to(allowed)
            return path
        except ValueError:
            continue
    raise PermissionError(f"Access denied: {path_str}")

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="read_file",
            description="Read a file's contents",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path"}
                },
                "required": ["path"]
            }
        ),
        Tool(
            name="write_file",
            description="Write content to a file",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "content": {"type": "string"}
                },
                "required": ["path", "content"]
            }
        ),
        Tool(
            name="list_directory",
            description="List files in directory",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string"}
                },
                "required": ["path"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    try:
        if name == "read_file":
            path = validate_path(arguments["path"])
            content = path.read_text()
            return [TextContent(type="text", text=content)]

        elif name == "write_file":
            path = validate_path(arguments["path"])
            path.write_text(arguments["content"])
            return [TextContent(type="text", text=f"Written to {path}")]

        elif name == "list_directory":
            path = validate_path(arguments["path"])
            if not path.is_dir():
                return [TextContent(type="text", text="Not a directory")]

            items = []
            for item in sorted(path.iterdir()):
                prefix = "📁" if item.is_dir() else "📄"
                items.append(f"{prefix} {item.name}")

            return [TextContent(type="text", text="\n".join(items))]

    except PermissionError as e:
        return [TextContent(type="text", text=f"Permission denied: {e}")]
    except FileNotFoundError:
        return [TextContent(type="text", text="File not found")]
```

## API Integration Server

```python
import httpx
from mcp.server import Server
from mcp.types import Tool, TextContent

server = Server("api-server")

API_BASE = "https://api.example.com"
API_KEY = os.environ.get("API_KEY")  # allow-secret

client = httpx.AsyncClient(
    base_url=API_BASE,
    headers={"Authorization": f"Bearer {API_KEY}"}
)

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="get_user",
            description="Get user by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"}
                },
                "required": ["user_id"]
            }
        ),
        Tool(
            name="search_users",
            description="Search for users",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "limit": {"type": "integer", "default": 10}
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="create_task",
            description="Create a new task",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                    "assignee_id": {"type": "string"}
                },
                "required": ["title"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    try:
        if name == "get_user":
            response = await client.get(f"/users/{arguments['user_id']}")
            response.raise_for_status()
            user = response.json()
            return [TextContent(
                type="text",
                text=f"User: {user['name']}\nEmail: {user['email']}"
            )]

        elif name == "search_users":
            response = await client.get("/users/search", params={
                "q": arguments["query"],
                "limit": arguments.get("limit", 10)
            })
            response.raise_for_status()
            users = response.json()["users"]

            result = f"Found {len(users)} users:\n"
            for u in users:
                result += f"- {u['name']} ({u['email']})\n"

            return [TextContent(type="text", text=result)]

        elif name == "create_task":
            response = await client.post("/tasks", json={
                "title": arguments["title"],
                "description": arguments.get("description", ""),
                "assignee_id": arguments.get("assignee_id")
            })
            response.raise_for_status()
            task = response.json()

            return [TextContent(
                type="text",
                text=f"Created task #{task['id']}: {task['title']}"
            )]

    except httpx.HTTPStatusError as e:
        return [TextContent(
            type="text",
            text=f"API Error: {e.response.status_code}"
        )]
```

## Combined Server Template

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server

# Create server with all capabilities
server = Server(
    "combined-server",
    version="1.0.0"
)

# Register tools
@server.list_tools()
async def list_tools():
    return [...]

@server.call_tool()
async def call_tool(name, arguments):
    return [...]

# Register resources
@server.list_resources()
async def list_resources():
    return [...]

@server.read_resource()
async def read_resource(uri):
    return ...

# Register prompts
@server.list_prompts()
async def list_prompts():
    return [...]

@server.get_prompt()
async def get_prompt(name, arguments):
    return {...}

# Main entry point
async def main():
    async with stdio_server() as (read, write):
        await server.run(read, write)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```
