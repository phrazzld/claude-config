---
name: launch-assets
description: |
  Generate complete launch asset package by composing primitives.
  Runs: /product-hunt-kit, /og-hero-image, /announce, /app-screenshots (if mobile).
  Use when: preparing full launch, generating all marketing assets at once.
  Keywords: launch, assets, marketing, bundle, all assets.
argument-hint: "[product name]"
effort: high
---

# /launch-assets

All launch assets. One command.

## What This Orchestrates
1. /brand-init (if no brand.yaml) or /brand-builder (legacy, if no brand-profile.yaml)
2. /brand-compile (if brand.yaml exists, compile tokens)
3. /brand-assets (if brand.yaml exists, generate OG cards + social images)
4. /product-hunt-kit - PH launch copy + checklist
5. /og-hero-image - AI hero image for social
6. /announce - Multi-platform launch posts
7. /app-screenshots - if apps/mobile exists
Usage:
- `/launch-assets heartbeat`
- `/launch-assets caesar without screenshots`
Output:
```text
launch-assets/
  product-hunt-kit.md
  og-hero-[name].png
  announcements/
  screenshots/ (if mobile)
```
Order Matters:
Brand profile → Copy → Images → Distribution
Each step informs the next.
