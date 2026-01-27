# kimi-as-mcp

MCP server for delegating tasks to Kimi K2.5 CLI agents.

## Installation

```bash
# Install globally via uv
uv tool install /path/to/kimi-as-mcp

# Or use directly with uvx
uvx --from /path/to/kimi-as-mcp kimi-as-mcp
```

## Prerequisites

1. Install Kimi CLI:
   ```bash
   uv tool install --python 3.13 kimi-cli
   ```

2. Authenticate (interactive OAuth flow):
   ```bash
   kimi login
   ```
   This opens a browser for Moonshot account authentication. Required before first use.

3. Verify authentication:
   ```bash
   kimi --print --prompt "Say hello"
   ```
   Should produce agent output (not "LLM not set" error).

## MCP Configuration

Add to your `.mcp.json`:

```json
{
  "mcpServers": {
    "kimi": {
      "type": "stdio",
      "command": "uvx",
      "args": ["--from", "/Users/phaedrus/.claude/mcps/kimi-as-mcp", "kimi-as-mcp"]
    }
  }
}
```

## Tools

### spawn_agent

Spawn a single Kimi K2.5 agent in the current working directory.

```json
{
  "prompt": "Create a React component for user authentication",
  "thinking": false
}
```

### spawn_agents_parallel

Spawn multiple agents in parallel (leverages Agent Swarm for 4.5x speedup).

```json
{
  "agents": [
    {"prompt": "Write unit tests for auth.ts"},
    {"prompt": "Write integration tests for auth flow", "thinking": true}
  ]
}
```

## Kimi K2.5 Strengths

- **Agent Swarm**: Coordinates up to 100 sub-agents, 1,500+ tool calls in parallel
- **Multimodal**: Text, images, video from single prompt
- **Frontend excellence**: Best open-source for visual coding
- **Cost-effective**: ~$0.15/M input, $2.50/M output tokens
- **Open weights**: Apache 2.0 license

## When to Use Kimi vs Codex

| Task Type | Preferred |
|-----------|-----------|
| Standard implementation | Codex |
| Budget-conscious work | Kimi |
| Frontend/visual coding | Kimi |
| Complex multi-step | Kimi (Agent Swarm) |
| Git-heavy workflows | Codex |
