# Workflow Integration: OAuth Flow Architect

This document describes how `oauth-flow-architect` integrates with other skills in the Integration & Authentication ecosystem.

## Related Skills

| Skill | Relationship | When to Invoke |
|-------|--------------|----------------|
| `mcp-builder` | **Upstream** | When building MCP servers that need OAuth |
| `mcp-integration-patterns` | **Complementary** | Securing MCP client connections |
| `mcp-server-orchestrator` | **Complementary** | Configuring auth in deployment |
| `webhook-integration-patterns` | **Complementary** | Validating webhook signatures |

## Prerequisites

Before invoking `oauth-flow-architect`, ensure:

1. **Provider identified** - OAuth provider (Google, GitHub, custom OIDC)
2. **Scopes defined** - What permissions the app needs
3. **Flow type known** - Authorization Code, Client Credentials, etc.

## Handoff Patterns

### From: mcp-builder

**Trigger:** MCP server tools need authenticated API access.

**What to receive:**
- APIs that require OAuth
- Required permission scopes
- User vs. service context needs

**Integration points:**
- Design appropriate OAuth flow
- Implement token management
- Add refresh logic

### To: mcp-integration-patterns

**Trigger:** MCP client connections need authentication.

**What to hand off:**
- Token acquisition method
- Header/transport authentication format
- Refresh handling approach

**Expected output from integration:**
- Authenticated client configuration
- Token injection middleware
- Error handling for auth failures

### To: mcp-server-orchestrator

**Trigger:** Deployment needs credential management.

**What to hand off:**
- Client ID/secret requirements
- Token storage needs
- Refresh scheduling requirements

**Expected output from orchestrator:**
- Secrets management configuration
- Environment variable setup
- Secure credential injection

### To: webhook-integration-patterns

**Trigger:** Webhooks need signature validation using OAuth credentials.

**What to hand off:**
- Signing key or secret
- Signature algorithm
- Validation requirements

**Expected output from webhooks:**
- Signature validation middleware
- Key rotation handling
- Validation error responses

## Workflow Sequence

```
┌─────────────────────────────────────────────────────────────┐
│                    OAuth Implementation                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. MCP-BUILDER: Identifies API auth requirements          │
│           │                                                 │
│           ▼                                                 │
│  2. OAUTH-FLOW-ARCHITECT: Design OAuth flow                │
│           │                                                 │
│           ├──────────────────────────────────────┐          │
│           ▼                                      ▼          │
│  3a. MCP-INTEGRATION-PATTERNS  3b. WEBHOOK-INTEGRATION     │
│      (client auth)                 (signature validation)  │
│           │                                      │          │
│           └──────────────────────────────────────┘          │
│                          │                                  │
│                          ▼                                  │
│  4. MCP-SERVER-ORCHESTRATOR: Deploy with secrets           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Integration Checklist

Before completing OAuth implementation, verify:

- [ ] OAuth provider application registered
- [ ] Redirect URIs configured correctly
- [ ] Scopes are minimal (least privilege)
- [ ] Token storage is secure
- [ ] Refresh logic handles expiry
- [ ] Error handling covers token failures
- [ ] PKCE implemented for public clients
- [ ] State parameter prevents CSRF

## Common Scenarios

### Authorization Code Flow

1. **OAuth Flow Architect:** Implement authorization URL generation
2. **OAuth Flow Architect:** Handle callback and token exchange
3. **MCP Builder:** Use tokens in tool implementations
4. **MCP Integration Patterns:** Refresh tokens on client calls

### Client Credentials Flow

1. **OAuth Flow Architect:** Implement token acquisition
2. **MCP Server Orchestrator:** Inject credentials securely
3. **MCP Integration Patterns:** Attach tokens to requests

### OIDC Single Sign-On

1. **OAuth Flow Architect:** Configure OIDC discovery
2. **OAuth Flow Architect:** Implement ID token validation
3. **MCP Integration Patterns:** Use claims for authorization

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Storing secrets in code | Security vulnerability | Use environment variables/vaults |
| Missing PKCE | Authorization code interception | Always use PKCE for public clients |
| Over-scoped permissions | Excessive access | Request minimal scopes |
| No refresh logic | Broken after token expiry | Implement automatic refresh |

## Related Resources

- [Integration & Auth Skills Ecosystem Map](../../../docs/guides/integration-auth-skills-ecosystem.md)
- [OAuth Security Reference](./oauth-security.md)
- [Provider Configurations](./provider-configs.md)
- [Token Patterns](./token-patterns.md)
