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

## Bounded Shell Output (MANDATORY)

- Size before detail: counts/metadata first
- Never print unbounded logs/comments
- Add explicit bounds: `--limit`, `head -n`, `tail -n`, `per_page`
- If no useful signal in 20s: abort, narrow, rerun
- Use `~/.claude/scripts/safe-read.sh` for large local files

## Workflow

### 1. Assess

```bash
gh pr view $PR --json number,title,headRefName,baseRefName,mergeable,reviewDecision,statusCheckRollup
gh pr checks $PR --json name,state,startedAt,completedAt,link
gh pr view $PR --json body --jq '.body | split("\n")[:80] | join("\n")'
```

Read PR description and linked issue. Understand **what this PR is trying to do** — semantic context drives conflict resolution and review decisions.

Fetch latest base:

```bash
BASE="$(gh pr view $PR --json baseRefName --jq .baseRefName)"
git fetch origin "$BASE"
```

Determine blockers: conflicts? CI failures? pending reviews? Build a checklist.

### 2. Resolve Conflicts

**Skip if**: `mergeable != CONFLICTING`

Rebase onto base branch:

```bash
git rebase "origin/$BASE"
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

**Skip condition**: zero open review threads AND zero unreplied review comments. Use the GraphQL query below — never rely on `reviewDecision` alone or prior "PR Unblocked" summary comments.

```bash
OWNER="$(gh repo view --json owner --jq .owner.login)"
REPO="$(gh repo view --json name --jq .name)"

# Count unresolved review threads (inline comments)
UNRESOLVED_THREADS="$(gh api graphql -f query='
  query($owner:String!, $repo:String!, $number:Int!){
    repository(owner:$owner,name:$repo){
      pullRequest(number:$number){
        reviewThreads(first:100){nodes{isResolved}}
      }
    }
  }' -F owner="$OWNER" -F repo="$REPO" -F number="$PR" \
  --jq '[.data.repository.pullRequest.reviewThreads.nodes[] | select(.isResolved==false)] | length')"
```

#### Independent verification (MANDATORY)

**Never trust prior session comments, "PR Unblocked" summaries, or claims that feedback was addressed.** For EVERY open review comment:

1. **Read the FULL comment body** — no truncation. Use the GitHub API without `.body[:N]` limits.
2. **Read the current file at the referenced line** to verify the fix is actually present.
3. **Reply directly on the comment thread** with the specific commit SHA and line confirming the fix. An open thread without a reply = unaddressed, regardless of what a summary comment claims.

```bash
# Fetch ALL review comments with full bodies — never truncate
gh api "repos/$OWNER/$REPO/pulls/$PR/comments?per_page=100" --paginate \
  --jq '.[] | {id, user: .user.login, path, line, body, in_reply_to_id}'
```

For each comment without a reply from this PR's author:
- If **already fixed in code**: reply with commit SHA + current line reference confirming the fix
- If **needs fixing**: fix it, then reply with commit SHA
- If **deferred**: reply with follow-up issue number
- If **declined**: reply with public reasoning

Bot feedback (CodeRabbit, Cerberus, Gemini, Codex) gets the same treatment as human feedback.

#### Execution

1. **Invoke `/respond`** — Categorize all feedback (critical / in-scope / follow-up / declined). Post transparent assessment to PR. Reviewer feedback CAN be declined with public reasoning.

2. **Invoke `/address-review`** — TDD fixes for critical and in-scope items. GitHub issues for follow-up items.

3. **Reply to every open thread** — use `gh api repos/$OWNER/$REPO/pulls/$PR/comments/$ID/replies -f body='...'` so the thread shows addressed.

4. **Resolve every thread via GraphQL** — Replies alone do NOT resolve threads. Non-outdated comments stay visible as open issues to reviewers even after fixing the code and replying. You MUST resolve them:

```bash
# Get unresolved thread IDs
gh api graphql -F owner="$OWNER" -F repo="$REPO" -F number=$PR -f query='
  query($owner: String!, $repo: String!, $number: Int!) {
    repository(owner: $owner, name: $repo) {
      pullRequest(number: $number) {
        reviewThreads(first: 100) {
          nodes { id isResolved isOutdated }
        }
      }
    }
  }' --jq '.data.repository.pullRequest.reviewThreads.nodes[] | select(.isResolved == false) | .id'

# Resolve each thread
gh api graphql -f query='mutation { resolveReviewThread(input: {threadId: "THREAD_ID"}) { thread { isResolved } } }'
```

Additive commits do NOT make comments outdated. Only changes to the diff hunk a comment is attached to trigger outdating. Resolve explicitly.

### 5. Verify and Push

```bash
git push --force-with-lease
```

Watch checks. If a phase-4 fix broke CI, invoke `/fix-ci` again (count toward 2-retry max).

If 2 full retries exhausted: stop, summarize state, ask user.

### 6. Update PR Description with Before / After

Edit the PR body to include a Before / After section documenting the fix:

```bash
# Get current body, append Before/After section
gh pr edit $PR --body "$(current body + before/after section)"
```

**Text (MANDATORY)**: Describe the blocked state (before) and the unblocked state (after).
Example: "Before: CI failing on type error in auth module. After: Types corrected, CI green."

**Screenshots (when applicable)**: Capture before/after for any visible change — CI status pages, error output, UI changes from review fixes. Use `![before](url)` / `![after](url)`.

Skip screenshots only when all fixes are purely internal (conflict resolution with no behavior change, CI config fixes with no visible output difference).

### 7. Signal

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
- **Trusting prior "PR Unblocked" or summary comments** — always verify each comment against current code independently. A previous session claiming "fixed" means nothing until you read the file yourself.
- **Leaving review threads without direct replies** — an open thread with no reply = unaddressed, even if the code is fixed. Reviewers can't see that you checked.
- **Truncating comment bodies** — never use `.body[:N]` when fetching review comments. The actionable detail is often at the end of long comments.
- **Replying without resolving** — a reply on a thread does NOT resolve it. Non-outdated threads with replies still show as open conversations. Use `resolveReviewThread` GraphQL mutation after replying.
- **NEVER lowering quality gates to pass CI** — coverage thresholds, lint rules, type strictness, security gates. If a gate fails, write tests/code to meet it. Moving the goalpost is not a fix. This is an absolute, non-negotiable rule.

## Output

Summary: blockers found, phases executed, conflicts resolved, CI fixes applied, reviews addressed/deferred/declined, final check status.
