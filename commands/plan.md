---
description: Transform DESIGN.md specs into atomic implementation tasks in TODO.md
---

# PLAN

> **STEVE JOBS REALITY FIELD**
> - Think Different: challenge the decomposition the PRD implies—seek better boundaries.
> - Obsess Over Details: each task names files, success criteria, tests.
> - Plan Like Da Vinci: visualize the whole system before listing tasks.
> - Craft, Don't Code: TODO entries should read like inevitable next moves.
> - Iterate Relentlessly: rewrite tasks until they sing.
> - Simplify Ruthlessly: TODO.md only contains code that must exist.

Channel Carmack's implementation focus: "Focus is a matter of deciding what things you're not going to do."

## Your Mission

You're breaking down DESIGN.md (from `/architect`) into atomic implementation tasks. The architecture is decided—module boundaries defined, interfaces specified, pseudocode written. Your job: translate concrete design into executable chunks an engineer can implement immediately.

If there is no DESIGN.md file, use the TASK.md file instead.

**The architecture tells you**:
- Module boundaries and responsibilities (already decided)
- File organization (where code lives)
- Interfaces and data structures (what to implement)
- Pseudocode (how algorithms work)
- Integration points (what to connect)

**Your job**: Create one task per module/component that implements the designed architecture.

## Investigation

Read DESIGN.md thoroughly:
- What modules are defined? (Each becomes one or more tasks)
- What's the file organization? (Tasks reference specific files)
- What pseudocode exists? (Tasks implement these algorithms)
- What integration points exist? (Tasks for database, APIs, etc.)
- What's the testing strategy? (Tasks include test requirements)
- **Infrastructure design**: Does DESIGN.md include quality gates, logging, error tracking, design tokens, or changelog setup? (These become setup tasks)

Search the codebase for implementation patterns:
- Use `ast-grep` and grep to find similar patterns
- Identify reusable components and established conventions
- Review test structure and naming conventions
- Note build/lint commands for validation

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
- Architecture: [Reference to DESIGN.md - selected approach]
- Key Files: [From DESIGN.md file organization]
- Patterns: [Existing code to follow]

## Infrastructure Tasks (if DESIGN.md includes infrastructure)

**Quality Gates**:
- [ ] Configure Lefthook (lefthook.yml)
  ```
  Files: lefthook.yml (new), .github/workflows/ci.yml (new)
  Architecture: Pre-commit hooks for linting/formatting, pre-push for tests
  Pseudocode: See DESIGN.md Infrastructure Design - Quality Gates
  Success: Hooks prevent bad commits, CI runs on PRs
  Test: git commit with bad code → blocked, git push with failing tests → blocked
  Dependencies: None (first task - enables quality for all other tasks)
  Time: 30min
  ```

**Structured Logging** (if included in DESIGN.md):
- [ ] Setup Pino logger with correlation IDs and redaction
  ```
  Files: utils/logger.ts (new)
  Architecture: Centralized logger with structured JSON, request correlation
  Pseudocode: See DESIGN.md Infrastructure Design - Structured Logging
  Success: Logger available, sensitive data redacted, correlation IDs working
  Test: Log password field → redacted, child logger includes requestId
  Dependencies: None
  Time: 30min
  ```

**Error Tracking** (if included in DESIGN.md):
- [ ] Configure Sentry with source maps and release tracking
  ```
  Files: utils/sentry.ts (new), next.config.js (modify)
  Architecture: Automatic error capture, sensitive data redaction
  Pseudocode: See DESIGN.md Infrastructure Design - Error Tracking
  Success: Errors sent to Sentry, source maps uploaded, sensitive data redacted
  Test: Throw error → appears in Sentry with source map, auth tokens not logged
  Dependencies: None
  Time: 45min
  ```

**Design System** (if included in DESIGN.md):
- [ ] Setup Tailwind 4 with @theme directive and design tokens
  ```
  Files: app/globals.css (modify), tailwind.config.ts (remove - CSS-first approach)
  Architecture: Design tokens in CSS using @theme, OKLCH colors
  Pseudocode: See DESIGN.md Infrastructure Design - Design System
  Success: Design tokens available in CSS, colors use OKLCH, typography scales defined
  Test: Use --color-primary in component → resolves to OKLCH value
  Dependencies: None
  Time: 30min
  ```

**Changelog Automation** (if included in DESIGN.md):
- [ ] Setup Changesets or semantic-release for version management
  ```
  Files: .changeset/config.json (new) OR .releaserc.js (new), .github/workflows/release.yml (new)
  Architecture: Automated version bumping and changelog generation
  Pseudocode: See DESIGN.md Infrastructure Design - Changelog Automation
  Success: Changesets create version PRs OR semantic-release auto-publishes
  Test: Create changeset → Version Packages PR created, conventional commit → version bumped
  Dependencies: None
  Time: 45min
  ```

## Implementation Tasks

- [ ] Implement [ModuleName] matching DESIGN.md specification
  ```
  Files: [From DESIGN.md file organization]
  Architecture: Implements [Module] interface from DESIGN.md
  Pseudocode: See DESIGN.md section [X.Y]
  Success: Interface matches design, pseudocode logic implemented, tests pass
  Test: [From DESIGN.md testing strategy]
  Dependencies: [From DESIGN.md module dependencies]
  Time: [estimate]
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
- **Infrastructure tasks included**: If DESIGN.md has infrastructure design, are setup tasks for quality gates, logging, error tracking, design tokens, and changelog included?

**Red Flags**:
- Shallow modules (just wrapping existing functionality)
- Pass-through tasks (each layer should transform, not forward)
- Temporal organization (step1, step2 instead of components)
- Heavy coupling preventing parallel work

## Grug Complexity Review

Before finalizing TODO.md, invoke Grug to check for complexity demon:

```bash
Task grug("Review plan for complexity demon. Check for over-abstraction, unnecessary layers, premature patterns")
```

**Grug checks for**:
- **Abstraction too early**: Interface before have two concrete use?
- **Too many layer**: Eight layer to change one value?
- **Big brain pattern**: Enterprise pattern when simple code work?
- **Microservices where not needed**: Split small app for no reason?
- **Framework overkill**: Complex framework when simple solution exist?

**Grug wisdom applied**:
- If task need create AbstractFactoryManager → probably complexity demon
- If can't explain to junior grug → probably too complex
- If more interface than implementation → shallow module, bad
- If "temporary" but permanent feel → remove or make real

**Common complexity demons Grug find in plans**:
```markdown
❌ Grug worry:
- [ ] Create AbstractUserFactory interface
- [ ] Implement UserFactoryManager
- [ ] Build dependency injection container
- [ ] Set up service locator pattern

✅ Grug prefer:
- [ ] Implement createUser() function
  (if need second way create user later, THEN abstract. not before)
```

**Review outcomes**:
- **Grug say "complexity demon here"**: Simplify plan before proceed
- **Grug say "look ok but watch"**: Note potential issues for /groom
- **Grug say "grug approve, make work"**: Proceed to implementation

**Integration with Ousterhout principles**:
- Grug detects over-abstraction (early warning)
- Ousterhout provides fix (design deep modules)
- Both want: simple interface, powerful implementation
- Difference: Grug says "not yet", Ousterhout says "do right"

## Next Steps

After creating TODO.md, check out a new branch for this work.

Remember: **The best plan gets code into production. Everything else is commentary.**
