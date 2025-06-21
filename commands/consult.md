# CONSULT

## GOAL
Generate alternative approaches and solutions for a blocked task by leveraging multiple AI models, then create specific follow-up tasks in TODO.md.

## 1. Formulate Request & Identify Task
- Identify the issue or blocked task you're struggling with (reference task ID if available).
- Create `CONSULT-REQUEST.md`.
- ***Think hard*** & populate with: `Task Description`, `Goal`, `Problem/Blocker` (Relate to leyline documents), `Context/History`, `Key Files`, `Errors`, `Desired Outcome`.
- Identify the ten files most relevant to the problem you're struggling with.
- Identify leyline documents

## 2. Generate Alternative Approaches
- Add to `CONSULT-REQUEST.md`: "Keep the program's purpose in mind and strive for the highest quality maintainable solutions while avoiding overengineering."
- **Think very hard** about alternative solutions to unblock the task:
    - Analyze the problem from multiple angles and perspectives
    - Consider different architectural approaches that could work
    - Think about similar problems you've solved and how those solutions might apply
    - Explore trade-offs between different solutions (complexity, performance, maintainability)
    - Consider both short-term fixes and long-term sustainable solutions
    - Think about edge cases and potential failure modes for each approach
    - Evaluate each solution against the project's development philosophy and leyline documents
- Create `CONSULTANT-PLAN.md` with multiple detailed solution approaches, including:
    - Pros and cons of each approach
    - Implementation complexity
    - Alignment with project principles
    - Recommended approach with justification

## 3. Generate Resolution Tasks in TODO.md
- Create `CONSULT-CONTEXT.md` with task generation context:
    ```markdown
    # Consultation Task Generation

    ## Consultation Plan
    [Summary of key points from CONSULTANT-PLAN.md]

    ## Task Requirements
    - Decompose the consultant's plan into new, atomic tasks for TODO.md
    - Assign appropriate task IDs based on project conventions
    - Format tasks according to project's task format
    - Ensure final task resolves the original issue
    ```
- **Think very hard** about breaking down the chosen solution into implementable tasks:
    - Decompose the solution into atomic, testable components
    - Identify dependencies between tasks and order them appropriately
    - Include tasks for writing tests to verify the solution
    - Add tasks for updating documentation if needed
    - Consider tasks for handling edge cases identified in the plan
    - Ensure each task has clear acceptance criteria
    - Think about verification steps to confirm the original issue is resolved
- Insert well-formatted tasks into `TODO.md`, maintaining consistent formatting.
- Remove `CONSULT-REQUEST.md`, `CONSULTANT-PLAN.md`, `CONSULT-TASKGEN-REQUEST.md`.
- Report: "Generated resolution tasks in TODO.md for the original issue. Proceed via /execute."
- **Stop** `/consult`.