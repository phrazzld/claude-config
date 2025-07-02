# Claude Code Commands Improvement TODO.md

## Phase 1: Directory Structure & Organization

- [x] Create namespace directories in `/Users/phaedrus/.claude/commands/`: `mkdir -p backlog task todo git analysis setup meta`
- [x] Move `ideate.md`, `backlog-ideate.md` → `backlog/ideate.md` and consolidate content into single focused command
- [x] Move `groom.md`, `backlog-groom.md`, `backlog-align.md` → `backlog/groom.md` with unified grooming approach
- [x] Move `plan.md`, `task-plan.md` → `task/plan.md` focusing on TASK.md breakdown generation
- [x] Move `execute.md` → `todo/execute.md` maintaining current comprehensive execution flow
- [x] Move `carmack.md`, `chill.md` → `meta/carmack.md`, `meta/chill.md` preserving step-back-and-think philosophy
- [x] Move `debug.md` → `analysis/debug.md` keeping multi-agent RCA approach
- [x] Move `push.md` → `git/push.md` maintaining quality gate workflow
- [x] Move `respond.md` → `git/respond.md` for PR feedback handling

## Phase 2: Command Consolidation

- [x] Consolidate all `add-*-mcp.md` commands into single `setup/mcp.md` that accepts MCP type as `$ARGUMENTS` (github, linear, azure, context7, playwright)
- [x] Merge `setup-*.md` commands into unified `setup/project.md` with language detection and appropriate setup
- [x] Combine `consult.md` and `resolve.md` into `todo/consult.md` focused on unblocking stuck tasks
- [x] Replace all `thinktank-wrapper` references with raw `thinktank instructions.txt ./src` or `gemini --prompt` commands
- [x] Merge `sync-project-commands.md` functionality into `setup/sync.md` for updating commands to match project state

## Phase 3: Command Standardization

- [x] Update every command to start with one-sentence purpose statement as first line
- [x] Remove all "CONTEXT" and "When to use" sections from commands - user knows when they're invoking
- [x] Standardize thinking directives: use "Think hard about", "Think very hard about", "Ultrathink about" appropriately
- [x] Ensure all commands use proper file references with `@BACKLOG.md`, `@TASK.md`, `@TODO.md`
- [x] Update bash command syntax to use `!command` format consistently

## Phase 4: Workflow Integration

- [x] Update `backlog/ideate.md` to append generated ideas directly to BACKLOG.md with proper formatting
- [x] Modify `task/plan.md` to read from BACKLOG.md and create detailed breakdowns in TASK.md
- [x] Create `task/ready.md` command to convert TASK.md items into actionable TODO.md entries
- [x] Ensure `todo/execute.md` properly updates task status markers: `[ ]` → `[~]` → `[x]`
- [x] Add `backlog/promote.md` to move items from BACKLOG.md → TASK.md for planning

## Phase 5: Special Commands

- [x] Preserve `meta/carmack.md` with enhanced ultrathinking about current approach and potential pivots
- [x] Keep `meta/chill.md` for stress reduction and perspective maintenance during difficult tasks
- [x] Create `meta/step-back.md` combining carmack/chill philosophy: "Ultrathink: Are we solving the right problem? What would an expert do differently?"
- [x] Ensure `analysis/debug.md` maintains parallel Task agent approach for comprehensive RCA
- [x] Update `git/pr.md` to include automatic PR description generation from commit history

## Phase 6: Cleanup & Documentation

- [x] Delete redundant commands after consolidation (all `add-*-mcp.md`, `setup-*.md`, duplicate backlog commands)
- [x] Update main `README.md` to reflect new namespace organization and consolidated command set
- [x] Create namespace README files (`backlog/README.md`, `task/README.md`, etc.) listing commands in each category
- [x] Remove all references to deprecated tools and outdated patterns
- [ ] Test complete workflow: backlog → task → todo → execute → push