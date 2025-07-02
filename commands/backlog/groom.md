Organize, prioritize, and enhance BACKLOG.md by analyzing tasks and ensuring philosophy alignment.

# GROOM

Organize, prioritize, and enhance @BACKLOG.md by analyzing existing tasks, identifying missing work, and checking philosophy alignment.

## 1. Prepare Context
- Read current @BACKLOG.md to understand existing tasks and structure
- Read project-specific leyline documents in `./docs/leyline/` if they exist
- Analyze current project priorities, constraints, and architecture

## 2. Comprehensive Backlog Analysis
- **Leyline Pre-Processing**: Query relevant leyline documents for grooming context:
  - Tenets related to project value, continuous delivery, and maintainability
  - Bindings for project organization and quality standards
  - Principles that guide prioritization and task decomposition
- Think very hard about comprehensive backlog grooming for THIS PROJECT:
  - Thoroughly analyze the current @BACKLOG.md tasks
  - Consider the project's current architecture, direction, and constraints
  - Identify:
    * Missing tasks that should be added (project-specific technical debt, improvements, features)
    * Existing tasks that need clarification, expansion, or better priority assignment
    * Outdated tasks that should be removed or modified for current project state
    * Dependencies between tasks that affect prioritization
    * Tasks that should be broken down into smaller, more atomic pieces
    * Tasks that should be consolidated if they're too granular
    * Philosophy alignment issues that warrant new tasks

## 3. Philosophy Alignment Check
- Think hard about the current project's alignment with development philosophy:
  - Systematically analyze major components against core principles:
    * Simplicity and modularity in current project context
    * Testability and explicit contracts in existing code
    * Maintainability and clarity of current implementation
    * Automation and tooling adherence for this specific project
  - For each misalignment found, create specific `[ALIGN]` tasks
  - Ensure alignment tasks are concrete and actionable for current codebase

## 4. Update @BACKLOG.md Structure
- **Reorganize tasks** by moving items between priority sections as needed
- **Update task descriptions** to be more specific and actionable
- **Remove completed/outdated tasks** or move to appropriate sections
- **Add missing tasks** identified during analysis
- **Add alignment tasks** for any philosophy violations found
- **Consolidate or split tasks** as appropriate for better workflow
- **Ensure consistent formatting**: `- [ ] [PRIORITY] [TYPE] Description`
  - Types: ALIGN/REFACTOR/FEATURE/BUG/DOCS/TEST/CHORE

## 5. Document Grooming Results
- Create brief summary of changes made:
  * Tasks added/removed/reprioritized
  * Alignment issues identified
  * Key dependencies or sequencing notes
  * Any project-specific considerations