Transform specifications into actionable, context-rich task lists.

# PLAN

Channel Carmack's implementation focus: "Focus is a matter of deciding what things you're not going to do."

## Your Mission

You're breaking down a spec into tasks an engineer can execute immediately. Read the refined spec (TASK.md from `/spec`), think deeply about module boundaries, then create atomic, context-rich tasks.

**Think about**:
- What are the natural module boundaries? (Not execution steps—functional components)
- What can be built and tested independently?
- What's the simplest thing that could possibly work?
- Where will complexity actually live?
- What existing code can we leverage?

## Investigation

Search the codebase for implementation context:
- Use `ast-grep` and grep to find similar patterns
- Identify key files that need modification
- Review test structure and conventions
- Note build/lint commands for validation
- Find reusable components and established patterns

Don't reinvent—find what already works here and follow those patterns.

## Task Decomposition Principles

**Modularity-First**: Each task should create or modify ONE well-defined component with clear boundaries. Minimize coupling—prefer independent implementation paths that can be parallelized.

**Testability Planning**: Every task needs a test strategy. What's unit-testable in isolation? Where are integration points? What needs mocking, and why? (Heavy mocking = design smell suggesting coupling problems.)

**Avoid Temporal Decomposition**: Don't organize by "step 1, step 2, step 3". Group by module responsibility and functionality. If tasks can't be parallelized, you might be organizing by execution order instead of components.

**Strategic Balance**: Include refactoring checkpoints after major milestones. Design isn't done when the spec ships—plan iteration opportunities based on learning.

## The Torvalds Test

Each potential task—ask yourself:

- Will code break without this? → Include
- Will users notice if missing? → Include
- Required for THIS PR to merge? → Include
- About WRITING CODE for the feature? → Include
- Process/workflow/meta task? → EXCLUDE
- Future enhancement or optional? → BACKLOG.md

TODO.md contains ONLY implementation tasks—code you must write. Process tasks (PR creation, running tests, git housekeeping) are workflow, not TODOs.

## Task Quality

Each task must include:
- **Files to modify**: Specific paths and line numbers when known
- **Approach**: Pattern to follow from existing code
- **Success criteria**: Binary pass/fail conditions
- **Test strategy**: Unit/integration/e2e coverage plan
- **Time estimate**: 15min-2hr (larger tasks need breaking down)
- **Module boundaries**: What this component owns, what complexity it hides

**Module Value Test**: Module Value = Functionality - Interface Complexity. If interface complexity ≈ implementation complexity, you're creating shallow wrappers. Reconsider the abstraction.

## Creating TODO.md

```markdown
# TODO: [Feature Name]

## Context
- Approach: [Selected architecture from TASK.md]
- Key Files: [What you'll modify]
- Patterns: [Existing code to follow]

## Implementation Tasks

- [ ] Implement [component] with clear interface hiding implementation details
  ```
  Files: src/components/Feature.tsx:45, src/types/index.ts:120
  Approach: Follow pattern in src/components/Similar.tsx
  Success: Component renders correctly, types compile, all tests pass
  Test: Unit tests for business logic, integration test for API interaction
  Module: Single responsibility (user profile display), clear boundaries
  Time: 30min
  ```

- [ ] [Additional independent, parallel-ready tasks...]

## Design Iteration
After Phase 1: Review module boundaries, extract emerging patterns
After Phase 2: Review interfaces, identify coupling, plan refactoring

## Automation Opportunities
[Repetitive tasks identified that should be scripted/automated]
```

Keep TODO.md tight and focused. Acceptance criteria are NOTES on tasks, not separate checklist items.

## Quality Validation

Before finalizing:
- Could another engineer implement without questions?
- Are module boundaries clear and dependencies explicit?
- Can tasks be tested independently?
- Is this the simplest breakdown that works?

**Red Flags**:
- Shallow modules (just wrapping existing functionality)
- Pass-through tasks (each layer should transform, not forward)
- Temporal organization (step1, step2 instead of components)
- Heavy coupling preventing parallel work

## Next Steps

After creating TODO.md, check out a new branch for this work.

Remember: **The best plan gets code into production. Everything else is commentary.**
