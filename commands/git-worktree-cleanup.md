---
description: Remove stale git worktrees and clean up orphaned references
---

Clean up stale worktrees and prune git references.

# GIT WORKTREE CLEANUP

Remove inactive worktrees safely with intelligent recommendations. Detects merged, stale, and orphaned worktrees.

## Intent

Clean up worktrees systematically:
1. List all worktrees
2. **Detect status for all worktrees IN PARALLEL** (merged, active, stale, orphaned)
3. Present interactive selection with smart recommendations
4. Safely remove selected worktrees with uncommitted change protection
5. Prune orphaned git references

## Key Optimization

**Run status detection for all worktrees concurrently** rather than sequentially. Each worktree requires multiple git operations (check merge status, get last commit, check for changes). Parallel processing scales O(N) → O(1), providing 30-40% speedup with 5+ worktrees.

## What It Does

**Detect Status (Parallel):**
For each worktree, determine:
- **MERGED**: Branch merged to main (safe to remove)
- **ACTIVE**: Recent commits within 7 days (keep)
- **STALE**: No activity >7 days (consider removing)
- **ORPHANED**: Directory missing but git ref remains (force remove)

**Interactive Selection:**
```
Found 3 worktrees:

[ ] ../project-worktree-feature-auth
    Branch: feature/auth
    Status: ACTIVE (last commit 2 hours ago)

[✓] ../project-worktree-pr-123
    Branch: review/pr-123
    Status: MERGED (PR merged 3 days ago)
    Disk: 450MB

[✓] ../project-worktree-hotfix-bug
    Branch: hotfix/critical-bug
    Status: STALE (last commit 14 days ago)
    Disk: 450MB

Remove selected? [y/N]
```

**Safe Removal:**
- Check for uncommitted changes before removal
- Offer to stash changes if detected
- Never remove main/master/develop branches
- Report disk space freed

## Workflow Example

```bash
# After PR merged or weekly cleanup
/git-worktree-cleanup

# Review recommendations and select worktrees to remove
# Confirms and removes safely

# Output:
✅ Removed 2 worktrees
✅ Freed 900MB disk space
✅ Pruned 2 orphaned references
```

## Cleanup Modes

**Conservative (Default):**
- Suggests only merged/stale worktrees
- Asks for confirmation
- Checks for uncommitted changes
- Safe for regular use

**Aggressive (--all):**
- Suggests all non-main worktrees
- Still asks for confirmation
- Useful for fresh start

**Automatic (--force):**
- No confirmations, immediate removal
- Use with caution

## Constraints

- **Protected branches**: Never suggest removing main/master/develop or current branch
- **Uncommitted changes**: Check before removal, offer stash option
- **Safety first**: Confirm before destructive operations
- **Parallel detection**: Process all worktrees concurrently for speed

## Common Issues

**"Worktree is locked" error:**
```bash
# Force remove locked worktree
git worktree remove --force $WORKTREE_DIR
```

**Directory exists but git doesn't see it:**
```bash
# Manual cleanup
rm -rf $WORKTREE_DIR
git worktree prune
```

**Can't remove current worktree:**
You can't remove the worktree you're in. Switch to main project first.

**Disk space not freed:**
Run `du -sh node_modules` to verify size. May need to manually `rm -rf node_modules` if removal failed.

## Safety Features

**Uncommitted Changes Protection:**
- Detect uncommitted work before removal
- Show changes with `git status --short`
- Offer to create safety stash
- Stash stored in main repo: `git stash list`

**Branch Protection:**
Never suggest removing:
- main, master, develop
- Current branch (the one you're working in)

## Cleanup

Prune orphaned references after removal:
```bash
git worktree prune
```

## Related Commands

- `/git-worktree-create` - Create new worktree
- `/git-worktree-review` - Review PR in worktree
- `git worktree list` - List all worktrees
- `git worktree prune` - Clean refs only
