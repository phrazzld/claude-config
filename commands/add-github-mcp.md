# Add GitHub MCP to Repository

Adds GitHub MCP server configuration to the current repository.

**Usage**: `/user:add-github-mcp`

## What This Does

1. Creates `.mcp.json` in the repository root with GitHub configuration
2. Commits the file to git for team sharing
3. Provides setup instructions for team members

## Implementation

```bash
# Copy the GitHub-only template to repository root
cp ~/.claude/templates/mcp-github-only.json ./.mcp.json

# Add to git
git add .mcp.json
git commit -m "feat: add GitHub MCP server configuration

Enables GitHub repository management integration for all team members.
Team members should run: claude mcp install --scope project"

echo "✅ GitHub MCP configuration added and committed"
echo ""
echo "Team setup instructions:"
echo "1. Pull the latest changes"
echo "2. Run: claude mcp install --scope project"
echo "3. Approve the GitHub server when prompted"
echo "4. Create a GitHub Personal Access Token:"
echo "   - Go to GitHub Settings > Developer settings > Personal access tokens"
echo "   - Generate new token with 'repo' scope (or 'public_repo' for public only)"
echo "   - Set environment variable: GITHUB_PERSONAL_ACCESS_TOKEN=<your_token>"
echo ""
echo "Note: GitHub MCP provides tools for:"
echo "- Repository management and file operations"
echo "- Issue and pull request management"
echo "- Code search and analysis"
echo ""
echo "⚠️  Security: Keep GitHub tokens secure and never commit them to the repository"
```

This gives your entire team access to GitHub repository management directly from Claude.