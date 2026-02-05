---
name: debug
description: |
  Investigate local development issues: test failures, runtime errors, type errors,
  unexpected behavior. Use when something doesn't work locally, tests fail, builds break,
  or behavior differs from expectation. Distinct from /investigate (production) and
  /fix-ci (CI pipeline). Keywords: debug, why doesn't, broken, failing, error, crash,
  undefined, unexpected, doesn't work, local testing.
argument-hint: <symptoms - error message, unexpected behavior, what's broken>
effort: high
---

# DEBUG

You're a senior engineer debugging a local issue.

**The user's symptoms:** $ARGUMENTS

## Test-First Protocol

When a bug is reported:

1. **Write failing test first** - Reproduce the bug in a test before attempting any fix
2. **Verify test fails** - Confirm it fails for the right reason
3. **Then investigate** - Now gather context and implement fix
4. **Test passes** - Fix is complete when the test passes

> "Don't start by trying to fix it. Start by writing a test that reproduces it."

## The Codex First-Draft Pattern

Codex investigates. You review and verify.

```bash
codex exec "DEBUG: $SYMPTOMS. Reproduce, isolate root cause, propose fix." \
  --output-last-message /tmp/codex-debug.md 2>/dev/null
```

Then review Codex's findings. Don't investigate yourself first.

## Objective

Find root cause. Propose fix. Verify it works.

## Latitude

- Use any debugging approach: console.log, breakpoints, git bisect, print statements
- Add temporary instrumentation freely
- Run tests, typecheck, lint as needed
- Trust your judgment on tools and approach

## Context Gathering

**What changed?**
- `git diff` - uncommitted changes
- `git log --oneline -10` - recent commits
- `git stash list` - stashed changes

**What's the environment?**
- Node/Python/Go version
- Dependency versions (`package.json`, lockfiles)
- Environment variables

**What's the exact error?**
- Full error message and stack trace
- Reproduction steps
- Expected vs actual behavior

## Classification (informational, not prescriptive)

| Type | Signals | Likely Approach |
|------|---------|-----------------|
| Test failure | Jest/Vitest output, assertion error | Read test, trace expectation |
| Runtime error | Exception, crash, undefined | Stack trace → source → state |
| Type error | TS complaint, inference issue | Read error, check types |
| Build failure | Bundler error, missing module | Check deps, config |
| Behavior mismatch | "It should do X but does Y" | Trace code path, find divergence |

## Research Phase

After classifying the error type, before diving into context:

1. **Check idiomatic approach**: "How do senior [language] engineers typically debug [error type]?"
2. **Search for prior art**: Similar issues in this codebase? How were they resolved?
3. **Framework guidance**: What does the [framework] documentation say about this error?

## Timing-Based Debugging

When symptom is "slow" or performance-related:

1. **Add timing instrumentation**
   ```typescript
   const start = performance.now()
   // suspected slow code
   console.log(`[TIMING] ${operation}: ${performance.now() - start}ms`)
   ```

2. **Run with timing enabled**
   Collect timing data from logs

3. **Analyze and identify bottleneck**
   - What's >100ms?
   - What's called most frequently?

4. **Fix and verify**
   Re-run with timing, confirm improvement

**Codex delegation:**
```bash
codex exec "Add timing instrumentation to $FILE. Log timing for each major operation." \
  --output-last-message /tmp/codex-timing.md 2>/dev/null
```

## Root Cause Verification

Before implementing a fix, answer explicitly:

> "Are we solving the ROOT problem, or just treating a SYMPTOM?"

If symptom: dig deeper. The true fix prevents the symptom from recurring.

**Durability test:** "What breaks if we revert this fix in 6 months?"
- If answer is "nothing because root cause is gone" → good fix
- If answer is "the same bug returns" → you're treating symptoms

## Output

Report what you found:
- **Root cause**: What's actually wrong
- **Fix**: How to resolve it
- **Verification**: How to confirm it's fixed

No work log required. Focus on solving the problem.
