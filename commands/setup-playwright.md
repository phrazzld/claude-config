Add Playwright MCP server configuration to enable browser automation capabilities.

# SETUP PLAYWRIGHT

Add Playwright MCP server configuration to the current repository.

## Installation

### Option 1: Using setup-mcp command
```bash
/setup-mcp playwright
```

### Option 2: Manual configuration

1. **Add to .mcp.json**:
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-playwright"]
    }
  }
}
```

2. **Install MCP server**:
```bash
claude mcp install --scope project
```

3. **Approve when prompted**:
- Select the Playwright server
- Confirm installation

## What Playwright MCP Provides

The Playwright MCP server enables:
- Browser automation and web scraping
- Web page interaction and testing  
- Screenshot capture and accessibility analysis
- Form filling and navigation workflows

**Note**: First use may trigger browser download (~100MB)

## Verification

Test the MCP server is working:
```bash
# In Claude Code, the playwright MCP tools will be available
# Tools include: playwright_navigate, playwright_screenshot, etc.
```