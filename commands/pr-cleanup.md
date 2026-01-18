---
description: Process open PRs, fix/close low-hanging fruit, especially dependabot with failing CI
---

# PR CLEANUP

> *"The best PR is a merged PR. The second best is a closed PR. The worst is a stale PR."*

Batch-process open PRs, prioritizing low-hanging fruit: green PRs needing merge, simple CI fixes, stale closures, and dependabot updates.

## Intent

Systematically reduce PR backlog:
1. Discover all open PRs (any author)
2. **Gather status in parallel** (CI, conflicts, age, author)
3. Categorize into GREEN/FIXABLE/STALE/COMPLEX
4. Present interactive selection
5. Process selected PRs (merge, fix, or close)
6. Report results

## Phase 1: Discovery

List all open PRs with metadata:
```bash
gh pr list --state open --limit 50 \
  --json number,title,headRefName,createdAt,author,labels,isDraft,reviewDecision
```

For each PR, gather status **in parallel**:
```bash
gh pr view $PR --json mergeable,mergeStateStatus,statusCheckRollup,headRefName,commits,reviews
```

**Key fields:**
- `author.login`: dependabot, renovate, human
- `mergeable`: MERGEABLE, CONFLICTING, UNKNOWN
- `statusCheckRollup[].conclusion`: SUCCESS, FAILURE, PENDING
- `reviewDecision`: APPROVED, CHANGES_REQUESTED, REVIEW_REQUIRED
- `isDraft`: skip unless explicitly included
- `createdAt`: age for staleness detection

## Phase 2: Categorize

### GREEN (Ready to Merge)
Criteria:
- CI passing (all checks SUCCESS)
- Mergeable (no conflicts)
- Approved OR no review required (dependabot, minor)
- Not a draft

Action: Merge immediately

### FIXABLE (Simple CI Issues)
Criteria:
- Mergeable OR lockfile-only conflicts
- CI failures in: lint, typecheck, lockfile, format, snapshots
- NOT test failures (unless snapshot-only)
- Author is dependabot/renovate OR patch/minor bump

