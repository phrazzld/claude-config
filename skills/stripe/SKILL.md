---
name: stripe
description: |
  Complete Stripe lifecycle management. Assesses current state and routes
  to appropriate workflow: setup (greenfield), fix (issues), or review (health check).
argument-hint: "[setup | fix | review]"
---

# /stripe

World-class Stripe integration, from zero to production.

## What This Does

Assesses your project's Stripe integration state and runs the appropriate workflow:

| State | Workflow | What Happens |
|-------|----------|--------------|
| No Stripe | `stripe-setup` | Design → scaffold → configure → verify |
| Has issues | `stripe-fix` | Audit → reconcile → verify |
| Healthy | `stripe-review` | Audit → verify |

## Usage

```
/stripe              # Auto-detect and run appropriate workflow
/stripe setup        # Force greenfield workflow
/stripe fix          # Force fix workflow
/stripe review       # Health check
```

Arguments are passed as `$ARGUMENTS`. Interpret naturally - "setup", "from scratch", "new integration" all mean greenfield. "fix", "repair", "there are issues" all mean fix workflow.

## Process

### 1. Assess

First, understand what exists:
- Is Stripe SDK installed?
- Are env vars configured?
- Does webhook handling exist?
- What's the integration level?

### 2. Route

Based on assessment:

**GREENFIELD** (no integration)
→ Run `stripe-setup` workflow
→ Design the integration with business model preferences
→ Scaffold all code (delegate to Codex)
→ Configure Stripe Dashboard and all deployments
→ Deep verification

**PARTIAL or HAS ISSUES** (broken/incomplete)
→ Run `stripe-fix` workflow
→ Deep audit (spawn auditor subagent)
→ Reconcile all findings
→ Deep verification

**COMPLETE and HEALTHY**
→ Run `stripe-review` workflow
→ Audit for drift
→ Verify still working
→ Report health status

### 3. Execute

Run the selected workflow. Each workflow composes primitives:
- `stripe-assess` — understand state
- `stripe-design` — plan integration
- `stripe-scaffold` — generate code
- `stripe-configure` — set up services
- `stripe-audit` — find issues
- `stripe-reconcile` — fix issues
- `stripe-verify` — prove it works

### 4. Quality Gate

Every workflow ends with `stripe-verify`. Nothing is complete until verification passes.

## Key Principles

**Research first.** Before implementing anything, check current Stripe best practices. Use Gemini for documentation. Patterns change.

**Delegate aggressively.** Code generation goes to Codex. Deep analysis goes to the auditor subagent. Expert validation goes to Thinktank.

**Verify deeply.** Billing bugs are expensive. Test real flows, not just check code existence.

**Business model compliance.** Reference `business-model-preferences` throughout. Single tier, trial completion on upgrade, no freemium.

## Default Stack

Assumes Next.js + TypeScript + Convex + Vercel + Clerk. If different stack detected, adapt gracefully — the Stripe concepts are the same, only framework specifics change.

## What You Get

When complete:
- Working checkout flow
- Webhook handling with signature verification
- Subscription state management with proper trial handling
- Access control based on subscription status
- All configuration in place (dev and prod)
- Deep verification passing

User can:
- Run test checkout with 4242 4242 4242 4242
- See subscription state update
- Access gated features
- See trial honored on mid-trial upgrade
