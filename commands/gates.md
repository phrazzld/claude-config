Audit and improve quality infrastructure.

# GATES

Channel platform engineering thinking: critically examine quality gates and identify improvements.

## The North Star

> **"Merge to production Friday afternoon and turn your phone off."**
>
> If you can't do this, quality gates are either missing or not working. This command finds what's blocking supremely confident deployments.

## The Meta-Quality Principle

"Are we testing the right things, or just testing things?"

This command audits whether quality checks are worth running. **Establish git hooks** to catch issues locally before CI. Automation should enable deployment confidence, not create bureaucracy.

**The Friday Afternoon Test:**
- All checks green = production ready
- Zero manual verification needed
- No fear of weekend on-call
- AI agents maintain quality autonomously

## Git Hooks

**Setup & Tool Selection**:
- **Lefthook** (recommended): 3-5x faster than Husky, parallel by default
- **Husky**: Mature, large ecosystem, sequential execution
- Use `lint-staged` with either to run only on staged files

**Performance budgets**:
- pre-commit: <5s (format, lint, secrets scan)
- pre-push: <15s (type check, tests, build validation)
- If >20% of commits use `--no-verify`, hooks are too slow/strict

**Hook strategy**:
```yaml
pre-commit (parallel):
  - format: prettier --write {staged_files}
  - lint: eslint --fix --cache {staged_files}
  - secrets: trufflehog git file://. --only-verified --fail

pre-push (sequential ok):
  - type-check: tsc --noEmit --incremental
  - test: vitest --run --changed
  - build: next build (catch build errors locally)
```

**Critical questions**:
- Does this prevent a real CI failure or just annoy devs?
- Fast enough that people won't bypass?
- Provides immediate, actionable feedback?

**Optimization**: staged files only, parallel execution, caching flags, incremental checks.

## CI/CD Pipeline Analysis

Review `.github/workflows/`, `.gitlab-ci.yml`, or equivalent:

**Ask the Carmack question**: "Does this step prevent real bugs or just slow us down?"

- Is every check catching actual issues, or is it security theater?
- Which step is slowest? Can we parallelize or eliminate it?
- Are we running the same checks multiple times?
- Do we have flaky tests that randomly fail?

**Generate actionable improvements**:
- Remove checks that haven't caught real issues in 6 months
- Parallelize independent CI steps
- Fix or delete flaky tests

## PR Size Automation

**The problem**: Large PRs are hard to review, slow to merge, and risky to deploy.

**Target sizes**:
- ≤200 lines: Perfect size (thorough review possible)
- 201-400 lines: Acceptable (larger but manageable)
- 401-500 lines: Large (justify or split)
- >500 lines: Too large (requires splitting or stacking)

