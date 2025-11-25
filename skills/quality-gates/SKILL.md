---
name: quality-gates
description: "Apply quality gate standards for git hooks, testing, CI/CD, and automation using Lefthook, Vitest, GitHub Actions, and quality enforcement. Use when setting up quality infrastructure, configuring hooks, discussing automation, or reviewing quality practices."
---

# Quality Gates

Standards and patterns for maintaining code quality through automated gates, hooks, testing, and continuous integration.

## Philosophy

**Quality gates prevent problems before they reach production.** Automated checks provide immediate feedback, enforce standards consistently, and free developers to focus on building features rather than remembering process.

**Progressive enforcement:**
- **Pre-commit**: Fast checks (lint, format, typecheck) on staged files only
- **Pre-push**: Comprehensive checks (full test suite, coverage)
- **CI/CD**: Production-ready validation (build, E2E tests, security scans)

## Git Hooks: Lefthook (Recommended)

**Why Lefthook over Husky:**
- **Language-agnostic**: Go binary, no Node.js dependency
- **Faster**: Built in Go, parallel execution by default
- **Simpler**: YAML configuration, combines Husky + lint-staged functionality
- **Lightweight**: Single binary, smaller footprint
- **Modern**: Actively maintained by Evil Martians (2025 recommendation)

### Installation

```bash
# Install via package manager of choice
pnpm add -D lefthook
# or npm install -D lefthook
# or brew install lefthook (global)

# Initialize lefthook
pnpm lefthook install
# This creates .lefthook directory and configures git hooks
```

### Configuration: lefthook.yml

**Basic Setup (Next.js/TypeScript project):**

```yaml
# lefthook.yml - Place in project root
pre-commit:
  parallel: true  # Run commands in parallel for speed
  commands:
    lint:
      glob: "*.{js,ts,jsx,tsx}"
      run: pnpm eslint --fix {staged_files}
      stage_fixed: true  # Re-stage files after fixing

    format:
      glob: "*.{js,ts,jsx,tsx,json,md,css}"
      run: pnpm prettier --write {staged_files}
      stage_fixed: true

    typecheck:
      glob: "*.{ts,tsx}"
      run: pnpm tsc --noEmit
      # Note: Only checks, doesn't fix

pre-push:
  commands:
    test:
      run: pnpm test:ci
      # Full test suite with coverage

    build:
      run: pnpm build
      # Ensure production build succeeds

commit-msg:
  commands:
    commitlint:
      run: pnpm commitlint --edit {1}
      # Enforce conventional commits
```

**Advanced: Monorepo with Multiple Packages**

```yaml
pre-commit:
  parallel: true
  commands:
    # Package-specific linting
    lint-web:
      glob: "apps/web/**/*.{ts,tsx}"
      run: pnpm --filter web lint --fix {staged_files}
      root: apps/web/
      stage_fixed: true

    lint-api:
      glob: "apps/api/**/*.ts"
      run: pnpm --filter api lint --fix {staged_files}
      root: apps/api/
      stage_fixed: true

    # Shared package linting
    lint-shared:
      glob: "packages/**/*.{ts,tsx}"
      run: pnpm --filter @repo/* lint --fix {staged_files}
      stage_fixed: true

    # Global formatting
    format:
      glob: "**/*.{js,ts,jsx,tsx,json,md}"
      run: pnpm prettier --write {staged_files}
      stage_fixed: true

pre-push:
  commands:
    # Run tests for changed packages only
    test-changed:
      run: pnpm turbo run test --filter=[HEAD^1]

    # Type check all packages
    typecheck:
      run: pnpm turbo run typecheck

    # Build all packages
    build:
      run: pnpm turbo run build
```

**Convex-Specific Hooks**