Common fixable patterns:
- `pnpm-lock.yaml` conflict → regenerate
- Lint errors with auto-fix available
- Type errors from outdated types (often @types/* lag)
- Snapshot mismatches → update
- Format violations → auto-fix

Action: Attempt fix in worktree, merge if successful

### STALE (Should Close)
Criteria:
- PR older than 90 days with no activity
- Superseded by newer PR for same change
- Author no longer active on project
- Draft with no updates in 60+ days
- Dependabot PR with newer version available

Action: Close with explanatory comment

### COMPLEX (Skip for Now)
Criteria:
- Test failures (not snapshots)
- Major version bumps
- Source code conflicts
- Requires human review (changes requested)
- Large diff (>500 lines changed)

Action: Flag for manual attention, skip

## Phase 3: Triage Display

```
## PR Cleanup Triage

Found 18 open PRs:

### GREEN (Ready to Merge) - 4 PRs
[x] #234 @dependabot: Bump eslint 8.56→8.57 (patch, CI green)
[x] #245 @teammate: Fix typo in README (approved, CI green)
[x] #251 @renovate: Update @types/node 20.11.0→20.11.5 (patch)
[x] #253 @dependabot: Bump typescript 5.3.2→5.3.3 (patch)

### FIXABLE (CI Issues) - 5 PRs
[x] #236 @dependabot: Bump next 14.1.0→14.1.1 (lockfile conflict)
[x] #237 @dependabot: Bump @clerk/nextjs 4.29→4.29.5 (lint error)
[x] #240 @renovate: Update vitest 1.2.0→1.3.0 (snapshot mismatch)
[ ] #248 @teammate: Add logging util (2 type errors)
[ ] #250 @dependabot: Bump react 18.2→18.3 (minor, type errors)

### STALE (Close Candidates) - 3 PRs
[x] #198 @former-contributor: WIP feature (draft, 120 days, no activity)
[x] #210 @dependabot: Bump eslint 8.50→8.51 (superseded by #234)
[x] #215 @teammate: Experiment branch (180 days, abandoned)

### COMPLEX (Manual Review) - 6 PRs
[ ] #242 @dependabot: Bump next 14→15 (MAJOR)
[ ] #243 @teammate: Refactor auth (test failures, 800 lines)
[ ] #246 @teammate: New feature (changes requested)
...

---
Selection: [a]ll GREEN+FIXABLE, [g]reen only, [f]ixable only, [s]elect specific
```

## Phase 4: Processing

### For GREEN PRs
```bash
gh pr merge $PR --squash --delete-branch
```

### For FIXABLE PRs

**Step 1: Checkout in worktree**
```bash
git worktree add ../pr-fix-$PR_NUM $(gh pr view $PR --json headRefName -q .headRefName)
cd ../pr-fix-$PR_NUM
```

**Step 2: Apply fixes (ordered by likelihood)**

1. **Lockfile regeneration** (most common for dependabot):
```bash
rm pnpm-lock.yaml && pnpm install
```

2. **Lint auto-fix**:
```bash
pnpm lint --fix
```

3. **Format**:
```bash
pnpm format
```

4. **Snapshot update**:
```bash
pnpm test -- -u
```

5. **Simple type fixes**: Analyze errors, attempt minimal fix if <3 errors

**Step 3: Verify locally**
```bash
pnpm typecheck && pnpm lint && pnpm test
```

**Step 4: Push fix**
```bash
git add -A
git commit -m "chore: fix CI issues

Co-Authored-By: Claude <noreply@anthropic.com>"
git push
```

**Step 5: Wait for CI (5 min timeout)**
```bash
gh pr checks $PR --watch --timeout 300
```

**Step 6: Merge if green**
```bash
gh pr merge $PR --squash --delete-branch
```

**Step 7: Cleanup worktree**
```bash
cd ..
git worktree remove pr-fix-$PR_NUM
```

### For STALE PRs
```bash
gh pr close $PR --comment "Closing as stale. [Reason: $REASON]

This PR hasn't seen activity in $DAYS days. Feel free to reopen if still relevant."
```

For superseded dependabot PRs:
```bash
gh pr close $PR --comment "Closing as superseded by #$NEWER_PR which bumps to a more recent version."
```

## Phase 5: Report

```markdown
## PR Cleanup Summary

### Merged (7 PRs)
- #234 eslint 8.56→8.57 ✓
- #245 Fix typo in README ✓
- #236 next 14.1.0→14.1.1 (fixed: lockfile) ✓
- #237 @clerk/nextjs 4.29→4.29.5 (fixed: lint) ✓
...

### Closed (3 PRs)
- #198 WIP feature (stale draft, 120 days)
- #210 eslint bump (superseded)
- #215 Experiment (abandoned)

### Fixed Issues
- 3 PRs: lockfile regeneration
- 2 PRs: lint --fix
- 1 PR: snapshot update

### Skipped (6 PRs need manual attention)
- #242 next 14→15 (major version)
- #243 auth refactor (test failures)
- #246 new feature (changes requested)

### Recommendations
1. **#242**: Schedule Next.js 15 migration
2. **#243**: Review test failures, possible API change
3. **#246**: Address reviewer feedback
```

## Safety Constraints

**Never auto-process:**
- Major version bumps (X.0.0)
- PRs with test failures (except snapshots)
- PRs with source code conflicts
- PRs with "changes requested" review
- PRs from unknown external contributors (security)

**Always verify:**
- Local CI passes before merge attempt
- Remote CI passes before merge
- PR is not a security-sensitive change

**Protected packages (always COMPLEX for major):**
- Authentication: `@clerk/*`, `next-auth`, `@auth/*`
- Database: `convex`, `prisma`, `drizzle`
- Framework: `next`, `react`, `vue`
- Monitoring: `@sentry/*`

## Conflict Resolution

**Lockfile conflicts:**
```bash
git checkout --theirs pnpm-lock.yaml 2>/dev/null || true
rm -f pnpm-lock.yaml package-lock.json yarn.lock
pnpm install
```

**package.json version-only conflicts:**
```bash
# If dependabot's version is newer, take theirs
git checkout --theirs package.json
pnpm install
```

**Any other conflict → COMPLEX**

## Error Handling

**CI timeout:** Mark SKIPPED, continue to next
**Fix attempt fails:** Restore state, mark COMPLEX, continue
**Merge race condition:** Pull rebase, retry once, then COMPLEX
**Rate limiting:** Back off, reduce parallelism

## Quick Reference

```bash
# Just merge green PRs
/pr-cleanup --green-only

# Include fixing CI issues
/pr-cleanup --with-fixes

# Full cleanup including stale closures
/pr-cleanup --full

# Target specific author
/pr-cleanup --author dependabot

# Dry run (report only, no actions)
/pr-cleanup --dry-run
```

## Integration with Other Commands

- `/dependabot-merge` - Focused dependabot processing (subset of this)
- `/ci` - Diagnose specific CI failure
- `/git-worktree-create` - Isolated branch work
- `/git-worktree-cleanup` - Clean up after processing

## Philosophy

> **"PRs are like dishes—wash them promptly or they pile up."**

A clean PR queue:
- Reduces cognitive overhead
- Keeps dependencies fresh
- Encourages small, frequent merges
- Maintains team velocity

Don't let the backlog become a burden. Process regularly, close decisively.
