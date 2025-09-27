Transform specifications into highly actionable, context-rich task lists. Channel Carmack's implementation focus.

# PLAN

Channel dual energy - Torvalds' pragmatism: "Talk is cheap. Show me the code." meets Carmack's depth: "Focus is a matter of deciding what things you're not going to do."

## The Implementation Principle

*"The difference between a plan and wishful thinking is specificity."*

Every TODO must be atomic, context-rich, and immediately executable.

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
3. Is this required for THIS PR? → TODO
4. Does this create good module boundaries? → TODO
5. Can this be tested independently? → TODO
6. Everything else? → BACKLOG

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

## Phase 4: Polish & Long-term Design [If time permits]

- [ ] Performance optimizations
- [ ] Additional error handling
- [ ] Documentation updates

## Tenet-Enhanced Validation Checklist

**Code Quality Gates:**
- [ ] Run `npm test` - all tests pass
- [ ] Run `npm run typecheck` - no type errors
- [ ] Run `npm run lint` - no lint errors
- [ ] Manual testing of happy path
- [ ] Manual testing of error cases

**🎯 Tenet Compliance Validation:**
- [ ] **Modularity**: Each component has single responsibility and clear interfaces
- [ ] **Testability**: All components can be tested in isolation
- [ ] **Design Evolution**: Refactoring opportunities identified and documented
- [ ] **Automation**: Quality gates automated where possible
- [ ] **Binding Compliance**: Relevant leyline bindings validated

**Quality Metrics:**
- [ ] Test coverage meets project standards
- [ ] No circular dependencies introduced
- [ ] Component complexity within acceptable limits
- [ ] Performance benchmarks maintained
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
