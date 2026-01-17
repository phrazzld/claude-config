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

## UI Work Detection

If issue involves frontend (tsx/jsx/vue/svelte files, CSS, Tailwind, components):
- Invoke `Skill("aesthetic-system")` for design guidance
- Apply `aesthetic-system/references/implementation-constraints.md` during implementation
- Use `references/banned-patterns.md` to avoid AI slop

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

## External Integration Checks

If changes touch payment/auth/external API code:

1. **Invoke relevant skill explicitly**:
   - Stripe code (payment, checkout, subscription, webhook) → `Skill("stripe-best-practices")`
   - Auth code (clerk, auth, session) → `Skill("billing-security")`
   - Any external API → `Skill("external-integration-patterns")`

2. **Verify config patterns**:
   - Runtime env validation at module load (fail fast, not silent)
   - No secrets in code: `grep -r "sk_\|whsec_\|pk_live" --include="*.ts" --include="*.tsx"`
   - Error handling returns useful diagnostics (userId, operation, error)

3. **Check for integration tests**:
   - If touching webhook handler, verify test exists
   - If adding new external call, verify mock/stub exists
   - Warn if critical path has no integration test

4. **Spawn config-auditor** for external integrations:
   - Env vars documented and validated at runtime
   - Health check endpoint exists
   - Error handling logs with context

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

## Post-Implementation Documentation

After successful implementation, run `/document` to:
- Generate state diagrams for any stateful components added
- Update READMEs for new directories
- Add architecture diagrams if module boundaries changed

## Post-Implementation Simplification

Launch the `code-simplifier:code-simplifier` agent to refine recently modified code:
- Preserves functionality while improving clarity
- Applies project standards from CLAUDE.md
- Reduces unnecessary complexity and nesting
- Improves naming and consolidates related logic

Commit any simplifications: `refactor: simplify implementation (#$1)`

## Post-Implementation Deep Module Review

After simplification, invoke the `ousterhout` agent to review for architectural quality:

Launch `ousterhout` agent with prompt:
```
Review the recently modified code for deep module design:
- Module depth: Is interface simple relative to functionality?
- Information hiding: Are implementation details hidden?
- Change amplification: Would small changes require many edits?
- Red flags: Shallow modules, generic names, pass-through methods?

Focus on files changed in this implementation. Suggest concrete refactorings.
```

If agent identifies issues:
1. Implement suggested refactorings for high-impact items
2. Commit: `refactor: improve module depth (#$1)`

## Post-Implementation Codification

After documentation, autonomously preserve learnings.

### Doc-Check First

Run /doc-check to understand existing documentation structure. Codification should respect and extend what exists, not create parallel docs.

### Scan and Codify

1. **Scan the diff** for patterns worth keeping:
   - Code used 3+ times → extract to shared utility
   - Bug fix with non-obvious cause → add regression test
   - Multi-step workflow discovered → consider as skill
   - Quality issue caught → add to relevant agent

2. **Codification targets** (informed by doc-check):
   - CLAUDE.md for conventions (extend existing, don't duplicate)
   - Existing docs/adr/ for architectural decisions
   - Existing agent files for enforcement rules
   - Module READMEs for module-specific patterns

3. **Confidence-based action**:
   - HIGH confidence (clear pattern, obvious value) → codify directly
   - MEDIUM confidence (useful but uncertain) → add to CLAUDE.md staging section
   - LOW confidence (one-off, context-specific) → skip

4. **Codify in same PR** when possible. Keep implementation + codification atomic.

No prompting required. Use judgment about what's worth preserving.
