Check CI status for the current PR and generate actionable resolution tasks for failures.

# CI

## Check CI Status

Use `gh` to check CI status for the current PR:
- If successful, celebrate and stop
- If in progress, wait 30 seconds and check again
- If failed, proceed to analyze

## Analyze CI Failure

Create `CI-FAILURE-SUMMARY.md` with comprehensive failure details: build info, error logs, failed steps, affected components.

**Make the invisible visible**—don't guess at CI failures. Add logging, capture state, trace the failure path. Document actual vs expected behavior clearly. Surface all assumptions about the CI environment and make hidden dependencies obvious.

## Generate Resolution Plan

**Think critically about failure sources**. CI failures stem from two distinct sources—carefully evaluate both:

**1. Code Issues** (problems in the code being tested):
- Your changes introduced bugs or regressions
- Tests legitimately catching errors in business logic
- Dependencies or integrations not working as expected

**2. CI Infrastructure Issues** (problems with CI system itself):
- Flaky tests failing intermittently
- Environmental configuration problems
- CI pipeline design flaws or misconfigurations
- Resource constraints (timeouts, memory limits)
- External service dependencies unavailable
- Outdated or incorrect test data/fixtures

**Analyze deeply**:
- First determine: Is this legitimate code issue or CI infrastructure problem?
- Analyze error messages and stack traces in detail
- Look for patterns: Has this test failed before? Known to be flaky?
- Identify specific components or tests failing
- Consider environmental factors causing failure
- Think about recent changes that could have introduced issue
- Develop multiple hypotheses, categorizing each as code or CI issue
- Prioritize most likely causes based on evidence

Create `CI-RESOLUTION-PLAN.md` with your comprehensive analysis and resolution approach.

## Generate Resolution Tasks

Break down the resolution plan into actionable tasks:

**For Code Issues**:
- Fix actual bugs or regressions in code
- Update unit tests to cover fixed scenarios
- Verify integrations and dependencies work correctly

**For CI Infrastructure Issues**:
- Mark flaky tests for refactoring or add retry mechanisms
- Update CI configuration to address environmental issues
- Fix resource constraints or timeout settings
- Update test fixtures or mock external dependencies
- Document known CI quirks for future reference

**Label each task clearly**: [CODE FIX] or [CI FIX]

Decompose fixes into atomic, testable steps. Consider order of operations to avoid breaking other functionality. Include verification steps. Add tasks for preventing similar failures. Think about edge cases. Ensure each task is clear and independently executable.

Insert specific, well-formatted tasks into `@TODO.md`, then remove temporary files.