```yaml
pre-commit:
  parallel: true
  commands:
    # Standard linting/formatting
    lint:
      glob: "*.{js,ts,jsx,tsx}"
      run: pnpm eslint --fix {staged_files}
      stage_fixed: true

    # Convex function validation
    convex-typecheck:
      glob: "convex/**/*.ts"
      run: pnpm tsc --noEmit --project convex/tsconfig.json

    # Convex schema validation (if you have validation scripts)
    convex-schema:
      glob: "convex/schema.ts"
      run: pnpm convex dev --once --run convex/validateSchema.ts
      # Only run if schema changed

pre-push:
  commands:
    test:
      run: pnpm test:ci

    # Deploy to preview environment for testing
    convex-preview:
      run: |
        pnpm convex deploy --preview-name ci-$(git rev-parse --short HEAD)
        echo "Preview deployed to: $(pnpm convex dashboard --preview-name ci-$(git rev-parse --short HEAD))"
```

### Skip Hooks (Emergency Use Only)

```bash
# Skip pre-commit hooks (use sparingly!)
git commit --no-verify -m "emergency fix"

# Skip pre-push hooks
git push --no-verify

# Skip specific lefthook command
LEFTHOOK_EXCLUDE=test git push
```

## Coverage Gates (GitHub Actions)

Use `vitest-coverage-report-action` for PR comments:
- Shows coverage diff (before/after)
- Links to uncovered lines in PR
- Zero external service required
- Free for private repos

**Setup**:
```yaml
- uses: davelosert/vitest-coverage-report-action@v2
  permissions:
    contents: write
    pull-requests: write
  with:
    file-coverage-mode: changes  # Only show changed files
```

**Standards**:
- **Patch coverage**: 80%+ for new/changed code (block if lower)
- **Overall coverage**: Track but don't block
- **Critical paths**: 90%+ (payment, auth, data integrity)

## PR Size Gates

Use `pr-size-labeler` for automatic size labeling:
- Auto-labels: xs (<50), s (<150), m (<300), l (<500), xl (>500)
- Optional: fail workflow if XL
- Configure thresholds in workflow YAML

**Setup**:
```yaml
- uses: CodelyTV/pr-size-labeler@v1
  with:
    xs_max_size: '50'
    s_max_size: '150'
    m_max_size: '300'
    l_max_size: '500'
    fail_if_xl: 'true'
    message_if_xl: 'PR exceeds 500 lines. Please split into smaller PRs.'
```

**Benefits**:
- Automatic PR labeling
- Visual size feedback
- Optional hard enforcement
- Free, no external service

## Testing Strategy: Vitest

**Why Vitest:**
- Fast, modern test runner
- Jest-compatible API (easy migration)
- Great TypeScript support
- Built-in coverage with c8/v8
- Watch mode with intelligent re-runs

### Configuration

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './test/setup.ts',
    include: ['**/*.{test,spec}.{js,ts,jsx,tsx}'],
    exclude: ['**/node_modules/**', '**/dist/**', '**/.next/**'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html', 'lcov'],
      exclude: [
        '**/node_modules/**',
        '**/dist/**',
        '**/.next/**',
        '**/test/**',
        '**/*.config.{js,ts}',
        '**/*.d.ts',
      ],
      // Don't enforce arbitrary thresholds
      // Use coverage to find untested paths, not as success metric
      thresholds: {
        lines: 60,    // Baseline, not target
        functions: 60,
        branches: 60,
        statements: 60,
      },
    },
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})
```

### Package.json Scripts

```json
{
  "scripts": {
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:ci": "vitest run --coverage",
    "test:watch": "vitest --watch",
    "typecheck": "tsc --noEmit",
    "lint": "eslint . --ext .ts,.tsx,.js,.jsx",
    "lint:fix": "eslint . --ext .ts,.tsx,.js,.jsx --fix",
    "format": "prettier --write \"**/*.{ts,tsx,js,jsx,json,md,css}\"",
    "format:check": "prettier --check \"**/*.{ts,tsx,js,jsx,json,md,css}\""
  }
}
```

## CI/CD: GitHub Actions

**Why GitHub Actions:**
- Native GitHub integration
- Free for public repos, generous free tier for private
- Matrix builds for testing multiple environments
- Artifact storage and caching
- Secrets management

### Basic Workflow

```yaml
# .github/workflows/ci.yml
name: CI