**Automated labeling** (free, CLI-only):
```yaml
# .github/workflows/pr-size-labeler.yml
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

**Why this approach**:
- $0 cost (GitHub Action only)
- Automatic visibility into PR size
- No external service dependencies
- CLI-based via `gh pr list --label "size/XL"`

**Splitting strategies**:
- **Vertical slicing**: Feature by feature (each PR adds value)
- **Architectural layering**: Backend → Frontend → Tests
- **Stacked PRs**: Use `git-spr` for dependent changes
- **Feature flags**: Ship incomplete work behind toggles

**Actions**:
- Set up pr-size-labeler workflow
- Establish team norm: Justify any PR >400 lines
- Use `git-spr` for stacking when needed
- Review size distribution monthly (too many XL = process issue)

## Testing & Coverage

**Kent Beck principle**: "Test until fear turns to boredom, then stop."

**Coverage guidelines** (Google research):
- 60% = acceptable, 75% = commendable, 90% = exemplary
- But coverage measures execution, not quality
- Critical paths (payment, auth, data integrity) should be >80%

**Critical audit questions**:
- Testing behavior or implementation details?
- Would these catch last production bug?
- Tests that always pass? Delete them.
- Mocking so much tests prove nothing?
- Runtime acceptable? Can it be 10x faster?

**Anti-patterns**:
- Arbitrary 100% coverage mandates
- Testing getters/setters, framework code
- Shallow tests with no assertions
- Flaky tests (fix or delete)

**What matters**:
- Regression test for every production bug
- Tests fail when behavior changes
- Integration tests for cross-module flows
- **E2E tests for every critical happy path** (auth, checkout, core features)
- Coverage trends (delta, not absolute)

**Tools**:
- **Vitest**: Fast Next.js/React testing with built-in coverage
- **Playwright**: E2E tests (preferred - faster, more reliable)
- **Stryker**: Mutation testing (tests your tests)

## E2E Happy Path Tests (Critical)

**The non-negotiable**: If a user can't complete core flows, nothing else matters.

Unit tests prove components work. E2E tests prove the **product** works. Happy path e2e tests are the final gate before confident deployment—they catch the integration failures that unit tests miss.

**What are happy paths?**
- The journeys that make or break your product
- **Auth**: signup → login → password reset
- **Commerce**: browse → add to cart → checkout → confirmation
- **Core feature**: the main thing users come for
- **Onboarding**: first-time user experience

**Target**: 100% coverage of critical user journeys. Not 100% of all scenarios—just the paths that matter.

**Why e2e for happy paths specifically?**
- Unit tests miss integration failures (API + UI + DB working together)
- Happy paths = highest traffic, highest impact if broken
- A failing happy path test = **blocked deploy** (not optional)
- Catch regressions before users do

**The Friday connection**: You can't turn your phone off if the signup flow might be broken.

**Implementation standards**:
```typescript
// Playwright example - auth happy path
test('user can sign up and access dashboard', async ({ page }) => {
  await page.goto('/signup');
  await page.fill('[name="email"]', 'test@example.com');
  await page.fill('[name="password"]', 'SecurePass123!');
  await page.click('button[type="submit"]');

  await expect(page).toHaveURL('/dashboard');
  await expect(page.locator('h1')).toContainText('Welcome');
});
```

**Tagging convention**: Use `@happy-path` tag on critical journey tests. These run on every PR. Other e2e tests run nightly or on main only.

**Speed optimizations**:
- Parallel execution across browsers/workers
- Shared auth state (login once, reuse session)
- Skip redundant setup (seed data once per suite)
- Run critical paths on every PR, full suite nightly

**CI integration**:
```yaml
# Run happy paths on every PR (fast, critical)
- name: E2E Happy Paths
  run: pnpm exec playwright test --grep @happy-path

# Full suite on main branch only
- name: E2E Full Suite
  if: github.ref == 'refs/heads/main'
  run: pnpm exec playwright test
```

**Red flags**:
- No e2e tests at all (shipping blind)
- E2e tests exist but skip core flows
- Tests only run manually or "when we remember"
- Happy path tests flaky (fix immediately or they become ignored)
- E2E only in nightly builds (regressions discovered too late)

**Coverage Automation (Zero External Services)**:
```yaml
# .github/workflows/ci.yml
- name: Test Coverage
  run: pnpm test -- --coverage

- name: Report Coverage
  if: always()
  uses: davelosert/vitest-coverage-report-action@v2
