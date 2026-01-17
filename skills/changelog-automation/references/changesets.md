# Changesets

**Best for:** Monorepos, teams wanting explicit change declarations, gradual adoption.

## Installation

```bash
pnpm add -D @changesets/cli
pnpm changeset init  # Creates .changeset directory
```

## Configuration

```json
// .changeset/config.json
{
  "$schema": "https://unpkg.com/@changesets/config@3.0.0/schema.json",
  "changelog": "@changesets/cli/changelog",
  "commit": false,
  "fixed": [],
  "linked": [],
  "access": "public",
  "baseBranch": "main",
  "updateInternalDependencies": "patch",
  "ignore": ["@repo/config", "@repo/tsconfig"]
}
```

## Workflow

### 1. Create Changeset

```bash
pnpm changeset
# Interactive prompts:
# - Select packages
# - Choose version bump (patch/minor/major)
# - Add description
```

Creates `.changeset/random-name.md`:

```markdown
---
"@repo/ui": minor
---

Added dark mode toggle component with theme persistence
```

### 2. Commit with Code

```bash
git add .changeset/random-name.md src/
git commit -m "feat: add dark mode toggle"
git push
```

### 3. Automated Release (GitHub Actions)

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    branches: [main]

concurrency: ${{ github.workflow }}-${{ github.ref }}

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile

      - uses: changesets/action@v1
        with:
          publish: pnpm release
          commit: "chore: version packages"
          title: "chore: version packages"
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
```

**What happens:**
1. Changesets merged to main → Creates "Version Packages" PR
2. PR updates package.json and CHANGELOG.md
3. Merge PR → Packages published automatically

### Manual Release

```bash
pnpm changeset version  # Bump versions
git add .
git commit -m "chore: version packages"
pnpm changeset publish  # Publish to npm
git push --follow-tags
```

## Package.json Scripts

```json
{
  "scripts": {
    "changeset": "changeset",
    "changeset:version": "changeset version",
    "release": "pnpm build && pnpm changeset publish"
  }
}
```

## Example Changeset Files

**Patch (bug fix):**
```markdown
---
"@repo/api": patch
---

Fixed race condition in authentication middleware
```

**Minor (new feature):**
```markdown
---
"@repo/ui": minor
"@repo/utils": patch
---

Added new DataTable component with sorting and filtering.
Updated formatDate utility to handle more formats.
```

**Major (breaking change):**
```markdown
---
"@repo/api": major
---

BREAKING: Renamed getUser() to fetchUser() for consistency.
Migration: Replace all getUser() calls with fetchUser().
```