on:
  pull_request:
    branches: [main, develop]
  push:
    branches: [main, develop]

jobs:
  quality-checks:
    name: Quality Checks
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup pnpm
        uses: pnpm/action-setup@v2
        with:
          version: 8

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: 'pnpm'

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Lint
        run: pnpm lint

      - name: Type check
        run: pnpm typecheck

      - name: Test
        run: pnpm test:ci

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          files: ./coverage/coverage-final.json
          fail_ci_if_error: false

      - name: Build
        run: pnpm build

      - name: Upload build artifacts
        uses: actions/upload-artifact@v4
        with:
          name: build-output
          path: .next/
          retention-days: 7
```

### Advanced: Matrix Testing + E2E

```yaml
# .github/workflows/comprehensive-ci.yml
name: Comprehensive CI

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  # Unit and integration tests across Node versions
  test-matrix:
    name: Test (Node ${{ matrix.node-version }})
    runs-on: ubuntu-latest

    strategy:
      matrix:
        node-version: [20, 22]

    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'pnpm'

      - run: pnpm install --frozen-lockfile
      - run: pnpm test:ci
      - run: pnpm build

  # E2E tests with Playwright
  e2e:
    name: E2E Tests
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
      - uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: 'pnpm'

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Install Playwright browsers
        run: pnpm playwright install --with-deps chromium

      - name: Build application
        run: pnpm build

      - name: Run E2E tests
        run: pnpm test:e2e
        env:
          PLAYWRIGHT_BROWSERS_PATH: 0

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 30

  # Security scanning
  security:
    name: Security Scan
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
      - uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: 'pnpm'

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Audit dependencies
        run: pnpm audit --audit-level=moderate

      - name: Check for vulnerabilities
        run: pnpm dlx @socketsecurity/cli audit
```

### Convex-Specific CI

```yaml
# .github/workflows/convex-ci.yml
name: Convex CI

on:
  pull_request:
    branches: [main]
    paths:
      - 'convex/**'
      - 'src/**'

jobs:
  convex-validate:
    name: Validate Convex Functions
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
      - uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: 'pnpm'

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Type check Convex functions
        run: pnpm tsc --noEmit --project convex/tsconfig.json

      - name: Deploy to preview
        env:
          CONVEX_DEPLOY_KEY: ${{ secrets.CONVEX_DEPLOY_KEY }}
        run: |
          pnpm convex deploy --preview-name pr-${{ github.event.pull_request.number }}

      - name: Run Convex tests
        run: pnpm test:convex

      - name: Comment preview URL
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `🚀 Convex preview deployed: https://dashboard.convex.dev/t/pr-${{ github.event.pull_request.number }}`
            })
```

## Branch Protection

Configure in GitHub Settings → Branches → Branch protection rules for `main`:

**Required settings:**
- ✅ Require a pull request before merging
- ✅ Require approvals: 1
- ✅ Require status checks to pass before merging
  - Select: `Quality Checks`, `Test`, `Build`, `E2E Tests`
- ✅ Require branches to be up to date before merging
- ✅ Require conversation resolution before merging
- ✅ Do not allow bypassing the above settings

**Optional but recommended:**
- ✅ Require signed commits
- ✅ Require linear history
- ✅ Lock branch (for production branches)

## Coverage Reporting: Codecov

**Setup:**

1. Sign up at codecov.io with GitHub
2. Add repository
3. Add Codecov token to GitHub secrets: `CODECOV_TOKEN`
4. Configure codecov.yml in project root:

```yaml
# codecov.yml
coverage:
  status:
    project:
      default:
        target: auto  # Maintain current coverage
        threshold: 5%  # Allow 5% decrease
        if_ci_failed: error

    patch:
      default:
        target: 70%  # New code should be well-tested
        if_ci_failed: error

