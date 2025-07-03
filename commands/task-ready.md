Convert @TASK.md implementation plan into discrete, actionable @TODO.md entries.

# READY

Read detailed breakdown from @TASK.md and convert implementation steps into discrete, actionable entries in @TODO.md.

## 1. Read Current @TASK.md
- **Analyze task structure**: Extract title, description, implementation steps, and success criteria
- **Identify discrete actions**: Break down each implementation step into specific, actionable items
- **Assess complexity**: Determine if any steps need further subdivision into atomic tasks

## 2. Generate Actionable TODO Items
- **Think very hard about task decomposition**: Convert each step into specific actions that can be completed in one work session
- **Ensure atomic scope**: Each TODO item should be:
  - **Discrete**: One specific action (e.g., "Create UserAuth component in src/components/")
  - **Well-defined**: Clear boundaries and scope (e.g., "Add login form validation to UserAuth.tsx")
  - **Narrowly scoped**: Focused on single concern (e.g., "Write unit tests for login validation")
  - **Highly detailed**: Include file paths, function names, specific requirements
  - **Context rich**: Reference existing patterns, dependencies, constraints
  - **Actionable**: Start with action verbs (Create, Update, Add, Refactor, Test, etc.)

## 3. Structure TODO Items
- **Use standard format**: `- [ ] [Context] Specific action: implementation details`
- **Examples of good TODO items**:
  ```
  - [ ] Create UserAuth component: implement login form in src/components/UserAuth.tsx following existing form patterns
  - [ ] Add validation logic: integrate Yup schema validation for email/password in UserAuth component
  - [ ] Update AuthContext: add login/logout methods to src/contexts/AuthContext.tsx
  - [ ] Write unit tests: create UserAuth.test.tsx with login form validation scenarios
  - [ ] Update routing: add protected route wrapper in src/App.tsx using AuthContext
  ```

## 4. Write to @TODO.md
- **Initialize if needed**: Create @TODO.md with proper structure if it doesn't exist:
  ```markdown
  # PROJECT TODO

  ## Current Sprint

  ## Next Up

  ## Completed
  ```
- **Read existing @TODO.md**: Understand current structure and avoid duplication
- **Append new items**: Add converted TODO items to "Current Sprint" or "Next Up" section
- **Maintain organization**: Group related items together, preserve existing structure
- **Update @TODO.md**: Write complete updated file with new actionable items integrated

## 5. Update Status Tracking
- **Mark TASK.md as processed**: Update @BACKLOG.md to show task has been broken down (if applicable)
- **Prepare for execution**: Ensure @TODO.md is ready for `todo/execute.md` command
- **Validate breakdown**: Confirm all TODO items are properly formatted and actionable