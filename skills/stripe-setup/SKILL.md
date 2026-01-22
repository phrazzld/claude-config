---
name: stripe-setup
description: |
  Full Stripe integration from scratch. Greenfield workflow.
  Composes: assess → design → scaffold → configure → verify
---

# Stripe Setup

Complete Stripe integration for a project that doesn't have one.

## When to Use

Project has no Stripe integration (or negligible fragments). Starting fresh.

## Workflow

This workflow composes primitives in sequence:

### 1. Assess (confirm greenfield)

Run `stripe-assess` to confirm this is actually greenfield. If partial integration exists, consider `stripe-fix` instead.

### 2. Design

Run `stripe-design` to create the integration plan:
- Reference `business-model-preferences` for constraints
- Research current Stripe best practices (use Gemini)
- Run design through Thinktank for validation
- Output: design document

### 3. Scaffold

Run `stripe-scaffold` with the design:
- Delegate code generation to Codex
- Generate all components (client, routes, handlers, state management)
- Run quality gates: typecheck, lint, test
- Output: working code

### 4. Configure

Run `stripe-configure`:
- Guide through Stripe Dashboard setup
- Set env vars on all deployments (local, Convex dev, Convex prod, Vercel)
- Verify webhook URL accessibility
- Output: configuration checklist

### 5. Verify

Run `stripe-verify` (deep mode):
- Test real checkout flow
- Verify webhook delivery
- Test subscription state transitions
- Verify access control
- Check business model compliance
- Output: verification report

## Quality Gate

Do not consider setup complete until `stripe-verify` passes. Billing is critical infrastructure — no shortcuts.

## Handoff

When complete, the project should have:
- Working checkout flow
- Webhook handling with signature verification
- Subscription state management
- Access control based on subscription status
- All configuration in place (dev and prod)
- Verified end-to-end

User should be able to:
- Test a real checkout with test card
- See subscription state update
- Access gated features as subscriber
- See access blocked when not subscribed
