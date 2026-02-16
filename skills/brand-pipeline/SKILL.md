---
name: brand-pipeline
description: |
  Master orchestrator: brand-init → brand-compile → brand-assets.
  One command to go from zero to full brand system.
argument-hint: "[project-name]"
effort: high
---

# /brand-pipeline

Full brand system setup in one command.

## What This Does

Orchestrates the complete brand-as-code pipeline:
1. Create `brand.yaml` (if missing)
2. Compile to CSS/Tailwind/TypeScript tokens
3. Generate visual assets (OG cards, social images)

## Process

### Step 1: Brand Identity

Check for existing brand files:
- `brand.yaml` exists → skip to Step 2
- `brand-profile.yaml` exists → offer migration via `brand-kit migrate`
- Neither exists → run `/brand-init` interactively

### Step 2: Compile Tokens

```bash
node ~/Development/brand-kit/dist/src/cli.js compile --out ./src/styles
```

Verify output:
- `tokens.css` — CSS custom properties
- `theme.css` — Tailwind 4 @theme
- `tokens.ts` — TypeScript export

### Step 3: Integrate

Check project setup and wire tokens:
- If Tailwind project: verify `@import "./theme.css"` in CSS entry
- If TypeScript: verify tokens.ts is importable
- Run typecheck: `pnpm typecheck` or `npx tsc --noEmit`

### Step 4: Generate Assets

Determine needed assets from project context:
- Always: `og-default`
- If blog exists: `og-blog` + `blog-header`
- If launching: `launch-hero` + `social-announce`
- If changelog: `og-changelog`

```bash
node ~/Development/brand-kit/dist/src/cli.js render og-default \
  --title "[Brand Name]" --subtitle "[Tagline]" --out ./public/og.png
```

### Step 5: Summary

Report what was created:
- brand.yaml location
- Token output files
- Generated assets
- Integration status

## Flags

- `--skip-init` — Skip brand-init, require existing brand.yaml
- `--skip-assets` — Only compile tokens, skip asset generation
- `--out <dir>` — Override token output directory

## Related Skills

- `/brand-init` — Interactive brand discovery
- `/brand-compile` — Token compilation
- `/brand-assets` — Asset generation
- `/launch-assets` — Full launch package (uses brand-pipeline internally)
