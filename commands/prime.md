# PRIME

Comprehensive context gathering to establish situational awareness

## 1. PROJECT CONTEXT

### Core Documentation
- @README.md
- @CLAUDE.md (both ~/.claude/CLAUDE.md and ./CLAUDE.md if exists)
- docs/leyline/* (project philosophy and guidelines)

### Task Management
- @TODO.md (current task state and progress)
- @TASK.md (active task specification)
- @BACKLOG.md (future work items)

## 2. CODEBASE STATE

### Git Status
- !git status --short --branch
- !git log --oneline -10 --graph --decorate

### Recent Activity
- !git diff --stat HEAD~5..HEAD
- !git show --name-only --format="Commit: %h %s (%cr)" HEAD

### Directory Structure
- !find . -type f -name "*.md" | grep -E "(README|TODO|TASK|BACKLOG|CLAUDE)" | head -20
- !ls -la

## 3. DEVELOPMENT WORKFLOW

### Available Commands
- commands/README.md
- !ls -1 commands/*.md | head -10

### Configuration
- settings.json
- .env (if exists)
- package.json (if exists)

## 4. QUICK ASSESSMENT

### Complexity Indicators
- !git ls-files | wc -l (total tracked files)
- !git diff --name-only | wc -l (modified files)
- !find . -name "*.test.*" -o -name "*.spec.*" | wc -l (test files)

### Key Patterns
- !rg "TODO|FIXME|HACK|XXX" --stats-only 2>/dev/null || echo "No ripgrep available"

## SUCCESS CRITERIA

✓ Understand project purpose and structure
✓ Know current branch and recent changes
✓ Aware of active tasks and priorities
✓ Familiar with available commands and workflows
✓ Ready to proceed with informed context
