---
name: codex-coworker
description: "Invoke Codex CLI as a coworker for implementation, brainstorming, specs, and reviews. Use when you want parallel thinking, cheap execution, or a second opinion. Codex tokens are cheaper than yours — delegate aggressively. Keywords: codex, delegate, implement, draft, review, brainstorm, write tests, code review."
---

# Codex as Coworker

Codex is a capable senior engineer you can delegate to. Think of it as having a coworker who can:

- Draft specs while you think through architecture
- Implement code based on patterns you've identified
- Review your work for bugs and edge cases
- Write tests for code you've written
- Brainstorm approaches to a problem

Your tokens are expensive and limited. Codex tokens are cheap. Delegate aggressively.

## Invocation

**Preferred: File output (minimizes your token consumption)**
```bash
codex exec --full-auto "Implement X" --output-last-message /tmp/codex-out.md 2>/dev/null
# Then validate via: git diff --stat, pnpm test, or read summary only if needed
```

**Quick tasks (output comes back to you):**
```bash
codex exec --full-auto "Implement X following the pattern in Y"
```

**Interactive session for complex problems:**
```bash
codex "Let's design the data model for this feature"
```

## Token Economics

Your output tokens cost 5x your input tokens. Codex tokens are separate.

- Codex generates 1000 tokens of code → costs Codex, not you
- You read Codex's output → input tokens (cheap)
- You generate same code yourself → output tokens (expensive)

**Net savings: ~80% on code generation by delegating to Codex.**

To maximize savings:
1. Have Codex write to files directly
2. Validate by running tests or checking `git diff --stat`
3. Only read full output when debugging failures

## Reasoning Effort

Always use `gpt-5.2-codex`. Vary reasoning effort based on task complexity:

| Task | Effort | Flag |
|------|--------|------|
| Simple edits, boilerplate, straightforward | `medium` | `-c model_reasoning_effort=medium` |
| Most implementation work (default) | `high` | `-c model_reasoning_effort=high` |
| Complex debugging, tricky logic, architecture | `xhigh` | `-c model_reasoning_effort=xhigh` |

Examples:
```bash
# Standard (most tasks) - high effort
codex exec --full-auto "Implement auth middleware"

# Simple task - dial down to medium
codex exec --full-auto -c model_reasoning_effort=medium "Add getter/setter methods"

# Hard problem - dial up to xhigh
codex exec --full-auto -c model_reasoning_effort=xhigh "Debug this race condition"
```

Default to `high`. Drop to `medium` for trivial work. Escalate to `xhigh` for genuinely hard problems.

## When to Delegate

**Good candidates:**
- Implementation from a clear spec or pattern
- Writing tests for existing code
- Code review and analysis
- Drafting specs for you to refine
- Exploring multiple approaches in parallel
- Boilerplate and CRUD operations
- Refactoring with clear before/after

**Keep for yourself:**
- Novel architecture decisions
- Deep codebase reasoning you've already done
- Integration across unfamiliar systems
- Anything requiring context you already have loaded
- Quick one-liners where overhead isn't worth it

## Parallel Work

You can think while Codex works:
- Have Codex draft code while you design the architecture
- Have Codex write tests while you implement
- Get Codex's review while you plan the next step

## Trust but Verify

Always review Codex output before committing. Run tests. Check it fits codebase patterns. Codex is good but not infallible.

## Context Passing

Give Codex enough context to succeed:
- Reference specific files or patterns to follow
- Include relevant constraints
- Be specific about what you want

Bad: "Write a user service"
Good: "Implement a UserService class following the pattern in src/services/AuthService.ts. Include CRUD operations for users with proper error handling."
