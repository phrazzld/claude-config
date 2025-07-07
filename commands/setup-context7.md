Add Context7 MCP server configuration for library and framework documentation access.

# SETUP CONTEXT7

Add Context7 MCP server configuration to the current repository.

## Installation

### Option 1: Using setup-mcp command
```bash
/setup-mcp context7
```

### Option 2: Manual configuration

1. **Add to .mcp.json**:
```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@context7/mcp-server"]
    }
  }
}
```

2. **Install MCP server**:
```bash
claude mcp install --scope project
```

3. **Approve when prompted**:
- Select the Context7 server
- Confirm installation

## What Context7 MCP Provides

The Context7 MCP server enables:
- Up-to-date documentation for thousands of libraries
- Code snippets and examples from official docs
- API references and configuration options
- Version-specific documentation

Available tools:
- `mcp__context7__resolve-library-id`: Find library IDs
- `mcp__context7__get-library-docs`: Fetch documentation

## Verification

Test the MCP server is working:
```bash
# In Claude Code, you can now use:
# mcp__context7__resolve-library-id("react")
# mcp__context7__get-library-docs("/facebook/react")
```