# Quality Gates Implementation Plan

## Problem Statement

Database credentials (`config/database.env`) were committed to git history because:
1. No git hooks configured (only `.sample` files in `.git/hooks/`)
2. No secret scanning (gitleaks, trufflehog, etc.)
3. `.gitignore` pattern `.env*` doesn't catch `config/*.env` (subdirectory)

## Scope for This Branch

Add basic quality gates to prevent future credential leaks:

1. **Fix .gitignore** - catch env files in all directories
2. **Install Lefthook** - fast, modern git hooks (per skill recommendation)
3. **Configure gitleaks** - already installed at `/opt/homebrew/bin/gitleaks`
4. **Pre-commit hooks** - lint, typecheck, gitleaks scan
5. **Pre-push hooks** - full test suite

---

## Implementation

### 1. Update .gitignore

Add these patterns to catch env files everywhere:

```gitignore
# env files - catch in all directories
.env*
**/*.env
**/database.env
*.env.*

# secrets
*.pem
*.key
**/secrets/**
```

### 2. Install Lefthook

```bash
pnpm add -D lefthook
pnpm lefthook install
```

### 3. Create lefthook.yml

```yaml
# lefthook.yml
pre-commit:
  parallel: true
  commands:
    gitleaks:
      run: gitleaks protect --staged --verbose
      # Scans staged files for secrets before commit

    lint:
      glob: "*.{js,ts,jsx,tsx}"
      run: pnpm eslint {staged_files} --max-warnings=0

    typecheck:
      glob: "*.{ts,tsx}"
      run: pnpm type-check

pre-push:
  commands:
    typecheck:
      run: pnpm type-check
      # Fast ~5s check, CI handles full test suite
```

### 4. Create .gitleaks.toml (optional customization)

```toml
# .gitleaks.toml
title = "sploot gitleaks config"

[allowlist]
description = "Global allowlist"
paths = [
  '''\.test\.ts$''',
  '''\.spec\.ts$''',
  '''vitest\.setup\.ts$''',
]

# Allow test database credentials (CI-only, ephemeral)
regexes = [
  '''postgres:postgres@localhost''',
]
```

### 5. Add npm scripts

```json
{
  "scripts": {
    "prepare": "lefthook install",
    "secrets:check": "gitleaks detect --verbose"
  }
}
```

The `prepare` script ensures Lefthook installs automatically after `pnpm install`.

---

## Files to Create/Modify

| File | Action |
|------|--------|
| `.gitignore` | Add env patterns |
| `package.json` | Add lefthook + scripts |
| `lefthook.yml` | Create (git hooks config) |
| `.gitleaks.toml` | Create (secret scanning config) |

## Verification

After implementation:

```bash
# Test gitleaks catches secrets
echo "password=secret123" > test-secret.txt
git add test-secret.txt
git commit -m "test"  # Should fail with gitleaks error
rm test-secret.txt

# Verify hooks are active
ls -la .git/hooks/pre-commit  # Should exist (not .sample)
```

## Out of Scope (Future)

- Commitlint for conventional commits
- PR size labeling
- CI/CD workflow updates
- Branch protection rules
- Codecov integration
