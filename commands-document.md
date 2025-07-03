Perform comprehensive documentation audit and generate actionable improvement tasks for repository documentation.

# DOCUMENT

## GOAL
Audit, critique, evaluate, consolidate, expand, and improve the documentation in the current repository.

## PROCESS
1. Analyze the repository's markdown documentation files
2. Evaluate structure, completeness, clarity, consistency, and organization
3. Generate a comprehensive TODO list with specific improvement tasks

## 1. Prepare Context
- Gather all the markdown documentation files in the project
- Review `@BACKLOG.md` to understand current documentation-related tasks
- Read leyline documents for documentation standards and expectations

## 2. Create Context File
- Create `DOCUMENT-CONTEXT.md` with project-specific documentation context:
  ```markdown
  # Documentation Context

  ## Project Structure
  [Brief description of project layout and documentation organization]

  ## Documentation Priorities
  [List specific areas where documentation improvements are most needed]

  ## Current Documentation Issues
  [Known documentation problems or gaps]
  ```

## 3. Execute Documentation Audit
- Think very hard about the documentation quality and completeness:
  - Analyze all markdown files for structure, clarity, and consistency
  - Evaluate documentation coverage against codebase functionality
  - Check for missing or outdated information
  - Assess organization and navigation ease
  - Identify redundancies and inconsistencies
  - Review adherence to documentation standards in leyline documents
  - Consider documentation accessibility and target audience needs
  - Evaluate code examples, diagrams, and cross-references
- Create `DOCUMENTATION_IMPROVEMENT_PLAN.md` with:
  - Current documentation state assessment
  - Gaps and issues identified
  - Prioritized improvement recommendations
  - Specific action items for each documentation area

## 4. Create Detailed TODO List
- Extract actionable tasks from the improvement plan
- Format as specific, detailed TODO items that can be implemented
- Include current issues, improvement recommendations, and priority levels

## 5. Present Results
- Summarize key findings and highest priority recommendations
- Provide the detailed TODO list for implementation