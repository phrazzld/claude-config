---
description: Validate pull request readiness with comprehensive quality gates
---

# PR READY

Comprehensive validation that work is ready for pull request creation.

## Mission

Give confidence before creating PR. Run automated checks to ensure quality gates pass, catch issues early, and prevent premature PRs.

## Quality Gates

### 1. Task Completion
**Check**: All TODO.md tasks marked `[x]` complete?

**Validation**:
- Read TODO.md
- Count tasks by status: `[ ]` pending, `[~]` in-progress, `[x]` complete
- Report: "Tasks: X complete, Y pending, Z in-progress"

**Blocker**: If any tasks pending or in-progress, list them and exit.

### 2. Test Suite
**Check**: All tests passing?

**Validation**:
- Detect test command from package.json: `npm test`, `pnpm test`, `yarn test`, etc.
- Run test suite
- Capture results

**Blocker**: If tests fail, report failures with file locations. Offer to run /debug on failing tests.

### 3. Linting
**Check**: Code style clean?

**Validation**:
- Detect lint command from package.json: `eslint`, `lint`, etc.
- Run linter
- Capture issues

**Blocker**: If linting fails, report issues. Offer to auto-fix: "Run lint --fix?"

### 4. Type Checking
**Check**: TypeScript/Flow types valid?

**Validation**:
- Check for tsconfig.json or .flowconfig
- Run type checker: `tsc --noEmit` or `flow check`
- Capture type errors

**Blocker**: If type errors exist, report with file:line locations.

### 5. Build Validation
**Check**: Production build succeeds?

**Validation**:
- Detect build command from package.json
- Run build (or skip if no build step)
- Check for build errors

**Blocker**: If build fails, report error details.

### 6. Debug Artifact Scan
**Check**: No debugging artifacts left in code?

**Validation**:
- Grep for common debug patterns:
  - `console.log`, `console.debug`, `console.trace`
  - `debugger` statements
  - `TODO`, `FIXME`, `HACK` comments (warn only)
  - `.only` in tests (jest.only, it.only, describe.only)

**Warning**: Report locations but don't block (some may be intentional).

### 7. Branch Synchronization
**Check**: Branch up to date with main?

**Validation**:
- Run `git fetch origin main`
- Check if branch behind main: `git rev-list HEAD..origin/main --count`
- Report: "Branch is X commits behind main"

**Blocker**: If behind, recommend: "Run /git-merge-main to update branch first."

### 8. Uncommitted Changes
**Check**: All changes committed?

**Validation**:
- Run `git status --short`
- Check for uncommitted changes

**Blocker**: If uncommitted changes exist, list them and recommend committing first.

## Report Format

```markdown
## PR Readiness Check

✅ Tasks: 8/8 complete
✅ Tests: 47 passing
✅ Linting: No issues
✅ Type check: No errors
✅ Build: Success
⚠️  Debug artifacts: 2 console.log statements found (review recommended)
✅ Branch sync: Up to date with main
✅ Git status: All changes committed

**Status**: READY ✅

Proceed with /git-pr to create pull request.
```

Or if blockers found:

```markdown
## PR Readiness Check

✅ Tasks: 8/8 complete
❌ Tests: 3 failing (src/utils/parser.test.ts)
✅ Linting: No issues
❌ Type check: 5 errors in src/types/user.ts:23-45
⚠️  Build: Not run (fix tests and types first)
✅ Branch sync: Up to date with main
✅ Git status: All changes committed

**Status**: BLOCKED ❌

**Critical Issues**:
1. Fix 3 failing tests in src/utils/parser.test.ts
2. Resolve 5 type errors in src/types/user.ts

Run /debug to investigate test failures, or fix manually and re-run /pr-ready.
```

## Automatic Fixes

For fixable issues, offer automatic remediation:
- Linting issues: "Run lint --fix?" (if user confirms, run and re-check)
- Behind main: "Merge main branch?" (if confirmed, run /git-merge-main)
- Debug artifacts: "Remove console.log statements?" (list locations, ask confirmation)

## Success Criteria

- Clear READY/BLOCKED status
- Specific file:line locations for all issues
- Actionable next steps
- Option to run /git-pr immediately if all gates pass

## Philosophy

"Catch issues before code review, not during. Reviewers should focus on design and logic, not lint errors and failing tests."

Quality gates should be automatic and fast. If checks take >30s, optimize them (parallel execution, caching, incremental checks).
