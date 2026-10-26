---
name: agent-development-pack
description: Curated bundle for building, testing, and coordinating AI agent systems. Includes multi-agent orchestration, agent testing, cross-agent handoff, MCP server building, and prompt engineering. Use when developing AI agent workflows or multi-agent systems.
license: MIT
complexity: intermediate
time_to_learn: 5min
tags:
  - bundle
  - agents
  - multi-agent
  - testing
  - orchestration
inputs:
  - agent-requirements
outputs:
  - skill-bundle
includes:
  - agent-swarm-orchestrator
  - agent-testing-patterns
  - cross-agent-handoff
  - mcp-builder
  - prompt-engineering-patterns
tier: core
governance_phases: [build, prove]
organ_affinity: [organ-iv]
triggers: [context:agent-development, context:multi-agent, context:mcp-server]
---

# Agent Development Pack

A curated bundle for building, testing, and coordinating AI agent systems with proper handoff and tool integration.

## What's Included

- **agent-swarm-orchestrator** — Design multi-agent systems with coordinated swarms and task distribution
- **agent-testing-patterns** — Test agent tool use, non-deterministic outputs, and multi-turn conversations
- **cross-agent-handoff** — Transfer context between agent sessions with structured handoff protocols
- **mcp-builder** — Build MCP (Model Context Protocol) servers for extending agent capabilities
- **prompt-engineering-patterns** — Design effective prompts with structured formats and chain-of-thought

## Getting Started

Install this bundle when building AI agent systems. The recommended workflow:

1. **Design:** Use prompt-engineering-patterns to architect system prompts and tool definitions
2. **Build:** Use mcp-builder for custom tool servers and agent-swarm-orchestrator for multi-agent coordination
3. **Test:** Use agent-testing-patterns for unit, integration, and E2E agent testing
4. **Coordinate:** Use cross-agent-handoff for reliable session continuity

This pack is the foundation for ORGAN-IV (orchestration) agent development.
