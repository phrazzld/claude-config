# SYNC

Analyze the current project and update all project-specific Claude commands to align with current tools, patterns, and best practices.

**Usage**: `/user:sync-project-commands`

## GOAL

Synchronize all project-specific commands in `.claude/commands/` with the current project state, ensuring they reflect:
- Current technology stack and dependencies
- Updated development practices and conventions
- New tools and integrations
- Latest leyline documentation principles
- Current testing and quality standards

## ANALYZE

### Phase 1: Project State Discovery

1. **Technology Stack Analysis**
   - Read package.json, Gemfile, requirements.txt, go.mod, etc.
   - Identify new dependencies or version changes
   - Check for new build tools or scripts
   - Detect framework updates or migrations

2. **Convention and Pattern Analysis**
   - Scan codebase for emerging patterns
   - Identify new file structures or architectures
   - Check for updated naming conventions
   - Review recent commits for style changes

3. **Documentation Review**
   - Read all leyline documents in `./docs/leyline/`
   - Check README for new procedures
   - Review CONTRIBUTING.md for updated guidelines
   - Scan for new ADRs or design documents

4. **Tool and Integration Discovery**
   - Check for new CI/CD configurations
   - Identify new linters or formatters
   - Detect new testing frameworks
   - Find new development tools (like thinktank)

### Phase 2: Command Inventory

1. **Discover Project Commands**
   - List all `.md` files in `.claude/commands/`
   - Categorize by type (planning, execution, utility)
   - Note creation dates and last modifications
   - Identify command dependencies and relationships

2. **Analyze Command Content**
   - Extract key patterns and references from each command
   - Identify outdated tool references
   - Find hard-coded values that should be dynamic
   - Note missing recent project capabilities

### Phase 3: Intelligent Updates

For each project command, apply updates while preserving intent:

1. **Tool and Dependency Updates**
   - Update package/module references to current versions
   - Replace deprecated tools with modern equivalents
   - Add references to newly available tools
   - Update command syntax for tool changes

2. **Pattern and Convention Alignment**
   - Adjust code examples to match current style
   - Update file paths and project structure references
   - Align with current naming conventions
   - Incorporate new architectural patterns

3. **Enhancement Integration**
   - Add references to new leyline principles
   - Include newly available MCP servers
   - Integrate new testing requirements
   - Add quality gates from current CI/CD

4. **Context Preservation**
   - Maintain the command's core purpose and workflow
   - Preserve any project-specific customizations
   - Keep user-friendly descriptions and examples
   - Retain command personality and tone

## EXECUTE

### 1. **Create Update Plan**
   Generate a comprehensive update plan:
   ```
   === PROJECT COMMAND SYNC PLAN ===
   
   Current Project State:
   - Technology: [detected stack]
   - New Tools: [list of new tools]
   - Updated Patterns: [key changes]
   
   Commands to Update:
   1. /project:plan
      - Add reference to new Context7 endpoints
      - Update expert personas for domain
      
   2. /project:ticket
      - Include new PR size guidelines
      - Add team's updated task format
      
   3. /project:execute
      - Update test commands to new framework
      - Add new linting requirements
   ```

### 2. **Backup Current Commands**
   Before making changes:
   - Note current command state for potential rollback
   - Document what specific changes will be made
   - Prepare clear change summaries

### 3. **Apply Updates Systematically**
   For each command:
   - Read current content
   - Apply identified updates
   - Validate syntax and structure
   - Ensure command remains executable
   - Write updated content back

### 4. **Cross-Command Consistency**
   Ensure all commands:
   - Use consistent terminology
   - Reference same tool versions
   - Follow same formatting patterns
   - Share common project understanding

### 5. **Validation Phase**
   After updates:
   - Verify each command is syntactically valid
   - Check that core workflows remain intact
   - Ensure no critical functionality was lost
   - Confirm commands work together cohesively

## REPORTING

Generate comprehensive sync report:

```markdown
# Project Commands Sync Report

## Project Analysis
- Detected [X] new tools/dependencies
- Found [Y] updated conventions
- Identified [Z] new leyline principles

## Commands Updated

### /project:plan
**Changes Made:**
- Updated Context7 integration to use new endpoints
- Added reference to new architecture patterns
- Included latest performance considerations

### /project:ticket  
**Changes Made:**
- Adjusted task format to match team's new standard
- Added integration with new project board tool
- Updated PR size recommendations

### /project:execute
**Changes Made:**
- Updated test commands from `npm test` to `npm run test:all`
- Added new pre-commit hook requirements
- Integrated new code coverage thresholds

## Recommendations
- Consider creating command for [new workflow]
- Review [specific command] for deeper customization
- Update team documentation about command changes
```

## SUCCESS CRITERIA

- All project commands reflect current project state
- No functionality lost during updates
- Commands remain intuitive and well-documented
- Consistency maintained across all commands
- Clear audit trail of what changed and why
- Project-specific customizations preserved

## EDGE CASES

Handle special situations:
- **Missing leyline docs**: Use project README and conventions
- **Conflicting patterns**: Prefer most recent/most used
- **Breaking changes**: Flag for manual review
- **Custom workflows**: Preserve unless clearly outdated

Execute this comprehensive command synchronization process now.