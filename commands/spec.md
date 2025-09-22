Transform vague ideas into precise specifications through deep investigation and clarification.

# SPEC

Channel Dijkstra's precision: "The question of whether a computer can think is no more interesting than the question of whether a submarine can swim."

## The Dijkstra Principle

*"Simplicity is prerequisite for reliability."*

A specification isn't about what you want to build - it's about what must work.

## 1. Task Analysis & Deep Investigation

**What would Dijkstra specify?**
- Read @TASK.md with a critical eye
- Extract invariants that must hold
- Define preconditions and postconditions
- Identify edge cases before features

**Ultrathink: The Investigation Phase**
- What are the core problems we're actually solving?
- What are 3-5 fundamentally different approaches?
- What are the tradeoffs between simplicity and flexibility?
- Where are the natural system boundaries?
- What constraints are real vs. assumed?
- What would this look like if built from scratch today?
- What existing solutions can we learn from or build upon?

## 2. Parallel Research & Architecture Exploration

**Gather intelligence through comprehensive parallel research:**

```
Task 1: "Research current best practices for the task in TASK.md:
- Use gemini --prompt for industry patterns and 2025 standards
- Find proven architectural approaches and their tradeoffs
- Identify common failure modes and how to prevent them
- Security vulnerabilities and mitigation strategies
- Performance bottlenecks and optimization patterns
Focus on production-proven solutions with real-world validation."

Task 2: "Find relevant documentation using Context7 MCP:
- Resolve library IDs for potential technology choices
- Compare APIs and capabilities of alternative solutions
- Extract configuration patterns and best practices
- Note version constraints, breaking changes, and migration paths
- Identify ecosystem maturity and community support
Prioritize battle-tested libraries with strong documentation."

Task 3: "Explore alternative architectures and implementations:
- Use ast-grep to find similar patterns in the codebase
- Research competing approaches (monolith vs microservices, sync vs async, etc.)
- Evaluate different toolchains and build systems
- Consider data flow patterns (event-driven, request-response, streaming)
- Assess integration complexity with existing systems
Bring back 3-5 concrete alternatives with pros/cons."
```

## 3. Design Brainstorming & Evaluation

**Channel Thompson's simplicity while exploring alternatives:**

### Pattern Discovery
- Grep codebase for existing patterns we can leverage
- Find what already works and why
- Identify reusable components and abstractions
- Note architectural decisions we must respect

### Alternative Approaches (Generate 3-5)
For each approach, consider:
- **Approach Name**: Brief description
- **Complexity**: Implementation and maintenance burden
- **Performance**: Expected throughput, latency, resource usage
- **Scalability**: How it handles growth
- **Risk**: What could go wrong
- **Time**: Realistic implementation estimate

### Evaluation Matrix
| Approach | Simplicity | Performance | Maintainability | Risk | Time |
|----------|------------|-------------|-----------------|------|------|
| Option 1 | High/Med/Low | Score | Score | Score | Estimate |
| Option 2 | ... | ... | ... | ... | ... |

**Recommendation**: [Selected approach with justification based on Dijkstra's simplicity principle]

## 4. Clarifying Questions

**Generate concrete questions to refine the specification:**

### Critical Questions (Must answer before proceeding)
1. **Scale**: What's the expected load? (users, requests/sec, data volume)
2. **Constraints**: What are the hard limits? (budget, timeline, team size)
3. **Integration**: What systems must this work with? What are their APIs?
4. **Users**: Who exactly will use this? What's their technical level?
5. **Success**: How will we measure success? What metrics matter?

### Design Questions (Shape the architecture)
6. **Flexibility**: What needs to be configurable vs. hardcoded?
7. **Evolution**: What features are likely to be added in 6 months?

*Present these questions to the user and incorporate answers into the refined specification.*

## 5. Refined Specification Structure

**Update TASK.md with the refined specification:**

```markdown
# TASK
[Original task description preserved at top]

## Refined Specification

### Selected Approach
[Chosen architecture with justification]

### Requirements
#### Functional (What it MUST do)
- [ ] Invariant 1: [specific, testable]
- [ ] Invariant 2: [measurable outcome]

#### Non-Functional (How well it must do it)
- Performance: [specific metrics based on research]
- Security: [threat model from security analysis]
- Reliability: [failure modes and recovery]

### Constraints Discovered
- Technical: [existing system boundaries found]
- Resource: [realistic time/space limits]
- Integration: [API contracts, data formats]

### Implementation Strategy
#### Phase 1: Core Functionality
- Minimal viable solution
- Focus on critical path

#### Phase 2: Hardening
- Edge cases identified in research
- Error handling patterns
- Performance optimization opportunities

### Success Criteria
- [ ] All invariants hold
- [ ] Performance meets targets
- [ ] Security scan passes
- [ ] Integration tests pass

### Key Decisions
- [Decision 1]: [Rationale]
- [Decision 2]: [Rationale]

### Open Questions (if any remain)
- [Unresolved question needing user input]
```

## 6. Validation & Next Steps

**The Hoare Test: "There are two ways of constructing a software design: One way is to make it so simple that there are obviously no deficiencies."**

Validate the specification:
- Can this fail silently? → Document failure modes
- What happens at the boundaries? → Define edge cases
- Is this the simplest solution? → Justify complexity
- Would Dijkstra approve? → Ensure mathematical precision

**Next Command**: Run `/plan` to decompose this specification into actionable tasks

Remember: **A good specification is not when there is nothing left to add, but when there is nothing left to take away.**