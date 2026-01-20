---
description: Verify project quality standards and infrastructure completeness before deployment
---

# QUALITY-CHECK

> **THE FRIDAY AFTERNOON TEST** + **MISTY STEP STANDARDS**
>
> *"Can I merge to production Friday at 5pm and turn my phone off?"*
>
> If the answer is NO, quality gates are missing. This command finds what's blocking supremely confident deployments AND implements fixes.

> **QUALITY GATE CHECKPOINT** (17 Categories)
> - **Deployment Confidence**: All checks green = production ready, zero manual verification needed
> - **Infrastructure Validation**: Ensure logging, error tracking, quality gates operational
> - **Build Confidence**: Verify tests pass, types check, build succeeds
> - **Design Consistency**: Validate design tokens, brand elements, accessibility
> - **Release Readiness**: Confirm changelog automation, version strategy
> - **Misty Step Standards**: Clerk auth, ConvexDB, strict TypeScript, branded footer

You're the quality gatekeeper enabling fearless deployments. This verification runs before critical workflow transitions (pre-PR, pre-deploy, post-setup). Every missing gate = weekend on-call risk.

**This command audits AND implements.** After discovery, you'll be prompted to fix critical gaps automatically.

## Your Mission

Systematically verify project quality standards and infrastructure completeness. Report findings with actionable fixes. Implement missing infrastructure with user confirmation.

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

---

## Phase 0: Project Type Detection

**Auto-detect project type to skip irrelevant checks silently.**

```bash
# Detect Next.js project
IS_NEXTJS=$(test -f "next.config.ts" -o -f "next.config.js" -o -f "next.config.mjs" && echo "true" || echo "false")

# Detect Convex backend
HAS_CONVEX=$(test -d "convex" && echo "true" || echo "false")

# Detect CLI tool (has bin in package.json)
IS_CLI=$(test -f "package.json" && grep -q '"bin"' package.json && echo "true" || echo "false")

# Detect library (no Next.js, no bin, has main/exports)
IS_LIBRARY=$(test -f "package.json" && grep -qE '"main"|"exports"' package.json && [ "$IS_NEXTJS" = "false" ] && [ "$IS_CLI" = "false" ] && echo "true" || echo "false")
```

**Project Type Matrix** (what to check):

| Project Type | Skip These Checks |
|--------------|-------------------|
| **Next.js Web App** | None - all 17 categories apply |
| **Next.js + Convex** | None - all 17 categories + Convex-specific |
| **CLI Tool** | Clerk, Convex, Footer, Vercel Analytics, Design System, E2E |
| **Library** | Clerk, Convex, Footer, Vercel Analytics, E2E |

**Key Enforcement Rules**:
- **Clerk Auth**: REQUIRED for all Next.js web apps (not optional)
- **E2E Tests**: CRITICAL for web apps (fail quality check if missing)
- **ConvexDB**: Only checked when `convex/` directory exists

---

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

### 5. Changelog Automation (Critical)

**Check for**:
```bash
# Changesets (monorepos) OR semantic-release (single packages)
[ -d .changeset ] || grep -q "semantic-release" package.json

# Conventional commit enforcement - REQUIRED
[ -f commitlint.config.js ] || [ -f commitlint.config.cjs ] || grep -q "@commitlint" package.json

# Commitlint packages installed
grep -q "@commitlint/cli" package.json
grep -q "@commitlint/config-conventional" package.json

# Lefthook has commit-msg hook with commitlint
grep -q "commit-msg:" lefthook.yml && grep -q "commitlint" lefthook.yml

# Release workflow configured
[ -f .github/workflows/release.yml ]
```

**Pass Criteria**:
- Changesets configured (.changeset/config.json) OR semantic-release configured (.releaserc.js)
- Conventional commits enforced with commitlint (REQUIRED)
- @commitlint/cli and @commitlint/config-conventional installed
- Lefthook commit-msg hook runs commitlint
- Automated release workflow in GitHub Actions

**If Missing**:
Apply `changelog-automation` skill:
1. Install commitlint: `pnpm add -D @commitlint/cli @commitlint/config-conventional`
2. Create commitlint.config.js:
```javascript
module.exports = { extends: ['@commitlint/config-conventional'] }
```
3. Add to lefthook.yml:
```yaml
commit-msg:
  commands:
    commitlint:
      run: pnpm commitlint --edit {1}
```
4. Setup Changesets (monorepos) or semantic-release (single packages)

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

# E2E tests exist (CRITICAL for web apps)
[ -d "e2e" ] || [ -d "tests/e2e" ] || [ -d "__tests__/e2e" ]
grep -q "playwright\\|cypress" package.json

