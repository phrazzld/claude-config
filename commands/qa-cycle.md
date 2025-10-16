---
description: Integrated manual QA with inline debugging and fix tracking
---

# QA CYCLE

Streamlined manual quality assurance with integrated debugging and immediate fix workflow.

## Mission

Close the loop between QA, debugging, and fixes. Keep everything in conversational flow without breaking context or switching to external tools.

## When to Use

- After completing TODO.md implementation
- Before creating pull request
- After addressing PR feedback
- When manual testing is required (UI, integration, user workflows)

## Phase 1: Test Planning

**Generate test scenarios** based on implemented work:

1. Read TODO.md completed tasks
2. Identify what changed (features added, bugs fixed, refactorings)
3. Generate test scenarios covering:
   - **Happy paths**: Expected user workflows
   - **Edge cases**: Boundary conditions, unusual inputs
   - **Regression**: Previously broken functionality
   - **Integration**: Component interactions
   - **UI/UX**: Visual correctness, responsive design

4. Create test checklist:
```markdown
## QA Test Plan

### Feature: [Feature Name]

**Happy Path Tests**:
- [ ] Test 1: Description of scenario and expected outcome
- [ ] Test 2: ...

**Edge Cases**:
- [ ] Test 3: Boundary condition to verify
- [ ] Test 4: ...

**Regression**:
- [ ] Test 5: Verify bug X still fixed
- [ ] Test 6: ...

**Integration**:
- [ ] Test 7: Component A + B interaction
- [ ] Test 8: ...
```

## Phase 2: Guided Testing

Present test cases one at a time for manual execution:

**For each test**:
1. **Present scenario**: "Test 3: Click submit button with empty form"
2. **Expected behavior**: "Should display validation error messages"
3. **User performs test** manually
4. **User reports result**: PASS / FAIL / BLOCKED

### On PASS
- ✅ Mark test passed
- Document passing behavior
- Move to next test

### On FAIL
- ❌ Capture failure details immediately:
  - "What happened instead of expected behavior?"
  - "Can you paste screenshot?" (user can paste image directly)
  - "Any error messages in console?"
  - "Steps to reproduce?"

- **Launch inline debugging**:
  - Analyze failure with captured evidence
  - Form hypothesis about root cause
  - Investigate code (grep, read relevant files)
  - Identify specific issue with file:line

- **Generate fix**:
  - Offer options:
    - **Fix now**: Create TODO item and execute immediately
    - **Add to TODO**: Add fix task to TODO.md for later
    - **Add to BACKLOG**: Not critical, backlog it

- **If fix now**:
  - Create task: `- [ ] Fix: [issue description]` in TODO.md
  - Run /execute to implement fix
  - After fix committed, **re-run failed test**
  - Verify PASS before continuing

### On BLOCKED
- ⚠️ Capture blocker details
- Add blocker to BACKLOG.md with context
- Mark test as blocked, move to next

## Phase 3: Regression Tracking

After all tests complete or fixes applied:

**Re-run failed tests** to verify fixes:
- Present previously failed tests again
- User re-tests manually
- Confirm all now PASS

**Generate test summary**:
```markdown
## QA Results

**Tests Run**: 12
**Passed**: 10 ✅
**Failed → Fixed**: 2 ✅
**Blocked**: 0

**Issues Found & Resolved**:
1. Submit button validation - Fixed in abc123
2. Modal scroll behavior - Fixed in def456

**Status**: All tests passing ✅
```

## Phase 4: Documentation

Update any relevant documentation based on findings:
- Discovered edge cases worth documenting?
- User workflows that need clarity?
- Known limitations to note?

## Multimodal Evidence Support

**Screenshots**: User can paste images directly during FAIL reporting
**Logs**: User can paste console errors, stack traces inline
**Videos**: User can reference video files

All evidence analyzed immediately for debugging.

## Success Criteria

- All critical tests passing
- Failures debugged and fixed in same session
- No context switching to external tools
- Clear QA summary generated
- Ready for /pr-ready validation

## Example Session Flow

```
> /qa-cycle

Analyzing completed work...
Generated 8 test scenarios.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Test 1/8: Login with valid credentials
Expected: User redirected to dashboard
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Result? [PASS/FAIL/BLOCKED]: PASS

✅ Test passed

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Test 2/8: Login with invalid password
Expected: Error message displayed
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Result? [PASS/FAIL/BLOCKED]: FAIL

What happened instead?
> No error message, page just refreshes

Can you paste screenshot or console errors?
> [user pastes screenshot showing blank page]

Analyzing failure...

Found issue: LoginForm.tsx:45 - error state not being set
Root cause: Missing error handler in auth service

Options:
1. Fix now (create task + execute immediately)
2. Add to TODO.md for next session
3. Add to BACKLOG.md (not critical)

Choice [1/2/3]: 1

Adding task to TODO.md and fixing...
[executes fix]
Fix committed: abc123

Please re-test: Login with invalid password

Result? [PASS/FAIL/BLOCKED]: PASS

✅ Test now passing

[continues through remaining tests...]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
QA Complete: 8/8 tests passing ✅
2 issues found and fixed
Ready for /pr-ready
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Philosophy

"QA should catch issues, debugging should find root causes, and fixes should happen immediately. Don't let bugs wait."

Keep the feedback loop tight: Test → Fail → Debug → Fix → Re-test. All in one conversational flow.
