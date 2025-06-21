# REFACTOR

## GOAL
Analyze the codebase and generate GitHub issues for code refactoring while preserving functionality.

## 1. Prepare Context
- Fetch current GitHub issues to understand existing tasks:
  ```bash
  gh issue list --state open --json number,title,body,labels --limit 100
  ```
- Read leyline documents.
- Identify all `glance.md` files in the codebase to gather architectural insights.

## 2. Create Context File
- Create `REFACTOR-CONTEXT.md` with the following content:
  ```markdown
  # Refactoring Analysis Context

  ## Current Issues
  [Include output from GitHub issues list]

  ## Request
  Analyze the codebase and generate items for code refactoring while preserving functionality.
  Focus on improving maintainability, readability, and reducing technical debt.
  ```

## 3. Generate Refactoring Items
- ***Think very hard*** about code refactoring opportunities by:
  - **Overview analysis**: Analyze codebase structure to identify key areas needing refactoring based on simplicity, readability, and maintainability goals
  - **Refactoring opportunities**: Break down effort into concrete, actionable tasks such as:
    - Removing duplicate functions across files
    - Improving naming consistency in modules
    - Restructuring modules to separate concerns
    - Simplifying complex logic in functions
    - Breaking up large files (approaching/exceeding 1000 lines)
    - Enhancing code organization by feature/domain
  - **Risk assessment**: For each opportunity, consider potential challenges (breaking changes, complex dependencies), verification strategy, and expected benefits
  - **Prioritization**: Categorize as Critical/High/Medium/Low based on impact and complexity (Simple/Medium/Complex)
- Ensure 100% of existing functionality is maintained while improving code quality
- Balance high-quality, maintainable code with avoiding overengineering
- For each refactoring opportunity, create a GitHub issue with appropriate details and labels
