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

Before finalizing implementation, run these checks:

**Deep vs Shallow Module**: Am I creating a deep module (simple interface, powerful implementation) or a shallow wrapper? If interface complexity ≈ implementation complexity, reconsider the abstraction. Module Value = Functionality - Interface Complexity.

**Information Leakage Test**: If I change this module's implementation, will calling code break? If yes, implementation details are leaking through the interface. Example: returning raw database rows forces callers to know your data structure.

**Dependencies vs Obscurity**: Does this change add new dependencies between components? Does it make behavior less obvious? Both increase complexity (Complexity = Dependencies + Obscurity). Can I avoid them?

**Avoid Red Flags**:
- **Generic names** (`Manager`, `Util`, `Helper`, `Context`) suggest unfocused responsibility and become dumping grounds
- **Pass-through methods** that only call another method with same signature indicate shallow abstractions - each layer should change abstraction level
- **Configuration overload** - exposing dozens of parameters forces users to understand implementation. Provide sensible defaults.
- **Temporal decomposition** - organizing code by execution order rather than functionality creates change amplification

**Strategic Investment**: Am I just getting it working (tactical) or also improving the design (strategic)? Aim for 10-20% time on making the system better, not just completing the feature. Tactical programming creates complexity that compounds. Strategic programming pays design dividends.

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

**Test:** Can you explain it in one sentence? Would a junior understand immediately?
**Avoid:** YAGNI violations, clever solutions, factories for single types, interfaces with one implementation
**Remember:** Simplicity enables reliability. Every line of code is a liability.

## Maintainability Guidelines

**Test:** Would you be frustrated modifying this in six months?
**Principles:** Code announces intent, functions understandable without full system knowledge, obvious extension points
**Naming:** Based on purpose not mechanism, avoid generic names, be specific
**Organization:** Group by feature, keep related code together, explicit dependencies

## 🎯 FIX BROKEN WINDOWS

**Philosophy:** Fix quality issues immediately (<2 min). Technical debt compounds.
**Fix on sight:** Dead code, unused imports, poor names, magic numbers, duplication, long functions
**Quality indicators:** Old TODOs, inconsistent style, skipped tests, empty error handlers, debug statements
**Boy Scout Rule:** Leave files better than you found them

## 🎯 EXPLICIT OVER IMPLICIT

**Behavior:** Dependencies visible in signatures, clear inputs/outputs, no magic
**Principles:** Prefer pure functions, use verbs for side effects (update/delete/save), pass dependencies explicitly
**Checklist:** Inputs visible, return types clear, side effects obvious, behavior understandable from signature

## 🎯 BINDING VALIDATION

**Technology-Specific:**
- TypeScript: Strong typing, avoid 'any', clear interfaces, strict null checks
- React: Validate props, follow hooks rules, pure components, consistent state management
- Go: Explicit errors, context propagation, interface segregation, prefer composition
- Database: Foreign keys, indexes, NOT NULL constraints, consistent naming

**Architecture:** Component isolation, single responsibilities, no circular dependencies, testable in isolation, backward-compatible interfaces, dependencies point inward

**Process:** Identify file type → Apply relevant constraints → Validate compliance → Fix violations immediately

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
