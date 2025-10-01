Transform skeletal TODOs into executable specifications through deep analysis.

# FLESH

Channel Carmack: "Focus is a matter of deciding what things you're not going to do."

## The Carmack Principle

*"The difference between a TODO and a specification is understanding."*

A vague task hides complexity. Flesh it out before you code it out.

## 1. Find the Next Task

**Extract the skeleton**:
- Read TODO.md for first `[ ]` or `[~]` task
- Copy the task description verbatim
- Note any existing work log or context
- Ultrathink: What does this task REALLY require?

## 2. Deep Task Analysis

**The Three Questions**:
1. What must change? (scope)
2. What must not break? (constraints)
3. What could go wrong? (risks)

**Ultrathink about**:
- Ultrathink
- Hidden dependencies and assumptions
- Edge cases lurking in the shadows
- Performance implications at scale
- Security considerations
- Testing requirements

### Modular Task Analysis

**Evaluate Independence**: Can task be split into smaller, testable modules? What are natural boundaries?
**Key Questions**: Independently testable parts? Input/output boundaries? Parallel work? Required interfaces? Existing module integration?
**Optimize**: Minimize dependencies, define clear contracts, single responsibilities, avoid conflicts

### Testability Expansion

**Strategy**: Identify test scenarios (unit/integration/e2e), required mocks, test data
**Test Cases**: Happy path, edge cases, error conditions, performance benchmarks, security vulnerabilities
**Coverage**: Minimum requirements, critical paths, existing infrastructure reuse, setup/teardown needs

### Automation Opportunity Detection

**Identify Patterns**: Repetitive actions, code generation opportunities, boilerplate templates
**Candidates**: File operations, validation steps, reusable scripts, manual processes that slow development
**Investment**: Time to automate vs future savings, recurrence frequency, consistency/error reduction benefits

## 3. Parallel Research

**Launch three research agents simultaneously**:

```
Task 1: "Research best practices for [task description]:
- Use gemini --prompt for current industry patterns
- Find proven implementation approaches
- Identify common pitfalls and failure modes
- Security and performance considerations
Focus on production-ready solutions, not experiments."

Task 2: "Find relevant documentation for [task description]:
- Use Exa MCP to search for documentation and code examples
- Extract critical APIs and usage patterns
- Note version constraints and breaking changes
- Identify configuration requirements
Only include what's needed for THIS task."

Task 3: "Analyze codebase patterns for [task description]:
- Use ast-grep to find similar implementations
- Grep for existing utilities and helpers
- Identify conventions to follow
- Find reusable components
Don't reinvent what already exists here."
```

## 4. Flesh Out the TODO

**Expand the task with discovered intelligence**:

```markdown
- [ ] [Original task description]
  ```
  Implementation Approach:
  - [Step-by-step approach based on research]
  - [Key files to modify: file1.ts:45, file2.py:120]
  - [Patterns to follow from existing code]

  Modularity Analysis:
  - Components: [List of independent modules identified]
  - Interfaces: [Contracts between modules]
  - Can be parallelized: [Which parts can be done simultaneously]
  - Integration points: [How modules connect]

  Test Strategy:
  - Unit tests: [Specific functions/modules to test]
  - Integration tests: [Module interaction scenarios]
  - Edge cases: [Specific edge conditions to validate]
  - Test data: [Required test fixtures or mocks]
  - Coverage target: [Minimum coverage percentage]

  Automation Opportunities:
  - [Identified repetitive pattern that could be automated]
  - [Potential for code generation or templating]
  - [Manual process that could be scripted]

  Success Criteria:
  - [ ] [Specific, measurable outcome 1]
  - [ ] [Specific, measurable outcome 2]
  - [ ] Tests pass: [specify which tests]
  - [ ] Module boundaries maintained
  - [ ] Test coverage meets target

  Constraints & Risks:
  - [Discovered dependency or limitation]
  - [Potential breaking change to watch for]
  - [Performance consideration]

  Dependencies:
  - Requires: [what must exist first]
  - Blocks: [what can't proceed until this is done]

  Estimated Complexity: [SIMPLE|MEDIUM|COMPLEX]
  Estimated Time: [15m|30m|1h|2h|4h]
  ```
```

## 5. Validation Checklist

**Before marking the task as fleshed**:
- [ ] Can someone else implement this without asking questions?
- [ ] Are success criteria binary (pass/fail)?
- [ ] Are all discovered risks documented?
- [ ] Is the approach the simplest that works?
- [ ] Would Carmack start coding or keep thinking?

## Output

The same TODO item, but now with:
- Clear implementation roadmap
- Discovered constraints and dependencies
- Specific success criteria
- Realistic time estimate
- No surprises during execution

Remember: **A well-fleshed task is half-implemented. The other half is just typing.**
