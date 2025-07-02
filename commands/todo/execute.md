Execute the next available task from TODO.md with adaptive context gathering and planning.

# EXECUTE

Execute the next available task from @TODO.md with adaptive context gathering and planning based on task complexity.

## ACQUISITION

Select the next available ticket from @TODO.md queue. Prioritize in progress `[~]` tickets, then grab next unblocked `[ ]` ticket. If all tickets completed, halt and say something witty.

**Mark task as in-progress**: If selected task is `[ ]`, immediately update it to `[~]` in @TODO.md to indicate work has started.

## DYNAMIC CONTEXT GATHERING

Assess task complexity and gather context accordingly:

**For simple tasks** (bug fixes, small features, documentation):
- Quick codebase scan of relevant files
- `!gemini --prompt "quick tips for [task type]"`

**For medium tasks** (new features, refactors):
- Read relevant leyline docs if applicable
- `!gemini --prompt "best practices for [task domain] in 2025"`
- Analyze existing patterns in codebase
- Use Context7 MCP for specific library docs if needed

**For complex tasks** (architecture changes, system design):
- **Launch parallel research agents**:
  ```
  Task 1: "Use gemini to research current industry patterns for [task domain]"
  Task 2: "Analyze codebase architecture and identify integration points"
  Task 3: "Use Context7 MCP to deep-dive relevant framework documentation"
  Task 4: "Search for similar implementations or prior art"
  ```
- Consider invoking `!thinktank instructions.txt ./src` for architectural guidance

## ADAPTIVE STRATEGIC PLANNING

**For simple tasks**:
- Think about the most direct solution
- What would Carmack do? (simplest path forward)

**For medium tasks**:
- Think hard about implementation approach
- Consider 2-3 options and pick the most pragmatic
- Balance speed with maintainability

**For complex tasks**:
- **Ultrathink** with parallel expert personas:
  ```
  Task 1: "As John Carmack, what's the minimal essential solution?"
  Task 2: "As [Domain Expert], what are critical considerations?"
  Task 3: "As pragmatic engineer, what can we reuse/adapt?"
  Task 4: "As future maintainer, what will cause least pain?"
  ```
- Synthesize expert perspectives into cohesive plan
- Identify risks and mitigation strategies

## IMPLEMENTATION

Execute plan with appropriate vigor:
- **Simple tasks**: Direct implementation, test, done
- **Medium tasks**: Implement, validate approach works, refine if needed
- **Complex tasks**: Implement incrementally, validate assumptions at each step

If encountering unexpected blockers or significant new information, halt and report the situation for reassessment.

## CLEANUP

Update ticket status to [x] in @TODO.md upon completion.