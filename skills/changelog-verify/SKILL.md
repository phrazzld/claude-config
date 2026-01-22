---
name: changelog-verify
description: |
  End-to-end verification of changelog infrastructure.
  Tests commit enforcement, release flow, LLM synthesis, and public page.
---

# Changelog Verify

Comprehensive end-to-end verification. Prove it works, don't assume.

## Objective

Verify the entire release pipeline functions correctly. Not "config looks right" — actually works.

## Process

### 1. Commit Enforcement Verification

**Test that commitlint rejects bad commits:**
```bash
# This should FAIL
echo "bad commit message" | pnpm commitlint
# Expected: error about format

# This should PASS
echo "feat: add new feature" | pnpm commitlint
# Expected: no errors
```

**Test Lefthook integration:**
```bash
# Verify hook is installed
ls .git/hooks/commit-msg

# Test with actual commit (in test branch)
git checkout -b test-commitlint
echo "test" > test-file.txt
git add test-file.txt

# This should fail
git commit -m "bad message" 2>&1 | grep -q "commitlint" && echo "HOOK WORKING" || echo "HOOK NOT WORKING"

# This should succeed
git commit -m "test: verify commitlint hook"

# Cleanup
git checkout main
git branch -D test-commitlint
```

### 2. Local Release Dry Run

**Test semantic-release locally (dry run):**
```bash
# Dry run - shows what would happen without actually releasing
pnpm semantic-release --dry-run

# Expected output:
# - Version that would be released
# - Commits that would be included
# - Changelog that would be generated
```

### 3. GitHub Actions Workflow Verification

**Check workflow syntax:**
```bash
# Validate workflow YAML
gh workflow view release.yml

# Check recent workflow runs
gh run list --workflow=release.yml --limit 5
```

**Verify workflow triggers:**
- Push a test commit to a feature branch
- Create PR to main
- Merge PR
- Verify workflow runs

**Check workflow outputs:**
```bash
# Get latest run
RUN_ID=$(gh run list --workflow=release.yml --limit 1 --json databaseId -q '.[0].databaseId')

# View run details
gh run view $RUN_ID

# Check for release job success
gh run view $RUN_ID --json jobs -q '.jobs[] | select(.name=="release") | .conclusion'

# Check for synthesis job (if release happened)
gh run view $RUN_ID --json jobs -q '.jobs[] | select(.name | contains("synthesize")) | .conclusion'
```

### 4. Release Creation Verification

**Check recent releases:**
```bash
# List releases
gh release list --limit 5

# View latest release
gh release view --json tagName,name,body,createdAt

# Verify release has:
# - Tag name (semantic version)
# - Release title
# - Body (should have LLM-synthesized notes)
```

**Verify CHANGELOG.md updated:**
```bash
# Check CHANGELOG.md has recent entry
head -50 CHANGELOG.md

# Verify version matches latest release
LATEST_TAG=$(gh release view --json tagName -q '.tagName')
grep -q "$LATEST_TAG" CHANGELOG.md && echo "CHANGELOG IN SYNC" || echo "CHANGELOG OUT OF SYNC"
```

### 5. LLM Synthesis Verification

**Check release notes quality:**
```bash
# Get release body
BODY=$(gh release view --json body -q '.body')

# Check it's not just raw commits
echo "$BODY" | grep -qE "^[a-f0-9]+ " && echo "WARNING: Raw commits in notes" || echo "Notes appear synthesized"

# Check for user-friendly language
echo "$BODY" | grep -qiE "feature|improvement|fix|update|better|faster|easier" && echo "User-friendly language found" || echo "WARNING: May not be user-friendly"
```

**Test synthesis script directly:**
```bash
# Run synthesis on latest release (if script supports it)
GEMINI_API_KEY=test node scripts/synthesize-release-notes.mjs --dry-run
```

### 6. Public Page Verification

**Page renders:**
```bash
# Start dev server (or use production URL)
# Then check page loads
curl -s http://localhost:3000/changelog | grep -q "changelog\|release" && echo "PAGE RENDERS" || echo "PAGE BROKEN"

# Or with production URL
curl -s https://your-app.com/changelog | head -100
```

**Page shows releases:**
```bash
# Check page contains recent release info
curl -s http://localhost:3000/changelog | grep -q "$(gh release view --json tagName -q '.tagName')" && echo "SHOWS LATEST RELEASE" || echo "MISSING LATEST RELEASE"
```

**RSS feed works:**
```bash
# Check RSS feed
curl -s http://localhost:3000/changelog.xml | head -20

# Validate RSS format
curl -s http://localhost:3000/changelog.xml | grep -q "<rss\|<feed" && echo "RSS VALID" || echo "RSS INVALID"
```

**Page is public (no auth):**
```bash
# Access without auth headers
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/changelog
# Expected: 200 (not 401 or 302)
```

### 7. End-to-End Flow Test

**Full cycle test:**
1. Create a test commit with `feat:` prefix
2. Push to main (or merge PR)
3. Wait for GitHub Actions
4. Verify new release created
5. Verify LLM notes in release body
6. Verify public page shows new release

```bash
# Quick E2E test (if you have a test branch setup)
echo "// test change $(date)" >> src/test-file.ts
git add src/test-file.ts
git commit -m "feat: add test feature for verification"
git push origin main

# Wait for workflow
sleep 60

# Check release
gh release view --json tagName,body
```

## Output

Verification report:

```
CHANGELOG VERIFICATION REPORT
=============================

COMMIT ENFORCEMENT
✓ commitlint rejects bad commits
✓ commitlint accepts good commits
✓ Lefthook hook installed and working

SEMANTIC RELEASE
✓ Dry run succeeds
✓ Configuration valid
✓ Plugins load correctly

GITHUB ACTIONS
✓ Workflow syntax valid
✓ Recent runs successful
✓ Release job completes
✓ Synthesis job completes

RELEASE CREATION
✓ Releases being created
✓ Tags follow semver
✓ CHANGELOG.md in sync

LLM SYNTHESIS
✓ Release notes populated
✓ Notes are user-friendly (not raw commits)
⚠ Could not test synthesis script directly (no API key in env)

PUBLIC PAGE
✓ Page renders at /changelog
✓ Shows latest releases
✓ RSS feed valid
✓ No auth required

---
STATUS: VERIFIED

All critical components working. Ready for production use.
```

## Failure Handling

If verification fails:
1. Document what failed
2. Check logs for errors
3. Route back to `changelog-reconcile` for fixes
4. Re-verify after fixes

## When to Run

- After `changelog-setup` (new infrastructure)
- After `changelog-reconcile` (fixes applied)
- Before relying on the pipeline for production releases
- Periodically as health check
