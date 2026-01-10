---
description: Implement GitHub issue with semantic commits
argument-hint: <issue-id>
allowed-tools: Bash(gh:*), Bash(git:*)
---

# BUILD

> Stop planning. Start shipping. — Carmack

Implement Issue #$1. Autonomous execution with semantic commits.

## Mission

Execute the product spec and technical design from Issue #$1. Ship working, tested, committed code.

## Prerequisites

If on `master` or `main`, checkout a work branch named after the issue (e.g., `feature/issue-$1` or `fix/issue-$1` depending on issue type).

## Startup

```bash
gh issue view $1 --comments
gh issue edit $1 --remove-label "status/ready" --add-label "status/in-progress"
```

Extract from comments:
- **Product Spec**: WHAT and WHY
- **Technical Design**: HOW

## Execution Loop

```
while not complete and not blocked:
    1. Identify next logical chunk
    2. Implement (parallelize if independent modules)
    3. Test
    4. Verify (build, lint)
    5. Commit: `feat: description (#$1)`
```

## Commit Strategy

- Semantic commits referencing issue: `feat: add auth endpoint (#$1)`
- Logical units (not too granular, not too large)
- Final commit closes: `feat: complete auth flow (closes #$1)`

## Quality Gates

Before commit: `pnpm build && pnpm test && pnpm lint`

## UI Verification (Web Projects)

If Next.js/React project AND dev server is running (localhost:3000):

1. Use Chrome MCP to navigate to affected routes
2. Take screenshot + read console for errors
3. Fix any console errors or visual issues
4. Re-verify until clean

This implements the Boris Cherny pattern: Claude verifies its own UI work.

```
# Automatic UI verification loop
for each affected_route:
    navigate(localhost:3000 + route)
    screenshot()
    console_errors = read_console()
    if console_errors:
        fix_errors()
        re-verify()  # loop until clean
```

## Stopping Conditions

**Continue until**: All stories implemented, tests pass, build succeeds, issue closed.

**Stop if blocked**: Need user input, major architectural deviation required, environment broken.

## Completion

```markdown
## Build Complete: [Feature]

**Commits**: N semantic commits
**Files Changed**: N files

**What was built**:
- [Module]: [description]

**Verification**: ✅ tests ✅ build ✅ lint
```
