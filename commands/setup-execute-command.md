# Setup Execute Command - Generate Systematic Task Execution Command

Generate a project-specific `/project:execute` command that methodically works through TODO.md tasks with expert-level execution strategies.

**Usage**: `/user:setup-execute-command`

## Implementation Instructions

Create a project-specific "execute" command that systematically completes tasks from TODO.md using strategic planning and expert execution patterns.

### Command Generation Process

1. **Analyze Project Context**
   - Read the current project structure and technology stack
   - Identify relevant leyline documents in `./docs/leyline/` if they exist
   - Understand existing development workflows and execution patterns
   - Check for project-specific tooling and testing requirements

2. **Generate the Execute Command**
   Create a command file at `.claude/commands/execute.md` with the following structure:

   ```markdown
   # Strategic Task Executor - Systematic TODO Completion

   Methodically execute tasks from TODO.md with expert-level strategic planning and implementation.

   **Usage**: `/project:execute`

   ## GOAL

   Select and complete the next available task from TODO.md using comprehensive analysis, strategic planning, and flawless execution.

   ## ACQUISITION

   Select the next available ticket from TODO.md following this priority:
   1. In-progress tasks marked with `[~]` - Continue where work was paused
   2. Unblocked tasks marked with `[ ]` - Start fresh work
   3. Consider task dependencies and critical path
   4. Skip blocked tasks until dependencies are resolved

   If all tasks in TODO.md are completed:
   - Celebrate completion appropriately
   - Suggest next strategic moves
   - Halt

   ## CONTEXT GATHERING

   Conduct comprehensive review before execution:

   ### 1. **Codebase Analysis**
   - Read all files mentioned in or relevant to the task
   - Understand existing patterns and conventions
   - Identify potential impact areas and dependencies

   ### 2. **Documentation Review**
   - Study relevant leyline documents for foundational principles
   - Check project README and contributing guidelines
   - Review any architectural decision records (ADRs)

   ### 3. **External Research**
   - Use Context7 MCP server for framework/library documentation
   - Conduct web searches for best practices and common pitfalls
   - Research similar implementations in respected codebases

   ### 4. **Advanced Analysis** (when task complexity warrants)
   - Invoke `thinktank` CLI for multi-perspective analysis
   - Consider security, performance, and maintainability angles
   - Evaluate long-term implications of implementation choices

   ## STRATEGIC PLANNING

   ### Multi-Expert Planning Session

   For complex tasks, use the Task tool to consult expert perspectives:

   **Task 1: John Carmack - First Principles Engineering**
   - Prompt: "As John Carmack, analyze this implementation task. What's the most elegant, performant solution? Consider algorithmic efficiency, system design, and mathematical elegance. What would you optimize?"

   **Task 2: Linus Torvalds - Pragmatic Excellence**
   - Prompt: "As Linus Torvalds, review this task. What's the most practical, maintainable approach? Focus on code that works reliably, handles edge cases, and doesn't over-engineer."

   **Task 3: Kent Beck - Incremental Perfection**
   - Prompt: "As Kent Beck, plan this implementation. How would you approach it test-first? What's the smallest change that could possibly work? How do we ensure correctness?"

   ### Plan Synthesis
   - Combine expert insights into a cohesive strategy
   - Create step-by-step implementation plan
   - Identify checkpoints for validation
   - Plan for rollback if issues arise

   ## IMPLEMENTATION

   Execute the approved plan with precision:

   ### 1. **Pre-Implementation Setup**
   - Create feature branch if required
   - Set up test infrastructure
   - Prepare any necessary tooling

   ### 2. **Incremental Execution**
   - Implement in small, testable increments
   - Run tests after each significant change
   - Commit working states frequently
   - Follow project's code style and conventions

   ### 3. **Continuous Validation**
   - Run linters and formatters as specified in leyline docs
   - Execute test suite after each component
   - Verify no regressions introduced
   - Check performance implications

   ### 4. **Adaptive Response**
   If encountering unexpected situations:
   - **HALT** implementation immediately
   - Document the specific issue encountered
   - Analyze implications for the current approach
   - Present findings to user with recommendations
   - Wait for guidance before proceeding

   ## QUALITY ASSURANCE

   Before marking task complete:

   ### 1. **Code Quality Checks**
   - All tests pass (unit, integration, e2e as applicable)
   - Linting and formatting compliance
   - No commented-out code or TODOs left
   - Documentation updated if needed

   ### 2. **Functional Validation**
   - Task requirements fully met
   - Edge cases handled appropriately
   - Performance acceptable
   - No security vulnerabilities introduced

   ### 3. **Integration Verification**
   - Changes work with existing codebase
   - No breaking changes unless intended
   - API contracts maintained
   - Backward compatibility preserved

   ## CLEANUP

   Upon successful completion:

   ### 1. **Task Management**
   - Update task status to `[x]` in TODO.md
   - Add completion notes if helpful for future reference
   - Check for any follow-up tasks that are now unblocked

   ### 2. **Code Finalization**
   - Ensure all changes committed with clear messages
   - Update any relevant documentation
   - Clean up any temporary files or branches

   ### 3. **Progress Assessment**
   - Review remaining tasks in TODO.md
   - Consider if BACKLOG.md needs attention
   - Identify any emergent tasks from implementation
   - Prepare summary of what was accomplished

   ## SUCCESS CRITERIA

   - Task completed according to specifications
   - Code quality meets or exceeds project standards
   - All tests pass and coverage maintained
   - Implementation follows project conventions
   - No technical debt introduced
   - Clear documentation of any decisions made
   - Ready for code review and integration

   ## FAILURE PROTOCOLS

   If unable to complete task:
   - Document specific blockers encountered
   - Update task with `[!]` blocked status
   - Create new tasks for unblocking work
   - Communicate clearly about obstacles
   - Suggest alternative approaches

   Execute the next task with strategic excellence and systematic precision.
   ```

3. **Project-Specific Adaptations**
   Customize the generated command for the current project:
   - Reference specific build/test commands from package.json or Makefile
   - Include project-specific quality gates and checks
   - Adapt expert personas to relevant domain experts
   - Include project-specific tooling (thinktank, specific linters, etc.)
   - Reference team's definition of "done"

4. **Create and Confirm**
   - Write the customized command to `.claude/commands/execute.md`
   - Verify the command integrates with existing TODO.md workflow
   - Confirm the command is available as `/project:execute`

Execute the execute command generation now, creating a project-tailored systematic task executor.
