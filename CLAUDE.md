# CLAUDE

Sacrifice grammar for the sake of concision.

## Software Design Philosophy

**Foundation**: Informed by John Ousterhout's "A Philosophy of Software Design" - managing complexity is the primary challenge in software engineering.

### Complexity Management
- **The Enemy**: Complexity is anything that makes software hard to understand or modify
- **Two Sources**: Dependencies (linkages between components) + Obscurity (non-obvious information)
- **Zero Tolerance**: Fight accumulating complexity with every decision

### Module Design
- **Deep Modules**: Simple interfaces hiding powerful implementations
- **Value Formula**: Module worth = Functionality - Interface Complexity
- **Watch For**: Shallow modules where interface ≈ implementation complexity
- **Layer Discipline**: Each abstraction layer must change vocabulary and concepts

### Information Architecture
- **Hide Implementation**: Internal details stay internal
- **Expose Intention**: Interfaces define "what" not "how"
- **Detect Leakage**: If implementation changes break callers, you have leakage
- **Design for Misuse**: Make interfaces hard to use incorrectly

### Strategic Programming
- **Time Investment**: Dedicate 10-20% to design improvement, not just feature completion
- **Tactical vs Strategic**: Recognize when taking shortcuts vs investing in future velocity
- **Comments as Design**: Document reasoning, invariants, and intent code cannot express
- **Red Flags**: Watch for `Manager`/`Util`/`Helper` names, pass-through methods, config overload

## Essential Tools

**Code Analysis:**
* Use `ast-grep` for semantic code search and structural pattern matching
  ```bash
  ast-grep --lang typescript -p 'function $NAME($$$) { $$$ }'
  ast-grep --lang rust -p 'impl $TRAIT for $TYPE'
  ```

**Parallel Execution:**
* Use the `Task` tool to launch multiple agents in parallel when actions operate in distinct, non-conflicting spaces:
  - Research from different perspectives or domains
  - Brainstorming ideas with independent expert viewpoints
  - Conducting investigations across separate code areas
  - Writing code/tests/docs in isolated modules
  ```bash
  # Example: Launch parallel research agents
  Task 1: "Research authentication patterns in codebase"
  Task 2: "Investigate API rate limiting best practices"
  Task 3: "Analyze error handling conventions"
  ```
