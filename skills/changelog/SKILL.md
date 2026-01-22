---
name: changelog
description: |
  Complete changelog and release notes infrastructure. Audits current state,
  implements missing components, and verifies the release pipeline works end-to-end.
argument-hint: "[focus area, e.g. 'LLM synthesis' or 'public page']"
---

# /changelog

Automated changelogs, semantic versioning, and user-friendly release notes. Audit, fix, verify—every time.

## What This Does

Examines your release infrastructure, identifies every gap, implements fixes, and verifies the full pipeline works. No partial modes. Every run does the full cycle.

## Process

### 1. Audit

Check what exists and what's broken:

```bash
# Configuration
[ -f ".releaserc.js" ] || [ -f ".releaserc.json" ] && echo "✓ semantic-release" || echo "✗ semantic-release"
[ -f "commitlint.config.js" ] || [ -f "commitlint.config.cjs" ] && echo "✓ commitlint" || echo "✗ commitlint"
grep -q "commit-msg" lefthook.yml 2>/dev/null && echo "✓ commit-msg hook" || echo "✗ commit-msg hook"

# GitHub Actions
[ -f ".github/workflows/release.yml" ] && echo "✓ release workflow" || echo "✗ release workflow"
grep -q "semantic-release" .github/workflows/release.yml 2>/dev/null && echo "✓ runs semantic-release" || echo "✗ doesn't run semantic-release"
grep -q "GEMINI_API_KEY" .github/workflows/release.yml 2>/dev/null && echo "✓ LLM synthesis configured" || echo "✗ LLM synthesis missing"

# Public page
ls app/changelog/page.tsx src/app/changelog/page.tsx 2>/dev/null && echo "✓ changelog page" || echo "✗ changelog page"

# Health
gh release list --limit 3 2>/dev/null || echo "✗ no releases"
```

**Commit history check:**
```bash
git log --oneline -10 | while read line; do
  echo "$line" | grep -qE "^[a-f0-9]+ (feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\(.+\))?: " || echo "NON-CONVENTIONAL: $line"
done
```

### 2. Plan

From audit findings, build remediation plan. Every project needs:

**Must have:**
- semantic-release configured with changelog, git, github plugins
- commitlint enforcing conventional commits
- Lefthook commit-msg hook running commitlint
- GitHub Actions workflow running semantic-release on push to main

**Should have:**
- LLM synthesis transforming technical changelog to user-friendly notes
- Public `/changelog` page fetching from GitHub Releases API
- RSS feed at `/changelog.xml` or `/changelog/rss`

### 3. Execute

**Fix everything.** Don't stop at a report.

**Installing semantic-release:**
```bash
pnpm add -D semantic-release @semantic-release/changelog @semantic-release/git @semantic-release/github
```

Create `.releaserc.js`:
```javascript
module.exports = {
  branches: ['main'],
  plugins: [
    '@semantic-release/commit-analyzer',
    '@semantic-release/release-notes-generator',
    ['@semantic-release/changelog', { changelogFile: 'CHANGELOG.md' }],
    ['@semantic-release/git', { assets: ['CHANGELOG.md', 'package.json'] }],
    '@semantic-release/github',
  ],
};
```

**Installing commitlint:**
```bash
pnpm add -D @commitlint/cli @commitlint/config-conventional
```

Create `commitlint.config.js`:
```javascript
module.exports = { extends: ['@commitlint/config-conventional'] };
```

Add to `lefthook.yml`:
```yaml
commit-msg:
  commands:
    commitlint:
      run: pnpm commitlint --edit {1}
```

**Creating release workflow:**
Create `.github/workflows/release.yml` per `changelog-setup` reference.

**Adding LLM synthesis:**
Create `scripts/synthesize-release-notes.mjs` that:
1. Fetches latest release from GitHub API
2. Sends changelog to Gemini 3 Flash
3. Gets user-friendly summary back
4. Updates release body via GitHub API

Configure `GEMINI_API_KEY` secret in GitHub.

**Creating public changelog page:**
Per `changelog-page`, create:
- `app/changelog/page.tsx` - Fetches from GitHub Releases API
- Groups releases by minor version
- No auth required (public page)
- RSS feed support

Delegate implementation to Codex where appropriate.

### 4. Verify

**Prove it works.** Not "config exists"—actually works.

**Commitlint test:**
```bash
echo "bad message" | pnpm commitlint
# Should fail

echo "feat: valid message" | pnpm commitlint
# Should pass
```

**Commit hook test:**
```bash
# Try to commit with bad message (should be rejected)
git commit --allow-empty -m "bad message"
# Should fail due to commitlint hook
```

**Release workflow test:**
If you can trigger a release:
1. Merge a PR with `feat:` or `fix:` commit
2. Watch GitHub Actions run
3. Verify:
   - Version bumped in package.json
   - CHANGELOG.md updated
   - GitHub Release created
   - Release notes populated (LLM synthesis ran)

**Public page test:**
- Navigate to `/changelog`
- Verify releases displayed
- Verify grouped by minor version
- Check RSS feed works

If any verification fails, go back and fix it.

## The Release Flow

```
Commit with conventional format (enforced by Lefthook)
       ↓
Push/merge to main
       ↓
GitHub Actions runs semantic-release
       ↓
Version bumped, CHANGELOG.md updated, GitHub Release created
       ↓
Post-release action triggers LLM synthesis
       ↓
Gemini 3 Flash transforms changelog → user notes
       ↓
Enhanced notes stored in GitHub Release
       ↓
Public /changelog page displays latest
```

## Key Principles

**Every merge is a release.** Web apps deploy on merge. Embrace frequent releases.

**Every change gets notes.** Even `chore:` commits become "Behind-the-scenes improvements."

**Group for readability.** Public page groups patches under their minor version.

**Auto-publish.** No human gate on LLM synthesis. Trust the pipeline.

## Default Stack

Assumes Next.js + TypeScript + GitHub. Adapts gracefully to other stacks.

## What You Get

When complete:
- semantic-release configured and working
- Conventional commits enforced (can't commit without format)
- GitHub Actions workflow for releases
- Gemini 3 Flash synthesis for user-friendly notes
- Public `/changelog` page
- RSS feed
- Verified end-to-end

User can:
- Merge a PR with conventional commit
- See automatic version bump
- See GitHub Release created
- See user-friendly notes synthesized
- View public changelog page
