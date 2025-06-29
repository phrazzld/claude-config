# SHRINK

## GOAL
Analyze the codebase and generate GitHub issues for code size optimization while preserving functionality.

## 1. Prepare Context
- Fetch current GitHub issues to understand existing tasks:
  ```bash
  gh issue list --state open --json number,title,body,labels --limit 100
  ```
- Read leyline documents.

## 2. Create Context File
- Create `SHRINK-CONTEXT.md` with the following content:
  ```markdown
  # Code Size Optimization Context

  ## Current Issues
  [Include output from GitHub issues list]

  ## Request
  Analyze the codebase and generate items for code size optimization while preserving functionality.
  Focus on reducing file sizes, eliminating duplicated code, and simplifying complex implementations.
  ```

## 3. Generate Size Optimization Items
- ***Think very hard*** about code size optimization opportunities by:
  - **Size analysis**: Identify largest files/modules, quantify codebase size metrics (LOC by file/module/type)
  - **Reduction opportunities**: Systematically catalog:
    - Redundant/duplicated code across the codebase
    - Unused/dead code (functions, methods, imports, variables)
    - Unnecessarily verbose implementations
    - Overengineered abstractions adding complexity without value
    - Unnecessary dependencies that could be removed
    - Over-commented code where self-documenting approaches would suffice
  - **Solution analysis**: For each opportunity, determine specific approach, potential size reduction, implementation risk, and verification strategy
  - **Prioritization**: Group by impact (Critical/High/Medium/Low) based on effort vs reduction potential
- Focus on dramatic size reduction while preserving 100% of essential functionality
- Balance quick wins (high impact, low effort) with strategic improvements
- For each size optimization opportunity, create a GitHub issue with appropriate details and labels
