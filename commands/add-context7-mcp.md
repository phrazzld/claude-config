# Add Context7 MCP to Repository

Adds Context7 MCP server configuration to the current repository.

**Usage**: `/user:add-context7-mcp`

## What This Does

1. Creates `.mcp.json` in the repository root with Context7 configuration
2. Commits the file to git for team sharing
3. Provides setup instructions for team members

## Implementation

```bash
# Copy the Context7-only template to repository root
cp ~/.claude/templates/mcp-context7-only.json ./.mcp.json

# Add to git
git add .mcp.json
git commit -m "feat: add Context7 MCP server configuration

Enables Context7 documentation server for all team members.
Team members should run: claude mcp install --scope project"

echo "✅ Context7 MCP configuration added and committed"
echo ""
echo "Team setup instructions:"
echo "1. Pull the latest changes"
echo "2. Run: claude mcp install --scope project"
echo "3. Approve the Context7 server when prompted"
```

This gives your entire team access to Context7's library documentation server automatically.