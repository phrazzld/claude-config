Create pull request with auto-generated title and description from commit history.

# PR

Open a pull request for current branch with punchy title and comprehensive description generated from commit history.

## 1. Analyze Branch Changes
- **Get commit history**: `!git log master..HEAD --oneline` to see all commits on current branch
- **Get detailed changes**: `!git log master..HEAD --pretty=format:"%h %s%n%b" --no-merges` for full commit details
- **Get file changes**: `!git diff --name-only master..HEAD` to understand scope of changes
- **Get stats**: `!git diff --stat master..HEAD` for change magnitude

## 1b. Pre-PR Quality Checks

**Size Check**:
```bash
# Show lines changed
git diff --stat master

# Count total lines
LINES=$(git diff --shortstat master | awk '{print $4+$6}')
echo "Total lines changed: $LINES"
```

**Size guidance**:
- ≤200 lines: ✅ Perfect size
- 201-400 lines: ✅ Good size
- 401-500 lines: ⚠️ Large - justify in PR description
- >500 lines: 🛑 Too large - strongly consider splitting

**If >400 lines**, ask:
```
This PR is large ($LINES lines). Options:
1. Proceed anyway (provide justification in PR)
2. Split into smaller PRs (recommended)
3. Use git-spr to create stacked PRs

Choice (1/2/3):
```

**Coverage Check** (if tests present):
```bash
# Show coverage for changed files
pnpm test -- --coverage --changed
```

If patch coverage <80%, warn:
```
⚠️ Coverage for new code is below 80%
Untested files: [list files with <80% coverage]

Add tests before creating PR? (y/n)
```

**Documentation Staleness Check**:
Before creating PR, audit documentation freshness for changed directories:

```bash
# Get directories with changes
git diff --name-only master | xargs -I {} dirname {} | sort -u
```

For each directory with changes:
1. Check if README.md/DOCS.md exists
2. Compare doc mtime vs changed file mtimes
3. Flag stale docs (doc older than changed files)

If stale docs found, report:
```
Documentation may need updates:

Files you changed in directories with stale docs:
  src/auth/login.ts, src/auth/logout.ts
    -> src/auth/README.md last updated 30 days ago

  src/api/routes.ts
    -> src/api/README.md last updated 14 days ago

Consider updating these READMEs before creating PR.
```

**Documentation Check** (manual):
Ask: "Did you update relevant documentation? Check all that apply:"
- [ ] README (if installation/usage changed)
- [ ] API docs (if public interfaces changed)
- [ ] ADR (if architectural decision made)
- [ ] Code comments (for complex logic)
- [ ] N/A - no docs needed

Add checklist to PR description.

## 2. Generate PR Title
- **Think hard about the work**: Analyze all commits to identify the main theme/goal
- **Create punchy title**: 50 characters or less, action-oriented, specific
- **Examples of good titles**:
  - "Add user authentication with JWT tokens"
  - "Refactor payment processing for better error handling"
  - "Implement dark mode toggle across all components"
  - "Fix memory leak in data processing pipeline"
- **Avoid generic titles**: "Updates", "Changes", "Misc fixes"

## 3. Generate Comprehensive Description
- **Synthesize commit messages** into coherent narrative
- **Structure the description**:
  ```markdown
  ## Summary
  [2-3 sentences explaining what this PR accomplishes and why]

  ## Changes Made
  - [High-level change 1 with impact]
  - [High-level change 2 with impact]
  - [High-level change 3 with impact]

  ## Technical Details
  [Brief explanation of implementation approach, key decisions, or architectural changes]

  ## PR Size
  - Lines changed: {LINES}
  - Files changed: {FILES}
  {If >400 lines: Justification for size: ...}

  ## Coverage
  - Patch coverage: {PERCENTAGE}%
  {If <80%: Justification: ...}

  ## Documentation Updated
  {Checkboxes from documentation check above}
  {If ADR created: Link to ADR-00XX}

  ## Testing
  - [ ] Core functionality works end-to-end
  - [ ] Edge cases handled appropriately
  - [ ] No regressions in existing features
  - [ ] [Specific test scenarios for this PR]

  ## Review Focus
  [Guide reviewers to key areas needing attention]
  ```

## 4. Create Pull Request
- **Use GitHub CLI**: `!gh pr create --draft --assignee phrazzld --title "[generated title]" --body "[generated description]"`
- **ALWAYS create as draft**: Use `--draft` flag to allow for review before marking ready
- **ALWAYS assign to phrazzld**: Use `--assignee phrazzld` for consistent ownership
- **Add labels** based on change type (feature, bugfix, refactor, etc.)
- **Link issues** if commit messages reference them

## 5. Confirm and Report
- **Display PR URL** for immediate access
- **Summarize what was created**: title, key changes, testing notes
- **Next steps**: mention review process, CI/CD checks, deployment considerations