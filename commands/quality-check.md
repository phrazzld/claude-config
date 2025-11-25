---
description: Verify project quality standards and infrastructure completeness before deployment
---

# QUALITY-CHECK

> **THE FRIDAY AFTERNOON TEST**
>
> *"Can I merge to production Friday at 5pm and turn my phone off?"*
>
> If the answer is NO, quality gates are missing. This command finds what's blocking supremely confident deployments.

> **QUALITY GATE CHECKPOINT**
> - **Deployment Confidence**: All checks green = production ready, zero manual verification needed
> - **Infrastructure Validation**: Ensure logging, error tracking, quality gates operational
> - **Build Confidence**: Verify tests pass, types check, build succeeds
> - **Design Consistency**: Validate design tokens, brand elements, accessibility
> - **Release Readiness**: Confirm changelog automation, version strategy

You're the quality gatekeeper enabling fearless deployments. This verification runs before critical workflow transitions (pre-PR, pre-deploy, post-setup). Every missing gate = weekend on-call risk.

## Your Mission

Systematically verify project quality standards and infrastructure completeness. Report findings with actionable fixes.

## When to Run /quality-check

**Workflow Checkpoints**:
- ✅ After initial project setup → Validate infrastructure baseline
- ✅ Before creating PR → Ensure quality standards met
- ✅ Before merging to main → Final gate before production path
- ✅ After major refactoring → Confirm nothing broke
- ✅ Periodic audits → Catch drift from standards

## Optional: Research Current Best Practices

Before running checks, consider researching latest quality standards:
```bash
gemini "What are current best practices for quality infrastructure in [framework] projects in 2025?
Include: testing strategies, linting, CI/CD, error tracking, logging"
```
Gemini's web grounding provides latest tooling recommendations and emerging patterns.

## Verification Categories

### 1. Quality Gates (Critical)

**Check for**:
```bash
# Lefthook configuration exists and is complete
[ -f lefthook.yml ]

# Pre-commit hooks configured
grep -q "pre-commit:" lefthook.yml
grep -q "lint:" lefthook.yml
grep -q "format:" lefthook.yml
grep -q "typecheck:" lefthook.yml

# Pre-push hooks configured
grep -q "pre-push:" lefthook.yml
grep -q "test:" lefthook.yml

# CI/CD pipeline exists
[ -f .github/workflows/ci.yml ]

# GitHub branch protection (manual check - report requirement)
```

**Pass Criteria**:
- lefthook.yml exists with pre-commit (lint, format, typecheck) and pre-push (test) hooks
- GitHub Actions CI workflow configured for pull requests
- Branch protection recommended for main branch

**If Missing**:
Apply `quality-gates` skill → Create lefthook.yml and .github/workflows/ci.yml

---

### 2. Structured Logging (Important)

**Check for**:
```bash
# Logger utility exists
[ -f utils/logger.ts ] || [ -f lib/logger.ts ] || [ -f src/logger.ts ]

# Pino dependency installed
grep -q "pino" package.json

# Logger includes redaction patterns
grep -q "redact" utils/logger.ts || grep -q "redact" lib/logger.ts

# Logger used in codebase (not just console.log)
git grep -q "logger\." src/
```

**Pass Criteria**:
- Centralized logger utility with Pino
- Sensitive data redaction configured (password, token, apiKey)
- Logger actively used in codebase
- Correlation ID support present

**If Missing**:
Apply `structured-logging` skill → Create utils/logger.ts with Pino, redaction, correlation IDs

---

### 3. Error Tracking (Important)

**Check for**:
```bash
# Sentry dependency installed
grep -q "@sentry/nextjs\\|@sentry/node\\|@sentry/react" package.json

# Sentry configuration exists
[ -f sentry.client.config.ts ] || [ -f sentry.server.config.ts ] || [ -f utils/sentry.ts ]

# SENTRY_DSN in environment
grep -q "SENTRY_DSN" .env.local || grep -q "SENTRY_DSN" .env.example

# Source maps configured
grep -q "sourcemaps" next.config.js || grep -q "sentry" next.config.js
```

**Pass Criteria**:
- Sentry SDK installed and configured
- SENTRY_DSN environment variable documented
- Source maps enabled for production debugging
- Sensitive data redaction in beforeSend hook

**If Missing**:
Install @sentry/nextjs → Configure sentry.*.config.ts → Update next.config.js for source maps

---

### 4. Design System (Frontend Projects)

**Check for**:
```bash
# Tailwind CSS installed
grep -q "tailwindcss" package.json

# Design tokens in CSS (@theme directive - Tailwind 4)
grep -q "@theme" app/globals.css || grep -q "@theme" styles/globals.css

# OKLCH colors used (perceptual uniformity)
grep -q "oklch" app/globals.css || grep -q "oklch" styles/globals.css

# Semantic token naming (--color-primary not --color-blue-500)
grep -q "\--color-primary\\|\--font-display\\|\--spacing-" app/globals.css
```

**Pass Criteria**:
- Tailwind 4 with @theme directive (CSS-first, no JS config)
- Design tokens use semantic names (--color-primary, --font-display)
- Colors defined in OKLCH for perceptual uniformity
- Typography and spacing scales established

