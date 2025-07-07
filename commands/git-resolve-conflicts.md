# RESOLVE

Resolve merge conflicts methodically and cautiously to unblock stuck tasks.

## 1. Analyze Conflict
- `!git status` (identify conflicted files).
- `!git diff --check` (view conflict markers).
- `!git log --merge -p <conflicted_file>` (understand changes).
- Think hard & identify conflict pattern (Text, Semantic, Structural, Dependency).

## 2. Plan Resolution Strategy
- Review leyline documents.
- Identify cross-file dependencies.
- Decide approach per file (Keep Ours, Keep Theirs, Combine, Rewrite).
- Document plan for complex conflicts.

## 3. Resolve File-by-File
- For each conflicted file:
    - Inspect conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`).
    - Think carefully & edit file per strategy (Step 2). Preserve intent, maintain standards.
    - Remove all conflict markers.
    - Verify syntax.
    - Document complex resolutions with inline comments.

## 4. Validate Resolution
- Verify syntax/linting for resolved files.
- `!git add <resolved_file>` for each.
- `!git status` (confirm all resolved).
- Run build/compilation step.
- Run test suite.
- Manually verify critical functionality if needed.

## 5. Finalize Merge
- Final `!git status`.
- `!git commit` (use detailed message for complex merges).
- `!git push` (if appropriate).
- Cleanup temporary branches

## 6. Post-Merge Validation
- Run comprehensive tests.
- Request code review for complex resolutions.
- Document complex merge strategies if needed.