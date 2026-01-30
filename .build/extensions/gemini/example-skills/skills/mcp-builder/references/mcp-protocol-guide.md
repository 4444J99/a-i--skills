# MCP Protocol Guide

Reference for building Model Context Protocol servers.

## Protocol Overview

MCP (Model Context Protocol) enables AI assistants to interact with external tools and resources through a standardized interface.

```
┌──────────────┐     JSON-RPC      ┌──────────────┐
│   AI Agent   │ ←───────────────→ │  MCP Server  │
│   (Client)   │                   │   (Tools)    │
└──────────────┘                   └──────────────┘
```

## Message Types

### Requests

```typescript
interface Request {
  jsonrpc: "2.0";
  id: string | number;
  method: string;
  params?: object;
}
```

### Responses

```typescript
interface Response {
  jsonrpc: "2.0";
  id: string | number;
  result?: any;
  error?: {
    code: number;
    message: string;
    data?: any;
  };
}
```

### Notifications

```typescript
interface Notification {
  jsonrpc: "2.0";
  method: string;
  params?: object;
}
```

## Core Methods

### Initialize

```typescript
// Request
{
  "method": "initialize",
  "params": {
    "protocolVersion": "0.1.0",
    "capabilities": {
      "tools": {}
    },
    "clientInfo": {
      "name": "Claude",
      "version": "1.0.0"
    }
  }
}

// Response
{
  "protocolVersion": "0.1.0",
  "capabilities": {
    "tools": {}
  },
  "serverInfo": {
    "name": "my-server",
    "version": "1.0.0"
  }
}
```

### List Tools

```typescript
// Request
{ "method": "tools/list" }

// Response
{
  "tools": [
    {
      "name": "search_files",
      "description": "Search for files matching a pattern",
      "inputSchema": {
        "type": "object",
        "properties": {
          "pattern": {
            "type": "string",
            "description": "Glob pattern to match"
          }
        },
        "required": ["pattern"]
      }
    }
  ]
}
```

### Call Tool

```typescript
// Request
{
  "method": "tools/call",
  "params": {
    "name": "search_files",
    "arguments": {
      "pattern": "*.md"
    }
  }
}

// Response
{
  "content": [
    {
      "type": "text",
      "text": "Found 3 files:\n- README.md\n- CHANGELOG.md\n- CONTRIBUTING.md"
    }
  ]
}
```

## Tool Definition

### Schema Format

```typescript
interface Tool {
  name: string;           // Unique identifier
  description: string;    // What the tool does
  inputSchema: {          // JSON Schema for parameters
    type: "object";
    properties: Record<string, {
      type: string;
      description: string;
      enum?: string[];    // For restricted values
    }>;
    required?: string[];
  };
}
```

### Example Tools

```typescript
const tools: Tool[] = [
  {
    name: "read_file",
    description: "Read contents of a file",
    inputSchema: {
      type: "object",
      properties: {
        path: {
          type: "string",
          description: "Path to the file"
        }
      },
      required: ["path"]
    }
  },
  {
    name: "search_code",
    description: "Search for pattern in codebase",
    inputSchema: {
      type: "object",
      properties: {
        query: {
          type: "string",
          description: "Search query"
        },
        fileType: {
          type: "string",
          description: "File extension filter",
          enum: ["ts", "js", "py", "go"]
        }
      },
      required: ["query"]
    }
  }
];
```

## Server Implementation

### TypeScript Template

```typescript
import { Server } from "@modelcontextprotocol/sdk/server";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio";

const server = new Server(
  {
    name: "my-mcp-server",
    version: "1.0.0"
  },
  {
    capabilities: {
      tools: {}
    }
  }
);

// Register tool handlers
server.setRequestHandler("tools/list", async () => ({
  tools: [
    {
      name: "hello",
      description: "Say hello",
      inputSchema: {
        type: "object",
        properties: {
          name: { type: "string" }
        },
        required: ["name"]
      }
    }
  ]
}));

server.setRequestHandler("tools/call", async (request) => {
  const { name, arguments: args } = request.params;

  if (name === "hello") {
    return {
      content: [
        { type: "text", text: `Hello, ${args.name}!` }
      ]
    };
  }

  throw new Error(`Unknown tool: ${name}`);
});

// Start server
const transport = new StdioServerTransport();
server.connect(transport);
```

### Python Template

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

server = Server("my-mcp-server")

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="hello",
            description="Say hello",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"}
                },
                "required": ["name"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "hello":
        return [TextContent(type="text", text=f"Hello, {arguments['name']}!")]
    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with stdio_server() as (read, write):
        await server.run(read, write)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## Error Handling

### Error Codes

| Code | Meaning |
|------|---------|
| -32700 | Parse error |
| -32600 | Invalid request |
| -32601 | Method not found |
| -32602 | Invalid params |
| -32603 | Internal error |

### Error Response

```typescript
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32602,
    "message": "Invalid params",
    "data": {
      "field": "path",
      "reason": "File not found"
    }
  }
}
```

## Best Practices

### Tool Design

1. **Clear names**: Use verb_noun pattern (`read_file`, `search_code`)
2. **Detailed descriptions**: Explain what tool does, when to use it
3. **Minimal parameters**: Only require what's essential
4. **Good defaults**: Provide sensible defaults for optional params
5. **Helpful errors**: Return actionable error messages

### Security

1. **Validate all inputs**: Check paths, sanitize queries
2. **Limit scope**: Restrict file access to allowed directories
3. **Rate limiting**: Prevent abuse
4. **Audit logging**: Log all tool invocations

### Performance

1. **Timeout handlers**: Don't hang indefinitely
2. **Stream large outputs**: For big files or results
3. **Cache when appropriate**: Avoid redundant operations
