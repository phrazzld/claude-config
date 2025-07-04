Check the CI status for the current PR and generate actionable resolution tasks for failures.

## 1. Check CI Status
- Use `gh` to check the CI status for the current PR
- If successful, celebrate and stop
- If in progress, wait thirty seconds and check again
- If failed, proceed to analyze the failure

## 2. Analyze CI Failure
- Create `CI-FAILURE-SUMMARY.md` with comprehensive failure details
- Include build information, error logs, failed steps, and affected components

## 3. Generate Resolution Plan
- **Leyline Pre-Processing**: Query failure analysis principles:
  - Tenets related to quality gates, automation, and systematic problem-solving
  - Bindings for CI/CD practices and failure remediation patterns
  - Internalize debugging methodologies and root cause analysis approaches
- **Critical Distinction**: CI failures can stem from two sources - carefully evaluate both:
  1. **Code Issues**: Problems in the code being tested
     - Your recent changes introduced bugs or regressions
     - Tests legitimately catching errors in business logic
     - Dependencies or integrations not working as expected
  2. **CI Infrastructure Issues**: Problems with the CI system itself
     - Flaky tests that fail intermittently
     - Environmental configuration problems
     - CI pipeline design flaws or misconfigurations
     - Resource constraints (timeouts, memory limits)
     - External service dependencies unavailable
     - Outdated or incorrect test data/fixtures
- Think very hard about the CI failure and its root causes:
  - First determine: Is this a legitimate code issue or a CI infrastructure problem?
  - Analyze the error messages and stack traces in detail
  - Look for patterns: Has this test failed before? Is it known to be flaky?
  - Identify the specific components or tests that are failing
  - Consider environmental factors that might be causing the failure
  - Think about recent changes that could have introduced the issue
  - Develop multiple hypotheses for the failure cause, categorizing each as either:
    - Code issue that needs fixing
    - CI issue that needs infrastructure/test improvements
  - Prioritize the most likely causes based on the evidence
- Create `CI-RESOLUTION-PLAN.md` with your comprehensive analysis and resolution approach

## 4. Generate Resolution Tasks
- Think very hard about breaking down the resolution plan into actionable tasks:
  - **For Code Issues**:
    - Fix the actual bugs or regressions in the code
    - Update unit tests to cover the fixed scenarios
    - Verify integrations and dependencies work correctly
  - **For CI Infrastructure Issues**:
    - Mark flaky tests for refactoring or add retry mechanisms
    - Update CI configuration to address environmental issues
    - Fix resource constraints or timeout settings
    - Update test fixtures or mock external dependencies
    - Document known CI quirks for future reference
  - Decompose the fix into atomic, testable steps
  - Consider the order of operations to avoid breaking other functionality
  - Include verification steps to ensure the fix works
  - Add tasks for preventing similar failures in the future
  - Think about edge cases that need to be addressed
  - Ensure each task is clear and independently executable
  - **Important**: Label each task clearly as either [CODE FIX] or [CI FIX]
- Create specific, well-formatted tasks and insert them into `@TODO.md`
- Remove temporary files