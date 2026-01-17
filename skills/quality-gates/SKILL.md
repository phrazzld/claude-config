---
name: quality-gates
description: "Apply quality gate standards for git hooks, testing, CI/CD, and automation using Lefthook, Vitest, GitHub Actions, and quality enforcement. Use when setting up quality infrastructure, configuring hooks, discussing automation, or reviewing quality practices."
---

# Quality Gates

**Quality gates prevent problems before they reach production.**

## Philosophy

**Progressive enforcement:**
- **Pre-commit**: Fast checks (lint, format, typecheck) on staged files only
- **Pre-push**: Comprehensive checks (full test suite, coverage)
- **CI/CD**: Production-ready validation (build, E2E tests, security scans)

## Tool Choices

### Git Hooks: Lefthook (not Husky)
- Language-agnostic Go binary
- Faster with parallel execution
- Simpler YAML configuration
- Combines Husky + lint-staged functionality

### Testing: Vitest
- Fast, Jest-compatible API
- Built-in coverage with v8
- Great TypeScript support

### CI/CD: GitHub Actions
- Native GitHub integration
- Matrix builds, artifact storage
- Free tier for private repos

### Coverage: vitest-coverage-report-action
- Shows coverage diff in PRs
- Links to uncovered lines
- Zero external service required

## Quality Checklist

### Essential (Must Have)
- [ ] Lefthook pre-commit (lint, format, typecheck)
- [ ] Lefthook pre-push (test, build)
- [ ] GitHub Actions CI (lint, typecheck, test, build)
- [ ] Branch protection on main
- [ ] Test framework (Vitest)
- [ ] Coverage reporting

### Recommended
- [ ] E2E testing (Playwright)
- [ ] Dependency audit in CI
- [ ] Conventional commits (commitlint)
- [ ] Preview deployments for PRs
- [ ] Security scanning

## Anti-Patterns

- **Husky** → Use Lefthook (faster, simpler)
- **Arbitrary coverage targets** → Use coverage as diagnostic, not metric
- **Testing implementation details** → Test behavior
- **Heavy mocking** → Prefer real integration tests
- **Skipping hooks routinely** → Fix the problem
- **CI only on main** → Test every PR
- **No branch protection** → Enforce quality before merge

## Coverage Philosophy

**Coverage is a diagnostic tool, not a goal.**
- 60% meaningful coverage beats 95% testing implementation details
- Patch coverage: 80%+ for new code
- Critical paths (payment, auth): 90%+
- Overall: Track but don't block

## References

Detailed configurations:
- `references/lefthook-config.md` — Hook configurations (basic, monorepo, Convex)
- `references/github-actions.md` — CI workflows (basic, matrix, E2E, Convex)
- `references/vitest-config.md` — Test configuration and scripts
- `references/branch-protection.md` — GitHub settings, Codecov setup

## Quick Setup

```bash
# Install tools
pnpm add -D lefthook vitest @vitest/coverage-v8 \
  eslint prettier @commitlint/cli @commitlint/config-conventional

# Initialize hooks
pnpm lefthook install

# Create configs (see references/)
# - lefthook.yml
# - vitest.config.ts
# - .github/workflows/ci.yml
```

**Quality is not a phase—it's built into the process.**
