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
- Think very hard about the CI failure and its root causes:
  - Analyze the error messages and stack traces in detail
  - Identify the specific components or tests that are failing
  - Consider environmental factors that might be causing the failure
  - Think about recent changes that could have introduced the issue
  - Develop multiple hypotheses for the failure cause
  - Prioritize the most likely causes based on the evidence
- Create `CI-RESOLUTION-PLAN.md` with your comprehensive analysis and resolution approach

## 4. Generate Resolution Tasks
- Think very hard about breaking down the resolution plan into actionable tasks:
  - Decompose the fix into atomic, testable steps
  - Consider the order of operations to avoid breaking other functionality
  - Include verification steps to ensure the fix works
  - Add tasks for preventing similar failures in the future
  - Think about edge cases that need to be addressed
  - Ensure each task is clear and independently executable
- Create specific, well-formatted tasks and insert them into `@TODO.md`
- Remove temporary files
