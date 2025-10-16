---
description: Complete workflow from specification to shipped pull request
---

# SHIP

End-to-end feature development and delivery orchestration.

## Mission

Take a feature from concept to PR-ready code through automated workflow orchestration. Single command for the entire development cycle.

## When to Use

- Starting a new feature or significant change
- Want automated workflow without manual command chaining
- Prefer guided process with validation gates

## Process

### Phase 1: Specification
Run /spec to create comprehensive specification in TASK.md.

Wait for user input and clarifying questions. Finalize spec before proceeding.

### Phase 2: Planning
Once spec is complete, run /plan to convert specification into actionable TODO.md tasks.

### Phase 3: Execution
Run /execute repeatedly until all tasks complete:
- Check task readiness before execution
- If task lacks specificity, gather context and refine inline
- Implement with principles (simplicity, explicitness, maintainability)
- Commit atomically after each completed task
- Mark complete and move to next task
- Continue until all tasks marked [x]

### Phase 4: Validation
Run /pr-ready to ensure all quality gates pass:
- All TODO.md tasks completed
- Tests passing
- Linting clean
- Build succeeds
- No debugging artifacts
- Branch up to date with main

If validation fails, address blockers and re-validate.

### Phase 5: Delivery
Once validation passes, run /git-pr to create pull request with auto-generated description.

## Success Criteria

- Pull request created and ready for review
- All quality gates green
- Clear PR description generated
- No manual command chaining required

## Notes

This command orchestrates your full development workflow. It will pause for user input during spec refinement and address blockers as they arise.

If you prefer more control, use individual commands (/spec, /plan, /execute, /git-pr) instead.
