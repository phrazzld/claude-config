---
name: pr-fix
description: |
  Unblock a PR: resolve conflicts, fix CI, address reviews.
  Composes: git-mastery conflict resolution, /fix-ci, /respond, /address-review.
  Use when: PR is blocked by conflicts, red CI, or unaddressed review feedback.
argument-hint: "[PR-number]"
effort: high
---

# /pr-fix

One command takes a blocked PR to green.

## Role

Senior engineer unblocking a PR. Methodical, not reactive. Each phase resolves a class of blocker in dependency order.

## Objective

Take PR `$ARGUMENTS` (or current branch's PR) from blocked to mergeable: no conflicts, CI green, reviews addressed.

## Dependency Order

Conflicts -> CI -> Reviews. Can't run CI on conflicted code. Can't address reviews on broken builds.

## Workflow

### 1. Assess

```bash
gh pr view $PR --json number,title,body,headRefName,baseRefName,mergeable,reviewDecision,statusCheckRollup
gh pr checks $PR
```

Read PR description and linked issue. Understand **what this PR is trying to do** — semantic context drives conflict resolution and review decisions.

Fetch latest base:

```bash
git fetch origin main
```

Determine blockers: conflicts? CI failures? pending reviews? Build a checklist.

### 2. Resolve Conflicts

**Skip if**: `mergeable != CONFLICTING`

Rebase onto base branch:

```bash
git rebase origin/main
```

When conflicts arise, resolve **semantically based on PR purpose**, not mechanically:

- Read both sides. Understand intent.
- Preserve the PR's behavioral changes. Integrate upstream structural changes.
- Reference `git-mastery/references/conflict-resolution.md` for strategies.
- Never blindly accept ours/theirs.

After resolution, verify locally:

```bash
git rebase --continue
# Run project's test/typecheck commands
```

### 3. Fix CI

**Skip if**: all checks passing.

Push current state and invoke `/fix-ci`:

```bash
git push --force-with-lease
```

Then run the `/fix-ci` skill. Wait for checks to go green.

If `/fix-ci` introduces changes that create new conflicts: return to Phase 2 (max 2 full-pipeline retries).

### 4. Address Reviews

**Skip if**: no pending review comments.

Two-step:

1. **Invoke `/respond`** — Categorize all feedback (critical / in-scope / follow-up / declined). Post transparent assessment to PR. Reviewer feedback CAN be declined with public reasoning.

2. **Invoke `/address-review`** — TDD fixes for critical and in-scope items. GitHub issues for follow-up items.

### 5. Verify and Push

```bash
git push --force-with-lease
```

Watch checks. If a phase-4 fix broke CI, invoke `/fix-ci` again (count toward 2-retry max).

If 2 full retries exhausted: stop, summarize state, ask user.

### 6. Signal

Post summary comment on PR:

```bash
gh pr comment $PR --body "$(cat <<'EOF'
## PR Unblocked

**Conflicts**: [resolved N files / none]
**CI**: [green / was: failure type]
**Reviews**: [N fixed, N deferred (#issue), N declined (see above)]

Ready for re-review.
EOF
)"
```

## Retry Policy

Max 2 full-pipeline retries when fixing one phase breaks another. After 2: stop and escalate to user with clear status.

## Anti-Patterns

- Mechanical ours/theirs conflict resolution
- Pushing without local verification
- Silently ignoring review feedback
- Retrying CI without understanding failures
- Fixing review comments that should be declined

## Output

Summary: blockers found, phases executed, conflicts resolved, CI fixes applied, reviews addressed/deferred/declined, final check status.
