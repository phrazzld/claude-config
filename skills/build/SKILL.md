---
name: build
description: |
  Implement GitHub issue with semantic commits.
  Codex writes first draft, you review and ship.
  Use when: building a feature, implementing an issue, shipping code.
  Composes: Codex delegation, quality gates, ousterhout review.
argument-hint: <issue-id>
effort: high
---

# /build

Stop planning. Start shipping.

## Role

Senior engineer. Codex is your software engineer.

## Objective

Implement Issue #`$ARGUMENTS`. Ship working, tested, committed code on a feature branch.

## Latitude

- Delegate ALL work to Codex by default (investigation AND implementation)
- Keep only trivial one-liners where delegation overhead > benefit
- If Codex goes off-rails, re-delegate with better direction

## Startup

```bash
gh issue view $1 --comments
gh issue edit $1 --remove-label "status/ready" --add-label "status/in-progress" --add-assignee phrazzld
```

If on `master`/`main`, branch: `feature/issue-$1` or `fix/issue-$1`.

## Execution Loop

For each logical chunk:

1. **Delegate** — Codex with clear spec + pattern reference + verify command
2. **Review** — `git diff --stat && pnpm typecheck && pnpm lint && pnpm test`
3. **Commit** — `feat: description (#$1)` if tests pass
4. **Repeat** until complete

Final commit: `feat: complete feature (closes #$1)`

## Post-Implementation

1. `code-simplifier:code-simplifier` agent for clarity
2. `ousterhout` agent for module depth review
3. Commit simplifications separately

## Issue Comments

Leave breadcrumbs: starting work, decision points, scope creep, completion. Concise, high-context, useful, human.

## Output

Commits made, files changed, verification status.
