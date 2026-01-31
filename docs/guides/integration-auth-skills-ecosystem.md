# Integration & Authentication Skills Ecosystem

This guide maps the relationships between integration and authentication-focused skills in this repository and provides workflow guidance for using them together effectively.

## Skill Overview

| Skill | Category | Focus Area |
|-------|----------|------------|
| [`mcp-integration-patterns`](../../skills/integrations/mcp-integration-patterns/) | integrations | MCP server/client integration patterns |
| [`mcp-builder`](../../skills/development/mcp-builder/) | development | Building MCP servers from scratch |
| [`mcp-server-orchestrator`](../../skills/development/mcp-server-orchestrator/) | development | Deploying and managing MCP infrastructure |
| [`oauth-flow-architect`](../../skills/integrations/oauth-flow-architect/) | integrations | OAuth 2.0/OIDC implementation patterns |
| [`webhook-integration-patterns`](../../skills/integrations/webhook-integration-patterns/) | integrations | Reliable webhook design and handling |

## Ecosystem Diagram

```mermaid
flowchart TB
    subgraph Build["Build Layer"]
        MB[mcp-builder]
    end

    subgraph Deploy["Deployment Layer"]
        MSO[mcp-server-orchestrator]
    end

    subgraph Integrate["Integration Layer"]
        MIP[mcp-integration-patterns]
        WIP[webhook-integration-patterns]
    end

    subgraph Auth["Authentication Layer"]
        OFA[oauth-flow-architect]
    end

    MB -->|"Server ready for"| MSO
    MSO -->|"Deployed servers use"| MIP
    MIP -->|"Receives events via"| WIP
    OFA -->|"Secures"| MIP
    OFA -->|"Authenticates"| WIP
    MB -.->|"May require auth"| OFA
    WIP -.->|"Can trigger"| MIP

    style MB fill:#e3f2fd
    style MSO fill:#e3f2fd
    style MIP fill:#e8f5e9
    style WIP fill:#e8f5e9
    style OFA fill:#fff3e0
```

## Workflow Scenarios

### Scenario 1: Claude MCP Integration

**Goal:** Build and deploy an MCP server that integrates with third-party APIs.

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant MB as mcp-builder
    participant OFA as oauth-flow-architect
    participant MSO as mcp-server-orchestrator
    participant MIP as mcp-integration-patterns

    Dev->>MB: 1. Create MCP server skeleton
    MB-->>Dev: Server with tools/resources defined
    Dev->>OFA: 2. Add OAuth for API access
    OFA-->>Dev: Token management, refresh logic
    Dev->>MSO: 3. Deploy to infrastructure
    MSO-->>Dev: Running server with health checks
    Dev->>MIP: 4. Integrate with Claude clients
    MIP-->>Dev: Transport config, error handling
```

**Skill Sequence:**
1. **`mcp-builder`** - Define server structure, tools, and resources
2. **`oauth-flow-architect`** - Implement authentication for external APIs
3. **`mcp-server-orchestrator`** - Deploy server with proper configuration
4. **`mcp-integration-patterns`** - Configure client integration patterns

### Scenario 2: Third-Party API Integration

**Goal:** Connect a service to your application via OAuth and webhooks.

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant OFA as oauth-flow-architect
    participant WIP as webhook-integration-patterns
    participant MB as mcp-builder
    participant MIP as mcp-integration-patterns

    Dev->>OFA: 1. Implement OAuth flow
    OFA-->>Dev: Authorization URL, token exchange
    Dev->>WIP: 2. Set up webhook receiver
    WIP-->>Dev: Endpoint, signature validation
    Dev->>MB: 3. Create MCP server to expose data
    MB-->>Dev: Tools wrapping webhook data
    Dev->>MIP: 4. Enable Claude access
    MIP-->>Dev: Client configuration
```

**Skill Sequence:**
1. **`oauth-flow-architect`** - Authenticate with third-party service
2. **`webhook-integration-patterns`** - Receive real-time events
3. **`mcp-builder`** - Expose webhook data as MCP tools
4. **`mcp-integration-patterns`** - Connect to Claude clients

### Scenario 3: Enterprise SSO Setup

**Goal:** Implement single sign-on with MCP authentication middleware.

