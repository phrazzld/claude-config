---
description: Transform vague tasks into executable specifications with specific files, approach, and success criteria
---

# FLESH

Transform a skeletal TODO into an executable specification.

## Mission

Take a vague task and make it specific enough to execute without questions. Identify files, approach, patterns, and success criteria.

## Input

Read TODO.md to find the task that needs refinement (typically the next `[ ]` or `[~]` task).

Copy the task description verbatim. Note any existing work log or context.

## Analysis

**What does this task REALLY require?**
- Which specific files need changes? (use Grep to find them)
- What pattern exists in the codebase to follow? (use ast-grep/Grep)
- What are the hidden dependencies?
- What edge cases matter?
- What does "done" look like specifically?

## Context Gathering

**Quick tasks** (obvious scope):
- Grep for similar patterns in codebase
- Identify which files need changes
- Find existing implementations to follow

**Complex tasks** (unclear scope):
- Launch parallel research using Task tool:
  - Codebase analysis: ast-grep for patterns, Grep for utilities
  - External research: Use gemini/Exa for best practices if needed
  - Documentation: Find relevant API docs and examples
- Consider modularity: Can this be split into smaller tasks?
- Identify testing needs: What scenarios must work?

## Output

Update the task in TODO.md with specifics:

```markdown
- [ ] [Original task description]
  ```
  Files: file1.ts:45, file2.py:120
  Pattern: Follow existing implementation in Similar.tsx:30-50

  Approach:
  1. [Specific step with file location]
  2. [Specific step with file location]
  3. [Specific step with file location]

  Success criteria:
  - [Specific, testable outcome]
  - [Specific, testable outcome]

  Edge cases: [List if any]
  Dependencies: [List if any]
  ```
```

**Essential elements**:
- **Files**: Exact locations (file:line)
- **Pattern**: Reference to similar code
- **Approach**: Step-by-step with specifics
- **Success criteria**: Binary pass/fail conditions

**Optional** (add if relevant):
- Edge cases to handle
- Dependencies or blockers
- Testing strategy
- Performance considerations

## Validation

Task is ready when:
✅ Someone else could implement it without questions
✅ Success criteria are specific and testable
✅ File locations identified
✅ Approach is clear and simple

Then mark task as refined and return control to /execute.
