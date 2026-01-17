# Semantic-release

**Best for:** Single packages, teams committed to conventional commits, fully automated releases.

## Installation

```bash
pnpm add -D semantic-release @semantic-release/git @semantic-release/changelog
```

## Configuration

```javascript
// .releaserc.js
module.exports = {
  branches: ['main'],
  plugins: [
    '@semantic-release/commit-analyzer',
    '@semantic-release/release-notes-generator',
    '@semantic-release/changelog',
    '@semantic-release/npm',
    [
      '@semantic-release/git',
      {
        assets: ['package.json', 'CHANGELOG.md'],
        message: 'chore(release): ${nextRelease.version} [skip ci]\n\n${nextRelease.notes}',
      },
    ],
    '@semantic-release/github',
  ],
}
```

## Conventional Commits

**Required format:**
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types that trigger releases:**
- `feat`: New feature → MINOR
- `fix`: Bug fix → PATCH
- `perf`: Performance → PATCH
- `BREAKING CHANGE:` in footer → MAJOR

**Types that don't trigger releases:**
- `docs`, `style`, `refactor`, `test`, `chore`

**Examples:**

```bash
# Patch (1.0.0 → 1.0.1)
git commit -m "fix: resolve authentication timeout issue"

# Minor (1.0.0 → 1.1.0)
git commit -m "feat: add dark mode support"

# Major (1.0.0 → 2.0.0)
git commit -m "feat: redesign API

BREAKING CHANGE: Renamed all get* methods to fetch*"

# No release
git commit -m "docs: update README"
```

## GitHub Actions

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    branches: [main]

jobs:
  release:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      issues: write
      pull-requests: write

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          persist-credentials: false

      - uses: pnpm/action-setup@v2
      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: 'pnpm'

      - run: pnpm install --frozen-lockfile
      - run: pnpm build

      - name: Release
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
        run: pnpm semantic-release
```

## Advantages

- Fully automated (no manual version bumping)
- Commit-based (version from messages)
- Consistent (enforces conventions)
- Rich integrations (GitHub, npm, Slack)

## Disadvantages

- Strict commits required
- Less control over version bump
- Monorepos need extra config
- Can't defer releases
