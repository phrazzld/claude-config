Execute the next available task from TODO.md.

# EXECUTE

Grab next task → Think deeply → Implement with principles → Commit atomically → Mark complete

## Process

**1. Find next task(s)**: Look for first `[~]` (in-progress) or `[ ]` (not started) in TODO.md
- **Batch tiny tasks**: Multiple bite-sized tasks (typo fix, rename, import update)? Execute consecutively, one semantic commit.
- **Single complex tasks**: Substantial tasks requiring thought? One at a time.

**2. Mark in-progress**: Update `[ ]` to `[~]` for tasks you're working on

**3. Think before acting**:
- What's the simplest solution that completely solves this?
- What existing patterns should I follow?
- Am I over-engineering this?

**4. Implement with principles**:

**Simplicity**: Boring > clever. Obvious > terse. If you can't explain it in one sentence, simplify.

**Maintainability**: Write for yourself in 6 months. Names based on purpose, not mechanism. Document the "why" behind decisions.

**Explicitness**: Dependencies visible in signatures, not hidden in globals. Behavior obvious from function signature. Side effects clear from naming (use verbs: update, delete, save).

**Fix Broken Windows**: See a problem (<2min fix)? Fix it now. Dead code, poor names, magic numbers—fix on sight. Technical debt compounds.

## Complexity Validation

Before finalizing implementation, check:

**Deep vs Shallow Module**: Am I creating value or just wrapping?
- Module Value = Functionality - Interface Complexity
- **Deep**: Simple interface hiding powerful implementation (e.g., Unix file I/O: open/read/write/close hides filesystem complexity)
- **Shallow**: Interface ≈ implementation (e.g., wrapper exposing most wrapped methods)
- If shallow, either simplify interface or merge with underlying module

**Information Leakage**: If I change implementation, does calling code break?
- **Leakage**: Returning raw DB rows forces callers to know schema
- **Pure**: Returning domain objects hides data structure
- Leakage couples modules—callers must understand internals

**Complexity Sources** (Complexity = Dependencies + Obscurity):
- **Dependencies**: Linkages between code. Does this add new module dependencies?
- **Obscurity**: Non-obvious information. Does this make behavior less clear?
- Both increase complexity—minimize aggressively

**Red Flags**:
- **Generic names** (Manager, Util, Helper, Context) → suggest unfocused responsibility
- **Pass-through methods** → only call another method with same signature. Each layer should transform.
- **Configuration overload** → dozens of parameters forcing implementation understanding. Provide defaults.
- **Temporal decomposition** → organizing by execution order (step1, step2) not functionality

**Strategic vs Tactical**: Am I just making it work (tactical) or also improving design (strategic)? Tactical gets it done but accumulates debt. Strategic invests 10-20% in making the system better. Aim for strategic.

**5. Commit atomically**:
- Every completed task → commit (no exceptions)
- Batched tiny tasks → one semantic commit
- `git add -p` or `git add [files]`, then `git commit -m "type: description"`
- Types: feat|fix|docs|refactor|test|chore

**6. Mark complete**: Update `[~]` → `[x]`

## The Carmack Rule

"A task without a commit is a task not done." Every completed task must result in an atomic commit.

## Work Logs

For complex tasks or discoveries, add work log under the task:

```markdown
- [~] Implement user authentication
  ```
  Work Log:
  - Found auth pattern in services/auth.ts
  - Need JWT approach from api/middleware
  - Blocked: clarify token expiry requirements
  ```
```

Work logs serve as scratchpad for discoveries, decisions made, blockers noted, memory for resumed tasks.

Remember: **Simplicity enables reliability. Every line of code is a liability.**
