# EXTRACT

## GOAL
Analyze the codebase to identify opportunities for extracting duplicated or related functionality into independent, reusable components that improve maintainability and adherence to development principles.

## 1. Prepare Context
- Fetch current GitHub issues to understand existing tasks:
  ```bash
  gh issue list --state open --json number,title,body,labels --limit 100
  ```
- Create `EXTRACT-CONTEXT.md` with the following content:
  ```markdown
  # Component Extraction Analysis Context

  ## Current Issues
  [Include output from GitHub issues list]

  ## Request
  Analyze the codebase to identify opportunities for extracting:
  1. Duplicated code across multiple files
  2. Related functionality that could be consolidated
  3. Complex code that would benefit from being modularized
  4. Implementation details that should be abstracted

  For each extraction opportunity, provide:
  - Description of the functionality to extract
  - Files/locations where this functionality currently exists
  - Benefits of extraction (reusability, maintainability, testability, etc.)
  - High-level approach for the extraction
  ```

## 2. Generate Extraction Opportunities
- ***Think very hard*** about component extraction opportunities by:
  - **Identifying cohesive units**: Find functionality that forms natural, self-contained modules with clear boundaries
  - **Analyzing duplication**: Detect code patterns repeated across files that could be consolidated
  - **Module definition**: For each extraction candidate, define:
    - Clear module boundaries and responsibilities
    - Public interfaces and contracts
    - Dependencies and coupling points
    - Implementation strategy preserving functionality
  - **Impact assessment**: Evaluate reuse potential, complexity reduction, maintainability improvements
  - **Prioritization**: Rank extractions by effort vs benefit, considering dependencies and risk
- Focus on creating independent, reusable components while maintaining 100% existing functionality
- Ensure extracted modules follow single responsibility principle and clean architecture
- Balance abstraction benefits against added complexity

## 3. Create GitHub Issues
- For each extraction opportunity identified, create a GitHub issue with:
  - Title describing the component to extract
  - Body containing:
    - Description of the functionality
    - Current implementation locations
    - Benefits of extraction
    - High-level extraction approach
  - Appropriate labels based on complexity, priority, and domain
- Tag related issues if the extraction depends on or impacts other work