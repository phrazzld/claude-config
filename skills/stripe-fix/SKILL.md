---
name: stripe-fix
description: |
  Fix existing Stripe integration issues.
  Composes: assess → audit → reconcile → verify
---

# Stripe Fix

Repair an existing Stripe integration that has issues.

## When to Use

Project has Stripe integration but something's wrong:
- Configuration drift (dev/prod mismatch)
- Webhook failures
- Subscription bugs
- Missing edge case handling
- Security issues
- Business model violations

## Workflow

This workflow composes primitives in sequence:

### 1. Assess

Run `stripe-assess` to understand current state:
- What exists?
- What's the integration level?
- Any obvious gaps?

Confirm this is a fix scenario (partial/complete state, not greenfield).

### 2. Audit

Run `stripe-audit` for deep analysis:
- Spawn `stripe-auditor` subagent for parallel analysis
- Run automated audit script
- Check all domains: configuration, webhooks, logic, security, business model
- Run findings through Thinktank for validation
- Output: findings report with severity levels

### 3. Reconcile

Run `stripe-reconcile` to fix issues:
- Configuration fixes: do directly
- Code fixes: delegate to Codex
- Verify each fix immediately
- Re-audit to confirm resolution

Iterate if needed — some fixes may reveal other issues.

### 4. Verify

Run `stripe-verify` (deep mode):
- Full end-to-end testing
- All subscription state transitions
- Edge cases (idempotency, failures)
- Access control verification
- Business model compliance

## Quality Gate

Do not consider fixed until `stripe-verify` passes. If verification reveals new issues, loop back to reconcile.

## Common Scenarios

**Configuration drift**
- Env vars set on dev but not prod
- Webhook URL changed, Stripe Dashboard not updated
- Test keys in prod, live keys in dev

**Webhook issues**
- URL redirects (Stripe doesn't follow)
- Missing signature verification
- Events not subscribed
- No idempotency handling

**Subscription bugs**
- Trial not honored on upgrade
- Zombie trials after subscription
- Wrong access control logic
- Missing edge cases

**Security issues**
- Hardcoded keys
- Secrets in logs
- Missing signature verification

## Handoff

When complete:
- All audit findings addressed
- Verification passes
- User can test checkout and see it work end-to-end
