---
name: stripe-review
description: |
  Quick health check of Stripe integration.
  Composes: assess → audit → verify
  Lighter than stripe-fix — for routine checks.
---

# Stripe Review

Health check for a working Stripe integration.

## When to Use

Integration is working (or believed to be working). Just want to verify everything is still correct:
- Before a major deployment
- Periodic health check
- After infrastructure changes
- When something feels off but you're not sure what

## Workflow

This workflow composes primitives in sequence:

### 1. Assess

Run `stripe-assess` for quick state check:
- Confirm integration is complete
- Note any obvious gaps

### 2. Audit

Run `stripe-audit`:
- Configuration verification
- Webhook health
- Code patterns check
- Security scan
- Business model compliance

This is the same audit as `stripe-fix` but we expect it to mostly pass.

### 3. Verify

Run `stripe-verify`:
- Quick configuration check
- Test checkout flow
- Verify webhook delivery
- Spot-check subscription states

## Difference from stripe-fix

`stripe-fix` expects problems and includes reconcile step.
`stripe-review` expects health and skips reconcile.

If audit finds issues, recommend switching to `stripe-fix` workflow.

## Output

Health report:

```
STRIPE HEALTH CHECK
==================

Status: HEALTHY | NEEDS ATTENTION | CRITICAL

Summary:
- Configuration: ✓
- Webhooks: ✓
- Code patterns: ✓
- Security: ✓
- Business model: ✓

Verification:
- Checkout flow: ✓
- Webhook delivery: ✓
- State management: ✓

[If issues found]
Recommendation: Run /stripe-fix to address:
- [Issue 1]
- [Issue 2]
```

## When to Escalate

If review finds issues, don't try to fix inline. Recommend `stripe-fix` workflow for proper triage and reconciliation.
