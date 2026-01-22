---
name: stripe-assess
description: |
  Assess current Stripe integration state. Determines whether this is greenfield,
  partial, or complete integration. Run first before any other Stripe operation.
---

# Stripe Assessment

Determine the current state of Stripe integration in this project.

## Objective

Quickly understand what exists and what's missing. Output a structured assessment that downstream skills can act on.

## What to Check

**SDK & Dependencies**
- Is `stripe` package installed?
- What version? Is it current?

**Environment Configuration**
- Are STRIPE_* variables defined (in .env files, Convex, Vercel)?
- Do both dev and prod deployments have them?
- Any obvious issues (wrong prefixes, likely test keys in prod)?

**Code Presence**
- Webhook handlers exist?
- Checkout session creation?
- Subscription state management?
- Access control logic?

**External Configuration**
- Can you reach Stripe CLI? (`stripe --version`)
- Any webhook endpoints registered?

## Output

Produce a structured assessment:

```
STATE: [GREENFIELD | PARTIAL | COMPLETE]

SDK: [not installed | v{version}]
ENV: [none | dev-only | prod-only | both]
CODE: [none | partial | complete]
EXTERNAL: [unconfigured | configured]

GAPS:
- [List what's missing or broken]

RECOMMENDATION: [stripe-setup | stripe-fix | stripe-review]
```

## Adaptation

Default stack is Next.js + Convex + Vercel + Clerk. If you detect a different stack, note it and adapt your assessment accordingly. The concepts are the same; the file locations differ.

## Research First

Before assessing, check what version of Stripe SDK is current. Documentation changes. Use Gemini or web search to verify you're checking against current best practices.
