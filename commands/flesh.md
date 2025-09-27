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

### 🎯 Modular Task Analysis

**Evaluate Task Independence**:
Analyze whether this task can be broken into smaller, independent modules. Consider if each component can be developed and tested in isolation. Identify natural boundaries where the task could be split. Check for coupling with other tasks - can this be completed without waiting for other work?

**Module Boundary Questions**:
- Can this task be divided into smaller, independently testable parts?
- What are the clear input/output boundaries?
- Which parts could be developed in parallel?
- What interfaces need to be defined between components?
- Are there existing modules this should integrate with cleanly?

**Independence Optimization**:
Structure the expanded task to minimize dependencies on other work. Define clear contracts between modules. Ensure each subtask has a single, well-defined responsibility. Create tasks that can be assigned to different developers without conflict.

### 🎯 Testability Expansion

**Test Strategy Development**:
For each task component, identify specific test scenarios that validate correctness. Consider unit tests for individual functions, integration tests for module interactions, and end-to-end tests for complete workflows. Define what mocks or stubs will be needed. Specify the test data required.

**Test Case Identification**:
- What are the happy path scenarios that must work?
- What edge cases could cause failures?
- What error conditions need to be handled?
- What performance benchmarks should be met?
- What security vulnerabilities need testing?

**Test Coverage Planning**:
Define minimum coverage requirements for the task. Identify critical paths that must have tests. Specify which parts can rely on existing test infrastructure. Note any special test setup or teardown requirements. Consider both positive and negative test cases.

### 🎯 Automation Opportunity Detection

**Identify Repetitive Patterns**:
Look for aspects of the task that involve repetitive actions. Consider whether any part of the implementation could be automated or generated. Check if similar tasks will need to be done in the future. Identify boilerplate code that could be templated.

**Automation Candidates**:
- Are there repetitive file operations or transformations?
- Could code generation reduce manual work?
- Are there validation or checking steps that could be automated?
- Would a script or tool make this task reusable?
- Are there manual processes that slow down development?

**Automation Investment Analysis**:
Evaluate whether the time to automate is worth the future time savings. Consider how often this pattern will recur. Assess the risk of automation versus manual implementation. Note if automation would improve consistency and reduce errors.

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
- Use Context7 MCP to resolve library IDs
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
