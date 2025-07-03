# PLAN-COMMAND

Generate a project-specific `/project:plan` command that creates comprehensive implementation plans using multi-agent expert analysis.

**Usage**: `/user:setup-plan-command`

## Implementation Instructions

Create a project-specific "plan" command that leverages multiple expert programming personas through Task tool subagents to generate the best possible implementation plan for tasks described in @TASK.md.

### Command Generation Process

1. **Analyze Project Context**
   - Read the current project structure and technology stack
   - Identify relevant leyline documents in `./docs/leyline/` if they exist
   - Check for existing command patterns in `.claude/commands/`
   - Understand the project's architectural patterns and conventions

2. **Generate the Plan Command**
   Create a command file at `.claude/commands/plan.md` with the following structure:

   ```markdown
   # Strategic Implementation Planner - Multi-Expert Analysis

   Create comprehensive implementation plans using legendary programmer perspectives and thorough research.

   **Usage**: `/project:plan`

   ## GOAL

   Generate the best possible implementation plan for the task described in @TASK.md by:
   - Conducting exhaustive research and context gathering
   - Leveraging multiple expert programming personas through subagents. Make sure each one only conducts research and investigations and brainstorms, and outputs all responses directly to chat -- they should not make code changes and they should not use plan mode
   - Synthesizing diverse perspectives into a strongly opinionated recommendation

   ## ANALYZE

   Your job is to make the best possible implementation plan for the task described in @TASK.md.

   ### Phase 1: Foundation Research
   1. Read @TASK.md thoroughly to understand requirements and constraints
   2. Comb through the codebase to collect relevant context and patterns
   3. Read relevant leyline documents in `./docs/leyline/` for foundational principles
   4. Use context7 MCP server to research relevant documentation
   5. Conduct web searches on the problem domain, solutions, and best practices

   ### Phase 2: Multi-Expert Analysis
   Launch parallel subagents embodying legendary programmer perspectives using the Task tool. Each subagent must run independently and in parallel for maximum efficiency. CRITICAL: All subagents operate in research/investigation mode only - they should NOT modify code, use plan mode, or create files. They must thoroughly review, investigate, audit, and analyze, outputting all findings directly to chat.

   **Task 1: John Carmack Perspective**
   - Prompt: "As John Carmack, analyze this task focusing on performance optimization, elegant algorithms, and first principles thinking. What would be the most algorithmically sound and performance-optimized approach? Consider memory management, computational complexity, and elegant mathematical solutions. IMPORTANT: You are in research mode only - do not modify any code, do not use plan mode, and output all your analysis directly to chat."

   **Task 2: Richard Stallman Perspective**
   - Prompt: "As Richard Stallman, analyze this task from software freedom, ethical considerations, and long-term maintainability perspectives. How would you ensure user freedom, avoid vendor lock-in, and create truly maintainable solutions that serve users rather than corporations? IMPORTANT: You are in research mode only - do not modify any code, do not use plan mode, and output all your analysis directly to chat."

   **Task 3: Linus Torvalds Perspective**
   - Prompt: "As Linus Torvalds, analyze this task focusing on pragmatic engineering, scalability, and robust system design. What would be the most practical, no-nonsense approach that scales well and handles edge cases gracefully? IMPORTANT: You are in research mode only - do not modify any code, do not use plan mode, and output all your analysis directly to chat."

   **Task 4: Jeff Dean Perspective**
   - Prompt: "As Jeff Dean, analyze this task from distributed systems, massive scale, and reliability engineering perspectives. How would you design this to handle enormous scale, ensure reliability, and optimize for distributed computing environments? IMPORTANT: You are in research mode only - do not modify any code, do not use plan mode, and output all your analysis directly to chat."

   **Task 5: Bret Taylor Perspective**
   - Prompt: "As Bret Taylor, analyze this task focusing on product-focused engineering and user experience. What approach would best serve actual user needs while being practically implementable and maintainable by a team? IMPORTANT: You are in research mode only - do not modify any code, do not use plan mode, and output all your analysis directly to chat."

   ### Phase 3: Design Exploration
   For each approach, consider:
   - **Simplest solutions**: Most straightforward, minimal viable approaches
   - **Complex solutions**: Comprehensive, feature-rich implementations
   - **Creative solutions**: Innovative, cut-the-gordian-knot style approaches
   - **Hybrid approaches**: Combinations that leverage multiple methodologies

   ## EXECUTE

   1. **Foundation Analysis**
      - Read and thoroughly understand @TASK.md requirements
      - Map out current codebase patterns and architectural decisions
      - Research domain-specific best practices and common pitfalls

   2. **Launch Expert Subagents**
      - Use the Task tool to create independent subagents for each programming legend
      - All subagents run in parallel for maximum efficiency
      - Each analyzes the problem through their distinctive lens in research mode only
      - Collect their unique recommendations via direct chat output

   3. **Cross-Pollination Round**
      - Launch follow-up subagents using the Task tool that review all expert perspectives
      - Subagents operate in research mode only - no code changes, no plan mode, output to chat
      - Identify synergies and conflicts between different approaches
      - Generate hybrid solutions that combine the best insights

   4. **Synthesis and Evaluation**
      - Compare all approaches across multiple dimensions:
        * Technical feasibility and complexity
        * Performance and scalability characteristics
        * Maintainability and long-term sustainability
        * User experience and practical utility
        * Implementation timeline and resource requirements
      - Evaluate tradeoffs and identify the optimal balance

   5. **Strategic Recommendation**
      - Present the best implementation approach with clear rationale
      - Include specific architectural decisions and design patterns
      - Provide implementation phases with risk mitigation strategies
      - Document alternative approaches and why they were not selected
      - Include success metrics and validation strategies

   ## Success Criteria

   - Comprehensive analysis incorporating multiple expert perspectives
   - Clear, actionable implementation plan with strong technical rationale
   - Consideration of both technical excellence and practical constraints
   - Strategic approach that maximizes probability of successful execution
   - Integration with existing codebase patterns and project conventions

   Execute this comprehensive multi-expert planning process now.
   ```

3. **Project-Specific Adaptations**
   Customize the generated command for the current project:
   - Reference specific technologies, frameworks, and architectural patterns used
   - Include project-specific file patterns and naming conventions
   - Adapt expert personas to focus on relevant technical domains
   - Include references to project-specific documentation and standards

4. **Create and Confirm**
   - Write the customized command to `.claude/commands/plan.md`
   - Verify the command is properly formatted and executable
   - Confirm the command is available as `/project:plan`

Execute the plan command generation now, creating a project-tailored strategic planning tool that leverages multi-agent expert analysis.
