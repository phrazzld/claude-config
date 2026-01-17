---
description: Execute quality gates (tidy, test, lint) then push to remote
---

# PUSH

Execute comprehensive quality gates before pushing code: tidy workspace, organize project, run linter/build/tests, then sync and push to remote.

## 1. Tidy
- Audit ALL unstaged changes and untracked files
- For each file, propose specific action:
  - **Commit**: If it's quality code that should be included
  - **Add to .gitignore**: If it's generated/temporary content
  - **Delete**: If it's no longer needed
- Execute cleanup decisions to ensure working directory is clean
- *(Proceed only when working directory is tidy)*

## 2. Organize
- Analyze project root structure and organization
- Identify opportunities for improvement:
  - Files that can be consolidated or moved to subdirectories
  - New directories that would improve organization
  - Items that should be added to .gitignore
  - Redundant or outdated files that can be deleted
- Execute reorganization plan to improve project structure
- *(Proceed only when project is well-organized)*

## 3. Quality Gates
- Run linter. Fix all issues.
- Run build. Resolve all errors.
- Run full test suite. Address all failures.
- *(Proceed only if all pass)*

## 4. Git Operations
- `!git fetch origin` (or relevant remote)
- Check if local branch is behind remote
- **If behind, sync automatically**:
  - `!git pull origin [branch]` to merge remote changes
  - **If merge conflicts occur**:
    - Think very hard about each conflict:
      - Understand the purpose of both changes
      - Identify which version preserves functionality
      - Consider if both changes can be integrated
      - Prioritize maintaining working code over personal preference
    - **Resolve methodically**:
      - Examine each conflict file individually
      - Choose resolution that maintains code quality and functionality
      - Test resolution by running linter/build/tests after each major conflict resolution
      - Commit resolved conflicts with clear message
- `!git push origin HEAD` (or relevant branch)
- Report success or specific push errors