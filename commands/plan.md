Generate a detailed implementation plan for a prioritized task, with focus on architecture, approach tradeoffs, implementation steps, testing strategy, and risk mitigation.

## 1. Select & Scope Task
- Fetch all open GitHub issues and examine their details:
  ```bash
  # Get all open issues
  gh issue list --state open --json number,title,labels,assignees --limit 100

  # After selecting an issue number, view its complete details
  gh issue view [issue-number] --json number,title,body,labels,assignees,milestone
  ```
- Select an important issue ready for implementation, prioritizing those with higher priority labels if available.

## 2. Generate Plan with Deep Analysis
- **Leyline Pre-Processing**: Based on selected issue characteristics:
  - Query tenets relevant to the planning domain (architecture, design, testing)
  - Identify bindings that constrain or guide the implementation approach
  - Internalize quality standards and architectural patterns from leyline documents
- Create `PLAN-CONTEXT.md` with the selected GitHub issue details:
  ```markdown
  # Task Description

  ## Issue Details
  [Issue title, number and URL]

  ## Overview
  [Brief description of the issue from body]

  ## Requirements
  [Extract requirements from issue description and/or labels]

  ## Technical Context
  [Any relevant technical details, constraints, or existing system information from the issue]

  ## Related Issues
  [Any linked or referenced issues]
  ```
- ***Think very hard*** about creating a ruthless, engineering-focused implementation plan by:
  - **Internalizing philosophy**: Read and deeply understand leyline documents and all their principles (simplicity, modularity, testability, etc.)
  - **Drafting multiple approaches**: Generate 2-3 distinct technical approaches, analyzing each against philosophy alignment, pros/cons, and risks
  - **Selecting the optimal path**: Choose the approach that best balances simplicity, maintainability, and avoiding overengineering
  - **Expanding into detailed plan**: Create a comprehensive PLAN.md with:
    - Architecture blueprint (modules, interfaces, data flow)
    - Precise build steps (ready to convert to tasks)
    - Testing strategy (layers, minimal mocking, coverage)
    - Logging & observability approach
    - Security & configuration considerations
    - Risk matrix with severities and mitigations
    - Open questions that need resolution
- Focus on hard engineering details, expose every technical decision and tradeoff
- Ensure the plan delivers practical value without unnecessary complexity

## 3. Checkout Branch
- Use `gh issue develop` to create and check out a branch that is automatically linked to the selected GitHub issue:
  ```bash
  gh issue develop [issue-number]
  ```
