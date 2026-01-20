---
description: Interactively merge dependabot PRs with smart CI fixing and conflict resolution
---

Batch merge dependabot PRs with intelligent triage, CI fix attempts, and safe merging.

# DEPENDABOT MERGE

> *"A stale dependency is a ticking time bomb. Keep them fresh, verify them fast."*

Transform dependency maintenance from a weekly chore into a 5-minute workflow. Process all open dependabot PRs through discovery, triage, interactive selection, and safe merging.

## Intent

Process dependabot PRs systematically:
1. Discover all open dependabot PRs
2. **Gather status for all PRs IN PARALLEL** (CI, conflicts, mergeable)
3. Triage into GREEN/FIXABLE/COMPLEX/STALE categories
4. Present interactive selection with smart defaults
5. Fix & merge selected PRs using worktrees for isolation
6. Report results with recommendations

## Key Optimization

**Run status detection for all PRs concurrently** rather than sequentially. Each PR requires multiple API calls (mergeable, CI checks, conflicts). Parallel processing provides 50-70% speedup with 5+ PRs.

## Phase 1: Discovery

List all open dependabot PRs:
```bash
gh pr list --author "app/dependabot" --state open \
  --json number,title,headRefName,createdAt,labels
```

For each PR, gather status in parallel:
```bash
gh pr view $PR --json mergeable,mergeStateStatus,statusCheckRollup,headRefName
```

**Key fields:**
- `mergeable`: MERGEABLE, CONFLICTING, UNKNOWN
- `statusCheckRollup[].conclusion`: SUCCESS, FAILURE, PENDING
- `statusCheckRollup[].name`: identifies which check failed

## Phase 2: Triage

Categorize each PR:

**GREEN (Ready to Merge):**
- Mergeable with all CI green
- Action: Merge immediately

**FIXABLE (CI Issues Likely Fixable):**
- Mergeable or lockfile-only conflicts
- CI failures in: lint, typecheck, lockfile, format
- No test failures
- Action: Attempt auto-fix in worktree

**COMPLEX (Manual Review Required):**
- Test failures
- Major version bump (X.0.0)
- Source code conflicts
- Protected packages (major bumps)
- Action: Skip, flag for review

**STALE (Superseded):**
- Older PR exists for same package with newer version
- Action: Close with comment

**Version Detection:**
Parse PR title to determine bump type:
- `1.0.0 to 1.0.1` = patch (safe)
- `1.0.0 to 1.1.0` = minor (usually safe)
- `1.0.0 to 2.0.0` = major (always COMPLEX)

## Phase 3: Interactive Selection

```
## Dependabot PR Triage

Found 12 open dependabot PRs:

### GREEN (Ready to Merge) - 5 PRs
[x] #234 Bump eslint from 8.56.0 to 8.57.0 (patch)
[x] #235 Bump typescript from 5.3.2 to 5.3.3 (patch)
[x] #238 Bump @types/node from 20.11.0 to 20.11.5 (patch)

### FIXABLE (CI Issues) - 3 PRs
[x] #236 Bump next from 14.1.0 to 14.1.1 (patch)
    Issue: Lockfile conflict
[x] #237 Bump @clerk/nextjs from 4.29.0 to 4.29.5 (patch)
    Issue: Lint error (auto-fixable)
[ ] #239 Bump react from 18.2.0 to 18.3.0 (minor)
    Issue: Type errors (2 files)

### COMPLEX (Manual Review) - 3 PRs
[ ] #242 Bump next from 14.1.0 to 15.0.0 (MAJOR)
    Reason: Major version, breaking changes likely
[ ] #243 Bump convex from 1.8.0 to 1.9.0 (minor)
    Reason: Test failures (3 tests)

### STALE (Superseded) - 1 PR
[x] #230 Bump eslint from 8.55.0 to 8.56.0
    Action: Will close (superseded by #234)

---
Selection: [a]ll GREEN+FIXABLE, [g]reen only, [s]elect specific, [n]one
```

## Phase 4: Fix & Merge Loop

For each selected PR:

**Step 1: Create worktree**
```bash
gh pr checkout $PR_NUM
# Or for isolation:
git worktree add ../project-dependabot-$PR_NUM $BRANCH
cd ../project-dependabot-$PR_NUM
```