```

**Why this approach**:
- $0 cost (no Codecov, Coveralls subscription)
- PR comments with patch coverage % (new code only)
- Works offline, no external dependencies
- Differential coverage: Focus on what changed, not legacy code

**Coverage standards**:
- **Patch coverage** (new code): 80%+ target
- **Critical paths** (payment, auth): 90%+ target
- **Standard modules**: 70%+ acceptable
- Don't chase absolute percentages on legacy code

**Actions**:
- Set coverage floor for critical modules only
- Track coverage trends via GitHub Action PR comments
- Remove tests that always pass (they provide false confidence)
- Fail CI if critical path coverage drops
- Use `pnpm test -- --coverage --changed` locally before push

## Linting & Formatting Audit

Are we arguing about style or catching bugs?

**Review linter configs** (ESLint/Prettier/Ruff/rustfmt):
- Which rules actually prevent bugs vs. annoy developers?
- Can we autofix more and review less?
- Are there rules everyone just ignores?
- Do we have conflicting formatters fighting each other?

Code conventions should be invisible, not obstacles.

## Security & Dependency Scanning

**Audit current setup**:
- Signal vs. noise—drowning in false positives?
- Patch speed for critical vulns?
- 500 "low severity" issues we ignore?

**Tools (2025)**:
- **TruffleHog** (preferred, pre-commit): Secrets detection with verification (fewer false positives)
- **Gitleaks** (alternative): Secrets detection, faster but more false positives
- **Trivy** (CI): Dependencies, containers, misconfigs, licenses
- **Dependabot/Renovate**: Auto dependency PRs (choose one)

**Next.js specifics**:
- Keep secrets server-side only (avoid `NEXT_PUBLIC_` prefix for sensitive data)
- Data Access Layer isolates `process.env`
- `process.env.SECRET` in client code = exposed at build

**Action**: Configure HIGH/CRITICAL alerts only. Generate improvements, not noise.

## Documentation Quality Automation

**The problem**: Docs rot faster than code. Broken links, stale examples, inconsistent style.

**Automated checks** (all CLI-first, offline, $0):

### 1. Link Checking (lychee - Rust binary)
```bash
# Install once
brew install lychee

# Check all markdown files
lychee **/*.md --offline --cache

# Add to CI
- name: Check Links
  run: lychee **/*.md --offline
```

**Why lychee**:
- 40x faster than markdown-link-check (Rust vs Node.js)
- Single binary, no npm packages
- Works completely offline
- Caches results for speed

### 2. Style Linting (Vale - Go binary)
```bash
# Install once
brew install vale

# Check documentation style
vale docs/

# Add to CI
- name: Lint Docs
  run: vale docs/
```

**Why Vale**:
- Enforces style guides (Google, Microsoft, write-good)
- Single binary, 100% offline
- YAML configuration (.vale.ini)
- No external dependencies

### 3. Freshness Detection (git-based)
```bash
# Find docs not updated in 90 days
find docs -name '*.md' | while read f; do
  age=$(( ($(date +%s) - $(git log -1 --format=%ct -- "$f")) / 86400 ))
  [ $age -gt 90 ] && echo "$f: $age days stale"
done
```

**Documentation discipline**:
- Update docs in same PR as code changes
- README Quick Start section always current
- ADRs for architectural decisions (never delete, only supersede)
- Living documentation over static docs

**Actions**:
- Install lychee and Vale locally
- Add both to pre-push hooks (fast fail on broken links)
- Run freshness check monthly
- Configure Vale with project style guide

## Changelog & Release Management

"Changelogs are for users, commits are for developers"

**Tool selection**:
- **Changesets**: Explicit declarations, monorepos/libraries, human control over phrasing
- **Release-please**: Analyzes commits, PR-based review, good for apps
- **Semantic-release**: Full automation, conventional commits → version → publish

**Quick map**:
- Monorepos → Changesets
- Apps with frequent deploys → Release-please
- OSS libraries → Semantic-release

**Red flags**:
- Manual `CHANGELOG.md` updates
- No git tag ↔ release correlation
- Breaking changes buried in minors
- 30-minute manual release process

**Action**: Choose tool, configure, automate version bumping. Make releases boring.

## Performance & Build Analysis

What would Knuth measure?
- Do we track bundle size? Build time? Runtime performance?
- Would we notice a 2x performance regression?
- Are we optimizing the right metrics?
- Is our build cache actually working?

## Environment Parity (Next.js/Vercel/Convex)

**The invisible killer**: Works locally, fails in production.

**Pre-deploy checklist**:
- `NEXT_PUBLIC_*` vars in Vercel (prod + preview)
- `CONVEX_DEPLOY_KEY` for preview environments
- Convex deploys **before** Next.js build
- Build succeeds locally with prod-like env vars

**Critical**: Build command must be `npx convex deploy && next build` (not just `next build`)

**Anti-patterns**:
- Secrets with `NEXT_PUBLIC_` prefix (exposed to browser)
- `process.env.SECRET` in client code (bundled at build)
- Different vars across local/preview/prod
- Missing vars discovered only when CI fails

**Automation**: Script to compare env vars across environments. Pre-push validates critical vars exist. Fail fast.

**Insight**: Vercel failures waste 5+ mins. Catch in <30s locally.

## Quick Setup Reference (Next.js/Vercel/Convex)

**Critical configurations**:
```bash
# package.json - key scripts
"build": "npx convex deploy && next build"  # Convex first!
"type-check": "tsc --noEmit --incremental"
"test": "vitest"
"prepare": "lefthook install"

