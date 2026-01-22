---
description: Tidy workspace, create semantically meaningful commits, and push
---

# COMMIT

Analyze changes, tidy up, create semantically meaningful commits, and push.

## 1. Analyze

First, understand what's changed:

```bash
git status --short
git diff --stat HEAD
```

For each changed/untracked file, categorize:
- **Commit**: Quality changes that belong in the repo
- **Gitignore**: Generated/temporary files that should be ignored
- **Delete**: Cruft, experiments, or files no longer needed
- **Consolidate**: Files that should be merged or reorganized

## 2. Tidy

Execute cleanup decisions:

**Gitignore additions:**
- Add patterns to `.gitignore`
- Stage the `.gitignore` update

**Deletions:**
- Remove files that shouldn't exist
- Confirm before deleting anything non-obvious

**Consolidation:**
- Move files to better locations
- Merge related content
- Update any imports/references

**Goal:** Working directory should only contain intentional changes ready for commit.

## 3. Group Commits

Analyze remaining changes and group into semantically meaningful commits:

| Change Type | Commit Prefix |
|-------------|---------------|
| New feature | `feat:` |
| Bug fix | `fix:` |
| Documentation | `docs:` |
| Refactoring | `refactor:` |
| Performance | `perf:` |
| Tests | `test:` |
| Build/deps | `build:` |
| CI/CD | `ci:` |
| Maintenance | `chore:` |

**Principles:**
- One logical change per commit
- Each commit should be independently meaningful
- Related changes go together (e.g., feature + its tests)
- Unrelated changes get separate commits

## 4. Create Commits

For each group:

```bash
git add <relevant files>
git commit -m "<type>(<scope>): <description>

<body if needed>

Co-Authored-By: Claude <noreply@anthropic.com>"
```

**Commit message guidelines:**
- Subject: imperative mood, lowercase, no period, ≤50 chars ideal
- Body: explain *why*, not *what* (code shows what)
- Reference issues if applicable

## 5. Quality Check (if applicable)

If the repo has quality gates:

```bash
pnpm lint      # or npm run lint
pnpm typecheck # if TypeScript
pnpm test      # if tests exist
pnpm build     # verify it builds
```

Fix any issues before proceeding. Skip if no package.json or quality scripts.

## 6. Push

```bash
git fetch origin
git status  # Check if behind

# If behind:
git pull --rebase origin <branch>
# Resolve conflicts if any

git push origin HEAD
```

## Example Flow

```
Initial state:
 M src/api/users.ts        # Bug fix
 M src/api/users.test.ts   # Test for bug fix
 M README.md               # Updated docs
?? src/experiments/        # Experiments to delete
?? .env.local.backup       # Should gitignore
?? src/utils/helpers.ts    # New utility

Actions:
1. Delete src/experiments/
2. Add *.backup to .gitignore
3. Commit 1: fix(api): resolve user lookup race condition
   - src/api/users.ts
   - src/api/users.test.ts
4. Commit 2: feat(utils): add date formatting helpers
   - src/utils/helpers.ts
5. Commit 3: docs: update API usage examples
   - README.md
6. Push
```

## Flags

`$ARGUMENTS` can modify behavior:

- `--no-push` or `dry`: Create commits but don't push
- `--quick` or `fast`: Skip quality gates
- `--amend`: Amend last commit instead of creating new one (use carefully)

## Safety

- Never force push
- Never push to main/master without confirmation if branch protection might be off
- Always fetch before push to avoid conflicts
- If unsure about a deletion, ask first
