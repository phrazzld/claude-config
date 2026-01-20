---
description: Deliver GitHub issue end-to-end with CI verification
argument-hint: <issue-id>
---

# DELIVER

> From issue to green CI in one command.

Take Issue #$1 through full delivery: spec → design → build → PR → CI.

## Phase 1: Spec Check

```bash
gh issue view $1 --comments
```

Examine the issue and its comments. If no `## Product Spec` section exists, run `/product $1`.

## Phase 2: Design Check

Re-examine the issue comments. If no `## Technical Design` section exists, run `/architect $1`.

## Phase 3: Build

Run `/build $1`.

This handles:
- Branch creation (`feature/issue-$1` or `fix/issue-$1`)
- Semantic commits referencing issue
- Build/test/lint verification
- Final commit closes issue

## Phase 3.5: Pre-Deploy Verification

**MANDATORY for projects with external integrations (Stripe, Clerk, etc.).**

### For Stripe projects: Run `/billing-preflight`

This verifies:
- Webhook URLs don't redirect (CRITICAL - Stripe won't follow 307s)
- Env vars exist on production (not just dev)
- No trailing whitespace in secrets

**If `/billing-preflight` fails, FIX before proceeding. Do not skip.**

### Additional checks:

1. **Run config verification script** (if exists):
   ```bash
   ./scripts/verify-env.sh --prod-only 2>/dev/null || echo "No verification script"
   ```

2. **Document pre-deploy checklist in PR description**:
   - [ ] Env vars set on production (not just dev)
   - [ ] Webhook URLs use canonical domain (no redirects)
   - [ ] Health check endpoint exists and passes

## Phase 4: Ship

Run `/open-pr`.

This handles:
- Size and coverage checks
- Documentation staleness audit
- Draft PR creation with auto-description

## Phase 5: CI Verification

Run `/ci` and block until pass or fail.

- If CI passes: Proceed to completion
- If CI fails: Classify failure, fix if possible, re-run

## Completion

Report summary:

```markdown
## Delivery Complete: Issue #$1

**Spec**: [Created | Already existed]
**Design**: [Created | Already existed]
**Commits**: N semantic commits
**PR**: [URL]
**CI**: [Passed | Failed with reason]

Next: Await review. After feedback, run `/git-respond`.
```
