Transform skeletal TODOs into executable specifications through deep analysis.

# FLESH

Channel Carmack: "Focus is a matter of deciding what things you're not going to do."

## The Carmack Principle

"The difference between a TODO and a specification is understanding."

A vague task hides complexity. Flesh it out before you code it out.

## Find the Next Task

Read TODO.md for first `[ ]` or `[~]` task. Copy the task description verbatim. Note any existing work log or context.

**Think deeply**: What does this task REALLY require?
- Hidden dependencies and assumptions?
- Edge cases lurking in the shadows?
- Performance implications at scale?
- Security considerations?
- Testing requirements?

## Research & Analysis

**Launch parallel research** (use Task tool for concurrent agents):

```
Task 1: "Research best practices for [task description]:
- Use gemini --prompt for current industry patterns
- Find proven implementation approaches and common pitfalls
- Security and performance considerations
Focus on production-ready solutions, not experiments."

Task 2: "Find relevant documentation:
- Use Exa MCP for documentation and code examples
- Extract critical APIs and usage patterns
- Note version constraints and breaking changes
Only include what's needed for THIS task."

Task 3: "Analyze codebase patterns:
- Use ast-grep to find similar implementations
- Grep for existing utilities and helpers
- Identify conventions to follow
Don't reinvent what already exists here."
```

## Task Expansion Principles

**Modularity Analysis**:
- Can task be split into smaller, testable modules?
- What are natural module boundaries?
- What parts can be parallelized?
- What interfaces are required?
- How does this integrate with existing modules?

**Testability Strategy**:
- What test scenarios? (unit/integration/e2e)
- What needs mocking and why?
- What test data is required?
- Happy path, edge cases, error conditions
- Minimum coverage requirements

**Automation Opportunities**:
- Repetitive patterns that could be automated?
- Code generation opportunities?
- Manual processes that slow development?
- Boilerplate templates needed?

## Flesh Out the TODO

Expand the task with discovered intelligence:

```markdown
- [ ] [Original task description]
  ```
  Approach: [Step-by-step based on research]
  Files: file1.ts:45, file2.py:120
  Pattern: Follow existing implementation in Similar.tsx

  Modularity:
  - Components: [Independent modules identified]
  - Interfaces: [Contracts between modules]
  - Parallelizable: [What can be done simultaneously]

  Test Strategy:
  - Unit: [Specific functions/modules to test]
  - Integration: [Module interaction scenarios]
  - Edge cases: [Specific conditions to validate]
  - Coverage: [Minimum percentage or critical paths]

  Automation: [Identified repetitive patterns to script]

  Success:
  - [ ] [Specific, measurable outcome 1]
  - [ ] [Specific, measurable outcome 2]
  - [ ] Tests pass, module boundaries maintained

  Constraints: [Dependencies, limitations, performance considerations]

  Complexity: [SIMPLE|MEDIUM|COMPLEX]
  Time: [15m|30m|1h|2h]
  ```
```

## Validation

Before marking fleshed:
- Can someone else implement without questions?
- Are success criteria binary (pass/fail)?
- Are all discovered risks documented?
- Is the approach the simplest that works?
- Would Carmack start coding or keep thinking?

Remember: **A well-fleshed task is half-implemented. The other half is just typing.**
