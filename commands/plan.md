Transform specifications into highly actionable, context-rich task lists. Channel Carmack's implementation focus.

# PLAN

Channel dual energy - Torvalds' pragmatism: "Talk is cheap. Show me the code." meets Carmack's depth: "Focus is a matter of deciding what things you're not going to do."

## The Implementation Principle

*"The difference between a plan and wishful thinking is specificity."*

Every TODO must be atomic, context-rich, and immediately executable.

## Strategic Programming Mindset

*"Working code isn't enough - invest 10-20% in design that pays compound interest."*

Balance tactical execution with strategic design:
- **Tactical Debt**: Note shortcuts taken for speed, plan paydown in later iterations. Recognize when you're trading implementation speed for design quality.
- **Module Depth**: Build deep modules (simple interfaces, powerful implementations) not shallow wrappers. Value = Functionality - Interface Complexity. If interface complexity ≈ implementation complexity, you've created a shallow, low-value abstraction.
- **Avoid Temporal Decomposition**: Group by functionality/module boundaries, not execution order. If your task list reads like sequential steps in a process, reorganize by component responsibility.
- **Design for Abstractions**: Each layer should change abstraction level, avoid pass-through methods that just call another method with the same signature.

## 1. Deep Task Analysis with Tenet Integration

**Read the refined specification:**
- Read @TASK.md (should contain refined spec from /spec command)
- Extract the selected approach and key decisions
- Note all constraints and dependencies discovered
- Identify the critical path to working software

**Ultrathink with Tenet Focus:**
- Ultrathink
- What's the simplest thing that could possibly work?
- **Modularity**: What are the natural module boundaries? How can we build independent, focused components with clear boundaries?
- **Design Never Done**: What assumptions might change? Where should we plan for iteration and refactoring?
- **Testability**: How can each component be tested in isolation? What are the testing seams?
- **Automation**: What repetitive tasks will emerge? What processes should be automated from the start?
- Where will the complexity actually live?
- What can be built in parallel vs. what must be sequential?
- What existing code can I leverage vs. what needs creation?
- Where are the performance bottlenecks likely to be?
- What will be hardest to change later if we get it wrong?

## 2. Context Gathering

**Investigate the codebase for implementation context:**

Use appropriate search tools to find similar patterns and existing functionality in the codebase. Identify key files related to your task. Review test patterns to understand the testing conventions. Look for examples that can guide your implementation approach.

**Gather intelligence about:**
- Existing patterns to follow
- Key files that need modification
- Test structure and requirements
- Build/lint commands to validate changes
- Dependencies and their versions

## 2.5. Leyline Binding Compliance Analysis

**Identify applicable bindings based on file types and technologies:**
- Analyze files to be modified/created for technology stack
- Reference relevant leyline bindings from /spec command binding preview
- Plan for binding compliance validation in each task
- Note specific binding requirements that affect task design

**Key Binding Categories to Consider:**
- **Core Bindings**: hex-domain-purity, automated-quality-gates, code-size
- **Technology-Specific**: Based on detected languages/frameworks
- **Architecture Bindings**: component-isolation, interface-contracts, dependency-inversion

## 3. Tenet-Driven Task Decomposition

**The Enhanced Carmack Method with Tenet Integration:**

Break down into atomic, context-rich, tenet-compliant tasks:
- Each task = one focused change with clear module boundaries
- Each task includes: files to modify, success criteria, estimated time, test strategy
- Implementation approach spelled out with testability considerations
- No task bigger than 2 hours (prefer 15-30 min tasks)
- Dependencies explicitly stated and minimized

**Modularity Decomposition Principles:**
- Each task should create or modify a single, well-defined component
- Minimize coupling between tasks - prefer independent implementation paths
- Design clear interfaces between components before implementation
- Ensure each component can be developed and tested in isolation

**Testability Planning Requirements:**
- Each task must include test strategy (unit/integration/e2e)
- Identify test setup requirements and mock boundaries
- Plan for test data and environment needs
- Design components for easy testing isolation

**Design Never Done Integration:**
- Include refactoring checkpoints after major milestones
- Plan iteration opportunities based on learning
- Identify assumptions that might change and plan flexibility points
- Schedule design review tasks after implementation phases

**Automation Opportunity Detection:**
- Identify repetitive tasks that should be automated
- Plan automation of quality gates (tests, linting, validation)
- Consider build/deployment automation needs
- Note manual processes that could be scripted

**Apply The Enhanced Torvalds Test:**
1. Will the code break without this? → TODO
2. Will users notice if this is missing? → TODO
3. Is this required for THIS PR to merge? → TODO
4. Does this create good module boundaries? → TODO
5. Can this be tested independently? → TODO
6. Is this about WRITING CODE for the feature? → TODO
7. Is this a process/workflow/meta task? → EXCLUDE
8. Is this a "future enhancement" or "optional"? → BACKLOG.md
9. Everything else? → BACKLOG.md or EXCLUDE

**Examples:**
- "Implement user login API" → TODO ✅
- "Create pull request" → EXCLUDE ❌
- "Monitor production errors" → EXCLUDE ❌
- "Optional: Add dark mode" → BACKLOG.md ✅
- "Run test suite" → EXCLUDE (implied by workflow) ❌
- "Address review feedback" → EXCLUDE ❌

## 3.5. TODO.md Scope Discipline (Critical)

**The Implementation-Only Rule:**
TODO.md contains ONLY implementation tasks - code you must write to complete this feature.