```mermaid
sequenceDiagram
    participant Arch as Architect
    participant OFA as oauth-flow-architect
    participant MIP as mcp-integration-patterns
    participant MSO as mcp-server-orchestrator

    Arch->>OFA: 1. Design OIDC flow
    OFA-->>Arch: Provider config, claims mapping
    Arch->>MIP: 2. Add auth middleware to MCP
    MIP-->>Arch: Token validation pattern
    Arch->>MSO: 3. Deploy with auth enabled
    MSO-->>Arch: Secure MCP endpoint
```

**Skill Sequence:**
1. **`oauth-flow-architect`** - Configure OIDC with identity provider
2. **`mcp-integration-patterns`** - Implement auth middleware for MCP
3. **`mcp-server-orchestrator`** - Deploy with authentication layer

## Decision Tree: Which Skill to Use?

```mermaid
flowchart TD
    Start([What do you need?]) --> Q1{MCP or external APIs?}

    Q1 -->|MCP| Q2{Build or integrate?}
    Q2 -->|Build new server| MB[mcp-builder]
    Q2 -->|Deploy existing| MSO[mcp-server-orchestrator]
    Q2 -->|Connect clients| MIP[mcp-integration-patterns]

    Q1 -->|External APIs| Q3{How does it connect?}
    Q3 -->|OAuth/OIDC| OFA[oauth-flow-architect]
    Q3 -->|Webhooks| WIP[webhook-integration-patterns]
    Q3 -->|Both| Q4[OFA then WIP]

    Q1 -->|Both| Q5{Starting fresh?}
    Q5 -->|Yes| MB
    Q5 -->|Existing server| MIP

    style MB fill:#e3f2fd
    style MSO fill:#e3f2fd
    style MIP fill:#e8f5e9
    style WIP fill:#e8f5e9
    style OFA fill:#fff3e0
```

## Cross-Reference Matrix

This matrix shows when each skill might invoke or reference another:

| Primary Skill | Invokes | For |
|---------------|---------|-----|
| `mcp-builder` | `oauth-flow-architect` | Adding authentication to server tools |
| `mcp-builder` | `mcp-integration-patterns` | Following protocol conventions |
| `mcp-server-orchestrator` | `mcp-builder` | Understanding server structure |
| `mcp-server-orchestrator` | `oauth-flow-architect` | Configuring auth in deployment |
| `mcp-integration-patterns` | `oauth-flow-architect` | Securing client connections |
| `mcp-integration-patterns` | `webhook-integration-patterns` | Receiving external events |
| `oauth-flow-architect` | `webhook-integration-patterns` | Token refresh via callbacks |
| `webhook-integration-patterns` | `oauth-flow-architect` | Validating webhook signatures |

## Common Handoff Patterns

### MCP Builder → OAuth Flow Architect
When building an MCP server that needs to call authenticated APIs:
- Server skeleton complete
- Tool definitions that require API calls
- Need to store and refresh tokens

### OAuth Flow Architect → Webhook Integration
After OAuth is set up, you often need to receive events:
- OAuth tokens enable webhook subscription
- Webhook validates using OAuth credentials
- Combined for real-time data sync

### MCP Builder → MCP Server Orchestrator
When the server is ready for deployment:
- Server code complete and tested
- Configuration for different environments
- Health check endpoints defined

### MCP Server Orchestrator → MCP Integration Patterns
After deployment, connect clients:
- Server URL and transport method
- Authentication configuration
- Error handling patterns

## Best Practices

### Sequential vs. Parallel Usage
- **Sequential:** New integration (builder → oauth → orchestrator → patterns)
- **Parallel:** Auth + webhooks simultaneously when both needed

### Avoiding Overlap
- **Build concerns:** `mcp-builder` owns server code
- **Deploy concerns:** `mcp-server-orchestrator` owns infrastructure
- **Auth concerns:** `oauth-flow-architect` owns token management
- **Event concerns:** `webhook-integration-patterns` owns event handling
- **Protocol concerns:** `mcp-integration-patterns` owns MCP conventions

### When to Combine Skills
Some tasks benefit from multiple skills in one session:
- **Full MCP pipeline:** builder + orchestrator + patterns
- **Authenticated webhooks:** oauth + webhooks
- **Secure MCP:** builder + oauth + patterns

## Related Resources

- [Creating Skills Guide](./creating-skills.md)
- [Skill Specification](../api/skill-spec.md)
- [Getting Started](./getting-started.md)
