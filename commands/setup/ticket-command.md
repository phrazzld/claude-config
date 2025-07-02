# TICKET-COMMAND

Generate a project-specific `/project:ticket` command that creates actionable @TODO.md files using multi-agent expert analysis.

**Usage**: `/user:setup-ticket-command`

## Implementation Instructions

Create a project-specific "ticket" command that leverages multiple expert programming personas through Task tool subagents to decompose plans into discrete, actionable task items.

### Command Generation Process

1. **Analyze Project Context**
   - Read the current project structure and technology stack
   - Identify relevant leyline documents in `./docs/leyline/` if they exist
   - Check for existing TODO.md patterns and task tracking conventions
   - Understand the project's development workflow and task granularity

2. **Generate the Ticket Command**
   Create a command file at `.claude/commands/ticket.md` with the following structure:

   ```markdown
   # Strategic Task Decomposition - Multi-Expert TODO Generation

   Transform high-level plans into discrete, actionable TODO.md items using legendary programmer perspectives.

   **Usage**: `/project:ticket`

   ## GOAL

   Synthesize implementation plans into a TODO.md file composed of discrete, well-defined, narrowly scoped, highly detailed, context-rich, atomic and actionable task items.

   ## ANALYZE

   Transform the current plan or requirements into the most effective task breakdown possible.

   ### Phase 1: Context Analysis
   1. Read any existing plans, TASK.md, or requirements documentation
   2. Understand the project's architecture and technical constraints
   3. Identify dependencies, risks, and critical path items
   4. Review leyline documents for development principles
   5. Analyze existing TODO patterns in the codebase

   ### Phase 2: Multi-Expert Task Decomposition
   Launch parallel subagents embodying legendary programmer perspectives using the Task tool. Each subagent must run independently and in parallel for maximum efficiency. CRITICAL: All subagents operate in research/investigation mode only - they should NOT modify code, use plan mode, or create files. They must output all thoughts, findings, and brainstorming directly to chat:

   **Task 1: John Carmack - Engineering Excellence**
   - Prompt: "As John Carmack, break down this plan into atomic engineering tasks. Focus on algorithmic clarity, performance considerations, and first principles. Each task should be technically precise and implementation-focused. What are the most fundamental units of work? IMPORTANT: You are in research mode only - do not modify any code, do not use plan mode, and output all your task breakdown directly to chat."

   **Task 2: David Allen - GTD Methodology**
   - Prompt: "As David Allen (Getting Things Done), decompose this plan into next actions that are concrete, actionable, and context-specific. Each task should have a clear 'done' state and be executable without further planning. Focus on removing ambiguity. IMPORTANT: You are in research mode only - do not modify any code, do not use plan mode, and output all your task breakdown directly to chat."

   **Task 3: Kent Beck - Test-Driven Development**
   - Prompt: "As Kent Beck, break down this plan into testable increments. Each task should represent a verifiable behavior change. Structure tasks to enable test-first development and continuous integration. IMPORTANT: You are in research mode only - do not modify any code, do not use plan mode, and output all your task breakdown directly to chat."

   **Task 4: Martin Fowler - Refactoring & Architecture**
   - Prompt: "As Martin Fowler, identify refactoring and architectural tasks. Break down the work to maintain clean architecture, enable incremental improvements, and prevent technical debt accumulation. IMPORTANT: You are in research mode only - do not modify any code, do not use plan mode, and output all your task breakdown directly to chat."

   **Task 5: Joel Spolsky - Pragmatic Product Development**
   - Prompt: "As Joel Spolsky, create tasks that balance engineering excellence with shipping. Include tasks for documentation, edge cases, user experience polish, and practical deployment considerations. IMPORTANT: You are in research mode only - do not modify any code, do not use plan mode, and output all your task breakdown directly to chat."

   ### Phase 3: Task Characteristics
   Each expert should ensure their tasks are:
   - **Atomic**: Cannot be meaningfully subdivided
   - **Actionable**: Clear implementation path
   - **Measurable**: Obvious completion criteria
   - **Independent**: Minimal blocking dependencies
   - **Timeboxed**: Completable in reasonable time
   - **Context-rich**: Include necessary implementation details

   ## EXECUTE

   1. **Gather Context**
      - Read all relevant planning documents and requirements
      - Map out the technical implementation landscape
      - Identify key milestones and dependencies

   2. **Launch Expert Subagents**
      - Use the Task tool to create independent subagents for each perspective
      - All subagents run in parallel for maximum efficiency
      - Each expert creates their task breakdown independently in research mode only
      - Collect all task lists with rationales via direct chat output

   3. **Synthesis Round**
      - Launch a synthesis subagent using the Task tool to merge all expert task lists
      - Synthesis agent operates in research mode only - no code changes, no plan mode, output to chat
      - Eliminate duplicates while preserving unique insights
      - Order tasks by dependencies and critical path
      - Ensure comprehensive coverage without gaps

   4. **Task Formatting**
      - Format each task as: `- [ ] [Context] Specific action: implementation details`
      - Group related tasks under clear headings
      - Include acceptance criteria where helpful
      - Add priority indicators and time estimates if applicable

   5. **Generate TODO.md**
      Create a comprehensive TODO.md file with:
      ```markdown
      # TODO

      ## Overview
      [Brief summary of the implementation plan]

      ## Critical Path
      [Tasks that block other work]

      ## Core Implementation
      - [ ] [Task with full context and details]
      - [ ] [Task with dependencies noted]

      ## Testing & Validation
      - [ ] [Test-specific tasks]

      ## Documentation & Polish
      - [ ] [User-facing improvements]

      ## Technical Debt & Refactoring
      - [ ] [Architecture improvements]
      ```

   6. **PR Scope Sanity Check**
      After generating the initial TODO.md:
      - Analyze the total scope of work represented
      - Estimate if completing all tasks would create a PR that is:
        * Too large (>500 lines of code changes)
        * Too broad in scope (touching >10 files or multiple subsystems)
        * Too difficult to review (mixing refactoring with new features)

      If the scope is too large:
      - Break the work into logical, self-contained chunks
      - Each chunk should represent one focused PR worth of work
      - Prioritize chunks by dependencies and value delivery

   7. **Scope Management**
      If breaking up is needed:
      - Take the highest priority chunk as the new TODO.md scope
      - Regenerate TODO.md with only tasks for this focused scope
      - Write remaining chunks to BACKLOG.md:
        * Check if BACKLOG.md exists
        * If exists: Integrate new items elegantly, maintaining existing structure
        * If not: Create new BACKLOG.md with clear organization

      BACKLOG.md format:
      ```markdown
      # BACKLOG

      ## Upcoming Work Chunks

      ### [Chunk Name] - [Brief Description]
      **Prerequisites**: [What needs to be done first]
      **Scope**: [What this chunk accomplishes]
      **Tasks**:
      - [ ] [High-level task items for this chunk]

      ### [Next Chunk Name]
      ...
      ```

   ## Success Criteria

   - Every task is immediately actionable without further clarification
   - Complete task list covers all aspects of the plan
   - Tasks are properly sequenced with dependencies clear
   - Each task includes sufficient context for implementation
   - The breakdown enables parallel work where possible
   - No critical steps are missing from the implementation path
   - TODO.md scope is appropriate for a single, reviewable PR
   - Larger work is properly organized in BACKLOG.md for future PRs

   Execute this comprehensive task decomposition process now.
   ```

3. **Project-Specific Adaptations**
   Customize the generated command for the current project:
   - Reference specific task tracking tools or systems used
   - Adapt task formatting to match project conventions
   - Include project-specific task categories or labels
   - Reference relevant team workflows and processes

4. **Create and Confirm**
   - Write the customized command to `.claude/commands/ticket.md`
   - Verify the command is properly formatted and executable
   - Confirm the command is available as `/project:ticket`

Execute the ticket command generation now, creating a project-tailored task decomposition tool that leverages multi-agent expert analysis.
