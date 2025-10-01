Transform specifications into highly actionable, context-rich task lists. Channel Carmack's implementation focus.

# PLAN

Channel dual energy - Torvalds' pragmatism: "Talk is cheap. Show me the code." meets Carmack's depth: "Focus is a matter of deciding what things you're not going to do."

## The Implementation Principle

*"The difference between a plan and wishful thinking is specificity."*

Every TODO must be atomic, context-rich, and immediately executable.

## Strategic Programming Mindset

*"Working code isn't enough - invest 10-20% in design that pays compound interest."*

When planning, balance tactical execution with strategic design:

**Recognize Tactical Debt**: Identify tasks that are quick wins vs. tasks that invest in system design. Note when you're consciously taking shortcuts for speed. Plan strategic paydown of tactical debt in later iterations.

**Module Depth Planning**: Plan for deep modules - simple interfaces hiding powerful implementations. When breaking down tasks, ask: "Are we creating shallow wrappers or meaningful abstractions?"

**Avoid Temporal Decomposition**: Don't organize tasks by execution order alone. Group by functionality and module boundaries. If your task list reads like a script of sequential steps, you're doing it wrong.

**Design for Different Abstractions**: If you're creating layers, ensure each task changes the abstraction level. Watch for pass-through methods that add no semantic value.

See [docs/ousterhout-principles.md](../docs/ousterhout-principles.md) for tactical debt detection patterns and strategic planning guidance.

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

**❌ NEVER Include These in TODO.md:**

**Process/Workflow Tasks:**
- "Create Pull Request" - use `/git-pr` when ready
- "Address Review Feedback" - handle when it happens
- "Respond to comments" - not an implementation task
- "Request reviews" - part of PR process, not code work
- "Squash commits" - git housekeeping, not code work

**Deployment/Operations Tasks:**
- "Deploy to staging/production" - use CI/CD or separate deployment process
- "Monitor Sentry for errors" - ongoing operations, not implementation
- "Set up monitoring" - unless monitoring code is THE feature being built
- "Post-merge retrospective" - team process, not code task
- "Check analytics" - operations task, not implementation

**Quality Gate Tasks:**
- "Run tests" - implied by dev workflow, not a separate task
- "Run linting" - handled by CI/CD and pre-commit hooks
- "Check bundle size" - validation, not implementation
- "Verify TypeScript compilation" - quality check, not code work

**Future/Optional Work:**
- "Optional: [feature]" → Write to BACKLOG.md
- "Future Enhancement: [idea]" → Write to BACKLOG.md
- "Nice-to-have: [improvement]" → Write to BACKLOG.md
- Anything with "if time permits" → Write to BACKLOG.md

**Pre-Merge Checklists:**
- These are validation steps, not implementation tasks
- Developer knows to run quality checks before committing
- Don't clutter TODO.md with process reminders

**✅ DO Include in TODO.md:**
- Writing new code/components/modules
- Modifying existing code to add/change functionality
- Creating/updating tests for your implementation
- Updating types, interfaces, schemas
- Refactoring code directly related to the feature
- Adding/updating code documentation (JSDoc, inline comments)

**Acceptance Criteria Format:**
```markdown
- [ ] Implement user authentication service
  ```
  Files to modify:
  - src/services/auth.service.ts - Create new service

  Implementation approach:
  - Use JWT tokens following existing pattern
  - Integrate with existing user repository

  Success criteria:
  - Service successfully authenticates valid users
  - Invalid credentials return appropriate error
  - JWT tokens generated with correct claims
  - Integration tests pass

  Time estimate: 45 minutes
  ```
```

**Note:** Acceptance criteria are NOTES explaining what success looks like, NOT separate `- [ ]` tasks.

**BACKLOG.md Generation:**
When you identify future enhancements, optional features, or nice-to-have improvements:

1. Create/update BACKLOG.md with structure:
   ```markdown
   # BACKLOG: [Feature Name]

   ## Future Enhancements
   - [Optional feature 1]: [brief description, value, estimated effort]
   - [Optional feature 2]: [brief description, value, estimated effort]

   ## Nice-to-Have Improvements
   - [Improvement 1]: [brief description, impact]

   ## Technical Debt Opportunities
   - [Refactoring opportunity]: [benefit if addressed]
   ```

