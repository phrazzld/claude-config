Clean up the changes made in the current branch before merging.

# TIGHTEN

Your branch works, but it's messy. Time to clean up the crime scene before code review.

## The Branch Cleanup Philosophy

"Make it work, make it right, make it fast" - Kent Beck

You made it work. Now make it right. This command focuses exclusively on cleaning up changes you've made in your current branch—not the entire codebase.

**Simplicity**: Prefer the simplest solution that solves the problem completely. Remove clever code in favor of boring, obvious implementations.

**Maintainability**: Write for the developer who will modify this in six months. Clear naming, consistent patterns, and obvious intent matter more than cleverness.

## Your Mission

First, figure out what branch you're merging into (usually main, master, or trunk). Then analyze everything that changed in your current branch and hunt for the mess we all leave behind while getting things to work.

**Look at the diff** between your branch and base branch. For every changed file, search for:

### Debug Artifacts We Forgot
console.log/console.error, print() statements, fmt.Println(), debugger statements, debug flags set to true, temporary logging, stack traces we were printing

### Temporary Code That Became Permanent
TODO/FIXME notes that should be addressed now, "quick fix" or "temporary" in comments, hardcoded values that should be configurable, magic numbers that should be constants, test data left in production code, commented-out code from refactoring, old implementations kept "just in case"

### Code Smells From Rushing
Copy-pasted code that should be extracted, overly complex conditionals that could be simplified, functions that got too long while debugging, variables named 'temp', 'test', 'foo', 'data', 'thing', deeply nested code from "one more if statement", error handling skipped with // TODO: handle error

### Low-Hanging Refactors
Easy wins that make code cleaner without changing behavior:
- Extract magic numbers to named constants
- Combine multiple similar if statements
- Replace complex conditionals with early returns
- Extract duplicate code blocks into functions
- Rename unclear variables to be descriptive
- Remove unnecessary else blocks after returns
- Simplify boolean expressions (if (x == true) → if (x))

## Organize by Priority

What would embarrass us most in code review?

```markdown
## Branch Cleanup Report

### 🚨 Critical - Debug Code in Production
- `src/api/handler.js:47` - console.log with user passwords
- `lib/auth.py:92` - debugger statement left in
- `main.go:156` - fmt.Println dumping entire request

### ⚠️ High - Temporary Code to Remove
- `components/Dashboard.tsx:234` - TODO: remove hardcoded API key
- `utils/helper.js:89-95` - Commented out old implementation
- `services/email.py:45` - FIXME: this is a hack

### 🧹 Medium - Code Quality Improvements
- `controllers/user.js:67-89` - Duplicate code, extract to function
- `models/order.py:234` - Magic number 86400, should be SECONDS_IN_DAY
- `components/Form.tsx:145-167` - Deeply nested, needs early returns

### 💅 Low - Polish
- `utils/calc.js:23` - Variable 'temp' should be 'normalizedValue'
- `lib/validator.py:67` - if result == True → if result
- `api/routes.go:89` - Remove else after return
```

## Golden Rules

1. **Only touch files changed in this branch** - Don't fix the whole codebase
2. **Don't change behavior** - We're cleaning, not refactoring
3. **Quick wins only** - If it takes more than 2 minutes, skip it
4. **No new features** - Save that for another branch

## Success Metrics

Your branch is clean when:
- No debug output in code
- No commented-out code blocks
- No TODOs that could be done now
- No obvious code duplication
- No magic numbers
- Variable names make sense
- The diff would make you proud in a job interview

Remember: **A clean branch is a mergeable branch.**
