---
description: Create a new git worktree for parallel development with automatic environment setup
---

Create isolated git worktree for parallel branch development.

# GIT WORKTREE CREATE

Create new worktree with automatic environment initialization. Provides filesystem isolation for true parallel development without git checkout thrashing.

## Intent

Set up new worktree with:
- New or existing branch
- Copied environment files (.env, .env.local, .env.development)
- **Fresh dependency install** via `pnpm install`
- Configured git hooks

## What It Does

**Create Worktree:**
- Determine worktree path: `../$PROJECT-worktree-$BRANCH_NAME`
- Create worktree with new branch: `git worktree add -b $BRANCH_NAME $PATH`
- Or checkout existing branch: `git worktree add $PATH $BRANCH_NAME`

**Environment Setup:**
- Copy environment files if they exist
- Run `pnpm install` for isolated dependencies
- Install git hooks with `lefthook install`
- Report location and next steps

## Workflow Example

```bash
# In main project
/git-worktree-create feature/auth

# Output shows path: ../myproject-worktree-feature-auth

# Open NEW terminal window
cd ../myproject-worktree-feature-auth
claude

# Work in isolated environment
/execute             # Implement tasks
/git-pr              # Create PR

# Each worktree = separate Claude session
# Main project continues unaffected
```

## Use Cases

**Parallel Features:**
Work on multiple features simultaneously without branch switching
```bash
/git-worktree-create feature/auth
/git-worktree-create feature/payments
# Work on both in separate terminals
```

**Hotfix During Feature Work:**
Fix production bug without interrupting main work
```bash
# Main session: Continue feature work
# New worktree: Quick hotfix
/git-worktree-create hotfix/critical-bug
```

**Stacked PRs:**
Build dependent PRs while base is under review
```bash
/git-worktree-create feature/base     # Base PR
/git-worktree-create feature/dependent  # Dependent PR
```

## Key Insights

**No Command Awareness Needed:**
Each worktree runs in separate Claude session with own filesystem. All commands (`/execute`, `/git-pr`, `/debug`) work without modification.

**True Parallelism:**
- Main branch: Continue feature work
- Worktree 1: Review PR
- Worktree 2: Hotfix
- No stashing, no context switching

**Environment Isolation:**
Each worktree has:
- Own .env files (copied)
- Own node_modules (fresh install)
- Own git hooks
- Own running servers (different ports if configured)

## Common Issues

**Worktree directory already exists:**
```bash
# Remove directory first
rm -rf $WORKTREE_DIR
/git-worktree-create $BRANCH_NAME
```

**Dependencies not working:**
```bash
# Clear and reinstall
cd $WORKTREE_DIR
rm -rf node_modules
pnpm install
```

**Git hooks not running:**
```bash
cd $WORKTREE_DIR
lefthook install
```

## Cleanup

When done with worktree:
```bash
/git-worktree-cleanup
```

## Related Commands

- `/git-worktree-review` - Review PR in isolated worktree
- `/git-worktree-cleanup` - Remove stale worktrees
- `/git-pr` - Create PR (works in worktree)
- `/execute` - Implement tasks (works in worktree)
