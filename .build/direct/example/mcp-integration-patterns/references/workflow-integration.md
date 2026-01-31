# Workflow Integration: MCP Integration Patterns

This document describes how `mcp-integration-patterns` integrates with other skills in the Integration & Authentication ecosystem.

## Related Skills

| Skill | Relationship | When to Invoke |
|-------|--------------|----------------|
| `mcp-builder` | **Upstream** | When you need to build a new MCP server |
| `mcp-server-orchestrator` | **Upstream** | For deployment configuration guidance |
| `oauth-flow-architect` | **Complementary** | When MCP connections need authentication |
| `webhook-integration-patterns` | **Complementary** | When receiving external events via MCP |

## Prerequisites

Before invoking `mcp-integration-patterns`, ensure:

1. **MCP server exists** - Either built or third-party server available
2. **Transport method decided** - stdio, SSE, or custom transport
3. **Client environment known** - Claude Desktop, API, or custom client

## Handoff Patterns

### From: mcp-builder

**Trigger:** Server is built and needs client integration.

**What to receive:**
- Server tool and resource definitions
- Transport configuration requirements
- Authentication method if any

**Integration points:**
- Map server capabilities to client configuration
- Configure error handling for each tool
- Set up proper timeout handling

### From: mcp-server-orchestrator

**Trigger:** Server is deployed and ready for connections.

**What to receive:**
- Server URL/endpoint
- Health check endpoints
- Environment-specific configuration

**Integration points:**
- Configure client connection strings
- Set up reconnection logic
- Enable monitoring integration

### To: oauth-flow-architect

**Trigger:** MCP transport needs authenticated access.

**What to hand off:**
- Required scopes for MCP operations
- Token storage requirements
- Refresh timing needs

**Expected output from oauth:**
- Token acquisition flow
- Middleware for request signing
- Refresh automation

### To: webhook-integration-patterns

**Trigger:** MCP server needs to receive external events.

**What to hand off:**
- Event types to receive
- Payload format expectations
- Processing requirements

**Expected output from webhooks:**
- Endpoint configuration
- Signature validation setup
- Event routing logic

## Workflow Sequence

```
┌─────────────────────────────────────────────────────────────┐
│                    MCP Client Integration                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. MCP-BUILDER: Create server with tools/resources        │
│           │                                                 │
│           ▼                                                 │
│  2. MCP-SERVER-ORCHESTRATOR: Deploy to infrastructure      │
│           │                                                 │
│           ▼                                                 │
│  3. MCP-INTEGRATION-PATTERNS: Configure client connection  │
│           │                                                 │
│           ├──────────────────────────────────────┐          │
│           ▼                                      ▼          │
│  4a. OAUTH-FLOW-ARCHITECT      4b. WEBHOOK-INTEGRATION     │
│      (if auth needed)              (if events needed)      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Integration Checklist

Before completing MCP integration, verify:

- [ ] Transport method configured (stdio/SSE/custom)
- [ ] Connection string properly formatted
- [ ] Error handling covers all tool failures
- [ ] Timeout values appropriate for operations
- [ ] Reconnection logic tested
- [ ] Authentication integrated if required
- [ ] Health checks passing
- [ ] Client can list tools/resources

## Common Scenarios

### Claude Desktop Integration

1. **MCP Integration Patterns:** Configure claude_desktop_config.json
2. **MCP Builder:** Ensure server follows stdio transport
3. **OAuth Flow Architect:** Add credential handling if needed

### API-Based Integration

1. **MCP Server Orchestrator:** Deploy with SSE transport
2. **MCP Integration Patterns:** Configure HTTP client
3. **OAuth Flow Architect:** Implement bearer token flow

### Custom Client Integration

1. **MCP Integration Patterns:** Define protocol handling
2. **MCP Builder:** Expose server capabilities
3. **Webhook Integration:** Add event streaming if needed

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Hardcoded URLs | Breaks across environments | Use configuration files |
| No error handling | Silent failures | Implement comprehensive error catching |
| Missing reconnection | Dropped connections stay dropped | Add exponential backoff reconnection |
| Ignored timeouts | Hung operations | Set appropriate timeout values |

## Related Resources

- [Integration & Auth Skills Ecosystem Map](../../../docs/guides/integration-auth-skills-ecosystem.md)
- [MCP Specification Reference](./mcp-specification.md)
- [Deployment Patterns](./deployment-patterns.md)
