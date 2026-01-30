# MCP Protocol Specification

## Protocol Overview

MCP (Model Context Protocol) enables communication between AI assistants and external tools/data sources.

```
┌────────────────┐                    ┌────────────────┐
│    Client      │                    │    Server      │
│ (AI Assistant) │◄──── JSON-RPC ────►│  (Your Tool)   │
└────────────────┘                    └────────────────┘
```

## Message Format

### JSON-RPC 2.0

```json
// Request
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "search",
    "arguments": {"query": "hello"}
  }
}

// Response
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {"type": "text", "text": "Search results..."}
    ]
  }
}

// Error
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32600,
    "message": "Invalid Request"
  }
}
```

## Initialization

### Handshake

```
Client                              Server
   │                                   │
   │──── initialize ──────────────────►│
   │                                   │
   │◄─── initialize result ────────────│
   │                                   │
   │──── initialized (notification) ──►│
   │                                   │
```

### Initialize Request

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {
      "sampling": {}
    },
    "clientInfo": {
      "name": "claude-code",
      "version": "1.0.0"
    }
  }
}
```

### Initialize Response

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2024-11-05",
    "capabilities": {
      "tools": {},
      "resources": {},
      "prompts": {}
    },
    "serverInfo": {
      "name": "my-server",
      "version": "1.0.0"
    }
  }
}
```

## Tools

### List Tools

```json
// Request
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/list"
}

// Response
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "tools": [
      {
        "name": "search_documents",
        "description": "Search internal documents",
        "inputSchema": {
          "type": "object",
          "properties": {
            "query": {
              "type": "string",
              "description": "Search query"
            }
          },
          "required": ["query"]
        }
      }
    ]
  }
}
```

### Call Tool

```json
// Request
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "search_documents",
    "arguments": {
      "query": "quarterly report"
    }
  }
}

// Response
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Found 3 documents matching 'quarterly report'..."
      }
    ],
    "isError": false
  }
}
```

## Resources

### List Resources

```json
// Request
{
  "jsonrpc": "2.0",
  "id": 4,
  "method": "resources/list"
}

// Response
{
  "jsonrpc": "2.0",
  "id": 4,
  "result": {
    "resources": [
      {
        "uri": "file:///config/settings.json",
        "name": "Application Settings",
        "mimeType": "application/json"
      }
    ]
  }
}
```

### Read Resource

```json
// Request
{
  "jsonrpc": "2.0",
  "id": 5,
  "method": "resources/read",
  "params": {
    "uri": "file:///config/settings.json"
  }
}

// Response
{
  "jsonrpc": "2.0",
  "id": 5,
  "result": {
    "contents": [
      {
        "uri": "file:///config/settings.json",
        "mimeType": "application/json",
        "text": "{\"debug\": true}"
      }
    ]
  }
}
```

### Resource Templates

```json
{
  "resourceTemplates": [
    {
      "uriTemplate": "db://tables/{table_name}/schema",
      "name": "Table Schema",
      "description": "Database table schema"
    }
  ]
}
```

## Prompts

### List Prompts

```json
// Request
{
  "jsonrpc": "2.0",
  "id": 6,
  "method": "prompts/list"
}

// Response
{
  "jsonrpc": "2.0",
  "id": 6,
  "result": {
    "prompts": [
      {
        "name": "code_review",
        "description": "Review code for issues",
        "arguments": [
          {
            "name": "code",
            "description": "Code to review",
            "required": true
          }
        ]
      }
    ]
  }
}
```

### Get Prompt

```json
// Request
{
  "jsonrpc": "2.0",
  "id": 7,
  "method": "prompts/get",
  "params": {
    "name": "code_review",
    "arguments": {
      "code": "function add(a, b) { return a + b; }"
    }
  }
}

// Response
{
  "jsonrpc": "2.0",
  "id": 7,
  "result": {
    "description": "Code review prompt",
    "messages": [
      {
        "role": "user",
        "content": {
          "type": "text",
          "text": "Please review this code: function add(a, b) { return a + b; }"
        }
      }
    ]
  }
}
```

## Error Codes

| Code | Name | Description |
|------|------|-------------|
| -32700 | Parse Error | Invalid JSON |
| -32600 | Invalid Request | Not valid JSON-RPC |
| -32601 | Method Not Found | Unknown method |
| -32602 | Invalid Params | Invalid method parameters |
| -32603 | Internal Error | Server error |

## Content Types

### Text Content

```json
{
  "type": "text",
  "text": "Hello, world!"
}
```

### Image Content

```json
{
  "type": "image",
  "data": "base64-encoded-image-data",
  "mimeType": "image/png"
}
```

### Resource Content

```json
{
  "type": "resource",
  "resource": {
    "uri": "file:///path/to/file",
    "text": "File contents",
    "mimeType": "text/plain"
  }
}
```
