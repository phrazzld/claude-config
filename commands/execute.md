---
description: Execute the next task from TODO.md with direct tactical focus
---

Execute the next task directly.

# EXECUTE

You're executing in a workflow that's successfully shipped 23 features this quarter with zero production incidents. The senior engineer reviewing your commits tomorrow values atomic changes, clear reasoning, and zero shortcuts. Every task you complete removes a blocker for 3 downstream developers. Channel Carmack: direct implementation, immediate refactoring, always shippable.

Grab next task → Implement → Commit → Mark complete

## Your Mission

Execute the next available task in TODO.md. The decision to work on this task has already been made during planning. Your job: carry it out skillfully.

## Process

**1. Find next task**: Read TODO.md, locate first `[~]` (in-progress) or `[ ]` (pending)

Batch tiny tasks (typo fix, rename, import): Execute consecutively, one commit.
Single substantial task: Execute it.

**2. Is task specific enough?**

Ask only: **"Do I know exactly what to do?"**

✅ Specific enough if task has:
- File locations OR clear scope
- Approach OR pattern to follow
- Success criteria

✅ YES → Proceed to step 3
🔍 NO → Run /flesh to make it specific, then proceed to step 3

**3. Mark in-progress**: Update `[ ]` → `[~]`

**4. Implement**

Read DESIGN.md for architectural guidance—the "how" is decided. Follow the module design, implement the pseudocode, match the interfaces. Your job: clean implementation of the planned architecture.

**Architecture blueprint** (from DESIGN.md):
- Module interfaces (match these exactly)
- Pseudocode algorithms (translate to real code)
- Data structures (use these types)
- Error handling strategy (follow this approach)
- Integration points (connect as specified)

**Apply principles while coding**:
- **Simplicity**: Prefer boring over clever. Aim for one-sentence explanations.
- **Maintainability**: Choose names that reveal purpose. Document "why" over "what".
- **Explicitness**: Make dependencies visible in signatures. Make side effects obvious from names.
- **Follow the blueprint**: Implement the architecture, don't redesign it.

**Check implementation quality**:
- Matches DESIGN.md? (Interface, behavior, error handling)
- Deep module? (Simple interface hiding powerful implementation)
- Information hiding intact? (Changing internals preserves caller code)
- Minimal complexity? (Few dependencies, clear behavior)
- Red flags absent? (Generic names, pass-through methods, temporal decomposition)

**5. Post-Implementation Simplicity Review**

Before committing, check for overcomplexity:

```
Task code-simplicity-reviewer("Review changes for simplification opportunities")
```

Review findings:
- **Trivial simplifications** (rename, extract small helper): Apply immediately
- **Substantial refactoring** (rethink approach): Add to task work log, address if time permits or note for future
- **No issues**: Proceed to commit

This enforces "leave code better than you found it" while context is fresh.

**6. Commit atomically**

Every completed task → atomic commit with clear message.
Types: feat|fix|docs|refactor|test|chore

**7. Mark complete**: Update `[~]` → `[x]`

**8. Continue or stop**: Proceed to next task when appropriate, or report completion.

## Execute Regardless Of

**Execute when task is specific, regardless of:**
- Task complexity (simple or complex)
- Time estimates (15 minutes or 3 hours)
- Session duration (first task or tenth task)
- Implementation challenge (straightforward or intricate)
- Task scope (focused or comprehensive)

**These concerns were addressed upstream**:
- Complexity → Handled in /plan (appropriate breakdown)
- Risk → Handled in /flesh (clear approach)
- Size → Handled in /plan (proper scoping)

**Valid reasons to pause**:
- ✅ Task blocked by missing dependency requiring user input
- ✅ Environment broken (build fails, tests unavailable, fundamental tool failure)
- ✅ Task remains unclear even after /flesh
- ✅ User explicitly requests pause

## The Contract

By the time you run /execute, the decision to do this work **has been made**. That decision happened during:
- `/plan` - Breaking work into appropriate tasks
- `/flesh` - Understanding scope and approach
- User running `/execute` - Choosing to proceed

**Your responsibility**: Carry out that decision skillfully.

**Your focus**: How to implement (quality, simplicity, maintainability), rather than whether to implement.

## Handling Complex Tasks

**Ineffective approach**: Refuse to execute due to perceived complexity.

**Effective approach**:
1. Task genuinely unclear → Run /flesh to clarify
2. Task clear but substantial → Execute it (this is the job)
3. Discover task merits splitting → Add work log noting this for future planning

**Key insight**: Complex tasks are normal in software engineering. Your role: handle them capably.

## Work Logs

For substantial tasks, document discoveries as you go:

```markdown
- [~] Implement user authentication
  ```
  Work Log:
  - Found auth pattern in services/auth.ts
  - Using JWT approach from api/middleware
  - Preserved existing session handling
  ```
```

Work logs capture discoveries, decisions, learnings for continuity.

## The Carmack Rule

**"A task without a commit is a task that's still pending."**

Every completed task results in an atomic commit. This is the definition of "done".

---

**Remember**: Execute is tactical. Strategic thinking happens upstream in plan/flesh. Your job: implement with quality, commit changes, mark complete. Repeat for next task.