2. Reference BACKLOG.md in TODO.md context section:
   ```markdown
   ## Context
   - **Future Work**: See BACKLOG.md for optional enhancements
   ```

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

- [ ] Set up basic structure for [component]
  ```
  Files to modify:
  - src/components/Feature.tsx:45 - Add new component
  - src/types/index.ts:120 - Define interfaces

  🎯 MODULARITY: Component boundaries and interfaces
  - Clear single responsibility: [describe component purpose]
  - Interface: [define props/api clearly]
  - Dependencies: [minimal external dependencies listed]

  🎯 TESTABILITY: Test strategy for this task
  - Unit tests: [specific test files and scenarios]
  - Mock boundaries: [what external dependencies to mock]
  - Test data: [required test fixtures or data]

  Implementation approach:
  - Follow existing pattern from src/components/Similar.tsx
  - Use established error handling from utils/errors.ts

  Success criteria:
  - [ ] Component renders without errors
  - [ ] Types compile successfully
  - [ ] Basic smoke test passes
  - [ ] Unit tests written and passing
  - [ ] Binding compliance verified (if applicable)

  🎯 BINDING COMPLIANCE: [List relevant bindings to validate]
  Time estimate: 30 minutes
  ```

- [ ] Implement core business logic
  ```
  Files to modify:
  - src/services/feature.service.ts - New file
  - src/services/index.ts:10 - Export new service

  🎯 MODULARITY: Service boundaries and interfaces
  - Single responsibility: [business logic focus]
  - Interface: [clear service contract]
  - Dependencies: [external services/repositories needed]

  🎯 TESTABILITY: Test strategy for this task
  - Unit tests: [business logic test scenarios]
  - Integration tests: [service integration points]
  - Mock strategy: [repository/external service mocks]

  Implementation approach:
  - Implement using existing BaseService pattern
  - Add input validation using zod schemas
  - Handle errors with established error classes

  Success criteria:
  - [ ] All unit tests pass
  - [ ] No type errors
  - [ ] Handles edge cases (null, empty, invalid)
  - [ ] Integration tests pass
  - [ ] Binding compliance verified

  🎯 BINDING COMPLIANCE: [hex-domain-purity, input-validation-standards]
  Time estimate: 45 minutes
  Dependencies: Previous task must be complete
  ```

## Phase 2: Integration & Testing [1-2 hours]

- [ ] Wire up API endpoints
- [ ] Add comprehensive integration tests

## Phase 3: Design Iteration & Automation [Continuous]

🎯 **DESIGN NEVER DONE - Iteration Checkpoints:**
- [ ] **Iteration Checkpoint 1**: After Phase 1 - Review component boundaries and interfaces
  ```
  Questions to evaluate:
  - Are the module boundaries correct?
  - What did we learn that might change the design?
  - Are there emerging patterns we should extract?

  Time estimate: 15 minutes
  ```

- [ ] **Iteration Checkpoint 2**: After Phase 2 - Review integration patterns
  ```
  Questions to evaluate:
  - Are the interfaces working well together?
  - What coupling issues emerged?
  - What should we refactor before moving forward?

  Time estimate: 15 minutes
  ```

🎯 **AUTOMATION OPPORTUNITIES:**
- [ ] **Quality Gate Automation**: Set up automated validation
  ```
  Automation tasks:
  - [ ] Add binding compliance check to CI pipeline
  - [ ] Automate test coverage reporting
  - [ ] Set up automated code quality metrics

  Time estimate: 30 minutes
  ```

- [ ] **Process Automation**: Identify and automate repetitive tasks
  ```
  Repetitive tasks identified:
  - [List tasks that could be automated]
  - [Consider build/deployment automation]
  - [Document manual processes to automate]

  Time estimate: Variable based on identified opportunities
  ```

## Quality Validation (Reference - Not TODO Tasks)

**IMPORTANT:** These are validation steps you'll perform during development, NOT separate TODO items.

