---
name: pr-polish
description: |
  Elevate a working PR: hindsight review, refactor, test audit, docs, quality gates.
  Composes: hindsight-reviewer agent, /refactor, /update-docs, /check-quality, /distill.
  Use when: PR works but could be better. "How would we do this knowing what we know now?"
argument-hint: "[PR-number]"
effort: high
---

# /pr-polish

Holistic quality elevation for a PR that already works.

## Role

Staff engineer doing a retrospective pass. Not finding bugs — asking "would we build it the same way starting over?"

## Objective

Elevate PR `$ARGUMENTS` (or current branch's PR) from "works" to "exemplary": clean architecture, solid tests, current docs.

## Precondition Gate

Before starting, verify:

```bash
gh pr view $PR --json mergeable,statusCheckRollup,reviewDecision
```

Requirements:
- No merge conflicts
- CI green
- No unaddressed critical review feedback

**If any fail**: Tell user to run `/pr-fix` first. Do not proceed.

## Workflow

### 1. Context

Read everything about this PR:

```bash
gh pr view $PR --json body,commits,files
gh pr diff $PR
```

Read linked issue(s). Read commit history. Understand the full arc of what was built and why.

### 2. Hindsight Review

Launch `hindsight-reviewer` agent via Task tool.

Key question: **"Knowing what we know now — the final shape of the code, the edge cases discovered, the patterns that emerged — would you build it the same way?"**

Feed it: full diff against main, PR description, linked issue.

Expect back: architectural observations, naming concerns, abstraction boundaries, missed simplifications.

### 3. Refactor

Invoke `/refactor` for findings that are addressable now:

- Naming improvements
- Shallow module consolidation
- Unnecessary abstraction removal
- Code path simplification

For architectural findings that require broader changes: create GitHub issues.

```bash
gh issue create --title "[Arch] Finding from PR #$PR hindsight review" --body "..."
```

### 4. Test Audit

Review test coverage for the PR's changed files. Look for:

- Missing edge cases
- Error path coverage
- Behavior tests (not implementation tests — per `/testing-philosophy`)
- Boundary conditions
- Integration gaps

Write missing tests. Each test should justify its existence — no coverage-padding.

### 5. Documentation

Invoke `/update-docs` for anything the PR affects:

- ADRs for architectural decisions made during implementation
- README updates for new features or changed behavior
- Architecture diagrams if module boundaries changed
- API docs if endpoints changed

### 6. Quality Gates

Invoke `/check-quality` and run project verification:

```bash
pnpm typecheck && pnpm lint && pnpm test
```

All gates must pass. Fix anything that doesn't.

### 7. Update PR Description with Before / After

Edit the PR body to include (or update) a Before / After section documenting the polish pass:

```bash
gh pr edit $PR --body "$(current body + before/after section)"
```

**Text (MANDATORY)**: Describe the state before polish (e.g., "working but with shallow modules and missing edge-case tests") and after (e.g., "consolidated modules, 12 new edge-case tests, updated architecture docs").

**Screenshots (when applicable)**: Capture before/after for any visible change — refactored UI output, improved error messages, updated docs pages. Use `![before](url)` / `![after](url)`.

Skip screenshots only when all polish was purely internal (refactoring with no visible output change).

### 8. Refresh Glance Summaries (Conditional)

If this PR added, removed, or significantly restructured directories:

```bash
glance   # run from repo root — skips up-to-date directories automatically
```

Do NOT pass `-force`. Glance handles intelligent regeneration based on existing `.glance.md` files. Only affects directories that changed.

Commit any updated `.glance.md` files with the PR branch.

### 9. Codify (Optional)

If patterns or learnings emerged during this polish pass, invoke `/distill` to capture them as permanent knowledge (hooks, agents, skills, CLAUDE.md entries).

Skip if nothing novel surfaced.

## Agent Teams Mode

For large PRs (>500 line diff), parallelize phases 3-5:

| Teammate | Task |
|----------|------|
| **Refactorer** | `/refactor` on hindsight findings |
| **Test writer** | Test audit + write missing tests |
| **Doc updater** | `/update-docs` |

Lead sequences: hindsight first (all teammates need its output), then parallel work, then quality gates.

## Anti-Patterns

- Polishing a PR that doesn't work yet (use `/pr-fix` first)
- Architectural refactors in a polish pass (create issues instead)
- Adding tests for coverage percentage instead of confidence
- Documenting obvious mechanics instead of non-obvious decisions
- Skipping hindsight and jumping straight to refactoring

## Output

Summary: hindsight findings, refactors applied, issues created, tests added, docs updated, quality gate results, learnings codified.
