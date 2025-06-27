# Add Linear MCP to Repository

Adds Linear MCP server configuration to the current repository.

**Usage**: `/user:add-linear-mcp`

## What This Does

1. Creates `.mcp.json` in the repository root with Linear configuration
2. Commits the file to git for team sharing
3. Provides setup instructions for team members

## Implementation

```bash
# Copy the Linear-only template to repository root
cp ~/.claude/templates/mcp-linear-only.json ./.mcp.json

# Add to git
git add .mcp.json
git commit -m "feat: add Linear MCP server configuration

Enables Linear project management integration for all team members.
Team members should run: claude mcp install --scope project"

echo "✅ Linear MCP configuration added and committed"
echo ""
echo "Team setup instructions:"
echo "1. Pull the latest changes"
echo "2. Run: claude mcp install --scope project"
echo "3. Approve the Linear server when prompted"
echo "4. Authenticate with Linear using OAuth when requested"
echo ""
echo "Note: Linear MCP provides tools for:"
echo "- Finding, creating, and updating issues"
echo "- Managing projects and comments"
echo "- Accessing Linear workspace data"
```

This gives your entire team access to Linear's project management features directly from Claude.