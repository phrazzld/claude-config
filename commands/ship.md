---
description: Ship current branch - create PR and verify CI
allowed-tools: Bash(gh:*), Bash(git:*)
---

# SHIP

> PR + CI in one command.

Create pull request for current branch and wait for CI to pass.

Use this when you've built something manually (or without a tracked issue) and want to ship it.

## Phase 1: Create PR

Run `/git-pr`.

This handles:
- Size check (warn if >400 lines)
- Coverage check (warn if patch <80%)
- Documentation staleness audit
- Auto-generated title and description from commits
- Draft PR creation

## Phase 2: CI Verification

Run `/ci` and block until pass or fail.

- If CI passes: Report success
- If CI fails: Classify failure type (code/infra/flaky/config), propose fix, await user decision

## Completion

Report summary:

```markdown
## Ship Complete

**PR**: [URL]
**CI**: [Passed | Failed with classification]

Next: Await review. After feedback, run `/git-respond`.
```
