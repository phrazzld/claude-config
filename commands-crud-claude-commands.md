# CRUD Claude Commands - Dynamic Command Management

Manage Claude Code custom commands through Create, Read, Update, and Delete operations.

**Usage**: `/project:crud-claude-commands <operation> <command-name> [content]`

## Operations

### CREATE
Create a new Claude command from user instructions.

**Usage**: `/project:crud-claude-commands create <command-name> "description of what the command should do"`

**Example**:
```bash
/project:crud-claude-commands create git-flow "Create a command that automates git flow operations like creating feature branches, PRs, and merging"
```

### READ
Display the content of an existing Claude command.

**Usage**: `/project:crud-claude-commands read <command-name>`

**Example**:
```bash
/project:crud-claude-commands read multi-mind
```

### UPDATE
Modify an existing Claude command based on user instructions.

**Usage**: `/project:crud-claude-commands update <command-name> "description of changes"`

**Example**:
```bash
/project:crud-claude-commands update page "Add support for JSON export format and include timestamp in filenames"
```

### DELETE
Remove a Claude command from the system.

**Usage**: `/project:crud-claude-commands delete <command-name>`

**Example**:
```bash
/project:crud-claude-commands delete old-command
```

### LIST
Show all available Claude commands.

**Usage**: `/project:crud-claude-commands list`

## Implementation Instructions

Execute the requested CRUD operation:

### For CREATE:
1. Parse the command name and description
2. Generate appropriate command content based on description
3. Create the command file at `.claude/commands/{command-name}.md`
4. Follow the standard command template:
   ```markdown
   # Command Title

   Brief description of the command.

   **Usage**: `/project:{command-name} $ARGUMENTS`

   ## Implementation

   [Detailed instructions for Claude]

   ## Examples

   [Usage examples]
   ```
5. Confirm creation with file path

### For READ:
1. Check if command exists at `.claude/commands/{command-name}.md`
2. Read and display the full content
3. Show usage examples if present

### For UPDATE:
1. Read existing command content
2. Apply requested modifications based on user description
3. Preserve command structure while updating functionality
4. Save updated content
5. Show before/after summary of changes

### For DELETE:
1. Confirm command exists
2. Display command content for reference
3. Delete the file
4. Confirm deletion

### For LIST:
1. List all `.md` files in `.claude/commands/`
2. Extract and display:
   - Command name
   - Brief description (first paragraph)
   - Usage syntax

## Command Synchronization

After any CREATE, UPDATE, or DELETE operation:

1. **Agent-guides repository reference**:
   - Repository: `https://github.com/tokenbender/agent-guides`
   - Commands directory: `/claude-commands/`
   - Scripts directory: `/scripts/`

2. **Sync instructions**:
   - Inform user to manually sync changes to the agent-guides repository
   - Provide the command content for easy copy/paste
   - Suggest creating a PR if appropriate

3. **Reference examples**:
   - View existing commands: https://github.com/tokenbender/agent-guides/tree/main/claude-commands
   - Extract session script: https://github.com/tokenbender/agent-guides/blob/main/scripts/extract-claude-session.py
   - Repository README: https://github.com/tokenbender/agent-guides/blob/main/README.md

## Error Handling

- **Command not found**: Suggest similar commands using fuzzy matching
- **Invalid operation**: Show valid operations (create, read, update, delete, list)
- **Permission errors**: Inform user about file access issues
- **Git errors**: Report but don't fail the primary operation

## Success Criteria

- Command operations complete successfully
- Files are properly formatted and functional
- Changes are synchronized to agent-guides if available
- User receives clear confirmation of actions taken
- Git commits are descriptive and accurate

## Examples of Generated Commands

When creating commands, consider these patterns:

1. **Analysis commands**: Like analyze-function, multi-mind
2. **Workflow commands**: Like page, search-prompts
3. **Automation commands**: Git operations, testing, deployment
4. **Documentation commands**: Generate docs, update READMEs

Ensure generated commands are:
- Reusable across projects
- Well-documented with examples
- Follow established patterns
- Include error handling
- Provide clear output

Execute the requested CRUD operation now.
