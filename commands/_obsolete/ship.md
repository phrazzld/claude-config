---
description: Ship current branch - create PR and verify CI
---

# SHIP

> PR + CI in one command.

Create pull request for current branch and wait for CI to pass.

Use this when you've built something manually (or without a tracked issue) and want to ship it.

## Phase 0: Pre-Deploy Verification

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

## Phase 1: Create PR

Run `/open-pr`.

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
