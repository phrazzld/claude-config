---
name: codex-coworker
description: "Invoke Codex as a coworker for implementation, brainstorming, specs, and reviews. Use when you want parallel thinking, cheap execution, or a second opinion. Codex tokens are cheaper than yours — delegate aggressively. Keywords: codex, delegate, implement, draft, review, brainstorm, write tests, code review, moonbridge."
effort: high
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

**Preferred: Moonbridge MCP (unified interface)**
```
mcp__moonbridge__spawn_agent({
  "prompt": "Implement X following the pattern in Y. Run pnpm typecheck after.",
  "adapter": "codex",
  "reasoning_effort": "high"
})
```

**Parallel tasks (multiple agents at once):**
```
mcp__moonbridge__spawn_agents_parallel({
  "agents": [
    {"prompt": "Implement feature A", "adapter": "codex", "reasoning_effort": "high"},
    {"prompt": "Write tests for A", "adapter": "codex", "reasoning_effort": "medium"},
    {"prompt": "Review for bugs", "adapter": "codex", "reasoning_effort": "high"}
  ]
})
```

**Fallback: CLI (when MCP unavailable)**
```bash
codex exec --full-auto "Implement X" --output-last-message /tmp/codex-out.md 2>/dev/null
# Then validate via: git diff --stat, pnpm test, or read summary only if needed
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

Vary reasoning effort based on task complexity:

| Task | Effort | When |
|------|--------|------|
| Simple edits, boilerplate | `medium` | Getters, CRUD, obvious changes |
| Most implementation (default) | `high` | Features, refactors, tests |
| Complex debugging, architecture | `xhigh` | Race conditions, security, hard bugs |

**Via Moonbridge MCP:**
```
mcp__moonbridge__spawn_agent({
  "prompt": "Debug this race condition",
  "adapter": "codex",
  "reasoning_effort": "xhigh"
})
```

**Via CLI (fallback):**
```bash
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

## Pre-Delegation Checklist

Before delegating, ask yourself:

1. **Does this file have existing tests?**
   → Add to prompt: "Don't break existing tests in [test file]"

2. **Should Codex ADD or REPLACE?**
   → Be explicit: "ADD to this file" vs "REPLACE this file"
   → Default to ADD unless rewrite is intentional

3. **What quality gates should Codex run?**
   → Include: "Run pnpm typecheck && pnpm lint after changes"

4. **What patterns should Codex follow?**
   → Include: "Follow the pattern in [reference file]"

## Prompt Templates

### Adding to existing file (safest):
```
ADD a new [function/component] to [file].
Follow the pattern used in [reference].
Don't modify existing functions.
Run pnpm typecheck after.
```

### Replacing/rewriting (use cautiously):
```
REPLACE [file] with [new implementation].
Note: This file has tests in [test file] - ensure they still pass.
Run pnpm typecheck && pnpm lint after.
```

### New file from scratch:
```
Create [file] implementing [spec].
Follow patterns from [reference].
Run pnpm typecheck after.
```

### With quality gates (recommended):
```bash
codex exec "ADD [function] to [file]. Follow pattern in [ref]. \
  Don't break tests in [test file]. Run pnpm typecheck after." \
  --output-last-message /tmp/codex-out.md 2>/dev/null
```

## Post-Delegation Validation

After Codex completes:

1. **Check what changed:**
   ```bash
   git diff --stat
   ```

2. **Run quality gates:**
   ```bash
   pnpm typecheck && pnpm lint
   ```

3. **Run tests:**
   ```bash
   pnpm test
   ```

4. **If tests broke:**
   - Check if Codex deleted/renamed functions tests depend on
   - Look for wholesale file replacement when ADD was intended
   - Review imports that may have been removed

5. **Review integration points:**
   - You handle complex integration across files
   - Check redirects, configs, and cross-file dependencies

## Why Moonbridge MCP

**Use Moonbridge for all Codex delegation:**

| Method | When |
|--------|------|
| `mcp__moonbridge__spawn_agent` | Primary method — unified interface |
| `codex exec` CLI | Fallback when MCP unavailable |

**Key benefits:**
- **Mixed parallel:** Run Codex + Kimi in same `spawn_agents_parallel` call
- **Consistent params:** Same interface for both adapters
- **Better control:** `reasoning_effort` for Codex, `thinking` for Kimi

See `/delegate` for full orchestration patterns.
