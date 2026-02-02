# CI/CD Patterns for Bun

## GitHub Actions

### Basic Setup

```yaml
name: CI

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: oven-sh/setup-bun@v2
        with:
          bun-version: latest

      - name: Install dependencies
        run: bun install --frozen-lockfile

      - name: Type check
        run: bun run typecheck

      - name: Lint
        run: bun run lint

      - name: Test
        run: bun test

      - name: Build
        run: bun run build
```

### With Caching

```yaml
- uses: oven-sh/setup-bun@v2
  with:
    bun-version: latest

- name: Cache Bun dependencies
  uses: actions/cache@v4
  with:
    path: ~/.bun/install/cache
    key: ${{ runner.os }}-bun-${{ hashFiles('**/bun.lock') }}
    restore-keys: |
      ${{ runner.os }}-bun-
```

### Matrix Testing

```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        bun-version: [latest, canary]
    steps:
      - uses: actions/checkout@v4
      - uses: oven-sh/setup-bun@v2
        with:
          bun-version: ${{ matrix.bun-version }}
      - run: bun install --frozen-lockfile
      - run: bun test
```

## Vercel Deployment

### Next.js with Bun Package Manager

```json
// vercel.json
{
  "installCommand": "bun install --frozen-lockfile",
  "buildCommand": "bun run build"
}
```

### Bun Runtime (Experimental)

```typescript
// app/api/route.ts
export const runtime = 'edge'; // or 'nodejs'

// For Bun runtime (when available):
// export const runtime = 'bun';
```

## Docker

### Multi-stage Build

```dockerfile
# Build stage
FROM oven/bun:1 AS builder
WORKDIR /app
COPY package.json bun.lock ./
RUN bun install --frozen-lockfile
COPY . .
RUN bun run build

# Production stage
FROM oven/bun:1-slim
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY package.json ./

EXPOSE 3000
CMD ["bun", "run", "dist/index.js"]
```

### Development Container

```dockerfile
FROM oven/bun:1

WORKDIR /app
COPY package.json bun.lock ./
RUN bun install

COPY . .

EXPOSE 3000
CMD ["bun", "run", "dev"]
```

## Fly.io

### fly.toml

```toml
app = "my-app"
primary_region = "iad"

[build]
  dockerfile = "Dockerfile"

[http_service]
  internal_port = 3000
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
```

## Common Patterns

### Frozen Lockfile in CI

Always use `--frozen-lockfile` in CI:

```yaml
- run: bun install --frozen-lockfile
```

Fails if lockfile would change, ensuring reproducible builds.

### Version Pinning

Pin Bun version in `package.json`:

```json
{
  "packageManager": "bun@1.1.0"
}
```

And in CI:

```yaml
- uses: oven-sh/setup-bun@v2
  with:
    bun-version: 1.1.0
```

### Comparing Against pnpm

Migration workflow - run both in parallel initially:

```yaml
jobs:
  pnpm:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - run: pnpm install --frozen-lockfile
      - run: pnpm test

  bun:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: oven-sh/setup-bun@v2
      - run: bun install --frozen-lockfile
      - run: bun test
```

Once Bun passes consistently, remove pnpm job.
