Execute the next available task from TODO.md.

# EXECUTE

Grab next task from TODO.md → Think about approach → Do the work → Commit atomically → Mark complete

## PROCESS

1. **Find next task(s)**: Look for first `[~]` (in-progress) or `[ ]` (not started) task in TODO.md
   - **Batch bite-sized tasks**: If multiple tasks are tiny and narrowly scoped (e.g., rename variable, fix typo, update import), execute them consecutively without returning to TODO.md between each one
   - **Single complex tasks**: For substantial tasks requiring thought and planning, execute one at a time

2. **Mark in-progress**: Update `[ ]` to `[~]` for all tasks you're about to work on
3. **Think deeply before acting**:
   - Consider the approach carefully and plan your implementation
   - Look for existing patterns in the codebase to follow
   - Identify relevant files and the best implementation approach
   - Ask yourself: "What's the simplest solution that completely solves this?"
   - Validate that you're not over-engineering the solution

4. **Do the work with principled implementation**:
   - **Simplicity**: Prefer the simplest solution that solves the problem completely. Choose boring, proven solutions over clever abstractions.
   - **Maintainability**: Write for the developer who will modify this in six months. Name things clearly based on purpose.
   - **Fix Issues Immediately**: When you see a problem, fix it now rather than deferring. Remove dead code, improve naming, correct formatting issues.
   - **Be Explicit**: Make dependencies visible, avoid hidden state, ensure behavior is obvious from function signatures.
   - **Follow Technology Standards**: Apply the appropriate patterns and best practices for the language and framework you're using.
5. **COMMIT ATOMICALLY**:
   - **For single tasks**: Every completed task gets a commit. No exceptions.
   - **For batched bite-sized tasks**: Group related tiny changes into one semantic commit (e.g., multiple typo fixes → one "fix: correct typos" commit)
   - Stage relevant changes: `git add -p` or `git add [files]`
   - Write semantic commit message: `git commit -m "type: concise description"`
   - Types: `feat|fix|docs|style|refactor|test|chore`
6. **Mark complete**: Update `[~]` to `[x]` for all completed tasks

## THE CARMACK RULE

*"A task without a commit is a task not done."*

Every completed task must result in an atomic commit. This isn't optional - it's fundamental to maintaining a clean, traceable history. If you can't commit it, the task isn't actually complete.

## COMPLEXITY & MODULE CHECKS

Before finalizing implementation, run these Ousterhout-inspired checks:

**Deep vs Shallow Module**: Am I creating a deep module (simple interface, powerful implementation) or a shallow wrapper? If interface complexity ≈ implementation complexity, reconsider the abstraction.

**Information Leakage Test**: If I change this module's implementation, will calling code break? If yes, implementation details are leaking through the interface.

**Dependencies vs Obscurity**: Does this change add new dependencies between components? Does it make behavior less obvious? Both increase complexity - can I avoid them?

**Avoid Red Flags**:
- Generic names (`Manager`, `Util`, `Helper`, `Context`) suggest unfocused responsibility
- Pass-through methods that add no semantic value indicate shallow abstractions
- Exposing configuration parameters that force users to understand implementation

**Strategic Investment**: Am I just getting it working (tactical) or also improving the design (strategic)? Aim for 10-20% time on making the system better, not just completing the feature.

See [docs/ousterhout-principles.md](../docs/ousterhout-principles.md) for detailed red flag examples and remediation patterns.

## WORK LOG

For complex tasks or when discovering important context, add a work log entry directly under the task in TODO.md:

```markdown
- [~] Implement user authentication
  ```
  Work Log:
  - Found existing auth pattern in services/auth.ts
  - Need to follow JWT token approach from api/middleware
  - Database schema already has user table, just needs session table
  - Blocked by: need to clarify token expiry requirements
  ```
```

This work log serves as:
- Scratchpad for discoveries and context
- Record of decisions made
- Place to note blockers or questions
- Memory for if task is resumed later


## Simplicity Validation

Before implementing any solution, think hard about simplicity.

### The Simplicity Test
Ask yourself whether the solution can be explained in one sentence. Consider if a junior developer would understand it immediately. Avoid solving problems that don't exist yet - remember YAGNI (You Aren't Gonna Need It). Choose boring, reliable solutions over clever ones.

### Watch For Complexity Creep
Be alert when you're tempted to write factories for single types, create interfaces with only one implementation, build generic solutions for specific problems, or add configuration for values that never change. These are signs you're overengineering.