# Vercel - Ignored Build Step (monorepos only)
npx turbo-ignore

# Vitest - coverage on critical paths only
coverage: {
  include: ['src/lib/payment/**', 'src/lib/auth/**'],
  thresholds: { lines: 80, functions: 80 }
}
```

**Setup principles**:
- Parallel execution, caching, incremental checks
- Format → lint → type → test → build progression
- Fail fast at earliest/cheapest stage
- Stack-aware: Convex deploys before Next.js builds

## Output Format

```markdown
## Quality Infrastructure Audit

### Git Hooks Setup
- **Current state**: No hooks / Using X tool
- **Recommendation**: Install `lefthook` (faster than Husky) with:
  - pre-commit: format + lint staged files + secrets scan (< 5s)
  - pre-push: type check + unit tests + Convex validation (< 15s)
- **Performance**: Currently takes Xs, target <5s pre-commit
- **Action**: Generate `.lefthook.yml` configuration

### CI/CD Pipeline
- **Waste**: Step X takes 5 minutes, catches nothing
- **Improvement**: Parallelize Y and Z (saves 3 minutes)
- **Delete**: Remove redundant check W

### Test Suite & Coverage
- **Current coverage**: X% overall, Y% on critical paths
- **Problem**: 200 tests for UI, 0 tests for payment logic
- **Fix**: Add payment integration tests (target >80% on critical paths)
- **Speed**: Replace heavy E2E with targeted unit tests
- **Coverage automation**: Add vitest-coverage-report-action to CI
  - $0 cost, PR comments with patch coverage
  - Focus on differential coverage (new code only)
  - Target: 80%+ patch, 90%+ critical paths
- **Action**: Configure GitHub Action for automated coverage reporting

### E2E Happy Path Tests
- **Current state**: No e2e tests / E2E exists but missing critical paths
- **Critical paths covered**: [List which flows have e2e tests]
- **Missing flows**: signup, checkout, [core feature X]
- **Fix**: Add Playwright tests for all critical user journeys
  - Tag with `@happy-path` for PR-level runs
  - Run on every PR (fast feedback on regressions)
- **Speed**: Parallelize, share auth state, target <2min for happy paths
- **Action**: Create e2e tests for: auth flow, checkout flow, [core feature]

### PR Size Management
- **Current state**: PRs average 600 lines, slow review cycle
- **Problem**: Large PRs = shallow reviews, delayed feedback
- **Fix**: Set up pr-size-labeler GitHub Action
  - Automatic size labeling (XS/S/M/L/XL)
  - Team norm: Justify any PR >400 lines
  - Use git-spr for stacked PRs when needed
- **Action**: Create .github/workflows/pr-size-labeler.yml

