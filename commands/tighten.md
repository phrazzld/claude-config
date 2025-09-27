Clean up the changes made in the current branch before merging.

# TIGHTEN

Your branch works, but it's messy. Time to clean up the crime scene before the code review.

Ultrathink.

## The Branch Cleanup Philosophy

*"Make it work, make it right, make it fast"* - Kent Beck

You made it work. Now make it right. This command focuses exclusively on cleaning up the changes you've made in your current branch - not the entire codebase.

## Your Mission

First, figure out what branch you're merging into (usually main, master, or trunk). Then analyze everything that changed in your current branch and hunt for the mess we all leave behind while getting things to work.

## Find the Mess

Look at the diff between your branch and the base branch. For every file that changed, search for:

### Debug Artifacts We Forgot
- console.log, console.error, console.warn statements
- print() statements in Python
- fmt.Println() in Go
- debugger statements
- Debug flags set to true
- Temporary logging we added to figure out what was breaking
- Stack traces we were printing

### Temporary Code That Became Permanent
- TODO comments that should be addressed now
- FIXME notes we left for ourselves
- "quick fix" or "temporary" in comments
- Hardcoded values that should be configurable
- Magic numbers that should be constants
- Test data left in production code
- Commented-out code from our refactoring
- Old implementations we kept "just in case"

### Code Smells From Rushing
- Copy-pasted code that should be extracted
- Overly complex conditionals that could be simplified
- Functions that got too long while debugging
- Variables named 'temp', 'test', 'foo', 'data', 'thing'
- Deeply nested code from adding "one more if statement"
- Error handling we skipped with // TODO: handle error

### Low-Hanging Refactors
Look for easy wins that make the code cleaner without changing behavior:
- Extract magic numbers to named constants
- Combine multiple similar if statements
- Replace complex conditionals with early returns
- Extract duplicate code blocks into functions
- Rename unclear variables to be descriptive
- Remove unnecessary else blocks after returns
- Simplify boolean expressions (if (x == true) → if (x))

## Output Format

Organize your findings by priority - what would embarrass us most in code review?

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

## Cleanup Checklist
- [ ] Remove all console.logs and debug statements
- [ ] Delete commented-out code blocks
- [ ] Replace magic numbers with constants
- [ ] Extract duplicate code segments
- [ ] Rename unclear variables
- [ ] Address or remove TODO/FIXME comments
- [ ] Simplify complex conditionals
```

## The Golden Rules

1. **Only touch files changed in this branch** - Don't go fixing the whole codebase
2. **Don't change behavior** - We're cleaning, not refactoring
3. **Quick wins only** - If it takes more than 2 minutes, skip it
4. **No new features** - Save that for another branch

## Success Metrics

Your branch is clean when:
- No debug output in the code
- No commented-out code blocks
- No TODOs that could be done now
- No obvious code duplication
- No magic numbers
- Variable names make sense
- The diff would make you proud in a job interview

Remember: **A clean branch is a mergeable branch.**
