---
name: changelog-assess
description: |
  Assess current state of changelog/release infrastructure.
  Determines if project needs setup, fix, or is healthy.
---

# Changelog Assess

Understand the current state of release infrastructure.

## Objective

Determine what exists and what's missing. Output a state assessment that tells the orchestrator which workflow to run.

## Process

### 1. Check for semantic-release

```bash
# Package installed?
grep -q "semantic-release" package.json && echo "INSTALLED" || echo "NOT INSTALLED"

# Config exists?
ls .releaserc* 2>/dev/null || ls release.config.* 2>/dev/null || echo "NO CONFIG"
```

**Alternative:** Check for Changesets (acceptable if already in use)
```bash
ls .changeset/config.json 2>/dev/null && echo "CHANGESETS DETECTED"
```

### 2. Check for Conventional Commits Enforcement

```bash
# commitlint installed?
grep -q "@commitlint" package.json && echo "COMMITLINT INSTALLED" || echo "NO COMMITLINT"

# commitlint config exists?
ls commitlint.config.* 2>/dev/null || ls .commitlintrc* 2>/dev/null || echo "NO COMMITLINT CONFIG"

# Lefthook configured with commit-msg hook?
grep -q "commit-msg" lefthook.yml 2>/dev/null && echo "LEFTHOOK COMMIT HOOK" || echo "NO COMMIT HOOK"
```

### 3. Check for GitHub Actions

```bash
# Release workflow exists?
ls .github/workflows/release.yml 2>/dev/null || \
ls .github/workflows/release.yaml 2>/dev/null || \
echo "NO RELEASE WORKFLOW"

# Check if it runs semantic-release
grep -q "semantic-release" .github/workflows/release.* 2>/dev/null && \
echo "WORKFLOW RUNS SEMANTIC-RELEASE" || echo "WORKFLOW DOES NOT RUN SEMANTIC-RELEASE"
```

### 4. Check for LLM Synthesis

```bash
# Release notes config exists?
ls .release-notes-config.yml 2>/dev/null || \
ls .release-notes-config.yaml 2>/dev/null || \
echo "NO LLM CONFIG"

# GitHub Action for synthesis exists?
grep -q "gemini" .github/workflows/*.yml 2>/dev/null && \
echo "GEMINI ACTION FOUND" || echo "NO GEMINI ACTION"

# Check for GEMINI_API_KEY reference
grep -q "GEMINI_API_KEY" .github/workflows/*.yml 2>/dev/null && \
echo "GEMINI KEY REFERENCED" || echo "NO GEMINI KEY REFERENCE"
```

### 5. Check for Public Changelog Page

```bash
# Next.js app router
ls app/changelog/page.tsx 2>/dev/null || \
ls src/app/changelog/page.tsx 2>/dev/null || \
echo "NO CHANGELOG PAGE (app router)"

# Next.js pages router
ls pages/changelog.tsx 2>/dev/null || \
ls src/pages/changelog.tsx 2>/dev/null || \
echo "NO CHANGELOG PAGE (pages router)"

# RSS feed
ls app/changelog.xml/route.ts 2>/dev/null || \
ls public/changelog.xml 2>/dev/null || \
echo "NO RSS FEED"
```

### 6. Check Recent Releases

```bash
# Any GitHub releases?
gh release list --limit 5 2>/dev/null || echo "NO RELEASES (or no gh CLI)"

# Any git tags?
git tag --list --sort=-creatordate | head -5 || echo "NO TAGS"

# CHANGELOG.md exists and has content?
test -s CHANGELOG.md && echo "CHANGELOG.md EXISTS" || echo "NO CHANGELOG.md"
```

## Output

State assessment report:

```
CHANGELOG INFRASTRUCTURE ASSESSMENT
===================================

VERSIONING
├── semantic-release: [INSTALLED | NOT INSTALLED]
├── Config: [FOUND | MISSING]
└── Alternative (Changesets): [DETECTED | NOT DETECTED]

COMMIT ENFORCEMENT
├── commitlint: [INSTALLED | NOT INSTALLED]
├── Config: [FOUND | MISSING]
└── Lefthook hook: [CONFIGURED | NOT CONFIGURED]

CI/CD
├── Release workflow: [FOUND | MISSING]
└── Runs semantic-release: [YES | NO]

LLM SYNTHESIS
├── Config: [FOUND | MISSING]
├── GitHub Action: [FOUND | MISSING]
└── API key reference: [FOUND | MISSING]

PUBLIC PAGE
├── Changelog route: [FOUND | MISSING]
└── RSS feed: [FOUND | MISSING]

RELEASE HISTORY
├── GitHub releases: [N releases | NONE]
├── Git tags: [N tags | NONE]
└── CHANGELOG.md: [EXISTS | MISSING]

---
STATE: [GREENFIELD | PARTIAL | COMPLETE]
RECOMMENDED: [changelog-setup | changelog-audit → changelog-reconcile | changelog-audit]
```

## State Definitions

**GREENFIELD:** No semantic-release, no release workflow, no changelog infrastructure. Start from scratch.

**PARTIAL:** Some components exist but incomplete. Missing critical pieces (no commit enforcement, no LLM synthesis, no public page). Needs fixes.

**COMPLETE:** All components present. May still have issues, but structure is there. Run audit to check health.

## Decision Matrix

| semantic-release | CI workflow | LLM synthesis | Public page | State |
|------------------|-------------|---------------|-------------|-------|
| ✗ | ✗ | ✗ | ✗ | GREENFIELD |
| ✓ | ✗ | ✗ | ✗ | PARTIAL |
| ✓ | ✓ | ✗ | ✗ | PARTIAL |
| ✓ | ✓ | ✓ | ✗ | PARTIAL |
| ✓ | ✓ | ✓ | ✓ | COMPLETE |

If Changesets detected instead of semantic-release, assess that setup instead. Don't force migration if it's working.
