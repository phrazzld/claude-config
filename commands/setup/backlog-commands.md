# BACKLOG-COMMANDS

Set up local @BACKLOG.md-based command suite for project-specific task management without GitHub dependencies.

## 1. Initialize @BACKLOG.md Structure
- Check if @BACKLOG.md exists in current project root
- If not present, create structured @BACKLOG.md template:
  ```markdown
  # BACKLOG

  ## High Priority
  
  ## Medium Priority
  
  ## Low Priority
  
  ## Ideas & Future Considerations
  
  ## Completed
  
  ---
  
  ### Task Format
  - `- [ ] [HIGH/MED/LOW] [TYPE] Description`
  - Types: ALIGN, REFACTOR, FEATURE, BUG, DOCS, TEST, CHORE
  - Example: `- [ ] [HIGH] [REFACTOR] Extract authentication logic into separate module`
  ```

## 2. Create Local Backlog Commands
- Create project-specific variants of existing commands that work with local @BACKLOG.md
- Install the following commands in the current project's `.claude/commands/` directory:

### Core Commands
!mkdir -p .claude/commands
!cp ~/.claude/commands/backlog/groom.md .claude/commands/backlog-groom.md
!cp ~/.claude/commands/backlog/ideate.md .claude/commands/backlog-ideate.md

## 3. Adapt Commands for Local Workflow
- Modify each command to:
  - Remove GitHub issue dependencies
  - Target local @BACKLOG.md file instead of creating GitHub issues
  - Focus analysis on current project context
  - Use project-specific leyline document analysis
  - Maintain structured task format for @BACKLOG.md

## 4. Verification
- Verify @BACKLOG.md structure is properly initialized
- Confirm all backlog commands are available in `.claude/commands/`
- Test that commands can read/write to local @BACKLOG.md
- Ensure commands work independently of GitHub access

