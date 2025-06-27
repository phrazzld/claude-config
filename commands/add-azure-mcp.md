# Add Azure MCP to Repository

Adds Azure MCP server configuration to the current repository.

**Usage**: `/user:add-azure-mcp`

## What This Does

1. Creates `.mcp.json` in the repository root with Azure configuration
2. Commits the file to git for team sharing
3. Provides setup instructions for team members

## Implementation

```bash
# Copy the Azure-only template to repository root
cp ~/.claude/templates/mcp-azure-only.json ./.mcp.json

# Add to git
git add .mcp.json
git commit -m "feat: add Azure MCP server configuration

Enables Azure cloud services integration for all team members.
Team members should run: claude mcp install --scope project"

echo "✅ Azure MCP configuration added and committed"
echo ""
echo "Team setup instructions:"
echo "1. Pull the latest changes"
echo "2. Run: claude mcp install --scope project"
echo "3. Approve the Azure server when prompted"
echo "4. Configure required environment variables:"
echo "   - AZURE_STORAGE_ACCOUNT_URL=https://<account>.blob.core.windows.net"
echo "   - AZURE_COSMOSDB_ENDPOINT=<your_cosmos_endpoint>"
echo "   - AZURE_COSMOSDB_KEY=<your_cosmos_key>"
echo ""
echo "Note: Azure MCP provides tools for:"
echo "- Azure Blob Storage (containers, blobs, upload/download)"
echo "- Azure Cosmos DB NoSQL API (containers, items, queries)"
echo "- Azure App Configuration (key-value pairs)"
```

This gives your entire team access to Azure cloud services directly from Claude with automatic logging and audit tracking.