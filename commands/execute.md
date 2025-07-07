Execute the next available task from @TODO.md with adaptive complexity and live progress logging.

# EXECUTE

Execute the next available task from @TODO.md with adaptive context gathering, dynamic reasoning allocation, and real-time progress logging.

## ACQUISITION

Select the next available task from @TODO.md queue:
1. Prioritize in-progress `[~]` tasks
2. Then grab next unblocked `[ ]` task
3. If all tasks completed, halt and say something witty

**Mark task as in-progress**: Immediately update `[ ]` to `[~]` in @TODO.md

## COMPLEXITY ASSESSMENT

Analyze the task to determine complexity level:

**SIMPLE** (0-2 files, straightforward changes):
- Bug fixes with clear solution
- Documentation updates
- Config changes
- Adding simple utility functions
- CSS/styling tweaks

**MEDIUM** (3-5 files, some integration):
- New features using existing patterns
- Refactoring within module boundaries
- Adding API endpoints
- Implementing UI components
- Test additions

**COMPLEX** (6+ files, cross-module impact):
- Architecture changes
- New subsystems
- Database schema changes
- Authentication/authorization changes
- Performance optimizations
- Third-party integrations

**VERY_COMPLEX** (system-wide impact):
- Breaking API changes
- Migration strategies
- Security implementations
- Distributed system changes
- Major refactoring across modules
- New architectural patterns

## DYNAMIC REASONING ALLOCATION

Based on complexity assessment:

**SIMPLE**: Direct execution
- No explicit thinking required
- Just implement the straightforward solution

**MEDIUM**: Think mode
- Think through the approach
- Consider edge cases
- Plan implementation steps

**COMPLEX**: Think hard mode
- Think hard!
- Deep analysis of implications
- Evaluate multiple approaches
- Consider long-term maintainability
- Identify potential risks

**VERY_COMPLEX**: Ultrathink mode
- Ultrathink
- Comprehensive architectural analysis
- Break down into subtasks
- Research best practices extensively
- Consider creating additional TODO items

## CONTEXT GATHERING

**For SIMPLE tasks**:
- Quick scan of relevant files
- Check existing patterns

**For MEDIUM tasks**:
- Read related code thoroughly
- `gemini --prompt "best practices for [specific task]"`
- Check existing similar implementations

**For COMPLEX tasks**:
- Read leyline philosophy docs
- Analyze codebase architecture
- Use Context7 MCP for framework documentation
- Search for similar patterns in codebase

**For VERY_COMPLEX tasks**:
- Launch parallel research agents:
  ```
  Task 1: "Research industry best practices for [domain]"
  Task 2: "Analyze all affected systems and dependencies"
  Task 3: "Investigate potential security implications"
  Task 4: "Evaluate performance and scalability impacts"
  ```
- Consider `thinktank` consultation
- Deep-dive into all related documentation

## LIVE PROGRESS LOGGING

Update @TODO.md in real-time with structured logs:

```markdown
## Task: [Description] [~]
### Complexity: MEDIUM
### Started: 2024-01-15 10:23

### Context Discovery
- Relevant files: user.service.ts:45, auth.middleware.ts:23
- Existing pattern: All API endpoints use validateRequest middleware
- Similar implementation: profile.controller.ts:updateAvatar()

### Execution Log
[10:25] Analyzing existing upload patterns
[10:30] Implementing multipart form handler
[10:35] Hit issue: CORS policy blocking uploads
[10:36] Solution: Adding upload endpoint to CORS whitelist
[10:45] Implementation complete, writing tests

### Approach Decisions
- Chose multipart over base64 for better performance
- Reused existing multer config from documents module
- Added file type validation at middleware level

### Learnings
- All file uploads must use server-side validation
- CORS config in config/cors.ts needs explicit endpoints
```

## IMPLEMENTATION

Execute based on complexity:

**SIMPLE**:
- Direct implementation
- Update TODO.md on completion

**MEDIUM**:
- Implement solution
- Test key scenarios
- Log approach decisions

**COMPLEX**:
- Implement incrementally
- Validate assumptions at checkpoints
- Log all significant decisions and discoveries
- Create follow-up tasks if needed

**VERY_COMPLEX**:
- Break into subtasks in TODO.md
- Implement most critical/risky parts first
- Extensive logging of decisions and rationale
- Regular progress updates
- Consider creating PLAN.md for very large changes

## ERROR HANDLING

If blocked or encountering issues:
1. Log the blocker with timestamp in TODO.md
2. Document attempted solutions
3. If truly blocked, mark task as blocked `[!]` with explanation
4. Move to next task or seek clarification

## COMPLETION

Upon task completion:
1. Update final execution log with summary
2. Document key learnings that should inform future work
3. Mark task as complete `[x]` in @TODO.md
4. If learnings are significant, consider running `/docs-sync` to update project documentation
