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
5. **Open draft PR** — Create draft, link to issue, assign to Phrazzld
6. **Add context comment** — If notable decisions were made, add a PR comment

## Comment Style

Write comments like a colleague leaving context for future-you. Be:
- **Concise** — No fluff. Get to the point.
- **High-context** — Reference specific files, functions, decisions
- **Useful** — What's not obvious from the diff? What might bite someone later?
- **Human** — Some wit is welcome. "Refactored for clarity" is boring. "This abstraction was fighting me—now it submits peacefully" lands better.

Good comment: "Had to plumb `userId` through three layers because the hook was eating it. Consider moving auth context higher if this keeps happening."

Bad comment: "Made some changes to the authentication system."

## Execution

```bash
# Check for uncommitted changes
git status --porcelain

# If changes exist, create semantic commit
git add -A && git commit -m "$(generate semantic message from diff)"

# Push branch
git push -u origin HEAD

# Create PR
gh pr create --draft --title "$TITLE" --body "$BODY" --assignee phrazzld
```

## Output

Return the PR URL.
