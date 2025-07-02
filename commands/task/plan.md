Select a task from @BACKLOG.md and create detailed breakdown in @TASK.md using parallel expert analysis.

# PLAN

Read available tasks from @BACKLOG.md, select highest priority task, and create detailed breakdown in @TASK.md using parallel expert analysis and research.

## 1. Task Selection & Analysis
- **Read @BACKLOG.md** to understand available tasks
- **Select highest priority task** from High Priority section, or present options if multiple HIGH tasks exist
- **Initialize @TASK.md** with selected task details
- **Launch parallel Task agents** for simultaneous analysis:
  ```
  Task 1: "Use gemini --prompt to research current best practices for [task domain] rapid implementation in 2025"
  Task 2: "Use Context7 MCP to find documentation for relevant libraries/frameworks mentioned in task"
  Task 3: "Analyze existing codebase patterns that could be reused/adapted for this task"
  Task 4: "Research common gotchas and quick solutions for [task type]"
  ```

## 2. Multi-Expert Analysis (Parallel Execution)
- **Launch parallel Task agents** with different expert perspectives:
  ```
  Task 1: "Ultrathink as John Carmack: What's the simplest, most direct solution?"
  Task 2: "[If user-facing] Think as Product/UX expert: What's the minimal delightful experience?"
  Task 3: "[If API/Backend] Think as Systems architect: What's the cleanest contract design?"
  Task 4: "[If data-related] Think as Data engineer: What's the most straightforward pipeline?"
  Task 5: "Think as pragmatic engineer: What existing code can we adapt/reuse?"
  ```

## 3. Generate Task Breakdown & Write to @TASK.md
- **Synthesize parallel findings** into cohesive approach
- **Break down if needed**: If task is too large for single PR, create logical chunks
- **Focus on speed**: Working prototype over perfect architecture
- **Write to @TASK.md** using this format:
  ```markdown
  # [Task Title from BACKLOG.md]
  
  ## Description
  [Clear description of what needs to be accomplished]
  
  ## Requirements
  - [Specific requirement 1 derived from analysis]
  - [Specific requirement 2]
  - [Specific requirement 3]
  
  ## Implementation Plan
  
  ### Quick Win Approach
  [Direct path to working solution based on expert synthesis]
  
  ### Implementation Steps
  1. [Specific first step with files/functions to modify]
  2. [Next step building on previous]
  3. [Continue until demonstrable]
  
  ### Breakdown (if task requires multiple PRs)
  - PR 1: [Focused deliverable]
  - PR 2: [Next logical chunk]
  
  ### Technical Choices
  - Using [X] because [already in codebase/fastest path]
  - Adapting pattern from [file:line] for consistency
  - Deferring [optimization] for future iteration
  
  ### Research Findings Applied
  - From Carmack perspective: [Simplification insight]
  - From [Expert] perspective: [Key consideration]
  - From research: [Best practice or library to use]
  
  ## Success Criteria
  - [ ] Core functionality works end-to-end
  - [ ] Basic tests demonstrate feature
  - [ ] Ready for stakeholder demo
  ```

## 4. Update @BACKLOG.md
- **Mark selected task as in progress**: Change `- [ ]` to `- [~]` for the selected task in @BACKLOG.md
- **Validate planning**: Ensure @TASK.md contains actionable breakdown with minimal complexity
- **Verify workflow**: Confirm approach leverages existing patterns and creates shippable chunks