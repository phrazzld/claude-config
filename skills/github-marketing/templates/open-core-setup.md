# Open Core Setup (MIT Core + Commercial)

Goal: free core stays useful, paid tier adds real leverage, no trust break.

## 1) Define the Boundary

Core should include:
- Core workflow, local dev, single-user use
- Stable API and migration path

Commercial should include:
- Team/enterprise needs (SSO, audit, RBAC)
- Scale features (multi-tenant, HA)
- Managed services or hosted SaaS

## 2) Repo Layout

Recommended:
```
repo/
  packages/core/            # MIT
  packages/cli/             # MIT
  packages/pro/             # Commercial
  packages/enterprise/      # Commercial
  docs/                     # MIT
```

## 3) Licenses

- `LICENSE` in repo root: MIT for core
- `LICENSE-PRO` in paid packages
- Add headers in paid source files if required

## 4) Feature Gating

- Use feature flags or license checks in paid packages
- Avoid hard-coded checks in core
- Keep core build clean without paid deps

## 5) Legal + Policy

- Add `COMMERCIAL_TERMS.md` for paid usage
- Add `TRADEMARK.md` for logo/name restrictions
- Add `CONTRIBUTING.md` with CLA/DCO policy

## 6) Docs + Messaging

- README clearly shows free vs paid
- Pricing page references open core
- “What’s free forever” section

## 7) Release Strategy

- Core is open, tagged, changelogged
- Paid release notes in same cadence
- Avoid private-only security fixes in core

## 8) Governance

- Publish a public roadmap
- Define maintainer rules
- Set response time expectations

## Checklist

- [ ] Boundary documented
- [ ] Licenses in place
- [ ] Paid code isolated
- [ ] README updated
- [ ] Terms + trademark files added
