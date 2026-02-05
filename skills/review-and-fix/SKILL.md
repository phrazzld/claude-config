---
name: review-and-fix
description: |
  Full code review, fix, quality, PR workflow.
  Chains review-branch, address-review, check-quality, and pr.
  Use when: code complete and ready for PR, want comprehensive review before shipping.
effort: high
---

# /review-and-fix

Code complete to PR ready in one command.

## Role

Thin orchestrator chaining review primitives.

## Objective

Take current branch from "code complete" to "PR ready" with comprehensive review, fixes, and quality gates.

## Latitude

- Run full review pipeline or skip steps with flags
- Loop back for re-review if Critical items found
- Create GitHub issues for out-of-scope findings

## Usage

```
/review-and-fix              # Full flow
/review-and-fix no-pr        # Stop after fixes
/review-and-fix verify       # Re-review after fixes
```

## Workflow

1. **Review** — `/review-branch` (~12 reviewers, parallel)
2. **Fix** — `/address-review` (TDD: failing test, fix, passing test, commit)
3. **Quality** — `pnpm typecheck && pnpm lint && pnpm test`
4. **Re-review** — If `verify` flag or Critical items found, loop to step 1
5. **Ship** — `/pr` (unless `no-pr`)

## Output

Summary: reviewers consulted, findings by severity, fixes applied, issues created, quality gates, PR URL.