comment:
  layout: "reach, diff, flags, files"
  behavior: default
  require_changes: false

ignore:
  - "**/*.test.ts"
  - "**/*.spec.ts"
  - "**/*.config.ts"
  - "**/*.d.ts"
  - "**/test/**"
  - "**/__tests__/**"
```

## Quality Checklist

When setting up quality gates for a new project:

### Essential (Must Have)
- [ ] **Lefthook configured** with pre-commit (lint, format, typecheck)
- [ ] **Lefthook configured** with pre-push (test, build)
- [ ] **GitHub Actions CI** with lint, typecheck, test, build
- [ ] **Branch protection** enabled on main branch
- [ ] **Test framework** set up (Vitest recommended)
- [ ] **Code coverage** reporting (Codecov or similar)

### Recommended (Should Have)
- [ ] **E2E testing** with Playwright for critical paths
- [ ] **Dependency audit** in CI (pnpm audit)
- [ ] **Conventional commits** enforcement (commitlint)
- [ ] **Coverage thresholds** as diagnostic (not arbitrary targets)
- [ ] **Security scanning** in CI
- [ ] **Preview deployments** for PRs

### Nice to Have
- [ ] **Matrix testing** across Node versions
- [ ] **Performance budgets** enforced
- [ ] **Bundle size tracking** in CI
- [ ] **Accessibility testing** automated
- [ ] **Visual regression testing** for UI projects

## Anti-Patterns to Avoid

❌ **Husky**: Use Lefthook (faster, language-agnostic, simpler)
❌ **Arbitrary coverage targets**: Use coverage to find gaps, not as success metric
❌ **Testing implementation details**: Test behavior, not internals
❌ **Heavy mocking**: Minimize mocks, prefer real integration tests
❌ **Skipping hooks routinely**: Fix the problem, don't bypass gates
❌ **CI that only tests on main**: Test on every PR
❌ **No branch protection**: Enforce quality before merge
❌ **Manual version bumping**: Automate with changesets/semantic-release

## Example: Full Project Setup

```bash
# 1. Initialize project
pnpm init

# 2. Install quality tools
pnpm add -D \
  lefthook \
  vitest @vitest/coverage-v8 \
  @testing-library/react @testing-library/jest-dom \
  eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin \
  prettier eslint-config-prettier \
  @commitlint/cli @commitlint/config-conventional

# 3. Initialize lefthook
pnpm lefthook install

# 4. Create configurations
# - lefthook.yml (git hooks)
# - vitest.config.ts (testing)
# - .github/workflows/ci.yml (CI/CD)
# - .prettierrc (formatting)
# - .eslintrc.js (linting)
# - commitlint.config.js (commit message validation)
# - codecov.yml (coverage reporting)

# 5. Add scripts to package.json
# (see scripts section above)

# 6. Configure GitHub branch protection

# 7. First commit
git add .
git commit -m "feat: setup quality gates infrastructure"
# Lefthook will run pre-commit hooks automatically
```

## Philosophy

**Quality is not a phase—it's built into the process.**

- Fast feedback loops (pre-commit) catch trivial issues
- Comprehensive validation (pre-push) prevents broken work from reaching CI
- CI/CD enforces production-readiness
- Branch protection ensures every change meets standards

**Coverage is a diagnostic tool, not a goal.** 60% meaningful coverage beats 95% testing implementation details.

**Automate everything.** Manual processes fail. Automated gates are consistent, fast, and free developers to build.

---

When agents design quality infrastructure, they should:
- Default to Lefthook for git hooks (not Husky)
- Configure parallel execution for speed
- Set up pre-commit for fast checks (staged files only)
- Set up pre-push for comprehensive validation
- Include GitHub Actions with matrix testing
- Enforce branch protection on main/production branches
- Use Codecov or similar for coverage tracking
- Focus on testing behavior, not implementation
