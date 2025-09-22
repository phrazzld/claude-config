Transform specifications into highly actionable, context-rich task lists. Channel Carmack's implementation focus.

# PLAN

Channel dual energy - Torvalds' pragmatism: "Talk is cheap. Show me the code." meets Carmack's depth: "Focus is a matter of deciding what things you're not going to do."

## The Implementation Principle

*"The difference between a plan and wishful thinking is specificity."*

Every TODO must be atomic, context-rich, and immediately executable.

## 1. Deep Task Analysis

**Read the refined specification:**
- Read @TASK.md (should contain refined spec from /spec command)
- Extract the selected approach and key decisions
- Note all constraints and dependencies discovered
- Identify the critical path to working software

**Ultrathink like Carmack:**
- What's the simplest thing that could possibly work?
- What are the natural implementation boundaries?
- Where will the complexity actually live?
- What can be built in parallel vs. what must be sequential?
- What existing code can I leverage vs. what needs creation?
- Where are the performance bottlenecks likely to be?
- What will be hardest to change later if we get it wrong?

## 2. Context Gathering

**Investigate the codebase for implementation context:**
```bash
# Find similar patterns
ast-grep --pattern 'relevant_pattern' .
grep -r "existing_functionality" --include="*.ts" --include="*.py"

# Identify key files
find . -name "*relevant*" -type f | head -20

# Check test patterns
grep -r "test\|spec" --include="*.test.*" --include="*.spec.*"
```

**Gather intelligence about:**
- Existing patterns to follow
- Key files that need modification
- Test structure and requirements
- Build/lint commands to validate changes
- Dependencies and their versions

## 3. Task Decomposition with Context

**The Carmack Method: Each task is a mini-specification**

Break down into atomic, context-rich tasks:
- Each task = one focused change
- Each task includes: files to modify, success criteria, estimated time
- Implementation approach spelled out
- No task bigger than 2 hours (prefer 15-30 min tasks)
- Dependencies explicitly stated

**Apply The Torvalds Test:**
1. Will the code break without this? → TODO
2. Will users notice if this is missing? → TODO
3. Is this required for THIS PR? → TODO
4. Everything else? → BACKLOG

## 4. Create Context-Rich TODO.md

**The Enhanced Carmack Structure:**

```markdown
# TODO: [Feature Name]

## Context
- **Approach**: [Selected architecture from TASK.md]
- **Key Files**: [Primary files that will be modified]
- **Patterns**: [Existing patterns to follow]
- **Dependencies**: [What must exist before starting]

## Phase 1: Core Implementation [2-4 hours]

- [ ] Set up basic structure for [component]
  ```
  Files to modify:
  - src/components/Feature.tsx:45 - Add new component
  - src/types/index.ts:120 - Define interfaces

  Implementation approach:
  - Follow existing pattern from src/components/Similar.tsx
  - Use established error handling from utils/errors.ts

  Success criteria:
  - [ ] Component renders without errors
  - [ ] Types compile successfully
  - [ ] Basic smoke test passes

  Time estimate: 30 minutes
  ```

- [ ] Implement core business logic
  ```
  Files to modify:
  - src/services/feature.service.ts - New file
  - src/services/index.ts:10 - Export new service

  Implementation approach:
  - Implement using existing BaseService pattern
  - Add input validation using zod schemas
  - Handle errors with established error classes

  Success criteria:
  - [ ] All unit tests pass
  - [ ] No type errors
  - [ ] Handles edge cases (null, empty, invalid)

  Time estimate: 45 minutes
  Dependencies: Previous task must be complete
  ```

## Phase 2: Integration & Testing [1-2 hours]

- [ ] Wire up API endpoints
  ```
  [Detailed implementation context...]
  ```

- [ ] Add comprehensive tests
  ```
  [Test scenarios and files...]
  ```

## Phase 3: Polish & Optimization [If time permits]

- [ ] Performance optimizations
- [ ] Additional error handling
- [ ] Documentation updates

## Validation Checklist
- [ ] Run `npm test` - all tests pass
- [ ] Run `npm run typecheck` - no type errors
- [ ] Run `npm run lint` - no lint errors
- [ ] Manual testing of happy path
- [ ] Manual testing of error cases
```

## 5. Implementation Hints

**Before starting, verify:**
- Can I execute the first task right now?
- Do I have all the context needed?
- Are success criteria binary (pass/fail)?
- Is the time estimate realistic?

**During implementation:**
- Start with the riskiest/most uncertain task
- Parallelize independent tasks
- Validate each task before moving on
- Update estimates based on actual time

**If blocked:**
- Create a new task for the blocker
- Document what's needed to unblock
- Move to parallel tasks if possible

## The Implementation Laws

1. **A TODO without file:line references is guesswork**
2. **A TODO without success criteria is wishful thinking**
3. **A TODO without context forces re-research**
4. **A TODO over 2 hours hides complexity**

## Quality Validation

**The Carmack Test for each TODO:**
- Could another developer implement this without asking questions?
- Are the specific files and line numbers identified?
- Is the implementation approach crystal clear?
- Are success criteria objective and testable?
- Is the time estimate based on similar past work?

**The Torvalds Test for the overall plan:**
- Will this ship working code TODAY?
- Is this the minimum that works?
- Did we avoid premature optimization?

## Next Steps

After creating TODO.md:
1. Run `/flesh` on complex tasks needing more detail
2. Run `/execute` to start implementation
3. Use `/debug` if you hit unexpected issues

Remember: **The best plan is one that gets code into production. Everything else is commentary.**