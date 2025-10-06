Audit and improve quality infrastructure.

# GATES

Channel platform engineering thinking: critically examine quality gates and identify improvements.

## The Meta-Quality Principle

"Are we testing the right things, or just testing things?"

This command doesn't run quality checks—CI/CD does that. This audits whether your quality checks are even worth running.

**Automation should catch real problems, not create bureaucracy**. Prefer simple checks preventing actual bugs over complex rules slowing development. If it can be automated, it should be—manual quality checks are bug-prone and time-consuming.

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

## Test Infrastructure Critique

Channel Kent Beck: "Test until fear turns to boredom, then stop."

**Examine test setup**:
- Are we testing implementation details or actual behavior?
- What's test runtime? Can we make it 10x faster?
- Do we have tests that always pass? Delete them.
- Are we mocking so much that tests prove nothing?
- Coverage percentage vs. actual confidence level?

**The key question**: Would these tests catch the bug that took down production last time?

## Linting & Formatting Audit

Are we arguing about style or catching bugs?

**Review linter configs** (ESLint/Prettier/Ruff/rustfmt):
- Which rules actually prevent bugs vs. annoy developers?
- Can we autofix more and review less?
- Are there rules everyone just ignores?
- Do we have conflicting formatters fighting each other?

Code conventions should be invisible, not obstacles.

## Security & Dependency Scanning

Audit Dependabot/Snyk/npm audit configurations:
- Signal vs. noise ratio—drowning in false positives?
- How fast do we actually patch critical vulnerabilities?
- Are we checking for secrets in the right places?
- Do we have 500 "low severity" issues we ignore?

Generate actionable improvements, not more noise.

## Performance & Build Analysis

What would Knuth measure?
- Do we track bundle size? Build time? Runtime performance?
- Would we notice a 2x performance regression?
- Are we optimizing the right metrics?
- Is our build cache actually working?

## Output Format

```markdown
## Quality Infrastructure Audit

### CI/CD Pipeline
- **Waste**: Step X takes 5 minutes, catches nothing
- **Improvement**: Parallelize Y and Z (saves 3 minutes)
- **Delete**: Remove redundant check W

### Test Suite
- **Problem**: 200 tests for UI, 0 tests for payment logic
- **Fix**: Add payment integration tests
- **Speed**: Replace heavy E2E with targeted unit tests

### Linting
- **Noise**: Rule X disabled 500 times
- **Action**: Remove rule—provides no value

### Security
- **Finding**: 50 vulnerabilities, 49 false positives
- **Fix**: Configure to alert only on exploitable issues

## Generated TODOs
- [ ] [HIGH] Add tests for payment processing (0% coverage on money code)
- [ ] [MEDIUM] Parallelize CI steps 3 and 4 (saves 3min/build)
- [ ] [LOW] Remove ESLint rule 'no-console' (disabled everywhere)
```

## The Philosophy

Quality gates should be like a bouncer at a club—keeping out actual troublemakers, not hassling everyone about their shoes. If a gate isn't preventing real problems, it's just theater.

Remember: **The goal isn't to have quality gates. The goal is to ship quality code.**
