Convert a fully-specified TASK.md into actionable TODO.md items with clear success criteria.

# PLAN

Read the enhanced TASK.md file (containing detailed requirements, constraints, architecture decisions, and implementation strategy) and generate a comprehensive TODO.md with prioritized, actionable tasks.

## 1. Read Enhanced TASK.md

**Input expectations**:
- TASK.md should contain:
  - Task description and objectives
  - Requirements and constraints
  - Architecture decisions and technology choices
  - Implementation strategy and approach
  - Acceptance criteria
  - Performance and security considerations
  - Risk analysis and mitigation strategies

## 2. Analyze Task Components

Break down the task into logical components:
- **Core functionality** - Essential features for MVP
- **Integration points** - APIs, services, database connections
- **UI/UX elements** - User-facing components and flows
- **Infrastructure** - Setup, configuration, deployment needs
- **Testing requirements** - Unit, integration, E2E test needs
- **Documentation needs** - API docs, user guides, README updates

## 3. Generate Prioritized TODO Items

**CRITICAL**: Only include actionable items needed for the current work in TODO.md.
Future enhancements and nice-to-haves go in BACKLOG.md (see section below).

Create TODO.md with the following structure:

```markdown
# [Project/Feature Name] Implementation TODO

Generated from TASK.md on [timestamp]

## Critical Path Items (Must complete in order)
- [ ] [Task 1] - [Clear description]
  - Success criteria: [Specific, measurable outcome]
  - Dependencies: [What must exist first]
  - Estimated complexity: [SIMPLE/MEDIUM/COMPLEX]
  
- [ ] [Task 2] - [Clear description]
  - Success criteria: [Specific, measurable outcome]
  - Dependencies: [Task 1]
  - Estimated complexity: [level]

## Parallel Work Streams

### Stream A: [Component Name]
- [ ] [Task A1] - [Description]
  - Success criteria: [Outcome]
  - Can start: Immediately
  
- [ ] [Task A2] - [Description]
  - Success criteria: [Outcome]
  - Dependencies: [Task A1]

### Stream B: [Different Component]
- [ ] [Task B1] - [Description]
  - Success criteria: [Outcome]
  - Can start: After [Critical Path Item X]

## Testing & Validation
- [ ] Write unit tests for [component]
  - Success criteria: 90%+ coverage, all tests passing
  
- [ ] Integration tests for [feature]
  - Success criteria: All API endpoints tested with success/error cases
  
- [ ] E2E test for [user flow]
  - Success criteria: Complete user journey works without errors

## Documentation & Cleanup
- [ ] Update API documentation
  - Success criteria: All new endpoints documented with examples
  
- [ ] Update README with [feature] usage
  - Success criteria: Clear examples and configuration options
  
- [ ] Code review and refactoring pass
  - Success criteria: No linting errors, follows project conventions

## Future Enhancements (Write to BACKLOG.md, NOT TODO.md)

**The Torvalds Test**: "If it's not needed for this PR to work, it's not a TODO."

Write these to BACKLOG.md, never TODO.md:
- [ ] [Enhancement 1] - [Nice-to-have feature]
- [ ] [Enhancement 2] - [Optimization for later]
- [ ] [Enhancement 3] - [Future improvement]

<!-- CRITICAL: These items must go in BACKLOG.md. TODO.md is for immediate work only. -->
```

## 4. Task Attributes

Each task should include:
- **Clear action verb** (Implement, Create, Update, Refactor, Fix, Add, Remove)
- **Specific scope** (which files, components, or systems)
- **Measurable success criteria** (tests pass, feature works, performance target met)
- **Dependencies** (what must be done first)
- **Complexity estimate** (helps execute.md allocate appropriate reasoning)

## 5. Task Decomposition & Complexity Assessment

### Task Analysis (Native Subagent)
Invoke `task-decomposer` to break down the task and assess complexity:
- Analyze TASK.md for major components and phases
- Break down into atomic, actionable tasks
- Identify dependencies and create valid execution DAG
- Estimate complexity based on past patterns from knowledge.md
- Identify parallelization opportunities
- Define clear success criteria for each task
- Learn from estimate accuracy for continuous improvement

**How to invoke**: Use Task tool with subagent_type: "general-purpose" and prompt to act as task-decomposer from /Users/phaedrus/.claude/agents/task-decomposer.md

**Process**:
1. Send TASK.md content to task-decomposer
2. Get decomposed tasks with complexity estimates
3. Review critical path and parallel work streams
4. Enrich tasks based on complexity level
5. Update knowledge.md with estimation lessons learned after completion

The task-decomposer will provide:
- Critical path items that must be done in order
- Parallel work streams that can proceed independently
- Complexity estimates (SIMPLE/MEDIUM/COMPLEX/VERY_COMPLEX)
- Success criteria for each task
- Risk mitigation tasks where needed
- Confidence level based on similar past projects

## 6. Validation Checklist

Before finalizing TODO.md:
- [ ] All acceptance criteria from TASK.md are covered
- [ ] Dependencies form a valid DAG (no circular dependencies)
- [ ] Each task is atomic and can be completed independently
- [ ] Success criteria are specific and testable
- [ ] Critical path is clearly identified
- [ ] Parallel work opportunities are maximized
- [ ] Risk mitigation tasks are included where needed

## 7. Output Format

Generate TODO.md with:
- Clear section headers
- Consistent task formatting
- Priority indicators (Critical Path vs Parallel)
- Complexity estimates for execute.md
- Dependencies clearly stated
- Success criteria that can be verified

## Example Task Breakdown

From TASK.md requirement: "Add user authentication with OAuth2"

Generates TODO items:
```markdown
## Critical Path Items
- [ ] Set up OAuth2 provider configuration
  - Success criteria: Environment variables configured, provider responds to test request
  - Dependencies: None
  - Estimated complexity: SIMPLE

- [ ] Implement OAuth2 callback handler
  - Success criteria: Successfully exchanges code for tokens, stores user session
  - Dependencies: OAuth2 provider configuration
  - Estimated complexity: MEDIUM

- [ ] Add authentication middleware
  - Success criteria: Protected routes return 401 when unauthenticated
  - Dependencies: OAuth2 callback handler
  - Estimated complexity: MEDIUM

## Parallel Work Streams

### Stream A: Frontend Auth Flow
- [ ] Create login button component
  - Success criteria: Clicking redirects to OAuth provider
  - Can start: Immediately
  
- [ ] Add user profile display
  - Success criteria: Shows logged-in user's name and avatar
  - Dependencies: Auth middleware working
```

