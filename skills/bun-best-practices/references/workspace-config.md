# Workspace Configuration: pnpm → Bun

## pnpm Workspace Structure

```yaml
# pnpm-workspace.yaml
packages:
  - 'apps/*'
  - 'packages/*'
  - 'tools/*'
```

```json
// package.json (pnpm)
{
  "name": "monorepo",
  "packageManager": "pnpm@9.0.0"
}
```

## Bun Workspace Structure

```json
// package.json (Bun)
{
  "name": "monorepo",
  "workspaces": [
    "apps/*",
    "packages/*",
    "tools/*"
  ]
}
```

No separate workspace file needed.

## Migration Steps

1. **Add workspaces to package.json:**
   ```json
   {
     "workspaces": ["apps/*", "packages/*"]
   }
   ```

2. **Remove pnpm-workspace.yaml:**
   ```bash
   rm pnpm-workspace.yaml
   ```

3. **Remove pnpm lockfile:**
   ```bash
   rm pnpm-lock.yaml
   ```

4. **Install with Bun:**
   ```bash
   bun install
   ```

5. **Update .gitignore:**
   ```diff
   - pnpm-lock.yaml
   + bun.lock
   ```

## Filter Commands

### pnpm
```bash
pnpm --filter @myorg/web run build
pnpm --filter "./apps/*" run test
```

### Bun
```bash
bun --filter @myorg/web run build
bun --filter "./apps/*" run test
```

Commands are largely compatible.

## Workspace Protocol

Both support `workspace:*` protocol:

```json
{
  "dependencies": {
    "@myorg/shared": "workspace:*"
  }
}
```

## Gotchas

### 1. Nested Workspaces

pnpm supports nested workspaces more robustly. If you have:
```
packages/
├── core/
│   └── packages/
│       └── nested/
```

Bun may require explicit listing:
```json
{
  "workspaces": ["packages/*", "packages/core/packages/*"]
}
```

### 2. Lockfile Format

Bun's `bun.lock` is binary by default. For readable diffs:
```bash
bun install --save-text-lockfile
```

Creates `bun.lockb` (binary) + `bun.lock` (text).

### 3. Package Manager Field

Update `packageManager` field:
```json
{
  "packageManager": "bun@1.1.0"
}
```

This ensures CI uses the correct version.
