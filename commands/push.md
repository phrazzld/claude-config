# PUSH

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
- `git fetch origin` (or relevant remote).
- Verify local branch not behind remote. **Stop** if behind (manual sync needed).
- `git push origin HEAD` (or relevant branch).
- Report success or specific push errors. **Stop**.

