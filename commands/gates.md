Audit and improve quality infrastructure.

# GATES

Channel platform engineering thinking: critically examine quality gates and identify improvements.

## The Meta-Quality Principle

"Are we testing the right things, or just testing things?"

This command audits whether quality checks are worth running. **Establish git hooks** to catch issues locally before CI. Automation should catch real problems, not create bureaucracy.

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
  - secrets: gitleaks protect --staged

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
- Coverage trends (delta, not absolute)

**Tools**:
- **Vitest**: Fast Next.js/React testing
- **Playwright**: E2E tests
- **Stryker**: Mutation testing (tests your tests)

**Actions**:
- Set coverage floor for critical modules only
- Track coverage trends
- Delete tests that never fail
- Fail CI if critical path coverage drops

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
- **Gitleaks** (pre-commit): Secrets detection
- **Trivy** (CI): Dependencies, containers, misconfigs, licenses
- **TruffleHog**: Git history secrets
- **Dependabot/Renovate**: Auto dependency PRs (choose one)

**Next.js specifics**:
- Never `NEXT_PUBLIC_` prefix secrets
- Data Access Layer isolates `process.env`
- `process.env.SECRET` in client code = exposed at build

**Action**: Configure HIGH/CRITICAL alerts only. Generate improvements, not noise.

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
- **Action**: Configure Vitest with coverage thresholds for critical modules only

### Linting
- **Noise**: Rule X disabled 500 times
- **Action**: Remove rule—provides no value

### Security Scanning
- **Current**: npm audit / Dependabot / None
- **Finding**: 50 vulnerabilities, 49 false positives
- **Recommendation**:
  - Add Gitleaks pre-commit hook (secrets detection)
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
- [ ] [HIGH] Add tests for payment processing (0% coverage on money code)
- [ ] [HIGH] Configure Convex deploy in Vercel build command
- [ ] [MEDIUM] Add Gitleaks pre-commit hook for secrets scanning
- [ ] [MEDIUM] Parallelize CI steps 3 and 4 (saves 3min/build)
- [ ] [MEDIUM] Set up Changesets for changelog automation
- [ ] [LOW] Remove ESLint rule 'no-console' (disabled everywhere)
- [ ] [LOW] Add coverage tracking for critical paths only
```

## The Philosophy

Quality gates should be like a bouncer at a club—keeping out actual troublemakers, not hassling everyone about their shoes. If a gate isn't preventing real problems, it's just theater.

Remember: **The goal isn't to have quality gates. The goal is to ship quality code.**
