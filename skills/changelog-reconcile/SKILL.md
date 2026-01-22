---
name: changelog-reconcile
description: |
  Fix issues found by changelog-audit.
  Reconciles configuration drift and missing components.
---

# Changelog Reconcile

Fix issues found by audit.

## Objective

Take the audit report and fix everything. Be systematic.

## Process

### 1. Parse Audit Report

Read the audit report from `changelog-audit`. Categorize issues:
- Configuration issues
- Missing components
- Workflow issues
- Secret issues

### 2. Fix Configuration Issues

**Invalid semantic-release config:**
- Check syntax errors
- Ensure all required plugins are listed
- Verify branch configuration matches actual branch names

**Missing commitlint config:**
```bash
# Create if missing
cat > commitlint.config.js << 'EOF'
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [2, 'always', [
      'feat', 'fix', 'docs', 'style', 'refactor',
      'perf', 'test', 'build', 'ci', 'chore', 'revert'
    ]],
    'subject-case': [2, 'always', 'lower-case'],
    'header-max-length': [2, 'always', 100],
  },
};
EOF
```

**Missing Lefthook hook:**
Add to `lefthook.yml`:
```yaml
commit-msg:
  commands:
    commitlint:
      run: pnpm commitlint --edit {1}
```

Then: `pnpm lefthook install`

### 3. Fix Missing Components

**Missing dependencies:**
```bash
# Check what's missing and install
pnpm add -D semantic-release @semantic-release/changelog @semantic-release/git @semantic-release/github
pnpm add -D @commitlint/cli @commitlint/config-conventional
```

**Missing synthesis script:**
Create `scripts/synthesize-release-notes.mjs` from template (see `references/llm-synthesis-script.md`).

**Missing release notes config:**
Create `.release-notes-config.yml` from template.

### 4. Fix Workflow Issues

**Missing or broken release workflow:**
Create/update `.github/workflows/release.yml` from template (see `references/github-actions-release.md`).

**Missing permissions:**
Ensure workflow has:
```yaml
permissions:
  contents: write
  issues: write
  pull-requests: write
```

**Missing fetch-depth:**
Ensure checkout step has:
```yaml
- uses: actions/checkout@v4
  with:
    fetch-depth: 0
```

**Missing synthesis job:**
Add the `synthesize-notes` job from template.

### 5. Fix Secret Issues

**Missing GEMINI_API_KEY:**
```bash
# Prompt user to add
echo "Add GEMINI_API_KEY to GitHub secrets:"
echo "  1. Go to https://aistudio.google.com/apikey"
echo "  2. Create or copy API key"
echo "  3. Run: gh secret set GEMINI_API_KEY"
```

**Missing NPM_TOKEN (if needed):**
```bash
echo "Add NPM_TOKEN to GitHub secrets:"
echo "  1. Go to https://www.npmjs.com/settings/~/tokens"
echo "  2. Create automation token"
echo "  3. Run: gh secret set NPM_TOKEN"
```

### 6. Fix Public Page Issues

**Missing changelog page:**
Run `changelog-page` to scaffold the page.

**Auth on changelog page:**
Remove any auth wrappers from the changelog route. It should be public.

**Missing RSS feed:**
Add RSS route from template.

### 7. Backfill Missing Releases

If commits exist that should have triggered releases but didn't:

```bash
# Option 1: Manually trigger release
pnpm semantic-release

# Option 2: Create manual release for missed versions
gh release create v1.2.3 --title "v1.2.3" --notes "Changelog catch-up release"
```

### 8. Verify Fixes

After fixing, run `changelog-verify` to confirm everything works.

## Output

Reconciliation report:

```
CHANGELOG RECONCILE REPORT
==========================

FIXED:
✓ Added missing commitlint config
✓ Updated Lefthook with commit-msg hook
✓ Created synthesis script
✓ Added GEMINI_API_KEY to workflow

REQUIRES MANUAL ACTION:
! Add GEMINI_API_KEY secret: gh secret set GEMINI_API_KEY
! Add NPM_TOKEN secret (if publishing to npm)

UNCHANGED (already correct):
- semantic-release config
- Release workflow structure

---
NEXT STEP: Run changelog-verify to confirm fixes
```

## Delegation

For complex fixes, delegate to Codex:
- Generating synthesis script
- Creating changelog page
- Updating complex workflow configurations

Use Gemini for research if unsure about current best practices.
