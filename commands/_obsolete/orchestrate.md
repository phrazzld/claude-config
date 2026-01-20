---
description: Orchestrate parallel task execution with dynamically-defined agents
---

Analyze TODO.md, spawn ad-hoc agents for parallelizable tasks, synthesize results.

# ORCHESTRATE

You're the engineering manager. Your team: dynamically-defined agents scoped to specific tasks. Your job: analyze dependencies, identify parallelization opportunities, delegate intelligently, synthesize results.

**Key distinction from /execute**: Execute handles one task sequentially. Orchestrate spawns multiple agents to work in parallel, then integrates their output.

## Intent

- Analyze TODO.md for parallelizable vs sequential tasks
- Group independent tasks into execution waves
- Define scoped ad-hoc agents for each task
- Execute waves in parallel
- Synthesize results with conflict resolution

## Your Approach

### 1. Analyze TODO.md

**Parse structure:**
- Extract all pending tasks (`[ ]` and `[~]`)
- Identify file scope per task (explicit or inferred)
- Map dependencies (explicit `Dependencies:` fields + inferred from shared files)

**Build dependency graph:**
- Nodes = tasks
- Edges = dependencies (explicit + implicit)
- Implicit dependency: tasks sharing files, interface producer→consumer

**Parallelization heuristics:**

| Safe to Parallelize | Must Sequence |
|---------------------|---------------|
| Different modules/directories | Same-file modifications |
| No file overlap | Database migrations |
| Infrastructure setup | Interface definition → implementation |
| Independent test suites | Setup → dependent features |

### 2. Plan Parallel Waves

Group tasks into waves:
- **Wave 1**: All tasks with no dependencies
- **Wave N**: Tasks whose dependencies completed in Wave N-1

**Risk assessment per wave:**
- File overlap within wave = conflict risk (flag it)
- Interface dependencies across waves = timing risk
- External dependencies = blocker risk

**Present plan to user:**

```
## Orchestration Plan

Analyzed TODO.md: [N] tasks

### Wave Breakdown
Wave 1 (parallel): [Task list] - no dependencies
Wave 2 (parallel): [Task list] - depends on Wave 1
Wave 3: [Task] - depends on Wave 2

### Risk Assessment
- [Task X + Y share file Z] - medium conflict risk
- [Task A depends on interface from Task B] - ensure B completes first

### Estimate
Sequential: ~[X] time
Orchestrated: ~[Y] time ([Z]% faster)

Proceed with orchestration? [y/n/customize]
```

Wait for user approval before spawning agents.

### 3. Define Ad-hoc Agents

For each task, dynamically create a scoped agent. **Do not use pre-defined agents** - define them based on task specifics.

**Agent prompt template:**

```markdown
You are implementing a specific task from a larger feature.

## Your Task
[Task description from TODO.md]

## Scope
Files to modify: [explicit file list from task]
Patterns to follow: [relevant patterns from codebase]

## Constraints
- ONLY modify files listed in your scope
- Follow existing patterns in the codebase
- Include tests that validate success criteria
- Commit atomically when complete with clear message
- If blocked by something outside your scope, document it but do NOT attempt to fix

## Success Criteria
[From TODO.md task block]

## Context
[Relevant architecture context from DESIGN.md or TODO.md header]
```

**Optional persona injection:**
- Database/migration task → "Channel data-integrity mindset"
- Test task → "Channel TDD discipline"
- Performance task → "Channel performance-first thinking"

### 4. Execute Waves

**Per wave**, spawn all agents in a single message for true parallelism:

```
Task implement-task-1("[scoped prompt for task 1]")
Task implement-task-2("[scoped prompt for task 2]")
Task implement-task-3("[scoped prompt for task 3]")
```

**During execution:**
- Monitor for completion/blockers
- If one agent fails, others continue (collect partial results)
- Collect commits and completion status from each

**Wave completion:**
- Wait for all wave agents to complete (or timeout)
- Collect results before proceeding to next wave
- Note any blockers for synthesis

### 5. Synthesize Results

**Collection phase:**
- Gather commits from all agents
- Collect completion status (done / blocked / failed)
- Gather blocker descriptions

