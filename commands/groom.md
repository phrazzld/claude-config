# GROOM

## GOAL
Create an organized, expanded, and prioritized issue backlog based on comprehensive codebase insights.

## 1. Prepare Context
- Fetch current GitHub issues to understand existing tasks and direction:
  ```bash
  gh issue list --limit 100 --json number,title,body,labels
  ```
- Read leyline documents to anchor new backlog items in project principles.

## 2. Generate Enhanced GitHub Issues with Thinktank
- **Leyline Pre-Processing**: Query relevant leyline documents for grooming context:
  - Tenets related to product value, continuous delivery, and maintainability
  - Bindings for project organization and quality standards
  - Synthesize principles that guide prioritization and task decomposition
- Create `GROOM-CONTEXT.md` with grooming criteria and current issues information:
  ```markdown
  # Backlog Grooming Context

  ## Current Issues
  [Include output from GitHub issues list]

  ## Grooming Goals
  - Prioritize items based on business value and technical dependencies
  - Identify missing tasks that should be added
  - Remove or modify outdated tasks
  - Ensure all tasks are clear, atomic, and actionable
  ```
- **Think very hard** about comprehensive backlog grooming:
  - Thoroughly analyze the current GitHub issues from your context
  - Consider the project's overall architecture and direction
  - Identify:
    * Missing tasks that should be added (technical debt, improvements, features)
    * Existing tasks that need clarification or expansion
    * Outdated tasks that should be closed or modified
    * Dependencies between tasks that affect prioritization
  - For each backlog item, ensure:
    * Clear acceptance criteria
    * Appropriate sizing (S/M/L/XL)
    * Correct priority based on value and dependencies
    * Proper labels for categorization
  - Create a comprehensive grooming plan that addresses all findings

## 3. Update GitHub Issues
- For each existing issue that needs modifications:
  ```bash
  gh issue edit [issue-number] --title "Updated Title" --body "Updated description" --add-label "priority:high,type:feature"
  ```
- For new issues identified during grooming:
  ```bash
  gh issue create --title "New Issue Title" --body "Detailed description" --label "priority:medium,type:feature,size:m"
  ```
- For issues that are no longer relevant:
  ```bash
  gh issue close [issue-number] --comment "Closing as no longer relevant: [explanation]"
  ```