**Before Each Commit:**
- Run `npm test` - all tests pass
- Run `npm run typecheck` - no type errors
- Run `npm run lint` - no lint errors
- Manual smoke test of changes

**🎯 Tenet Compliance (Self-Check):**
- **Modularity**: Each component has single responsibility and clear interfaces
- **Testability**: All components can be tested in isolation
- **Design Evolution**: Refactoring opportunities identified and documented
- **Automation**: Quality gates automated where possible
- **Binding Compliance**: Relevant leyline bindings validated

**Quality Metrics (Monitor):**
- Test coverage meets project standards
- No circular dependencies introduced
- Component complexity within acceptable limits
- Performance benchmarks maintained

---

## Next Steps After TODO.md Complete

1. Run `/execute` to start implementation
2. Use `/git-pr` when ready to create pull request
3. See BACKLOG.md for future enhancements (if created)

---

## BACKLOG: Future Enhancements (Optional)

*This section is an EXAMPLE of what goes in BACKLOG.md, NOT in TODO.md*

```markdown
# BACKLOG: [Feature Name]

## Future Enhancements

### Optional: Performance Optimizations
- [ ] Add caching layer for frequently accessed data
- [ ] Implement lazy loading for heavy components
- [ ] Optimize bundle size with code splitting

**Estimated effort:** ~1 day | **Priority:** Low | **Value:** Medium

### Optional: Enhanced Error Handling
- [ ] Add user-friendly error messages
- [ ] Implement error boundary components
- [ ] Add retry logic for transient failures

**Estimated effort:** ~4 hours | **Priority:** Low | **Value:** Medium

## Nice-to-Have Improvements
- Better loading states with skeleton screens
- Keyboard shortcuts for power users
- Accessibility improvements (ARIA labels, keyboard navigation)

## Technical Debt Opportunities
- Refactor duplicated validation logic into shared utility
- Extract common patterns into reusable hooks
- Improve test coverage in edge case scenarios
```

*End of BACKLOG.md example - this goes in separate file, not TODO.md*
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

## The Tenet-Enhanced Implementation Laws

1. **A TODO without file:line references is guesswork**
2. **A TODO without success criteria is wishful thinking**
3. **A TODO without context forces re-research**
4. **A TODO over 2 hours hides complexity**
5. **🎯 A TODO without clear module boundaries creates coupling debt**
6. **🎯 A TODO without test strategy creates testing pain later**
7. **🎯 A TODO without iteration planning assumes perfect initial design**
8. **🎯 A TODO without automation consideration wastes human potential**
9. **🎯 A TODO without binding compliance creates technical debt**

## Tenet-Enhanced Quality Validation

**The Enhanced Carmack Test for each TODO:**
- Could another developer implement this without asking questions?
- Are the specific files and line numbers identified?
- Is the implementation approach crystal clear?
- Are success criteria objective and testable?
- Is the time estimate based on similar past work?
- **🎯 Are module boundaries and interfaces clearly defined?**
- **🎯 Is the test strategy comprehensive and realistic?**
- **🎯 Are binding compliance requirements identified?**

**The Enhanced Torvalds Test for the overall plan:**
- Will this ship working code TODAY?
- Is this the minimum that works?
- Did we avoid premature optimization?
- **🎯 Are components modular and independently testable?**
- **🎯 Are iteration and refactoring opportunities planned?**
- **🎯 Are repetitive processes identified for automation?**

**The Tenet Integration Validation:**
- **Modularity**: Can each component be developed, tested, and deployed independently?
- **Testability**: Is every component designed with testing seams and clear boundaries?
- **Design Evolution**: Are assumptions explicit and iteration points planned?
- **Automation**: Are quality gates and repetitive processes automated?
- **Binding Compliance**: Are relevant leyline bindings integrated into the plan?

## Next Steps

After creating TODO.md:
1. Run `/flesh` on complex tasks needing more detail
2. Run `/execute` to start implementation
3. Use `/debug` if you hit unexpected issues

Remember: **The best plan is one that gets code into production. Everything else is commentary.**

---
*For complete tenet definitions and vocabulary, see [docs/tenets.md](../docs/tenets.md)*