**If Missing**:
Apply `design-tokens` + `frontend-design` skills → Migrate to Tailwind 4 @theme, define semantic tokens

---

### 5. Changelog Automation (Recommended)

**Check for**:
```bash
# Changesets (monorepos) OR semantic-release (single packages)
[ -d .changeset ] || grep -q "semantic-release" package.json

# Conventional commit enforcement
[ -f commitlint.config.js ] || grep -q "@commitlint" package.json

# Release workflow configured
[ -f .github/workflows/release.yml ]
```

**Pass Criteria**:
- Changesets configured (.changeset/config.json) OR semantic-release configured (.releaserc.js)
- Conventional commits enforced with commitlint
- Automated release workflow in GitHub Actions

**If Missing**:
Apply `changelog-automation` skill → Setup Changesets (monorepos) or semantic-release (single packages)

---

### 6. Build & Type Safety (Critical)

**Run**:
```bash
# Type checking
pnpm typecheck || pnpm tsc --noEmit

# Linting
pnpm lint

# Tests
pnpm test

# Build
pnpm build
```

**Pass Criteria**:
- ✅ No TypeScript errors
- ✅ No linting errors (warnings acceptable if documented)
- ✅ All tests passing
- ✅ Build succeeds without errors

**If Failing**:
Fix errors before proceeding → Re-run quality-check

---

### 7. Security & Dependencies (Recommended)

**Check for**:
```bash
# No secrets in .env files committed to git
git ls-files | grep -q "^\.env$" && echo "WARNING: .env committed to git"

# .env.example exists for documentation
[ -f .env.example ]

# Dependencies up to date (check for critical vulnerabilities)
pnpm audit --audit-level moderate

# Security headers configured (Next.js example)
grep -q "headers()" next.config.js
```

**Pass Criteria**:
- No .env files in git (only .env.example)
- No critical/high severity vulnerabilities in dependencies
- Security headers configured (HSTS, CSP, X-Frame-Options)

**If Issues Found**:
Add .env to .gitignore → Update dependencies → Configure security headers

---

### 8. Analytics & Monitoring (Recommended)

**Check for**:
```bash
# Vercel Analytics (for Next.js on Vercel)
grep -q "@vercel/analytics" package.json

# Performance monitoring configured
grep -q "Web Vitals\\|analytics\\|tracking" src/
```

**Pass Criteria**:
- Analytics package installed (@vercel/analytics, Plausible, etc.)
- Web Vitals tracking implemented
- User behavior tracking configured (respecting privacy)

**If Missing**:
Install @vercel/analytics → Add <Analytics /> component to layout

---

### 9. Test Coverage Infrastructure (Critical)

**Check for**:
```bash
# Vitest configured for coverage
grep -q "vitest" package.json
grep -q "coverage" vitest.config.ts || grep -q "@vitest/coverage" package.json

# GitHub Actions workflow includes coverage reporting
[ -f .github/workflows/ci.yml ]
grep -q "vitest.*--coverage" .github/workflows/ci.yml

# vitest-coverage-report-action configured (PR comments)
grep -q "vitest-coverage-report-action" .github/workflows/ci.yml
```

**Pass Criteria**:
- Vitest with coverage provider (@vitest/coverage-v8)
- GitHub Actions runs coverage on PRs
- vitest-coverage-report-action comments patch coverage on PRs
- No external service dependencies (Codecov, Coveralls, etc.)

**If Missing**:
Apply `code-quality-standards` and `quality-gates` skills → Add coverage to CI workflow with vitest-coverage-report-action

**Expected GitHub Action snippet**:
```yaml
- name: Test Coverage
  run: pnpm test -- --coverage

- name: Report Coverage
  if: always()
  uses: davelosert/vitest-coverage-report-action@v2
```

---

### 10. PR Size Automation (Recommended)

**Check for**:
```bash
# PR size labeler workflow exists
[ -f .github/workflows/pr-size-labeler.yml ]

# pr-size-labeler action configured
grep -q "codelytv/pr-size-labeler" .github/workflows/pr-size-labeler.yml
```

**Pass Criteria**:
- Automated PR size labeling configured
- Labels: XS (<10), S (<100), M (<200), L (<400), XL (≥400)
- Workflow triggers on pull_request events

**If Missing**:
Apply `quality-gates` skill → Create .github/workflows/pr-size-labeler.yml

**Expected workflow**:
```yaml
name: PR Size Labeler

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  size-label:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write
    steps:
      - uses: codelytv/pr-size-labeler@v1
        with:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          xs_label: 'size/XS'
          xs_max_size: 10
          s_label: 'size/S'
          s_max_size: 100
          m_label: 'size/M'
          m_max_size: 200
          l_label: 'size/L'
          l_max_size: 400
          xl_label: 'size/XL'
```

---

### 11. Documentation Quality (Recommended)

