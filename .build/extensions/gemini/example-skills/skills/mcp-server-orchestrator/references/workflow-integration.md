# Workflow Integration: MCP Server Orchestrator

This document describes how `mcp-server-orchestrator` integrates with other skills in the Integration & Authentication ecosystem.

## Related Skills

| Skill | Relationship | When to Invoke |
|-------|--------------|----------------|
| `mcp-builder` | **Upstream** | Receive server code for deployment |
| `mcp-integration-patterns` | **Downstream** | After deployment, configure client connections |
| `oauth-flow-architect` | **Complementary** | Configure authentication in deployment |
| `webhook-integration-patterns` | **Complementary** | Set up webhook endpoints in infrastructure |

## Prerequisites

Before invoking `mcp-server-orchestrator`, ensure:

1. **Server code ready** - Built and tested MCP server
2. **Infrastructure access** - Docker, cloud platform, or local environment
3. **Configuration documented** - Environment variables, secrets

## Handoff Patterns

### From: mcp-builder

**Trigger:** Server development is complete.

**What to receive:**
- Server codebase
- Dockerfile or build configuration
- Environment variable list
- Resource requirements

**Integration points:**
- Package server for deployment
- Configure environment
- Set up health checks

### To: mcp-integration-patterns

**Trigger:** Server is deployed and running.

**What to hand off:**
- Server URL/endpoint
- Transport configuration
- Authentication details if any
- Available tools/resources list

**Expected output from integration:**
- Client configuration
- Connection testing results
- Error handling setup

### To: oauth-flow-architect

**Trigger:** Deployment needs OAuth credential management.

**What to hand off:**
- Credential requirements
- Secret storage preferences
- Token refresh scheduling needs

**Expected output from oauth:**
- Secrets management configuration
- Token refresh automation
- Secure credential injection

### To: webhook-integration-patterns

**Trigger:** Deployment needs to receive external webhooks.

**What to hand off:**
- Endpoint requirements
- Load balancing needs
- SSL/TLS requirements

**Expected output from webhooks:**
- Ingress configuration
- Endpoint routing
- Rate limiting setup

## Workflow Sequence

```
┌─────────────────────────────────────────────────────────────┐
│                    MCP Server Deployment                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. MCP-BUILDER: Server code complete                      │
│           │                                                 │
│           ▼                                                 │
│  2. MCP-SERVER-ORCHESTRATOR: Package and configure         │
│           │                                                 │
│           ├──────────────────────────────────────┐          │
│           ▼                                      ▼          │
│  3a. OAUTH-FLOW-ARCHITECT      3b. WEBHOOK-INTEGRATION     │
│      (secrets management)          (ingress setup)         │
│           │                                      │          │
│           └──────────────────────────────────────┘          │
│                          │                                  │
│                          ▼                                  │
│  4. MCP-SERVER-ORCHESTRATOR: Deploy to infrastructure      │
│           │                                                 │
│           ▼                                                 │
│  5. MCP-INTEGRATION-PATTERNS: Configure clients            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Integration Checklist

Before completing deployment, verify:

- [ ] Container image built successfully
- [ ] Environment variables injected securely
- [ ] Health checks configured and passing
- [ ] Logging and monitoring enabled
- [ ] Resource limits set appropriately
- [ ] SSL/TLS configured for remote access
- [ ] Secrets stored in secure vault
- [ ] Scaling policy defined

## Common Scenarios

### Local Docker Deployment

1. **MCP Builder:** Provide Dockerfile and compose file
2. **MCP Server Orchestrator:** Configure docker-compose
3. **MCP Integration Patterns:** Connect via localhost

### Cloud Platform Deployment

1. **MCP Builder:** Provide containerized server
2. **OAuth Flow Architect:** Configure secrets management
3. **MCP Server Orchestrator:** Deploy to cloud (GCP, AWS, Azure)
4. **MCP Integration Patterns:** Configure remote access

### Kubernetes Deployment

1. **MCP Builder:** Provide container image
2. **MCP Server Orchestrator:** Create deployment manifests
3. **Webhook Integration:** Configure ingress
4. **MCP Integration Patterns:** Connect via service URL

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Secrets in image | Security vulnerability | Use external secrets manager |
| No health checks | Silent failures | Implement liveness/readiness probes |
| Missing resource limits | Resource exhaustion | Set CPU/memory limits |
| No logging | Debugging impossible | Configure structured logging |

## Related Resources

- [Integration & Auth Skills Ecosystem Map](../../../docs/guides/integration-auth-skills-ecosystem.md)
- [Debugging Guide](./debugging-guide.md)
- [Server Templates](./server-templates.md)
