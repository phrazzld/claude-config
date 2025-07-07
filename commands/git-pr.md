Create pull request with auto-generated title and description from commit history.

# PR

Open a pull request for current branch with punchy title and comprehensive description generated from commit history.

## 1. Analyze Branch Changes
- **Get commit history**: `!git log main..HEAD --oneline` to see all commits on current branch
- **Get detailed changes**: `!git log main..HEAD --pretty=format:"%h %s%n%b" --no-merges` for full commit details
- **Get file changes**: `!git diff --name-only main..HEAD` to understand scope of changes
- **Get stats**: `!git diff --stat main..HEAD` for change magnitude

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