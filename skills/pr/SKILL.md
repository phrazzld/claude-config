---
name: pr
description: |
  Full PR workflow from working directory to draft PR.
  Commits uncommitted changes, analyzes diff, writes description, opens draft.
  Use when: opening a pull request, shipping to review, creating PR.
effort: medium
---

# /pr

Open a pull request from current branch state.

## Role

Engineer shipping clean, well-documented PRs.

## Objective

Create a draft PR from current branch. Link to issue, explain what/why/how.

## Latitude

- Stage and commit any uncommitted changes with semantic message
- Read linked issue from branch name or recent commits
- Write PR body that explains decisions, not just changes

## PR Body Requirements (MANDATORY)

Every PR body must contain all six sections. A PR missing any section is not ready.

```
## Summary
What changed and why it matters. Not a diff recap — explain the significance.
Link to the issue. State the problem this solves or the capability this adds.

## Changes
Concise list of what was done. Reference key files/functions.

## Acceptance Criteria
Copied or derived from the linked issue. Checkboxes.

## Manual QA
Step-by-step instructions a reviewer can follow to verify the change works.
Include: setup steps, exact commands, expected output, URLs to visit.

## Before / After
Show the state before and after this PR. MANDATORY for every PR.

**Text**: Describe the previous behavior/state and the new behavior/state.
**Screenshots**: Include before and after screenshots for any user-facing change
(UI, CLI output, error messages, dashboards). Use `![before](url)` / `![after](url)`.

Skip screenshots ONLY when the change is purely internal (no visible output difference).
When in doubt, screenshot.

## Test Coverage
Pointers to specific test files and test functions that cover this change.
Note any gaps: what ISN'T tested and why.
```

## Workflow

1. **Clean** — Commit any uncommitted changes with semantic message
2. **Context** — Read linked issue, diff branch against main, identify relevant tests
3. **Describe** — Title from issue, body follows PR Body Requirements above (capture before state FIRST, before making changes if possible)
4. **Before/After** — Screenshot before state, apply changes, screenshot after state. For non-UI changes, describe behavioral difference in text.
5. **Open** — `gh pr create --draft --assignee phrazzld`
6. **Comment** — Add context comment if notable decisions were made

## Comment Style

Like a colleague leaving context for future-you:
- **Concise** — No fluff
- **High-context** — Reference files, functions, decisions
- **Useful** — What's not obvious from the diff?
- **Human** — Some wit welcome

## Output

PR URL.
