# MCP Server Templates

## Python Server with FastMCP

```python
#!/usr/bin/env python3
"""
MCP Server Template - FastMCP
Install: pip install fastmcp
Run: python server.py or uvx --from . server
"""

from fastmcp import FastMCP
from typing import Optional
import os

# Initialize server
mcp = FastMCP(
    name="my-server",
    version="1.0.0",
    description="Description of what this server provides"
)

# === TOOLS ===

@mcp.tool()
def simple_tool(input_text: str) -> str:
    """
    Brief description of what this tool does.
    
    Args:
        input_text: Description of the parameter
    
    Returns:
        Description of the return value
    """
    return f"Processed: {input_text}"


@mcp.tool()
def tool_with_options(
    required_param: str,
    optional_param: Optional[str] = None,
    flag: bool = False
) -> dict:
    """
    Tool with multiple parameter types.
    
    Args:
        required_param: This parameter is required
        optional_param: This parameter is optional
        flag: Boolean flag for behavior toggle
    """
    result = {"input": required_param, "flag": flag}
    if optional_param:
        result["optional"] = optional_param
    return result


# === RESOURCES ===

@mcp.resource("config://settings")
def get_settings() -> str:
    """Provide server configuration as a resource."""
    return "key=value\nother_key=other_value"


@mcp.resource("data://items/{item_id}")
def get_item(item_id: str) -> str:
    """Dynamic resource with URI parameter."""
    return f"Data for item: {item_id}"


# === PROMPTS ===

@mcp.prompt()
def analysis_prompt(topic: str) -> str:
    """Generate an analysis prompt for the given topic."""
    return f"""Please analyze the following topic thoroughly:

Topic: {topic}

Consider:
1. Key aspects and components
2. Relationships and dependencies
3. Potential improvements or issues
4. Recommendations"""


# === MAIN ===

if __name__ == "__main__":
    # Run with stdio transport (default for Claude integration)
    mcp.run()
```

## Node/TypeScript Server with MCP SDK

```typescript
#!/usr/bin/env node
/**
 * MCP Server Template - TypeScript SDK
 * Install: npm install @modelcontextprotocol/sdk
 * Run: npx ts-node server.ts or compile and run
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  ListResourcesRequestSchema,
  ReadResourceRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

// Initialize server
const server = new Server(
  {
    name: "my-server",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
      resources: {},
    },
  }
);

// === TOOL HANDLERS ===

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "simple_tool",
      description: "Brief description of what this tool does",
      inputSchema: {
        type: "object",
        properties: {
          input_text: {
            type: "string",
            description: "Description of the parameter",
          },
        },
        required: ["input_text"],
      },
    },
    {
      name: "tool_with_options",
      description: "Tool with multiple parameter types",
      inputSchema: {
        type: "object",
        properties: {
          required_param: { type: "string" },
          optional_param: { type: "string" },
          flag: { type: "boolean", default: false },
        },
        required: ["required_param"],
      },
    },
  ],
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  switch (name) {
    case "simple_tool":
      return {
        content: [
          { type: "text", text: `Processed: ${args?.input_text}` },
        ],
      };

    case "tool_with_options":
      const result = {
        input: args?.required_param,
        flag: args?.flag ?? false,
        ...(args?.optional_param && { optional: args.optional_param }),
      };
      return {
        content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
      };

    default:
      throw new Error(`Unknown tool: ${name}`);
  }
});

// === RESOURCE HANDLERS ===

server.setRequestHandler(ListResourcesRequestSchema, async () => ({
  resources: [
    {
      uri: "config://settings",
      name: "Server Settings",
      mimeType: "text/plain",
    },
  ],
}));

server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const { uri } = request.params;

  if (uri === "config://settings") {
    return {
      contents: [
        {
          uri,
          mimeType: "text/plain",
          text: "key=value\nother_key=other_value",
        },
      ],
    };
  }

  throw new Error(`Unknown resource: ${uri}`);
});

// === MAIN ===

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("MCP server running on stdio");
}

main().catch(console.error);
```

## Configuration Examples

### Claude Desktop - Multiple Servers

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/me/projects"],
      "disabled": false
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_..."
      }
    },
    "custom": {
      "command": "/usr/local/bin/python3",
      "args": ["-m", "my_custom_server"],
      "env": {
        "API_KEY": "sk-...",
        "DEBUG": "false"
      }
    }
  }
}
```

### pyproject.toml for Python Server

```toml
[project]
name = "my-mcp-server"
version = "0.1.0"
description = "Custom MCP server"
requires-python = ">=3.10"
dependencies = [
    "fastmcp>=0.1.0",
]

[project.scripts]
my-server = "my_server:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

### package.json for Node Server

```json
{
  "name": "my-mcp-server",
  "version": "1.0.0",
  "type": "module",
  "bin": {
    "my-server": "./dist/server.js"
  },
  "scripts": {
    "build": "tsc",
    "start": "node dist/server.js"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.0.0"
  },
  "devDependencies": {
    "typescript": "^5.0.0"
  }
}
```