**❌ NEVER Include:**
- Process tasks (PR creation, review responses, git housekeeping)
- Deployment/operations (staging deploys, monitoring, analytics)
- Quality gates (run tests, linting, bundle checks - these are implied by workflow)
- Future/optional work → Write to BACKLOG.md instead
- Pre-merge checklists (developer knows validation steps)

**✅ DO Include:**
- Writing/modifying code/components/modules
- Creating/updating tests for implementation
- Updating types, interfaces, schemas
- Code documentation (JSDoc, inline comments)

**Acceptance Criteria Format:**
```markdown
- [ ] Implement user authentication service
  ```
  Files: src/services/auth.service.ts
  Approach: Use JWT tokens, integrate with user repository
  Success: Authenticates valid users, rejects invalid credentials, tests pass
  Time: 45 minutes
  ```
```

**Note:** Acceptance criteria are NOTES on tasks, NOT separate `- [ ]` items.

**BACKLOG.md Generation:**
When identifying future enhancements or optional features:
1. Create/update BACKLOG.md with structure: Future Enhancements, Nice-to-Have Improvements, Technical Debt
2. Reference in TODO.md context: `**Future Work**: See BACKLOG.md for optional enhancements`

## 4. Create Tenet-Enhanced TODO.md

**The Tenet-Integrated Carmack Structure:**

```markdown
# TODO: [Feature Name]

## Context
- **Approach**: [Selected architecture from TASK.md]
- **Key Files**: [Primary files that will be modified]
- **Patterns**: [Existing patterns to follow]
- **Dependencies**: [What must exist before starting]

## Tenet Integration Plan
- **🎯 Modularity**: [Component boundaries and interfaces planned]
- **🎯 Testability**: [Overall test strategy - unit/integration/e2e coverage]
- **🎯 Design Evolution**: [Iteration points and refactoring opportunities identified]
- **🎯 Automation**: [Processes to automate, quality gates to implement]
- **🎯 Binding Compliance**: [Relevant leyline bindings to validate against]

## Phase 1: Core Implementation [2-4 hours]

- [ ] Implement [component/feature name]
  ```
  Files: src/components/Feature.tsx:45, src/types/index.ts:120

  🎯 MODULARITY: Single responsibility, clear interface, minimal dependencies
  🎯 TESTABILITY: Unit tests + integration tests, mock external dependencies
  🎯 BINDING COMPLIANCE: [List relevant bindings if applicable]

  Approach: Follow pattern in src/components/Similar.tsx
  Success: Component renders, types compile, tests pass
  Time: 30 minutes
  ```

- [ ] Additional implementation tasks following same format

## Phase 2: Integration & Polish [1-2 hours]

- [ ] Wire up API endpoints and add integration tests

## Phase 3: Design Iteration [Continuous]

🎯 **DESIGN NEVER DONE** - Schedule iteration checkpoints:
- After Phase 1: Review module boundaries, extract emerging patterns
- After Phase 2: Review interfaces, identify coupling issues, plan refactoring

🎯 **AUTOMATION** - Identify repetitive tasks to automate:
- Quality gates (binding compliance, test coverage, code metrics)
- Build/deployment processes
- Manual validation steps

## Quality Validation (Reference - Not TODO Tasks)

**Before commits:** Run tests, typecheck, lint, manual smoke test

**🎯 Tenet Compliance:**
- Modularity: Single responsibility, clear interfaces
- Testability: Components tested in isolation
- Design Evolution: Refactoring opportunities documented
- Automation: Quality gates automated
- Binding Compliance: Relevant bindings validated

**Metrics:** Coverage standards met, no circular dependencies, complexity within limits

---

## Next Steps After TODO.md Complete

1. Run `/execute` to start implementation
2. Use `/git-pr` when ready to create pull request
3. See BACKLOG.md for future enhancements (if created)

---

## BACKLOG.md Example (Optional)

*Future enhancements go in BACKLOG.md, NOT TODO.md*

```markdown
# BACKLOG: [Feature Name]

## Future Enhancements
- **Performance**: Caching, lazy loading, code splitting (effort: 1 day, priority: low)
- **Error Handling**: User-friendly errors, boundaries, retry logic (effort: 4h, priority: low)

## Nice-to-Have Improvements
- Loading states, keyboard shortcuts, accessibility

## Technical Debt Opportunities
- Refactor duplication, extract patterns, improve test coverage
```

## 5. Implementation Hints

**Before starting:** Verify first task is executable, all context available, success criteria binary, estimates realistic
**During:** Start with riskiest task, parallelize independent work, validate before moving on
**If blocked:** Create task for blocker, document requirements, move to parallel work

## The Implementation Laws

1. No file:line references = guesswork
2. No success criteria = wishful thinking
3. No context = forced re-research
4. Over 2 hours = hidden complexity
5. 🎯 No module boundaries = coupling debt
6. 🎯 No test strategy = testing pain later
7. 🎯 No iteration planning = perfect design assumption

## Quality Validation

**Carmack Test (per TODO):** Another dev can implement without questions, files/lines identified, approach clear, criteria testable, estimates realistic, 🎯 module boundaries defined, 🎯 test strategy comprehensive

**Torvalds Test (overall):** Ships TODAY, minimum that works, no premature optimization, 🎯 modular, 🎯 iteration planned

**Tenet Integration:** Each component independently developable/testable/deployable, testing seams clear, assumptions explicit, quality gates automated, bindings validated

## Next Steps

After creating TODO.md:
1. Run `/flesh` on complex tasks needing more detail
2. Run `/execute` to start implementation
3. Use `/debug` if you hit unexpected issues

Remember: **The best plan is one that gets code into production. Everything else is commentary.**

---
*For complete tenet definitions and vocabulary, see [docs/tenets.md](../docs/tenets.md)*
