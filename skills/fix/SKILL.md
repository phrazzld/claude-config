---
name: fix
description: |
  Diagnose and fix errors with Codex delegation.
  Traces error to root cause, researches approach, delegates fix, verifies.
  Use when: bug reports, error messages, stack traces, test failures.
argument-hint: <error>
effort: high
---

# /fix

Diagnose. Delegate. Verify.

## Role

Senior engineer debugging a production or development issue.

## Objective

Fix the error described in `$ARGUMENTS`. Root cause, not symptom.

## Latitude

- Delegate fix to Codex with diagnosis context
- Research idiomatic approach before implementing
- Write failing test first when feasible

## Workflow

1. **Diagnose** — Read the full error, locate source, understand context, form hypothesis
2. **Research** — Find similar issues, check docs for idiomatic solution
3. **Delegate** — Codex with: root cause, minimal fix, run tests after
4. **Verify** — `pnpm test && pnpm typecheck && pnpm lint`
5. **Commit** — `fix: description`

## Key Question

After investigation, before fix: "Are we solving the root problem or treating a symptom?"

## Output

Error resolved, tests passing, commit created.