**Integration phase:**
- Review commits in wave order
- Run validation: `pnpm typecheck && pnpm lint && pnpm test`
- Identify any conflicts

**Conflict resolution:**

| Type | Resolution |
|------|------------|
| Lint/format issues | Auto-fix |
| Type errors | Identify source, suggest fix |
| Test failures | Run in isolation to identify which agent's change broke |
| Merge conflicts | Present to user |

**Generate synthesis report:**

```
## Orchestration Complete

### Summary
Agents spawned: [N]
Completed: [N] | Blocked: [N] | Failed: [N]

### Commits Created
1. [hash] - [description] (task-1)
2. [hash] - [description] (task-2)
...

### Integration Status
- TypeScript: [Pass/Fail]
- Tests: [N/N passing]
- Lint: [Clean/Issues]

### Blockers Reported
- Task-X: "[blocker description]"

### Next Steps
[Specific actions for unresolved items]
```

## When NOT to Orchestrate

**Use /execute instead when:**
- Only 1-2 tasks remaining (overhead not worth it)
- All tasks have linear dependencies (no parallelization benefit)
- Tasks are tightly coupled to same files
- Quick tactical execution needed

**Orchestrate shines when:**
- 3+ independent tasks can run in parallel
- Feature spans multiple modules/directories
- Clear separation of concerns in task list
- Time savings justify coordination overhead

## Conflict Prevention

**Narrow agent scopes:**
- Each agent gets explicit file list
- Agents instructed to NOT modify files outside scope
- Blockers documented rather than fixed across boundaries

**Interface-first ordering:**
- If Task B needs interface from Task A, ensure A runs in earlier wave
- Or: have A define interface only, B implements consumer

**Trust-based isolation:**
- Agents work in same directory (no worktrees)
- Trust instructions to stay in scope
- Simpler than filesystem isolation, faster setup

## Example Workflow

**TODO.md:**
```markdown
# TODO: User Authentication

## Tasks
- [ ] Create User model and migration
  Files: prisma/schema.prisma, prisma/migrations/*

- [ ] Implement JWT token service
  Files: lib/jwt.ts, lib/jwt.test.ts

- [ ] Create login endpoint
  Files: api/auth/login.ts, api/auth/login.test.ts
  Dependencies: User model, JWT service

- [ ] Create registration endpoint
  Files: api/auth/register.ts, api/auth/register.test.ts
  Dependencies: User model

- [ ] Build LoginForm component
  Files: components/Auth/LoginForm.tsx
  Dependencies: Login endpoint
```

**Analysis:**
- Tasks 1, 2: No dependencies → Wave 1
- Tasks 3, 4: Depend on Wave 1 → Wave 2
- Task 5: Depends on Task 3 → Wave 3

**Orchestration plan:**
```
Wave 1 (parallel): User model, JWT service
Wave 2 (parallel): Login endpoint, Registration endpoint
Wave 3: LoginForm component

Time: 5 sequential → 3 waves (~40% faster)
```

**Execution:**
```
# Wave 1
Task implement-user-model("[prompt with schema.prisma scope]")
Task implement-jwt-service("[prompt with lib/jwt.ts scope]")

# [Wait for completion]

# Wave 2
Task implement-login-endpoint("[prompt with api/auth/login.ts scope]")
Task implement-registration("[prompt with api/auth/register.ts scope]")

# [Wait for completion]

# Wave 3
Task implement-login-form("[prompt with LoginForm scope]")
```

**Synthesis:**
- 5 commits created
- All tests pass
- No conflicts
- Feature complete

## Your Output

**Before execution:**
- Dependency graph analysis
- Wave breakdown with estimates
- Risk assessment
- User approval prompt

**During execution:**
- Progress per wave
- Blocker alerts

**After execution:**
- Synthesis report
- Integration status
- Next steps for any blockers

---

## Related Commands

- `/execute` - Single task execution (use when parallelization overhead not worth it)
- `/plan` - Create TODO.md from DESIGN.md (upstream of orchestrate)
- `/groom` - Backlog analysis with pre-defined agents (different purpose)
