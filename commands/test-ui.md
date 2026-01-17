---
description: Verify UI changes using Chrome automation with screenshot feedback
argument-hint: [optional: route to test, e.g. /dashboard]
---

# /test-ui - Browser UI Verification

Verify UI changes using Chrome automation. Implements the Boris Cherny pattern:
> "Claude tests every single change using the Claude Chrome extension. It opens a browser, tests the UI, and iterates until the code works and UX feels good."

## Arguments

- `$ARGUMENTS` - Optional: specific route(s) to test (e.g., `/dashboard`, `/settings`)
- If no arguments, test the root route `/`

## Workflow

### 1. Initialize Chrome Context

```
Use mcp__claude-in-chrome__tabs_context_mcp to get tab context.
If no tabs exist, use mcp__claude-in-chrome__tabs_create_mcp to create one.
```

### 2. Navigate and Capture

For each route to test:

1. Navigate to `http://localhost:3000{route}` (or $ARGUMENTS if full URL)
2. Wait 2 seconds for page to load
3. Take a screenshot using `mcp__claude-in-chrome__computer` with action: screenshot
4. Read console messages using `mcp__claude-in-chrome__read_console_messages` with pattern for errors/warnings

### 3. Analyze

For each captured screenshot + console output:

**Console Analysis:**
- Any red console errors? (Critical - must fix)
- Any warnings? (Review and fix if significant)
- Any unhandled promise rejections? (Must fix)

**Visual Analysis:**
- Layout renders correctly?
- No missing elements or broken styling?
- Text is readable?
- Interactive elements visible?

### 4. Report and Fix

If issues found:
1. List all issues with severity (Critical/Warning/Info)
2. For each Critical issue:
   - Identify root cause in code
   - Apply fix
   - Re-run verification
3. Loop until all Critical issues resolved

If no issues:
1. Report "UI verification passed"
2. Note any minor observations

## Example Usage

```
/test-ui                      # Test root route
/test-ui /dashboard           # Test specific route
/test-ui /login /signup       # Test multiple routes
/test-ui http://localhost:5173 # Test custom URL (Vite)
```

## Integration

This command is called automatically by `/build` for web projects when dev server is running.
Can also be invoked manually for targeted UI verification.

## Quality Standard

**Pass criteria:**
- Zero console errors
- All interactive elements accessible
- Layout matches expected design
- No visual regressions

**Iterate until passing** - this is the key to the 2-3x quality improvement.
