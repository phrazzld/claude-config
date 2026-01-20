---
description: Full PR workflow from working directory to draft PR
---

# PR

Open a pull request from current branch state.

## What This Does

1. **Clean working dir** — Stage and commit any uncommitted changes with semantic message
2. **Understand context** — Read linked issue (from branch name or recent commits)
3. **Analyze changes** — Diff branch against main, understand all modifications
4. **Write description** — Title from issue, body explains what/why/how
5. **Open draft PR** — Create draft, link to issue, assign to me

## Execution

```bash
# Check for uncommitted changes
git status --porcelain

# If changes exist, create semantic commit
git add -A && git commit -m "$(generate semantic message from diff)"

# Push branch
git push -u origin HEAD

# Create PR
gh pr create --draft --title "$TITLE" --body "$BODY" --assignee @me
```

## Output

Return the PR URL.
