# BACKLOG-ALIGN

## GOAL
Analyze the current project codebase against leyline development philosophy and add alignment improvement tasks to local BACKLOG.md.

## 1. Project Context Analysis
- Read local BACKLOG.md to understand existing tasks and avoid duplication
- Identify all `glance.md` files in the current project to gather architectural insights
- Read project-specific leyline documents in `./docs/leyline/` if they exist
- Analyze current project structure, technologies, and patterns

## 2. Create Context File
- Create `ALIGN-CONTEXT.md` with the following content:
  ```markdown
  # Philosophy Alignment Context

  ## Current BACKLOG.md Status
  [Include summary of existing backlog items to avoid duplication]

  ## Project Architecture
  [Brief overview of current project structure and technologies]

  ## Request
  Analyze the current project codebase against leyline documents and our development philosophy.
  Add concrete alignment improvement tasks to BACKLOG.md.
  Focus on project-specific issues, not general guidelines.
  ```

## 3. Generate Philosophy-Aligned Improvement Tasks
- **Leyline Pre-Processing**: Before analyzing alignment:
  - Read leyline documents from `./docs/leyline/` and `~/.claude/docs/leyline/`
  - Focus on principles relevant to identified project components and patterns
  - Internalize both philosophical foundations and practical implementation guidelines
- **Think very hard** about the current project's alignment with development philosophy:
  - Read and internalize leyline documents
  - Systematically analyze each major component/module against core principles:
    * Simplicity and modularity in current project context
    * Testability and explicit contracts in existing code
    * Maintainability and clarity of current implementation
    * Automation and tooling adherence for this specific project
  - Consider existing BACKLOG.md items to avoid duplication
  - Identify specific misalignments, anti-patterns, or areas for improvement in THIS PROJECT
  - For each finding, determine:
    * The specific principle being violated in current codebase
    * The impact on this project's maintainability
    * A concrete improvement strategy for current code
    * Priority level (HIGH/MED/LOW) based on project impact

## 4. Add Tasks to BACKLOG.md
- **Format**: Add tasks using standard BACKLOG.md format:
  ```
  - [ ] [PRIORITY] [ALIGN] Specific alignment improvement description
  ```
- **Organization**: Add to appropriate priority section in BACKLOG.md
- **Specificity**: Each task should be:
  - Actionable and concrete for this specific project
  - Reference specific files/modules where relevant
  - Include clear acceptance criteria
  - Focused on current codebase, not general principles

## 5. Update Context
- Document the analysis in `ALIGN-CONTEXT.md` for future reference
- Include rationale for each major alignment task added
- Note any project-specific constraints or considerations