**Check for**:
```bash
# lychee installed for link checking (Rust binary)
command -v lychee >/dev/null 2>&1

# Vale installed for style linting (Go binary)
command -v vale >/dev/null 2>&1

# README.md exists
[ -f README.md ]

# Documentation directory exists
[ -d docs ] || [ -d documentation ]

# Vale configuration exists
[ -f .vale.ini ] || [ -d .vale ]
```

**Pass Criteria**:
- lychee installed (`brew install lychee`) for link checking
- Vale installed (`brew install vale`) for style guide enforcement
- README.md exists with quick start section
- Documentation directory structured and maintained
- Vale configuration for style consistency (optional but recommended)

**If Missing**:
Apply `documentation-standards` skill → Install lychee and Vale, create .vale.ini

**Link checking command**:
```bash
lychee **/*.md --offline --cache
```

**Style linting command**:
```bash
vale docs/
```

**Freshness check**:
```bash
# Find docs not updated in 90 days
find docs -name '*.md' | while read f; do
  age=$(( ($(date +%s) - $(git log -1 --format=%ct -- "$f")) / 86400 ))
  [ $age -gt 90 ] && echo "$f: $age days stale"
done
```

---

### 12. ADR Infrastructure (Recommended)

**Check for**:
```bash
# ADR directory exists
[ -d docs/adr ]

# ADR index file exists
[ -f docs/adr/README.md ] || [ -f docs/adr/INDEX.md ]

# ADRs follow naming convention (ADR-NNNN-title.md)
ls docs/adr/ADR-*.md >/dev/null 2>&1

# ADR template available (optional)
[ -f docs/adr/TEMPLATE.md ]
```

**Pass Criteria**:
- /docs/adr/ directory exists for Architecture Decision Records
- ADR index file documenting all decisions
- ADRs follow naming: ADR-0001-title.md, ADR-0002-title.md
- MADR Light template format used (Context, Options, Decision, Consequences)

**If Missing**:
Create directory structure and bash function for easy ADR creation

**Directory structure**:
```
docs/
  adr/
    README.md          # Index of all ADRs
    TEMPLATE.md        # MADR Light template
    ADR-0001-initial-architecture.md
    ADR-0002-database-choice.md
```

**When to create ADRs** (from /spec and /architect):
- Decision is costly to reverse (migrations, vendor lock-in, framework choice)
- Multiple viable alternatives with meaningful trade-offs
- Affects team workflow or system architecture
- Requires explanation for future maintainers

---

## Verification Report

After running all checks, generate report:

```markdown
# Quality Check Report

## ✅ Passing Checks
- Quality Gates: Lefthook configured, CI/CD operational
- Test Coverage: vitest-coverage-report-action commenting on PRs
- PR Size Automation: pr-size-labeler workflow active
- Build & Types: All checks passing
- Documentation: lychee and Vale installed, README maintained
- [Additional passing checks]

## ⚠️ Warnings
- Design System: Tailwind config still in JS (migrate to @theme)
- Analytics: No Web Vitals tracking configured
- ADR Infrastructure: Directory exists but no recent ADRs created

## ❌ Critical Issues
- Error Tracking: Sentry not configured
- Structured Logging: Still using console.log
- Test Coverage: No coverage reporting on PRs

## Recommendations
1. **Critical (fix before PR)**:
   - Configure Sentry error tracking
   - Add vitest-coverage-report-action to CI
2. **Important (fix this sprint)**:
   - Migrate logging to Pino
   - Set up pr-size-labeler workflow
3. **Nice-to-have (backlog)**:
   - Add Web Vitals tracking
   - Install lychee/Vale for doc quality
   - Create ADR for recent architecture decision

## Next Steps
- Apply `structured-logging` skill to create utils/logger.ts
- Apply `quality-gates` skill to add coverage reporting
- Install @sentry/nextjs and configure error tracking
- Create .github/workflows/pr-size-labeler.yml
- Re-run /quality-check after fixes
```

## Automation

For CI/CD integration, create verification script:

```json
// package.json
{
  "scripts": {
    "verify": "pnpm typecheck && pnpm lint && pnpm test && pnpm build",
    "verify:full": "pnpm verify && pnpm audit --audit-level moderate"
  }
}
```

Add to GitHub Actions:
```yaml
# .github/workflows/quality-check.yml
name: Quality Check

on:
  pull_request:
  push:
    branches: [main]

jobs:
  quality-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile
      - run: pnpm verify:full
```

## Philosophy

**"Quality is never an accident; it is always the result of intelligent effort."** - John Ruskin

Verification catches issues when they're cheap to fix. Every check enforces standards that prevent costly debugging, security incidents, and technical debt accumulation.

**Fail fast, fix early, ship confidently.**

### The Friday Afternoon Standard

**Supremely confident deployments** = All checks green → merge to production → turn phone off → enjoy weekend.

If you can't do this, quality infrastructure is incomplete:
- Missing gates (Lefthook, CI/CD)
- Flaky tests requiring manual reruns
- Manual verification steps
- Undocumented deployment procedures
- Fear of breaking production

This command finds the gaps. Fix them once, deploy fearlessly forever.

---

**Remember**: /quality-check is a safety net, not a blocker. Use findings to improve incrementally, prioritizing critical issues before optional enhancements.