Remember: Simplicity is prerequisite for reliability. Every line of code is a liability - only keep the ones that pay rent.

## Maintainability Guidelines

Code is read far more often than it's written. Optimize for the reader, not the writer.

### The Future Developer Test
Consider what would frustrate you if you had to modify this code in six months. Write code that your future self will thank you for.

### Maintainability Principles
Ensure code clearly announces its intent rather than requiring deduction. Make it possible to understand a function without understanding the entire system. Create obvious extension points where future changes are likely. Follow consistent patterns throughout the codebase.

### Naming and Organization
Name functions and variables based on what they do, not how they work. Avoid generic names like "processData" or "helper" - be specific about the actual purpose. Group code by feature rather than by file type. Keep related code together, including tests near their implementations. Make all dependencies explicit and visible.

## 🎯 FIX BROKEN WINDOWS

*"One broken window, left unrepaired, leads to more broken windows."* - The Broken Windows Theory

### The Fix-It-Now Philosophy
While implementing any task, immediately fix small quality issues you encounter. Don't defer or document them for later - if it takes less than two minutes, fix it now. Technical debt compounds quickly.

### Code Smells to Fix On Sight
Remove commented-out code blocks, unreachable code, and unused imports. Rename poorly named variables, functions, and classes. Extract magic numbers to named constants. Eliminate code duplication. Break up functions that are too long to understand at a glance. Refactor deeply nested logic.

### Quality Erosion Indicators
Be alert for old TODO comments, inconsistent code style within files, skipped or commented tests, empty error handlers, and debug statements in production code. These are signs that code quality is degrading.

### The Boy Scout Rule
Leave every file better than you found it, even if you didn't create the original issues. Fix formatting, update stale comments, improve variable names, and simplify unnecessarily complex code as you work.

## 🎯 EXPLICIT OVER IMPLICIT

*"Explicit is better than implicit."* - The Zen of Python

### Making Behavior Obvious
Ensure all dependencies are visible in function signatures rather than hidden in global state or singletons. Make it clear what a function needs and what it produces. Avoid magic - if something affects a function's behavior, it should be passed as a parameter.

### Transparent Behavior Principles
Prefer pure functions that return consistent output for the same input. When functions must have side effects, make those effects obvious through clear naming - use verbs like "update", "delete", or "save" to signal state changes. Pass dependencies explicitly rather than reaching out to fetch them from the environment.

### The Explicit Checklist
Before completing any code, verify that all inputs are visible, return types are clear, side effects are obvious from naming, and someone could understand the behavior without reading the implementation. Make the implicit explicit.

## 🎯 BINDING VALIDATION

*"Architecture is about the important stuff. Whatever that is."* - Ralph Johnson

### Technology-Specific Validation
During implementation, ensure code follows the idiomatic patterns and best practices for its technology stack.

For TypeScript files, use strong typing and avoid 'any' without justification. Ensure interfaces define clear contracts and enable strict null checks.

For React components, validate props properly, follow hooks rules, keep components pure, and maintain consistent state management patterns.

For Go code, handle all errors explicitly, propagate context in APIs, follow interface segregation principles, and prefer composition over inheritance.

For database schemas, define foreign key constraints, add indexes for queried columns, prefer NOT NULL constraints, and follow consistent naming conventions.

### Architecture Principles
Maintain component isolation with single responsibilities and clear boundaries. Avoid circular dependencies and ensure components are testable in isolation.

Preserve interface contracts by maintaining backward compatibility, documenting version changes, and avoiding breaking changes without proper versioning.

Follow clean architecture dependency rules - dependencies should point inward, domain logic shouldn't depend on infrastructure, and the UI shouldn't directly access the data layer.

### Validation Process
Identify the type of file being worked on and apply the relevant technology and architecture constraints. Generate code that follows these binding requirements, then validate that the output meets all applicable standards. Immediately fix any violations found rather than deferring them.

## NOTES

- Always think through the approach before diving into implementation
- **Batch execution**: When you see a cluster of tiny, narrowly-scoped tasks (rename, typo fix, import update), execute them all in sequence
- If task includes context or detailed steps, follow them
- If blocked, mark as `[!]` with explanation in work log and move to next task
- Only preserve work logs that contain valuable context for future reference
- **ALWAYS commit changes after task completion** - no exceptions (batch tiny tasks into one semantic commit)
- **ALWAYS validate simplicity** - complexity is the enemy of reliability

---
*For complete tenet definitions and vocabulary, see [docs/tenets.md](../docs/tenets.md)*
