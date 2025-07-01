# Add Playwright MCP to Repository

Adds Playwright MCP server configuration to the current repository.

**Usage**: `/user:add-playwright-mcp`

## What This Does

1. Creates `.mcp.json` in the repository root with Playwright configuration
2. Commits the file to git for team sharing
3. Provides setup instructions for team members

## Implementation

```bash
# Copy the Playwright-only template to repository root
cp ~/.claude/templates/mcp-playwright-only.json ./.mcp.json

# Add to git
git add .mcp.json
git commit -m "feat: add Playwright MCP server configuration

Enables Playwright browser automation server for all team members.
Team members should run: claude mcp install --scope project"

echo "✅ Playwright MCP configuration added and committed"
echo ""
echo "Team setup instructions:"
echo "1. Pull the latest changes"
echo "2. Run: claude mcp install --scope project"
echo "3. Approve the Playwright server when prompted"
echo ""
echo "Note: Playwright MCP provides tools for:"
echo "- Browser automation and web scraping"
echo "- Web page interaction and testing"
echo "- Screenshot capture and accessibility tree analysis"
echo "- Form filling and navigation workflows"
echo ""
echo "⚠️  Note: First use may trigger browser download (~100MB)"
```

This gives your entire team access to Playwright's browser automation capabilities directly from Claude.