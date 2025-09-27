Execute the next available task from TODO.md.

# EXECUTE

Grab next task from TODO.md → Think about approach → Do the work → Commit atomically → Mark complete

## PROCESS

1. **Find next task**: Look for first `[~]` (in-progress) or `[ ]` (not started) task in TODO.md
2. **Mark in-progress**: Update `[ ]` to `[~]`
3. **Think very hard before acting**:
   - Think very hard
   - Consider the approach and plan implementation
   - Look for existing patterns in the codebase to follow
   - Identify relevant files and implementation approach
   - **🎯 SIMPLICITY VALIDATION**: Ask "What's the simplest solution that completely solves this?"
     - Reject clever solutions in favor of boring, obvious ones
     - If you can't explain it to a junior dev, it's too complex
     - Prefer explicit over implicit behavior
4. **Do the work**: Implement what the task describes
   - **🎯 SIMPLICITY DURING IMPLEMENTATION**:
     - Choose boring technology over exciting alternatives
     - Write code that reads like documentation
     - Make the happy path obvious
     - Keep cyclomatic complexity low
5. **COMMIT ATOMICALLY**:
   - Every completed task gets a commit. No exceptions.
   - Stage relevant changes: `git add -p` or `git add [files]`
   - Write semantic commit message: `git commit -m "type: concise description"`
   - Types: `feat|fix|docs|style|refactor|test|chore`
6. **Mark complete**: Update `[~]` to `[x]` when done

## THE CARMACK RULE

*"A task without a commit is a task not done."*

Every completed task must result in an atomic commit. This isn't optional - it's fundamental to maintaining a clean, traceable history. If you can't commit it, the task isn't actually complete.

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


## 🎯 SIMPLICITY VALIDATION CHECKLIST

Before implementing any solution, validate against these simplicity criteria:

### The Simplicity Test
- **Can I explain this solution in one sentence?** If not, it's too complex.
- **Would a junior developer understand this immediately?** If not, simplify.
- **Am I solving problems that don't exist yet?** YAGNI - You Aren't Gonna Need It.
- **Is this the "boring" solution?** Boring is reliable. Clever is suspicious.

### Code Simplicity Metrics
- **Line count**: Can this be done in fewer lines without sacrificing clarity?
- **Cyclomatic complexity**: Are there too many decision points?
- **Dependencies**: Am I adding complexity through external dependencies?
- **Abstraction layers**: Am I creating unnecessary indirection?

### The Simplicity Reflex
When you find yourself:
- Writing a factory for a single type → **Stop**, use direct instantiation
- Creating an interface with one implementation → **Stop**, wait for the second use case
- Building a generic solution for a specific problem → **Stop**, solve the specific problem
- Adding configuration for values that never change → **Stop**, use constants

## NOTES

- Always think through the approach before diving into implementation
- If task includes context or detailed steps, follow them
- If blocked, mark as `[!]` with explanation in work log and move to next task
- Only preserve work logs that contain valuable context for future reference
- **ALWAYS commit changes after task completion** - no exceptions
- **ALWAYS validate simplicity** - complexity is the enemy of reliability