# README has coverage badge
grep -qE "!\[.*coverage.*\]|!\[.*Coverage.*\]" README.md
```

**Pass Criteria**:
- Vitest with coverage provider (@vitest/coverage-v8)
- GitHub Actions runs coverage on PRs
- vitest-coverage-report-action comments patch coverage on PRs
- **E2E tests configured** (Playwright or Cypress) - CRITICAL for web apps
- **README.md contains coverage badge**
- No external service dependencies (Codecov, Coveralls, etc.)

**If Missing**:
Apply `code-quality-standards` and `quality-gates` skills:

1. Add coverage to CI workflow with vitest-coverage-report-action
2. Set up E2E tests:
```bash
pnpm add -D @playwright/test
pnpm playwright install
```
3. Add coverage badge to README:
```markdown
![Coverage](https://img.shields.io/badge/coverage-80%25-brightgreen)
```
Or use dynamic badge from vitest-coverage-report-action output.

**Expected GitHub Action snippet**:
```yaml
- name: Test Coverage
  run: pnpm test -- --coverage

- name: Report Coverage
  if: always()
  uses: davelosert/vitest-coverage-report-action@v2

- name: E2E Tests
  run: pnpm playwright test
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

**When to create ADRs** (from /product and /architect):
- Decision is costly to reverse (migrations, vendor lock-in, framework choice)
- Multiple viable alternatives with meaningful trade-offs
- Affects team workflow or system architecture
- Requires explanation for future maintainers

---

### 13. Clerk Authentication (Critical - Web Apps)

**Skip if**: CLI tool or library (no web frontend)

**Check for**:
```bash
# @clerk/nextjs dependency installed
grep -q "@clerk/nextjs" package.json

# ClerkProvider in app layout
grep -rq "ClerkProvider" app/layout.tsx || grep -rq "ClerkProvider" src/app/layout.tsx

# middleware.ts exists with clerkMiddleware
[ -f middleware.ts ] || [ -f src/middleware.ts ]
grep -q "clerkMiddleware" middleware.ts 2>/dev/null || grep -q "clerkMiddleware" src/middleware.ts 2>/dev/null

# Environment variables documented
grep -q "NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY" .env.example
grep -q "CLERK_SECRET_KEY" .env.example
```

**Pass Criteria**:
- @clerk/nextjs installed
- ClerkProvider wrapping app in layout.tsx
- middleware.ts with clerkMiddleware protecting routes
- NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY in .env.example
- CLERK_SECRET_KEY in .env.example

**If Missing**:
1. Install Clerk: `pnpm add @clerk/nextjs`
2. Create middleware.ts:
```typescript
import { clerkMiddleware } from "@clerk/nextjs/server"
export default clerkMiddleware()
export const config = {
  matcher: ["/((?!.*\\..*|_next).*)", "/", "/(api|trpc)(.*)"],
}
```
3. Wrap app in ClerkProvider in layout.tsx:
```tsx
import { ClerkProvider } from "@clerk/nextjs"
export default function RootLayout({ children }) {
  return (
    <ClerkProvider>
      <html><body>{children}</body></html>
    </ClerkProvider>
  )
}
```
4. Add to .env.example:
```
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=
CLERK_SECRET_KEY=
```

---

### 14. ConvexDB Setup (Critical - When convex/ exists)

**Skip if**: No convex/ directory exists

**Check for**:
```bash
# convex/ directory exists
[ -d "convex" ]

# convex/_generated/ is NOT in .gitignore (must be committed)
! grep -q "convex/_generated" .gitignore

# convex/_generated/ files exist and are tracked
[ -f "convex/_generated/api.d.ts" ]
git ls-files --error-unmatch convex/_generated/api.d.ts 2>/dev/null

# convex/schema.ts exists
[ -f "convex/schema.ts" ]

# ConvexClientProvider in app layout
grep -rq "ConvexProvider\\|ConvexClientProvider" app/ || grep -rq "ConvexProvider\\|ConvexClientProvider" src/app/

# Environment variables documented
grep -q "CONVEX_URL\\|NEXT_PUBLIC_CONVEX_URL" .env.example
```

**Pass Criteria**:
- convex/ directory exists with schema.ts
- convex/_generated/ committed to git (NOT in .gitignore) - CRITICAL for CI/CD
- ConvexProvider/ConvexClientProvider in app layout
- CONVEX_URL or NEXT_PUBLIC_CONVEX_URL in .env.example

**If Missing**:
Apply `convex-development` skill:
1. Ensure convex/_generated/ is NOT in .gitignore
2. Run `npx convex dev` to generate types
3. Commit generated files: `git add convex/_generated/`
4. Add ConvexClientProvider to layout
5. Add to .env.example:
```
NEXT_PUBLIC_CONVEX_URL=
```

**Critical**: Generated files MUST be committed for CI/CD type checking.

---

### 15. Misty Step Branding (Required - Web Apps)

**Skip if**: CLI tool or library

**Check for**:
```bash
# Footer component exists
[ -f "components/ui/footer.tsx" ] || [ -f "components/footer.tsx" ] || [ -f "src/components/ui/footer.tsx" ]

# Contains "misty step" text (case-insensitive)
grep -riq "misty.step" components/ || grep -riq "misty.step" src/components/

# Links to mistystep.io
grep -rq "mistystep.io" components/ || grep -rq "mistystep.io" src/components/

# Has support/contact email
grep -rq "hello@mistystep.io" components/ || grep -rq "hello@mistystep.io" src/components/
```

**Pass Criteria**:
- Footer component exists (shadcn/ui pattern)
- Contains "a misty step project" or similar branding text
- Links to https://mistystep.io
- Has support link to mailto:hello@mistystep.io

**If Missing**:
Create footer component:

```tsx
// components/ui/footer.tsx
import Link from "next/link"

export function Footer() {
  return (
    <footer className="border-t py-6 md:py-0">
      <div className="container flex flex-col items-center justify-between gap-4 md:h-16 md:flex-row">
        <p className="text-sm text-muted-foreground">
          a{" "}
          <Link
            href="https://mistystep.io"
            target="_blank"
            rel="noopener noreferrer"
            className="font-medium underline underline-offset-4 hover:text-primary"
          >
            misty step
          </Link>{" "}
          project
        </p>
        <Link
          href="mailto:hello@mistystep.io"
          className="text-sm text-muted-foreground underline underline-offset-4 hover:text-primary"
        >
          support
        </Link>
      </div>
    </footer>
  )
}
```

Then add to layout: `<Footer />` at bottom of page.

---

### 16. Strict TypeScript Configuration (Critical)

**Check for**:
```bash
# tsconfig.json exists
[ -f "tsconfig.json" ]

# strict mode enabled
grep -q '"strict":\s*true' tsconfig.json

# Additional strict flags
grep -q '"noUncheckedIndexedAccess":\s*true' tsconfig.json
grep -q '"noImplicitOverride":\s*true' tsconfig.json
grep -q '"noFallthroughCasesInSwitch":\s*true' tsconfig.json
```

**Pass Criteria**:
- `"strict": true` in compilerOptions
- `"noUncheckedIndexedAccess": true` (catches undefined access)
- `"noImplicitOverride": true` (explicit override keyword)
- `"noFallthroughCasesInSwitch": true` (prevent switch fallthrough bugs)

**Recommended additional flags**:
- `"exactOptionalPropertyTypes": true`
- `"noPropertyAccessFromIndexSignature": true`

**If Missing**:
Update tsconfig.json compilerOptions:
```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "noFallthroughCasesInSwitch": true,
    "exactOptionalPropertyTypes": true,
    "noPropertyAccessFromIndexSignature": true
  }
}
```

---

### 17. Next.js LTS Version (Important - Next.js Projects)

**Skip if**: Not a Next.js project

**Check for**:
```bash
# Get Next.js version from package.json
NEXTJS_VERSION=$(grep -o '"next":\s*"[^"]*"' package.json | grep -o '[0-9]*\.[0-9]*\.[0-9]*')

# Check if version >= 14.0.0 (LTS baseline)
# Manual verification needed - report version found
echo "Next.js version: $NEXTJS_VERSION"

# Check for App Router usage (preferred)
[ -d "app" ] || [ -d "src/app" ]
```

**Pass Criteria**:
- Next.js version >= 14.0.0 (current LTS baseline)
- Using App Router (app/ directory exists)
- Not using deprecated features (pages/ for new projects)

**If Missing or Outdated**:
Upgrade Next.js:
```bash
pnpm add next@latest react@latest react-dom@latest
```

Review migration guide: https://nextjs.org/docs/app/building-your-application/upgrading

---

## Phase 3: Implementation Flow

After running all checks, present findings and offer to implement:

```markdown
## Quality Check Complete

### Summary
- ✅ Passing: X categories
- ⚠️ Warnings: Y items
- ❌ Critical Issues: Z items

### Critical Issues (Must Fix)
1. [ ] Clerk authentication not configured
2. [ ] Strict TypeScript flags missing
3. [ ] E2E tests not found

### Important Issues (Should Fix)
4. [ ] Misty Step footer missing
5. [ ] Commitlint not enforced
6. [ ] Coverage badge not in README

### Recommendations (Nice to Have)
7. [ ] ADR directory not set up
8. [ ] Vale not installed for docs
```

**Implementation Prompt**:

After presenting findings, ask:

> **Implement fixes?**
> - `[a]` All critical issues
> - `[s]` Select specific items
> - `[n]` No, just report

If user confirms, implement each missing item using the templates and skills referenced above.

**Implementation Order** (dependencies first):
1. Strict TypeScript (affects all code)
2. Lefthook + commitlint (affects all commits)
3. Clerk authentication (affects routes)
4. ConvexDB setup (affects data layer)
5. Test infrastructure (E2E, coverage)
6. Misty Step footer (UI component)
7. Documentation (README badges, ADRs)

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
