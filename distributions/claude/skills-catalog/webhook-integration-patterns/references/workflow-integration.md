# Workflow Integration: Webhook Integration Patterns

This document describes how `webhook-integration-patterns` integrates with other skills in the Integration & Authentication ecosystem.

## Related Skills

| Skill | Relationship | When to Invoke |
|-------|--------------|----------------|
| `oauth-flow-architect` | **Upstream** | When webhook signatures use OAuth credentials |
| `mcp-integration-patterns` | **Complementary** | When webhook data feeds into MCP tools |
| `mcp-builder` | **Complementary** | When MCP server exposes webhook data |
| `mcp-server-orchestrator` | **Complementary** | When deploying webhook endpoints |

## Prerequisites

Before invoking `webhook-integration-patterns`, ensure:

1. **Event source identified** - Which service sends webhooks
2. **Payload format known** - JSON, XML, form-encoded
3. **Security requirements clear** - Signature validation, TLS

## Handoff Patterns

### From: oauth-flow-architect

**Trigger:** Webhook subscription requires OAuth authentication.

**What to receive:**
- Access token for subscription API
- Signing key for validation (if OAuth-based)
- Required scopes for webhook management

**Integration points:**
- Subscribe to webhook events using token
- Validate signatures using OAuth-derived keys
- Handle token refresh for long-running subscriptions

### To: mcp-integration-patterns

**Trigger:** Webhook events should be accessible via MCP.

**What to hand off:**
- Event types received
- Processed payload format
- Update frequency

**Expected output from integration:**
- MCP resource definitions for events
- Subscription patterns
- Error handling for missed events

### To: mcp-builder

**Trigger:** Creating MCP server that exposes webhook data.

**What to hand off:**
- Event data structure
- Storage/queuing mechanism
- Query patterns needed

**Expected output from builder:**
- MCP tools for querying events
- Resources for event streams
- Subscription-based updates

### To: mcp-server-orchestrator

**Trigger:** Webhook endpoint needs infrastructure.

**What to hand off:**
- Endpoint path requirements
- Expected traffic volume
- Reliability requirements

**Expected output from orchestrator:**
- Ingress/load balancer configuration
- SSL/TLS termination
- Auto-scaling setup

## Workflow Sequence

```
┌─────────────────────────────────────────────────────────────┐
│                    Webhook Integration                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. OAUTH-FLOW-ARCHITECT: Get API access for subscription  │
│           │                                                 │
│           ▼                                                 │
│  2. WEBHOOK-INTEGRATION-PATTERNS: Design endpoint          │
│           │                                                 │
│           ▼                                                 │
│  3. MCP-SERVER-ORCHESTRATOR: Deploy webhook receiver       │
│           │                                                 │
│           ▼                                                 │
│  4. WEBHOOK-INTEGRATION-PATTERNS: Subscribe to events      │
│           │                                                 │
│           ▼                                                 │
│  5. MCP-BUILDER: Expose events as MCP resources            │
│           │                                                 │
│           ▼                                                 │
│  6. MCP-INTEGRATION-PATTERNS: Connect clients              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Integration Checklist

Before completing webhook integration, verify:

- [ ] Endpoint accepts POST requests
- [ ] Signature validation implemented
- [ ] Replay attack protection (timestamps, nonces)
- [ ] Idempotency handling for duplicate events
- [ ] Quick response (< 5s) with async processing
- [ ] Retry handling for failed deliveries
- [ ] Dead letter queue for unprocessable events
- [ ] Monitoring and alerting configured

## Common Scenarios

### GitHub Webhook Integration

1. **OAuth Flow Architect:** Get GitHub OAuth token
2. **Webhook Integration Patterns:** Create webhook endpoint
3. **MCP Server Orchestrator:** Deploy with HTTPS
4. **MCP Builder:** Create tools for commit/PR data

### Stripe Webhook Integration

1. **Webhook Integration Patterns:** Handle Stripe signatures
2. **MCP Server Orchestrator:** Deploy secure endpoint
3. **MCP Builder:** Expose payment events as resources

### Multi-Provider Event Hub

1. **OAuth Flow Architect:** Auth for each provider
2. **Webhook Integration Patterns:** Normalize event formats
3. **MCP Builder:** Unified event access interface
4. **MCP Integration Patterns:** Real-time subscriptions

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Synchronous processing | Timeouts, missed events | Process async, respond immediately |
| No signature validation | Security vulnerability | Always validate signatures |
| Missing idempotency | Duplicate processing | Track event IDs, deduplicate |
| No retry handling | Lost events | Implement exponential backoff |

## Related Resources

- [Integration & Auth Skills Ecosystem Map](../../../docs/guides/integration-auth-skills-ecosystem.md)
- [Provider Examples](./provider-examples.md)
- [Testing Webhooks](./testing-webhooks.md)
- [Webhook Security](./webhook-security.md)
