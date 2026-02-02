---
description: Full code review → fix → quality → PR workflow
---

# REVIEW-AND-FIX

Thin orchestrator for the common "code complete → PR ready" flow.

## Usage

```
/review-and-fix              # Full flow: review → fix → quality → pr
/review-and-fix no-pr        # Stop after fixes, don't create PR
/review-and-fix verify       # Re-review after fixes
```

## Workflow

```
┌─────────────────────────────────────────────────────────────┐
│ /review-and-fix (Thin Orchestrator)                         │
│   Chains: review-branch → address-review → check-quality → pr│
├─────────────────────────────────────────────────────────────┤
│ PRIMITIVES                                                  │
├──────────────────┬──────────────────┬───────────────────────┤
│ /review-branch   │ /address-review  │ /respond              │
│ ~12 reviewers    │ TDD fix workflow │ Human PR feedback     │
│ parallel exec    │ GitHub issues    │ Radical transparency  │
└──────────────────┴──────────────────┴───────────────────────┘
```

### Step 1: Review Branch

Run `/review-branch` to get comprehensive multi-reviewer findings.

**Output:** Prioritized action plan with Critical, Important, Suggestion items.

### Step 2: Address Review

Run `/address-review` to systematically fix findings.

**In-scope items:** TDD workflow (failing test → fix → passing test → commit)
**Out-of-scope items:** Create GitHub issues

### Step 3: Verify Quality

Run quality gates:

```bash
pnpm typecheck && pnpm lint && pnpm test
```

If any fail, fix and repeat Step 3.

### Step 4: Optional Re-Review (verify mode)

If `verify` flag set or Critical items were found:
- Run `/review-branch` again
- Confirm all Critical/Important items resolved
- Loop back to Step 2 if new issues found

### Step 5: Create PR (unless no-pr)

Run `/pr` to create draft PR.

## Decision Points

### When to use `verify` mode

- Large PRs (>300 lines)
- Security-sensitive code
- Critical findings were addressed
- You want confidence before requesting human review

### When to use `no-pr` mode

- Still iterating on the feature
- Want to review changes locally first
- CI will be triggered by PR creation

## Output Summary

At completion, display:

```markdown
## Review & Fix Summary

### Review
- **Reviewers:** 10 (Grug, Carmack, Ousterhout, Beck, Fowler, security-sentinel, performance-pathfinder, data-integrity-guardian, architecture-guardian, hindsight-reviewer)
- **Findings:** X Critical, Y Important, Z Suggestions

### Fixes Applied
| Finding | Commit | Test |
|---------|--------|------|
| `file:line` - [issue] | abc1234 | ✅ |

### Issues Created
| Finding | Issue |
|---------|-------|
| [deferred item] | #123 |

### Quality Gates
- [x] typecheck
- [x] lint
- [x] test (X passed, Y new)

### PR
- **URL:** https://github.com/org/repo/pull/456
- **Status:** Draft
```

## Philosophy

**Every PR should be better than "just works."**

This workflow ensures:
1. Multiple expert perspectives reviewed the code
2. Critical issues are fixed with tests proving the fix
3. Non-critical issues are tracked (not forgotten)
4. Quality gates pass before human review

The goal: minimize back-and-forth in human code review by catching issues early.
