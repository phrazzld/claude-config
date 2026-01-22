# Lefthook Commit Hook Configuration

Configure Lefthook to run commitlint on commit-msg.

## Adding to Existing lefthook.yml

If you already have Lefthook configured (e.g., for pre-commit hooks), add the commit-msg section:

```yaml
# lefthook.yml

# Existing pre-commit hooks
pre-commit:
  parallel: true
  commands:
    lint:
      glob: "*.{js,ts,tsx}"
      run: pnpm eslint --fix {staged_files}
    format:
      glob: "*.{js,ts,tsx,json,md}"
      run: pnpm prettier --write {staged_files}
    typecheck:
      run: pnpm typecheck

# Add this section for conventional commits
commit-msg:
  commands:
    commitlint:
      run: pnpm commitlint --edit {1}
```

## Fresh Lefthook Setup

If starting fresh:

```yaml
# lefthook.yml

commit-msg:
  commands:
    commitlint:
      run: pnpm commitlint --edit {1}

pre-commit:
  parallel: true
  commands:
    lint:
      glob: "*.{js,ts,tsx}"
      run: pnpm eslint --fix {staged_files}
    format:
      glob: "*.{js,ts,tsx,json,md}"
      run: pnpm prettier --write {staged_files}
    typecheck:
      run: pnpm typecheck

pre-push:
  commands:
    test:
      run: pnpm test
    build:
      run: pnpm build
```

## Installation

```bash
# Install Lefthook
pnpm add -D lefthook

# Install hooks
pnpm lefthook install
```

## Verification

Test that the hook is installed:

```bash
# Should show commit-msg hook
ls -la .git/hooks/commit-msg

# Test with a bad commit (should fail)
git commit --allow-empty -m "bad commit message"

# Test with a good commit (should pass)
git commit --allow-empty -m "test: verify commitlint hook"

# Undo test commit
git reset HEAD~1
```

## Troubleshooting

**Hook not running:**
```bash
# Reinstall hooks
pnpm lefthook install

# Check hook exists
cat .git/hooks/commit-msg
```

**Wrong pnpm version:**
```bash
# Make sure pnpm is in PATH
which pnpm

# Or use npx
run: npx commitlint --edit {1}
```

**Bypass in emergency:**
```bash
# Skip hooks (use sparingly!)
git commit --no-verify -m "fix: emergency hotfix"
```

## Integration with Quality Gates

This hook integrates with the `quality-gates` skill. Full Lefthook configuration is documented there. The commit-msg hook is the addition for changelog automation.
