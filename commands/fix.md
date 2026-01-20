---
description: Diagnose and fix errors with Codex delegation
argument-hint: <error>
---

# FIX

Diagnose and fix an error or bug. Strongly prefers delegating to Codex CLI.

## Argument

- `error` — Error message, stack trace, or bug description

## What This Does

1. **Diagnose** — Trace error to root cause
2. **Research** — Find similar issues, check docs
3. **Delegate fix to Codex** — Clear instructions with context
4. **Verify** — Run tests, confirm error is resolved
5. **Commit** — Semantic commit message

## Execution

```bash
# Trace error location
rg "$ERROR_PATTERN" --type ts -A 5

# Delegate to Codex
codex exec "FIX: $ERROR. Root cause: $DIAGNOSIS. Apply minimal fix. Run pnpm test after." \
  --output-last-message /tmp/codex-out.md 2>/dev/null

# Verify
pnpm test  # Confirm error resolved
pnpm typecheck && pnpm lint  # No regressions

# Commit
git add -A && git commit -m "fix: $DESCRIPTION"
```

## Diagnosis Approach

1. **Read the error** — Full stack trace, not just message
2. **Locate source** — Where does the error originate?
3. **Understand context** — What was the code trying to do?
4. **Hypothesize** — What could cause this failure?
5. **Test hypothesis** — Minimal change to verify

## Output

Error resolved, tests passing, commit created.
