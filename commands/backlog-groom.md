# BACKLOG-GROOM

## GOAL
Organize, prioritize, and clean up the local BACKLOG.md file to maintain an actionable and well-structured task list.

## 1. Prepare Context
- Read current BACKLOG.md to understand existing tasks and structure
- Identify all `glance.md` files in the current project to gather architectural insights
- Read project-specific leyline documents in `./docs/leyline/` if they exist
- Analyze current project priorities and constraints

## 2. Create Context File
- Create `GROOM-CONTEXT.md` with grooming criteria and current backlog information:
  ```markdown
  # Backlog Grooming Context

  ## Current BACKLOG.md Structure
  [Include overview of existing sections and task counts]

  ## Current Tasks Summary
  ### High Priority
  [List current high priority tasks]
  
  ### Medium Priority
  [List current medium priority tasks]
  
  ### Low Priority
  [List current low priority tasks]

  ## Grooming Goals
  - Prioritize items based on project value and technical dependencies
  - Identify missing tasks that should be added for current project
  - Remove or modify outdated/irrelevant tasks
  - Ensure all tasks are clear, atomic, and actionable for this project
  - Maintain proper task format and organization
  ```

## 3. Comprehensive Backlog Grooming
- **Leyline Pre-Processing**: Query relevant leyline documents for grooming context:
  - Tenets related to project value, continuous delivery, and maintainability
  - Bindings for project organization and quality standards
  - Synthesize principles that guide prioritization and task decomposition for current project
- **Think very hard** about comprehensive backlog grooming for THIS PROJECT:
  - Thoroughly analyze the current BACKLOG.md tasks
  - Consider the project's current architecture, direction, and constraints
  - Identify:
    * Missing tasks that should be added (project-specific technical debt, improvements, features)
    * Existing tasks that need clarification, expansion, or better priority assignment
    * Outdated tasks that should be removed or modified for current project state
    * Dependencies between tasks that affect prioritization in this project
    * Tasks that should be broken down into smaller, more atomic pieces
    * Tasks that should be consolidated if they're too granular
  - For each backlog item, ensure:
    * Clear, actionable description specific to current project
    * Appropriate priority (HIGH/MED/LOW) based on project impact
    * Correct task type (ALIGN/REFACTOR/FEATURE/BUG/DOCS/TEST/CHORE)
    * Proper placement in priority sections
    * Atomic scope that can be extracted to task.md effectively

## 4. Update BACKLOG.md Structure
- **Reorganize tasks** by moving items between priority sections as needed
- **Update task descriptions** to be more specific and actionable
- **Remove completed tasks** to Completed section or delete if no longer relevant
- **Add missing tasks** identified during analysis
- **Consolidate or split tasks** as appropriate for better workflow
- **Ensure consistent formatting**: `- [ ] [PRIORITY] [TYPE] Description`

## 5. Document Grooming Results
- Update `GROOM-CONTEXT.md` with grooming decisions and rationale
- Include:
  * Summary of changes made
  * Rationale for priority adjustments
  * Notes about task dependencies or sequencing
  * Any project-specific considerations that influenced grooming