### Documentation Quality
- **Current**: No link checking, inconsistent style, 50% of docs >1yr old
- **Tools installed**: None
- **Fix**: Install lychee and Vale (single binaries, 100% offline)
  - lychee for link checking (40x faster than alternatives)
  - Vale for style guide enforcement
  - Git-based freshness detection script
- **Action**: Add to pre-push hooks, integrate into CI

### Linting
- **Noise**: Rule X disabled 500 times
- **Action**: Remove rule—provides no value

### Security Scanning
- **Current**: npm audit / Dependabot / None
- **Finding**: 50 vulnerabilities, 49 false positives
- **Recommendation**:
  - Add TruffleHog pre-commit hook (secrets detection with verification)
  - Add Trivy to CI (comprehensive scanning)
- **Fix**: Configure to alert only on HIGH/CRITICAL severity

### Changelog Management
- **Current**: Manual / None / Using X
- **Problem**: Releases undocumented, version bumps manual
- **Recommendation**: Changesets (monorepo) / Release-please (apps)
- **Action**: Configure automated changelog generation

### Environment Parity (Next.js/Vercel/Convex)
- **Issue**: Build succeeds locally, fails in Vercel
- **Missing**: CONVEX_DEPLOY_KEY not set for preview environments
- **Fix**: Update Vercel env vars, add pre-push env validation script
- **Action**: Ensure `npx convex deploy && next build` in Vercel config

## Generated TODOs
- [ ] [HIGH] Set up Lefthook with pre-commit/pre-push checks
- [ ] [HIGH] Add e2e tests for critical happy paths (auth, checkout, core features)
- [ ] [HIGH] Configure @happy-path tagged tests to run on every PR
- [ ] [HIGH] Add vitest-coverage-report-action to CI workflow
- [ ] [HIGH] Add tests for payment processing (0% coverage on money code)
- [ ] [HIGH] Configure Convex deploy in Vercel build command
- [ ] [MEDIUM] Set up pr-size-labeler GitHub Action workflow
- [ ] [MEDIUM] Install lychee and Vale for documentation quality
- [ ] [MEDIUM] Add TruffleHog pre-commit hook for secrets scanning
- [ ] [MEDIUM] Parallelize CI steps 3 and 4 (saves 3min/build)
- [ ] [MEDIUM] Set up Changesets for changelog automation
- [ ] [LOW] Remove ESLint rule 'no-console' (disabled everywhere)
- [ ] [LOW] Add lychee and Vale to pre-push hooks
- [ ] [LOW] Create freshness detection script for docs
```

## LLM-Specific Quality Gates

**Building LLM-powered apps?** Use `/llm-gates` for specialized audit covering:
- Model selection & routing (OpenRouter, fallbacks)
- Prompt testing & CI/CD (Promptfoo, regression tests)
- LLM observability (Langfuse, cost tracking)
- Security (red teaming, jailbreak protection)
- Cost control (token budgets, alerts)

This command focuses on traditional software quality. LLM apps need additional gates that `/llm-gates` provides.

## The Philosophy

Quality gates should be like a bouncer at a club—keeping out actual troublemakers, not hassling everyone about their shoes. If a gate isn't preventing real problems, it's just theater.

Remember: **The goal isn't to have quality gates. The goal is to ship quality code with supreme confidence.**

### The Friday Afternoon Standard

**Can you merge to production Friday at 5pm and turn your phone off?**

If NO:
- Gates are missing (no pre-commit hooks, no CI/CD)
- Gates are too slow (devs bypass with `--no-verify`)
- Gates are too noisy (false positives, flaky tests)
- Gates miss real bugs (no coverage, shallow checks)

If YES:
- All checks green = production ready
- Zero manual verification needed
- No fear of weekend on-call
- Fast feedback (< 10s pre-commit, < 5min CI)
- Catches real bugs (secret leaks, type errors, test failures, build breaks)

**Quality gates enable fearless deployments. That's the only metric that matters.**
