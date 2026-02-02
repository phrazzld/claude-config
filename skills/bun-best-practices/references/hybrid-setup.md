# Hybrid Setup: Bun + pnpm

When full Bun migration isn't feasible, run both strategically.

## Use Case

```
monorepo/
├── apps/
│   ├── web/          # Next.js → pnpm (Vercel deployment)
│   └── mobile/       # Expo → pnpm (EAS requires Node)
├── packages/
│   └── shared/       # Shared code → pnpm (matches apps)
├── tools/
│   └── cli/          # Internal CLI → Bun (fast startup)
└── scripts/          # Build scripts → Bun (fast execution)
```

## Configuration

### Root package.json

```json
{
  "name": "monorepo",
  "private": true,
  "workspaces": [
    "apps/*",
    "packages/*"
  ],
  "scripts": {
    "dev": "turbo run dev",
    "build": "turbo run build",
    "test": "turbo run test",
    "cli": "bun tools/cli/index.ts",
    "scripts:deploy": "bun scripts/deploy.ts"
  }
}
```

### pnpm-workspace.yaml

Keep for pnpm-managed workspaces:

```yaml
packages:
  - 'apps/*'
  - 'packages/*'
```

### tools/cli/package.json

Separate package with Bun:

```json
{
  "name": "@myorg/cli",
  "private": true,
  "type": "module",
  "scripts": {
    "start": "bun index.ts"
  }
}
```

## Installation Strategy

```bash
# Main monorepo (pnpm)
pnpm install

# CLI tool (Bun)
cd tools/cli && bun install
```

Or in a setup script:

```bash
#!/usr/bin/env bash
# scripts/setup.sh

echo "Installing main dependencies with pnpm..."
pnpm install

echo "Installing CLI dependencies with Bun..."
cd tools/cli && bun install
```

## CI Configuration

```yaml
name: CI

jobs:
  main:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # pnpm for main apps
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: 'pnpm'

      - run: pnpm install --frozen-lockfile
      - run: pnpm test
      - run: pnpm build

  cli:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # Bun for CLI
      - uses: oven-sh/setup-bun@v2

      - working-directory: tools/cli
        run: bun install --frozen-lockfile

      - working-directory: tools/cli
        run: bun test
```

## When to Use Each

### Use pnpm for:

- Apps deployed to Vercel/Netlify (Node.js required)
- Mobile apps with Expo/EAS
- Packages shared with production apps
- Anything requiring maximum stability

### Use Bun for:

- Internal CLI tools (fast startup matters)
- Build/deploy scripts (fast execution)
- Development utilities
- Isolated tools that don't share deps with main apps

## Lockfile Management

Keep lockfiles separate:

```
monorepo/
├── pnpm-lock.yaml    # Main monorepo
├── tools/
│   └── cli/
│       └── bun.lock  # CLI only
└── scripts/
    └── bun.lock      # Scripts only (optional)
```

## Gotchas

### 1. Don't Mix in Same Workspace

Bad:
```
packages/
├── shared/           # Uses pnpm
│   └── bun.lock     # Also has Bun lockfile
```

Good:
```
packages/
├── shared/           # Uses pnpm only
tools/
├── cli/              # Uses Bun only
```

### 2. Shared Types

If CLI needs types from shared packages:

```typescript
// tools/cli/index.ts
import type { Config } from '../../packages/shared/src/types';
// Works without installing - just type imports
```

### 3. Consistent Scripts

Keep script behavior consistent regardless of runner:

```json
{
  "scripts": {
    "typecheck": "tsc --noEmit",
    "lint": "biome check .",
    "test": "vitest run"
  }
}
```

These work identically with `pnpm run` or `bun run`.

## Migration Path

1. **Start hybrid**: Keep pnpm for apps, add Bun for tools
2. **Validate**: Ensure everything works in CI
3. **Expand gradually**: Move more tooling to Bun as confidence grows
4. **Full migration**: When platform support improves, consider full Bun
