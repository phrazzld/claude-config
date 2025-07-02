# Claude Commands

This directory contains custom slash commands for Claude Code CLI, providing structured workflows organized into logical namespaces for software development tasks.

## Purpose

These commands provide standardized templates and workflows that help maintain consistency across development activities. Each command follows best practices and ensures comprehensive coverage of critical aspects of the task at hand.

## Namespace Organization

Commands are organized into specialized namespaces for better discoverability and logical grouping:

### 📊 Analysis
Root cause analysis and debugging workflows.
- **analysis/debug.md** - Multi-methodology RCA using parallel Task agents

### 📋 Backlog Management  
Idea generation and backlog organization.
- **backlog/ideate.md** - Generate project-specific ideas and append to BACKLOG.md
- **backlog/groom.md** - Organize, prioritize, and enhance BACKLOG.md

### 🔧 Git Workflows
Git operations and GitHub integration.
- **git/pr.md** - Create pull requests with auto-generated descriptions
- **git/push.md** - Quality gate workflow before pushing code
- **git/respond.md** - Handle PR feedback and reviews

### 🧠 Meta Commands
Reflection and strategic thinking tools.
- **meta/carmack.md** - John Carmack-inspired technical problem-solving framework
- **meta/chill.md** - Structured reflection and stress reduction

### ⚙️ Setup & Configuration
Project setup and tool configuration.
- **setup/mcp.md** - Add MCP integrations (GitHub, Linear, Azure, Context7, Playwright)
- **setup/sync.md** - Update commands to match project state
- Plus various setup templates for logging, commands, reviews, etc.

### 📝 Task Management
Task planning and breakdown workflows.
- **task/plan.md** - Read BACKLOG.md and create detailed breakdowns in TASK.md
- **task/ready.md** - Convert TASK.md items into actionable TODO.md entries

### ✅ TODO Execution
Task execution and resolution workflows.
- **todo/execute.md** - Execute next available task from TODO.md with status tracking
- **todo/resolve.md** - Unblock stuck tasks and resolve issues

### 🛠️ Utility Commands (Root Level)
General-purpose development utilities.
- **audit.md** - Security audit documentation
- **prime.md** - Gather context from key repository files  
- **ticket.md** - Convert plans into prioritized task tickets
- **branch.md** - Create feature branches with proper naming
- Plus specialized tools like brainstorm.md, document.md, verify.md, etc.

## Workflow Integration

The commands follow an integrated workflow pattern:
```
BACKLOG.md → TASK.md → TODO.md → Execution
```

1. **backlog/ideate.md** → Generate ideas in BACKLOG.md
2. **backlog/groom.md** → Organize and prioritize backlog  
3. **task/plan.md** → Move items from BACKLOG.md to TASK.md with detailed planning
4. **task/ready.md** → Convert TASK.md to actionable TODO.md entries
5. **todo/execute.md** → Execute tasks with proper status tracking
6. **git/push.md** → Quality gates and code push
7. **git/pr.md** → Create pull requests

## Usage

Commands are invoked using slash syntax:
```bash
/backlog/ideate    # Generate project ideas
/task/plan         # Plan next task from backlog  
/todo/execute      # Execute next available task
/git/pr            # Create pull request
```

## File References

Commands use standardized file references:
- **@BACKLOG.md** - Project backlog and ideas
- **@TASK.md** - Current task being planned
- **@TODO.md** - Actionable task queue

## Development

When creating or modifying commands:
1. Use appropriate namespace for logical organization
2. Start with one-sentence purpose statement
3. Use proper file references (@BACKLOG.md, @TASK.md, @TODO.md)
4. Follow established thinking directive patterns
5. Integrate with existing workflow where applicable