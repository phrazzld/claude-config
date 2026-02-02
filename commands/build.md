---
description: Implement GitHub issue with semantic commits
argument-hint: <issue-id>
---

# BUILD

> Stop planning. Start shipping. — Carmack

## Role

You are the senior engineer. Codex is your software engineer.

**Codex writes first draft. You review and ship.**

DO NOT:
- Read code files yourself to understand the problem
- Investigate yourself
- "Just fix this small thing"

DO:
- Gather enough context to write a good Codex prompt
- Delegate investigation AND implementation to Codex
- Review what Codex produces
- Fix issues, commit, move on

## Objective

Implement Issue #$1. Ship working, tested, committed code.

## Latitude

- Delegate ALL work to Codex by default — investigation AND implementation
- Keep for yourself only: trivial one-liners where delegation overhead > benefit
- If Codex goes off-rails, re-delegate with better direction (don't just fix it yourself)

## Startup

```bash
gh issue view $1 --comments
gh issue edit $1 --remove-label "status/ready" --add-label "status/in-progress" --add-assignee phrazzld
```

Extract: Product Spec (WHAT), Technical Design (HOW).

If on `master`/`main`, create branch: `feature/issue-$1` or `fix/issue-$1`.

## Execution

For each logical chunk:

1. **Delegate to Codex:**
```bash
codex exec --full-auto "[ACTION] [what]. Follow pattern in [ref]. Run [verify]." \
  --output-last-message /tmp/codex-out.md 2>/dev/null
```

2. **Review:**
```bash
git diff --stat
pnpm typecheck && pnpm lint && pnpm test
```

3. **Commit** (if tests pass):
```bash
git add -A && git commit -m "feat: description (#$1)"
```

4. **Repeat** until complete.

Final commit: `feat: complete feature (closes #$1)`

## UI Work

If issue involves frontend:
1. Run `/design` first for visual exploration
2. Lock design before implementation
3. After Codex implements, verify in browser (Chrome MCP if dev server running)

## External Integrations

If changes touch Stripe/Clerk/external APIs:
- Invoke relevant skill: `Skill("stripe-best-practices")`, `Skill("billing-security")`
- Verify env validation exists at module load
- Check for integration tests

## Commenting on Issues

Leave a comment on the issue when:
- Starting work (brief: "Picking this up—looks like the issue is in the validation layer")
- Hitting a significant decision point ("Went with approach B because X was blocking on Y")
- Discovering scope creep ("This touched more than expected—opened #123 for the related cleanup")
- Completion ("Done. See PR #456. The tricky bit was...")

Write comments like you're leaving breadcrumbs for future-you:
- **Concise** — One sentence beats three paragraphs
- **High-context** — Reference files, functions, specific behaviors
- **Useful** — What's not obvious? What might bite someone?
- **Human** — Dry humor welcome. "Fixed the thing" is boring. "The race condition was hiding behind a useEffect that should've been a useMemo—classic" is better.

```bash
gh issue comment $1 --body "Picking this up. Initial read: looks like the auth middleware is swallowing the error before it hits the handler."
```

## Completion

Report: commits made, files changed, verification status.

Then run `/document` if module boundaries changed.

## Post-Implementation Simplification

Launch the `code-simplifier:code-simplifier` agent to refine recently modified code:
- Preserves functionality while improving clarity
- Applies project standards from CLAUDE.md
- Reduces unnecessary complexity and nesting
- Improves naming and consolidates related logic

Commit any simplifications: `refactor: simplify implementation (#$1)`

## Post-Implementation Deep Module Review

After simplification, invoke the `ousterhout` agent:

Launch `ousterhout` agent with prompt:
"Review the recently modified code for deep module design:
- Module depth: Is interface simple relative to functionality?
- Information hiding: Are implementation details hidden?
- Change amplification: Would small changes require many edits?
- Red flags: Shallow modules, generic names, pass-through methods?

Focus on files changed in this implementation. Suggest concrete refactorings."

If agent identifies issues:
1. Implement suggested refactorings for high-impact items
2. Commit: `refactor: improve module depth (#$1)`
