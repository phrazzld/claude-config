---
description: Code generation with Codex delegation
argument-hint: <task>
---

# IMPLEMENT

Implement a feature or task. Strongly prefers delegating to Codex CLI.

## Argument

- `task` — Description of what to implement, or GitHub issue ID

## Decision: Delegate or Keep?

**Delegate to Codex (default):**
- Clear spec or existing pattern to follow
- Writing tests, boilerplate, CRUD
- Implementation matches established conventions

**Keep for yourself only when:**
- Deep context already loaded AND task is trivial (<10 lines)
- Complex integration across unfamiliar systems

When in doubt, delegate.

## What This Does

1. **Understand task** — Read issue/spec, find existing patterns
2. **Prepare delegation** — Clear instructions with pattern references
3. **Delegate to Codex** — High reasoning level by default
4. **Validate** — Run typecheck, lint, tests
5. **Commit** — Semantic commit message

## Execution

```bash
# Find pattern to follow
rg "similar pattern" --type ts -l | head -3

# Delegate to Codex
codex exec "IMPLEMENT $TASK. Follow pattern in $REFERENCE. Run pnpm typecheck && pnpm test after." \
  --output-last-message /tmp/codex-out.md 2>/dev/null

# Validate
git diff --stat
pnpm typecheck && pnpm lint && pnpm test

# Commit
git add -A && git commit -m "feat: $DESCRIPTION"
```

## Pre-Delegation Checklist

1. Does target file have existing tests? → Warn Codex: "Don't break tests in [file]"
2. Add to or replace? → Be explicit: "ADD to this file" vs "REPLACE"
3. What patterns to follow? → Include: "Follow pattern in [reference]"
4. What quality gates? → Include: "Run pnpm typecheck after"

## Output

Files modified, tests passing, commit created.
