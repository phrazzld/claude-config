---
description: Review a GitHub pull request in an isolated git worktree with full environment setup
---

Review PR in isolated worktree without disrupting main work.

# GIT WORKTREE REVIEW

Checkout a GitHub pull request into an isolated worktree for review. Full environment setup with automated validation checks.

## Intent

Set up PR review environment with:
1. Fetch PR branch from GitHub
2. Create isolated worktree with proper environment
3. Install dependencies (isolated, not symlinked for safety)
4. **Run validation checks IN PARALLEL** (typecheck + lint + test)
5. Report results and provide review context

## Key Optimization

**Run all validation checks concurrently** rather than sequentially. These checks are independent and represent the slowest part of setup (~40-90s combined). Running in parallel can reduce total time by 30-40%.

## What It Does

**Fetch & Setup:**
- Use `gh pr view` to get PR details (number, title, actual branch name from `headRefName`)
- Fetch using actual branch name (e.g., `scoring-min-floor-fix`, NOT `pr-{number}`)
- Create worktree with meaningful name: `../{project}-worktree-{branch-name}`
- Copy environment files (.env, .env.local, .env.test)
- Run `pnpm install` (isolated dependencies for review safety)
- Setup git hooks if present (e.g., `lefthook install`)

**Validate (Parallel):**
Run these checks concurrently:
- TypeScript compilation (`pnpm run typecheck`)
- Linting (`pnpm run lint`)
- Test suite (`pnpm run test`)

**Report:**
- PR details (number, title, location)
- Check results (pass/fail for each)
- Next steps for review

## Workflow Example

```bash
# From main project (continue working normally)
/git-worktree-review 123

# Output shows: ../myproject-worktree-feature-branch-name

# Open NEW terminal window
cd ../myproject-worktree-feature-branch-name
claude

# Review in isolated environment
/groom              # Comprehensive review with all agents
git diff main       # Review code changes

# Leave feedback on GitHub
gh pr review 123 --approve --body "LGTM! Nice work on error handling."

# When done
exit                # Exit Claude session
cd ../myproject
/git-worktree-cleanup  # Remove review worktree
```

## Review Process

**Automated Review:**
Use `/groom` to run comprehensive audit with 16 specialized agents in parallel:
- complexity-archaeologist (design quality)
- security-sentinel (vulnerabilities)
- performance-pathfinder (bottlenecks)
- test-strategy-architect (coverage)
- ... and 12 more specialists

**Manual Review:**
- Code clarity and naming
- Documentation updates
- Breaking changes handling
- Test coverage for new code

**Leave Feedback:**
```bash
# Approve
gh pr review $PR_NUM --approve --body "Comments..."

# Comment (no approval)
gh pr review $PR_NUM --comment --body "Suggestions..."

# Request changes
gh pr review $PR_NUM --request-changes --body "Issues found..."
```

## Constraints

- **Isolated dependencies**: Always run `pnpm install` (never symlink for PR review)
- **Safety first**: Check PR source and permissions before reviewing
- **Parallel validation**: Run typecheck + lint + test concurrently
- **Clear results**: Report pass/fail for each validation check

## Common Issues

**PR fetch fails:**
Check gh CLI authentication: `gh auth status`

**Dependencies won't install:**
Clear cache and retry: `rm -rf node_modules pnpm-lock.yaml && pnpm install`

**Tests fail in worktree but pass locally:**
Check environment differences: `diff .env ../$MAIN_PROJECT/.env`
Verify ports aren't conflicting

**Can't push changes:**
You may lack write access. Instead suggest changes via comment:
`gh pr comment $PR_NUM --body "Suggestion: $(git diff)"`

## Cleanup

When done reviewing:
```bash
/git-worktree-cleanup
# Select the worktree by branch name to remove
```

## Related Commands

- `/git-worktree-create` - Create worktree for new branch
- `/git-worktree-cleanup` - Remove stale worktrees
- `/groom` - Comprehensive code audit (use during review)
