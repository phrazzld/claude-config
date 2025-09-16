Audit and improve our quality infrastructure.

# GATES

What would a platform engineer do? Critically examine our quality gates and identify improvements.

## The Meta-Quality Principle

*"Are we testing the right things, or just testing things?"* - Every Senior Engineer

This command doesn't run quality checks - CI/CD does that. This audits whether your quality checks are even worth running.

## 1. CI/CD Pipeline Analysis

**Review `.github/workflows/`, `.gitlab-ci.yml`, or equivalent:**

- **The Carmack Test**: "Does this step prevent real bugs or just slow us down?"
- Is every check catching actual issues, or is it security theater?
- Which step is the slowest? Can we parallelize or eliminate it?
- Are we running the same checks multiple times?
- Do we have flaky tests that randomly fail?

**Generate TODOs:**
- [ ] Remove checks that haven't caught a real issue in 6 months
- [ ] Parallelize independent CI steps
- [ ] Fix or delete flaky tests

## 2. Test Infrastructure Critique

**Channel Kent Beck**: "Test until fear turns to boredom, then stop."

**Examine test setup and configuration:**
- Are we testing implementation details or actual behavior?
- What's our test runtime? Can we make it 10x faster?
- Do we have tests that always pass? Delete them.
- Are we mocking so much that tests prove nothing?
- Coverage percentage vs. actual confidence level?

**The Torvalds Question**: "Would these tests catch the bug that took down production last time?"

## 3. Linting & Formatting Audit

**The Real Question**: Are we arguing about style or catching bugs?

**Review ESLint/Prettier/Ruff/rustfmt configs:**
- Which rules actually prevent bugs vs. annoy developers?
- Can we autofix more and review less?
- Are there rules that everyone just ignores?
- Do we have conflicting formatters fighting each other?

**The Crockford Test**: "Code conventions should be invisible, not obstacles."

## 4. Security & Dependency Scanning

**Audit Dependabot/Snyk/npm audit configurations:**
- Signal vs. noise ratio - are we drowning in false positives?
- How fast do we actually patch critical vulnerabilities?
- Are we checking for secrets in the right places?
- Do we have 500 "low severity" issues we ignore?

**Generate actionable improvements, not more noise.**

## 5. Performance & Build Analysis

**What would Knuth measure?**
- Do we track bundle size? Build time? Runtime performance?
- Would we notice a 2x performance regression?
- Are we optimizing the right metrics?
- Is our build cache actually working?

## Output Format

```markdown
## Quality Infrastructure Audit Results

### CI/CD Pipeline
- **Waste Found**: Step X takes 5 minutes, catches nothing
- **Improvement**: Parallelize Y and Z (saves 3 minutes)
- **Delete**: Remove redundant check W

### Test Suite
- **Problem**: 200 tests for UI, 0 tests for payment logic
- **Fix**: Add payment integration tests
- **Speed**: Replace heavy E2E tests with targeted unit tests

### Linting
- **Noise**: Rule X has 500 disabled instances
- **Action**: Remove rule X, it provides no value

### Security
- **Finding**: 50 npm vulnerabilities, 49 are false positives
- **Fix**: Configure to only alert on actually exploitable issues

## Generated TODOs
- [ ] [HIGH] Add tests for payment processing (0% coverage on money code)
- [ ] [MEDIUM] Parallelize CI steps 3 and 4 (saves 3 min per build)
- [ ] [LOW] Remove ESLint rule 'no-console' (disabled everywhere anyway)
```

## The Philosophy

Your quality gates should be like a bouncer at a club - keeping out actual troublemakers, not hassling everyone about their shoes. If a gate isn't preventing real problems, it's just theater.

Remember: **The goal isn't to have quality gates. The goal is to ship quality code.**