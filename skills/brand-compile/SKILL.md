---
name: brand-compile
description: |
  Compile brand.yaml into CSS custom properties, Tailwind 4 theme, and TypeScript tokens.
  Run after modifying brand.yaml or when setting up a new project.
argument-hint: "[--format css|tailwind|ts|all] [--out dir]"
effort: low
---

# /brand-compile

Compile brand tokens from `brand.yaml` into consumable formats.

## What This Does

Reads `brand.yaml` from project root and produces:
- `tokens.css` — CSS custom properties (`:root` + `.dark`)
- `theme.css` — Tailwind 4 `@theme inline` with OKLCH values
- `tokens.ts` — TypeScript const export for Satori templates and Remotion

## Process

1. Locate `brand.yaml` in the current project root
2. If no `brand.yaml` exists, check for `brand-profile.yaml` + `design-tokens.json` and offer to migrate:
   ```bash
   node ~/Development/brand-kit/dist/src/cli.js migrate --profile brand-profile.yaml --tokens design-tokens.json --out brand.yaml
   ```
3. Validate the schema:
   ```bash
   node ~/Development/brand-kit/dist/src/cli.js validate brand.yaml
   ```
4. Compile tokens:
   ```bash
   node ~/Development/brand-kit/dist/src/cli.js compile --out ./src/styles
   ```
5. Verify Tailwind `@theme` import exists in the project's CSS entry point (e.g., `globals.css`)
6. Run typecheck if TypeScript project: `pnpm typecheck` or `npx tsc --noEmit`

## Output

Default output directory: `./brand-output/`
Override with `--out ./src/styles` to place tokens where your project expects them.

```
brand-output/
  tokens.css    # CSS custom properties
  theme.css     # Tailwind 4 @theme inline
  tokens.ts     # TypeScript const export
```

## Format Selection

- `--format css` — Only CSS custom properties
- `--format tailwind` — Only Tailwind 4 theme
- `--format ts` — Only TypeScript tokens
- `--format all` — All three (default)

## Integration

After compiling, import in your project:

**Tailwind 4 (recommended):**
```css
/* globals.css */
@import "tailwindcss";
@import "./theme.css";
```

**Plain CSS:**
```css
@import "./tokens.css";
```

**TypeScript (Satori/Remotion):**
```typescript
import { brand } from "./tokens.js";
```

## Related Skills

- `/brand-init` — Create brand.yaml from scratch
- `/brand-assets` — Generate OG cards and social images
- `/og-card` — Legacy OG card generation (superseded by brand-assets)