**Step 2: Attempt fixes (ordered)**

1. **Lockfile regeneration** (most common):
```bash
rm pnpm-lock.yaml && pnpm install
```

2. **Lint auto-fix**:
```bash
pnpm lint --fix
```

3. **Format auto-fix**:
```bash
pnpm format
```

4. **Simple type errors**: Analyze error, attempt minimal fix

5. **Snapshot updates**:
```bash
pnpm test -- -u
```

Max 3 fix attempts per PR. If still failing → mark COMPLEX, skip.

**Step 3: Verify local CI (parallel)**
```bash
pnpm typecheck & pnpm lint & pnpm test
wait
```

**Step 4: Commit and push**
```bash
git add -A
git commit -m "chore: fix CI for dependency update"
git push
```

**Step 5: Wait for remote CI (5min timeout)**
```bash
gh pr checks $PR_NUM --watch --timeout 300
```

**Step 6: Merge**
```bash
gh pr merge $PR_NUM --squash --delete-branch
```

**Step 7: Cleanup**
```bash
cd ../project
git worktree remove ../project-dependabot-$PR_NUM
```

## Phase 5: Report

```markdown
## Dependabot Merge Summary

### Merged Successfully (6 PRs)
- #234 eslint 8.56.0 → 8.57.0
- #235 typescript 5.3.2 → 5.3.3
- #236 next 14.1.0 → 14.1.1 (fixed: lockfile)

### Fixed Issues
- 2 PRs required lockfile regeneration
- 1 PR required lint --fix

### Closed (Stale)
- #230 eslint (superseded by #234)

### Skipped (Manual Review Needed)
- #242 next 14 → 15 (major version)
- #243 convex (test failures)

### Recommended Actions
1. Schedule #242: Next.js 15 migration needs dedicated PR
2. Investigate #243: Test failures suggest API changes
```

## Conflict Resolution

**Lockfile conflicts (trivial):**
Always regenerate - dependabot's lockfile is based on old main.
```bash
git checkout --theirs pnpm-lock.yaml 2>/dev/null || true
rm pnpm-lock.yaml && pnpm install
```

**package.json version conflicts:**
If only version field and dependabot's is newer:
```bash
git checkout --theirs package.json
pnpm install
```
If complex → flag as COMPLEX.

**Source code conflicts:**
Never auto-resolve. Flag as COMPLEX immediately.

## Safety Constraints

**Never auto-merge:**
- Major version bumps (X.0.0)
- PRs with test failures
- Source code conflicts
- PRs older than 60 days

**Always verify:**
- Local CI passes before merge
- Remote CI passes
- Lockfile is valid

**Protected packages (always COMPLEX for major):**
`@clerk/*, convex, @sentry/*, next`

## Error Handling

**CI timeout:**
Mark as SKIPPED, report "CI didn't complete in 5 minutes", continue to next PR.

**Fix attempt failure:**
Restore worktree state, mark as COMPLEX, continue to next PR.

**Merge conflict during push:**
```bash
git pull --rebase
# Re-run local CI, if passes try again
# If fails, mark as COMPLEX
```

## Workflow Example

```bash
# Weekly Monday ritual
/dependabot-merge

# Output: triage results with selection UI
# Select [a] for all GREEN + FIXABLE

# Processing...
# ✅ Merged 6 PRs
# ✅ Fixed 2 CI issues
# ✅ Closed 1 stale PR
# ⚠️ Skipped 3 PRs (manual review needed)
```

## Common Issues

**"Branch not found" error:**
PR branch may have been deleted. Skip and close PR.

**CI flaky/stuck:**
Use `--timeout` flag, skip after timeout, retry later.

**Too many type errors:**
If >5 type errors, likely API change. Mark COMPLEX.

**Protected branch rules:**
Some repos require reviews. Use `gh pr merge --admin` if you have admin access.

## Related Commands

- `/git-worktree-create` - Create isolated worktree
- `/git-worktree-cleanup` - Clean up after processing
- `/ci` - Diagnose CI failures
- `/quality-check` - Verify before merge
