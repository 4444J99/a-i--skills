# Workflow Integration: MCP Builder

This document describes how `mcp-builder` integrates with other skills in the Integration & Authentication ecosystem.

## Related Skills

| Skill | Relationship | When to Invoke |
|-------|--------------|----------------|
| `mcp-server-orchestrator` | **Downstream** | After server is built, deploy to infrastructure |
| `mcp-integration-patterns` | **Downstream** | Configure client connections to your server |
| `oauth-flow-architect` | **Complementary** | When tools need authenticated API access |
| `webhook-integration-patterns` | **Complementary** | When tools should receive external events |

## Prerequisites

Before invoking `mcp-builder`, ensure:

1. **Use case defined** - What tools/resources the server will expose
2. **Language chosen** - TypeScript, Python, or other MCP SDK
3. **Transport decided** - stdio for local, SSE for remote

## Handoff Patterns

### To: mcp-server-orchestrator

**Trigger:** Server code is complete and tested locally.

**What to hand off:**
- Complete server codebase
- Environment variable requirements
- Health check endpoint (if any)
- Resource requirements (memory, CPU)

**Expected output from orchestrator:**
- Deployment configuration
- Container/service definition
- Monitoring setup

### To: mcp-integration-patterns

**Trigger:** Server needs to be connected to clients.

**What to hand off:**
- Tool and resource definitions
- Transport method used
- Any authentication requirements

**Expected output from integration:**
- Client configuration files
- Error handling patterns
- Reconnection logic

### To: oauth-flow-architect

**Trigger:** Server tools need to call authenticated external APIs.

**What to hand off:**
- APIs that require OAuth
- Required scopes
- Token storage location preference

**Expected output from oauth:**
- Token management code
- Refresh logic
- Secure storage pattern

### To: webhook-integration-patterns

**Trigger:** Server needs to expose webhook endpoints or receive events.

**What to hand off:**
- Event types to handle
- Payload processing requirements
- Response expectations

**Expected output from webhooks:**
- Endpoint handlers
- Signature validation
- Event queuing pattern

## Workflow Sequence

```
┌─────────────────────────────────────────────────────────────┐
│                    MCP Server Development                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. MCP-BUILDER: Define tools and resources                │
│           │                                                 │
│           ├──────────────────────────────────────┐          │
│           ▼                                      ▼          │
│  2a. OAUTH-FLOW-ARCHITECT      2b. WEBHOOK-INTEGRATION     │
│      (for authenticated APIs)      (for event reception)   │
│           │                                      │          │
│           └──────────────────────────────────────┘          │
│                          │                                  │
│                          ▼                                  │
│  3. MCP-SERVER-ORCHESTRATOR: Deploy server                 │
│           │                                                 │
│           ▼                                                 │
│  4. MCP-INTEGRATION-PATTERNS: Connect clients              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Integration Checklist

Before handing off to deployment, verify:

- [ ] All tools properly typed with input schemas
- [ ] Resources have appropriate URIs
- [ ] Error handling returns proper MCP error codes
- [ ] Local testing passes with MCP inspector
- [ ] Environment variables documented
- [ ] Dependencies declared in package.json/requirements.txt
- [ ] README includes usage examples

## Common Scenarios

### Simple Tool Server

1. **MCP Builder:** Create tools with input validation
2. **MCP Server Orchestrator:** Deploy locally or containerized
3. **MCP Integration Patterns:** Configure Claude Desktop

### API Wrapper Server

1. **MCP Builder:** Define tools wrapping API endpoints
2. **OAuth Flow Architect:** Handle API authentication
3. **MCP Server Orchestrator:** Deploy with secrets management
4. **MCP Integration Patterns:** Configure client access

### Event-Driven Server

1. **MCP Builder:** Create resource subscriptions
2. **Webhook Integration Patterns:** Receive external events
3. **MCP Server Orchestrator:** Deploy with event handling
4. **MCP Integration Patterns:** Enable subscription in clients

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Untyped inputs | Runtime errors, poor UX | Define JSON schemas for all tools |
| Blocking operations | Timeouts, hangs | Use async patterns, add timeouts |
| Secrets in code | Security risk | Use environment variables |
| No error codes | Unhelpful error messages | Return proper MCP error objects |

## Related Resources

- [Integration & Auth Skills Ecosystem Map](../../../docs/guides/integration-auth-skills-ecosystem.md)
- [MCP Protocol Guide](./mcp-protocol-guide.md)
