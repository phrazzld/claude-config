Add MCP server configuration to the current repository for specified service type.

# MCP

Add MCP server configuration to the current repository for specified service type.

**Usage**: Provide MCP type as argument: `github`, `linear`, `azure`, `context7`, or `playwright`

## Implementation

Based on the MCP type argument, copy the appropriate template and provide setup instructions:

### GitHub MCP
```bash
if [ "$ARGUMENTS" = "github" ]; then
    # Copy the GitHub-only template to repository root
    !cp ~/.claude/templates/mcp-github-only.json ./.mcp.json
    
    # Add to git
    !git add .mcp.json
    !git commit -m "feat: add GitHub MCP server configuration

Enables GitHub repository management integration for all team members.
Team members should run: claude mcp install --scope project"
    
    !echo "✅ GitHub MCP configuration added and committed"
    !echo ""
    !echo "Team setup instructions:"
    !echo "1. Pull the latest changes"
    !echo "2. Run: claude mcp install --scope project"
    !echo "3. Approve the GitHub server when prompted"
    !echo "4. Create a GitHub Personal Access Token:"
    !echo "   - Go to GitHub Settings > Developer settings > Personal access tokens"
    !echo "   - Generate new token with 'repo' scope (or 'public_repo' for public only)"
    !echo "   - Set environment variable: GITHUB_PERSONAL_ACCESS_TOKEN=<your_token>"
    !echo ""
    !echo "Note: GitHub MCP provides tools for:"
    !echo "- Repository management and file operations"
    !echo "- Issue and pull request management"
    !echo "- Code search and analysis"
    !echo ""
    !echo "⚠️  Security: Keep GitHub tokens secure and never commit them to the repository"
fi
```

### Linear MCP
```bash
if [ "$ARGUMENTS" = "linear" ]; then
    # Copy the Linear-only template to repository root
    !cp ~/.claude/templates/mcp-linear-only.json ./.mcp.json
    
    # Add to git
    !git add .mcp.json
    !git commit -m "feat: add Linear MCP server configuration

Enables Linear project management integration for all team members.
Team members should run: claude mcp install --scope project"
    
    !echo "✅ Linear MCP configuration added and committed"
    !echo ""
    !echo "Team setup instructions:"
    !echo "1. Pull the latest changes"
    !echo "2. Run: claude mcp install --scope project"
    !echo "3. Approve the Linear server when prompted"
    !echo "4. Authenticate with Linear using OAuth when requested"
    !echo ""
    !echo "Note: Linear MCP provides tools for:"
    !echo "- Finding, creating, and updating issues"
    !echo "- Managing projects and comments"
    !echo "- Accessing Linear workspace data"
fi
```

### Azure MCP
```bash
if [ "$ARGUMENTS" = "azure" ]; then
    # Copy the Azure-only template to repository root
    !cp ~/.claude/templates/mcp-azure-only.json ./.mcp.json
    
    # Add to git
    !git add .mcp.json
    !git commit -m "feat: add Azure MCP server configuration

Enables Azure cloud services integration for all team members.
Team members should run: claude mcp install --scope project"
    
    !echo "✅ Azure MCP configuration added and committed"
    !echo ""
    !echo "Team setup instructions:"
    !echo "1. Pull the latest changes"
    !echo "2. Run: claude mcp install --scope project"
    !echo "3. Approve the Azure server when prompted"
    !echo "4. Configure required environment variables:"
    !echo "   - AZURE_STORAGE_ACCOUNT_URL=https://<account>.blob.core.windows.net"
    !echo "   - AZURE_COSMOSDB_ENDPOINT=<your_cosmos_endpoint>"
    !echo "   - AZURE_COSMOSDB_KEY=<your_cosmos_key>"
    !echo ""
    !echo "Note: Azure MCP provides tools for:"
    !echo "- Azure Blob Storage (containers, blobs, upload/download)"
    !echo "- Azure Cosmos DB NoSQL API (containers, items, queries)"
    !echo "- Azure App Configuration (key-value pairs)"
fi
```

### Context7 MCP
```bash
if [ "$ARGUMENTS" = "context7" ]; then
    # Copy the Context7-only template to repository root
    !cp ~/.claude/templates/mcp-context7-only.json ./.mcp.json
    
    # Add to git
    !git add .mcp.json
    !git commit -m "feat: add Context7 MCP server configuration

Enables Context7 documentation server for all team members.
Team members should run: claude mcp install --scope project"
    
    !echo "✅ Context7 MCP configuration added and committed"
    !echo ""
    !echo "Team setup instructions:"
    !echo "1. Pull the latest changes"
    !echo "2. Run: claude mcp install --scope project"
    !echo "3. Approve the Context7 server when prompted"
fi
```

### Playwright MCP
```bash
if [ "$ARGUMENTS" = "playwright" ]; then
    # Copy the Playwright-only template to repository root
    !cp ~/.claude/templates/mcp-playwright-only.json ./.mcp.json
    
    # Add to git
    !git add .mcp.json
    !git commit -m "feat: add Playwright MCP server configuration

Enables Playwright browser automation server for all team members.
Team members should run: claude mcp install --scope project"
    
    !echo "✅ Playwright MCP configuration added and committed"
    !echo ""
    !echo "Team setup instructions:"
    !echo "1. Pull the latest changes"
    !echo "2. Run: claude mcp install --scope project"
    !echo "3. Approve the Playwright server when prompted"
    !echo ""
    !echo "Note: Playwright MCP provides tools for:"
    !echo "- Browser automation and web scraping"
    !echo "- Web page interaction and testing"
    !echo "- Screenshot capture and accessibility tree analysis"
    !echo "- Form filling and navigation workflows"
    !echo ""
    !echo "⚠️  Note: First use may trigger browser download (~100MB)"
fi
```

### Usage Validation
```bash
if [[ ! "$ARGUMENTS" =~ ^(github|linear|azure|context7|playwright)$ ]]; then
    !echo "❌ Invalid MCP type. Supported types:"
    !echo "  - github: GitHub repository management"
    !echo "  - linear: Linear project management"
    !echo "  - azure: Azure cloud services"
    !echo "  - context7: Context7 documentation"
    !echo "  - playwright: Playwright browser automation"
    !echo ""
    !echo "Usage: Specify MCP type as argument"
    exit 1
fi
```