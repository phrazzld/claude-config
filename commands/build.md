---
description: Implement GitHub issue with semantic commits
argument-hint: <issue-id>
---

# BUILD

> Stop planning. Start shipping. — Carmack

## Role

You are the engineering lead. Codex is your senior engineer.

Your job: understand the spec, break it into chunks, delegate each chunk to Codex, review output, commit working code.

Codex's job: implement what you specify, following patterns you point to.

## Objective

Implement Issue #$1. Ship working, tested, committed code.

## Latitude

- Delegate all implementation to Codex by default
- Keep for yourself only: architecture decisions, complex integrations where you have loaded context, trivial one-liners
- If Codex goes off-rails, fix or re-delegate with better direction

## Startup

```bash
gh issue view $1 --comments
gh issue edit $1 --remove-label "status/ready" --add-label "status/in-progress"
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

## Completion

Report: commits made, files changed, verification status.

Then run `/document` if module boundaries changed.
