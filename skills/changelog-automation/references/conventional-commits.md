# Conventional Commits

Enforce commit format for both Changesets and semantic-release.

## Commitlint Setup

```bash
pnpm add -D @commitlint/cli @commitlint/config-conventional
```

```javascript
// commitlint.config.js
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2,
      'always',
      [
        'feat',     // New feature
        'fix',      // Bug fix
        'docs',     // Documentation
        'style',    // Formatting
        'refactor', // Code refactoring
        'perf',     // Performance
        'test',     // Tests
        'build',    // Build system
        'ci',       // CI configuration
        'chore',    // Maintenance
        'revert',   // Revert commit
      ],
    ],
    'scope-case': [2, 'always', 'kebab-case'],
    'subject-case': [2, 'always', 'sentence-case'],
    'header-max-length': [2, 'always', 72],
  },
}
```

## Lefthook Integration

```yaml
# lefthook.yml
commit-msg:
  commands:
    commitlint:
      run: pnpm commitlint --edit {1}
```

## Validation Examples

```bash
git commit -m "add new feature"
# Error: subject may not be empty [subject-empty]

git commit -m "feat: add dark mode"
# Success
```

## Commit Types

| Type | Description | Release |
|------|-------------|---------|
| `feat` | New feature | MINOR |
| `fix` | Bug fix | PATCH |
| `perf` | Performance | PATCH |
| `docs` | Documentation | None |
| `style` | Formatting | None |
| `refactor` | Refactoring | None |
| `test` | Tests | None |
| `build` | Build system | None |
| `ci` | CI config | None |
| `chore` | Maintenance | None |
| `revert` | Revert | Depends |

## Breaking Changes

Add `BREAKING CHANGE:` in commit footer:

```
feat: redesign authentication API

BREAKING CHANGE: Renamed getUser() to fetchUser() for consistency.
All existing code must update method calls.
```

This triggers a MAJOR version bump.
