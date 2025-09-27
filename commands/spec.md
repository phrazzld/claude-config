Transform vague ideas into precise specifications through deep investigation and clarification.

# SPEC

Channel Dijkstra's precision: "The question of whether a computer can think is no more interesting than the question of whether a submarine can swim."

## The Dijkstra Principle

*"Simplicity is prerequisite for reliability."*

A specification isn't about what you want to build - it's about what must work.

## State Detection

**Check TASK.md to determine current state:**
- If `## Refined Specification` exists → Specification complete
- If `## Clarifying Questions` exists with answers → Continue with Phase 2
- If `## Clarifying Questions` exists without answers → Waiting for user input
- Otherwise → Start Phase 1

---

# PHASE 1: INVESTIGATION & CLARIFICATION

## 1. Task Analysis & Deep Investigation

**What would Dijkstra specify?**
- Read TASK.md with a critical eye
- Extract invariants that must hold
- Define preconditions and postconditions
- Identify edge cases before features

**Ultrathink: The Investigation Phase**
- Ultrathink
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
🎯 **SIMPLICITY TENET**: Prefer the simplest design that solves the problem completely.
🎯 **PRODUCT VALUE FIRST**: Every approach must justify existence through demonstrable user value.
🎯 **EXPLICIT OVER IMPLICIT**: Surface and document all assumptions, dependencies, and constraints.
For each approach, explicitly identify: dependencies on existing systems, assumptions about environment/users/scale, constraints and limitations, integration requirements, and potential side effects on other systems.
Evaluate each approach against user/business outcomes - reject technically interesting but low-value solutions.
Focus on production-proven solutions with real-world validation and clear user benefits."

Task 2: "Find relevant documentation using Context7 MCP:
- Resolve library IDs for potential technology choices
- Compare APIs and capabilities of alternative solutions
- Extract configuration patterns and best practices
- Note version constraints, breaking changes, and migration paths
- Identify ecosystem maturity and community support
🎯 **SIMPLICITY TENET**: Prefer the simplest design that solves the problem completely.
🎯 **PRODUCT VALUE FIRST**: Every technology choice must serve demonstrable user value.
🎯 **EXPLICIT OVER IMPLICIT**: Surface and document all assumptions, dependencies, and constraints.
For each technology choice, explicitly document: runtime dependencies, configuration requirements, assumptions about infrastructure/environment, integration constraints, breaking change risks, and compatibility requirements.
Evaluate libraries based on user benefits they enable, not feature richness or technical novelty.
Prioritize battle-tested libraries that directly support user-valuable functionality."

Task 3: "Explore alternative architectures and implementations:
- Use ast-grep to find similar patterns in the codebase
- Research competing approaches (monolith vs microservices, sync vs async, etc.)
- Evaluate different toolchains and build systems
- Consider data flow patterns (event-driven, request-response, streaming)
- Assess integration complexity with existing systems
🎯 **SIMPLICITY TENET**: Prefer the simplest design that solves the problem completely.
🎯 **PRODUCT VALUE FIRST**: Every architectural choice must demonstrate clear user value.
🎯 **EXPLICIT OVER IMPLICIT**: Surface and document all assumptions, dependencies, and constraints.
For each architecture, explicitly identify: existing system dependencies, data flow contracts, deployment assumptions, scalability constraints, team skill requirements, and operational complexity implications.
Question whether complex patterns serve users or just engineering preferences.
Bring back 3-5 concrete alternatives with pros/cons and clear user value propositions."
```

## 3. Leyline Binding Preview

**Identify relevant leyline bindings for implementation guidance:**

### Technology Detection & Binding Mapping
- Analyze TASK.md and current branch context for technology indicators
- Detect file types, frameworks, and languages that will be modified/created
- Map detected technologies to relevant leyline binding categories

### Applicable Leyline Bindings
Based on detected technologies, reference relevant bindings:

**Core Bindings (Always Applicable)**:
- [hex-domain-purity](../bindings/core/hex-domain-purity.md): Keep business logic pure and infrastructure-free
- [api-design](../bindings/core/api-design.md): Explicit component contracts and interfaces
- [automated-quality-gates](../bindings/core/automated-quality-gates.md): Prevent quality degradation through automation
- [code-size](../bindings/core/code-size.md): Small, focused files with clear responsibilities

**Technology-Specific Bindings** (Include based on detection):
- **TypeScript**: [no-any](../bindings/categories/typescript/no-any.md), [modern-typescript-toolchain](../bindings/categories/typescript/modern-typescript-toolchain.md)
- **React**: [react-framework-selection](../bindings/categories/react/react-framework-selection.md), [server-first-architecture](../bindings/categories/react/server-first-architecture.md)
- **Database**: [data-validation-at-boundaries](../bindings/categories/database/data-validation-at-boundaries.md), [migration-management-strategy](../bindings/categories/database/migration-management-strategy.md)
- **API**: [rest-api-standards](../bindings/categories/api/rest-api-standards.md), [api-versioning-strategy](../bindings/categories/api/api-versioning-strategy.md)
- **Security**: [input-validation-standards](../bindings/categories/security/input-validation-standards.md), [secrets-management-practices](../bindings/categories/security/secrets-management-practices.md)

### Binding Compliance Notes
- Consider these bindings during architecture selection
- Include binding compliance as evaluation criteria
- Plan for binding validation during implementation phase

## 4. Design Brainstorming & Evaluation

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
🎯 **SIMPLICITY TENET**: Prefer the simplest design that solves the problem completely.
🎯 **PRODUCT VALUE FIRST**: Every approach must justify existence through demonstrable user value.
🎯 **EXPLICIT OVER IMPLICIT**: Surface and document all assumptions, dependencies, and constraints.

| Approach | **User Value** | **Simplicity** | **Explicitness** | Performance | Maintainability | Risk | Time |
|----------|----------------|----------------|------------------|-------------|-----------------|------|------|
| Option 1 | High/Med/Low + user benefits | High/Med/Low + reasoning | High/Med/Low + details | Score | Score | Score | Estimate |
| Option 2 | High/Med/Low + user benefits | High/Med/Low + reasoning | High/Med/Low + details | ... | ... | ... | ... |

**User Value Evaluation Criteria** (Primary):
- **High**: Clear, measurable user benefits; solves real user problems; enables valuable user outcomes
- **Medium**: Indirect user benefits; improves user experience through infrastructure/performance gains
- **Low**: Technical improvement without clear user impact; serves engineering preferences over user needs

**Simplicity Evaluation Criteria**:
- **High**: Obvious design, minimal moving parts, clear mental model
- **Medium**: Some abstraction needed, manageable complexity
- **Low**: Multiple complex interactions, non-obvious behavior

**Explicitness Evaluation Criteria**:
- **High**: All dependencies, assumptions, and constraints clearly documented; no hidden behavior
- **Medium**: Most dependencies visible; some assumptions need clarification
- **Low**: Hidden dependencies, unstated assumptions, or unclear integration contracts

### Tenet Decision Matrix

**Structured decision framework prioritizing fundamental principles:**

| Decision Factor | Weight | Criteria | Decision Rule |
|----------------|--------|----------|---------------|
| **User Value** | 40% | Does this solve real user problems? | Reject if user value is unclear or theoretical |
| **Simplicity** | 30% | Is this the simplest viable solution? | Prefer obvious designs over clever alternatives |
| **Explicitness** | 20% | Are dependencies and assumptions clear? | Reject approaches with hidden complexity |
| **Implementation Risk** | 10% | What could realistically go wrong? | Prefer proven patterns over experimental approaches |

**Decision Algorithm**:
1. **User Value Filter**: Eliminate any approach that doesn't clearly benefit users
2. **Simplicity Preference**: Among valuable approaches, prefer simpler solutions
3. **Explicitness Check**: Ensure all dependencies and assumptions are documented
4. **Risk Assessment**: Consider implementation complexity and team capabilities

**Recommendation**: [Selected approach with justification using tenet decision matrix - prioritize user value, simplicity, and explicitness while managing implementation risk]

## 5. Clarifying Questions Generation

**Generate concrete questions to refine the specification:**

### Critical Questions (Must answer before proceeding)
1. **Scale**: What's the expected load? (users, requests/sec, data volume)
2. **Constraints**: What are the hard limits? (budget, timeline, team size)
3. **Integration**: What systems must this work with? What are their APIs?
4. **Users**: Who exactly will use this? What's their technical level?
5. **Success**: How will we measure success? What metrics matter?
6. **User Value**: What specific user problems does this solve? How will users' lives be better?
7. **Business Impact**: What business outcomes justify this investment? How do we measure ROI?

### Design Questions (Shape the architecture)
8. **Flexibility**: What needs to be configurable vs. hardcoded?
9. **Evolution**: What features are likely to be added in 6 months?
10. **[Add 1-3 context-specific questions based on research findings]**

## 6. Update TASK.md with Investigation & Questions

**Append findings and questions to TASK.md:**
```markdown
## Investigation Summary
- [Key finding 1 from research]
- [Key finding 2 from research]
- [Architecture tradeoffs discovered]
- [Existing patterns that could be leveraged]
- [Constraints identified]

## Clarifying Questions
Please answer these questions to refine the specification:

1. **Scale**: What's the expected load? (users, requests/sec, data volume)
2. **Constraints**: What are the hard limits? (budget, timeline, team size)
3. **Integration**: What systems must this work with? What are their APIs?
4. **Users**: Who exactly will use this? What's their technical level?
5. **Success**: How will we measure success? What metrics matter?
6. **Flexibility**: What needs to be configurable vs. hardcoded?
7. **Evolution**: What features are likely to be added in 6 months?
8. [Context-specific questions based on investigation]

*[Your answers here]*
```

## 🛑 STOP HERE - PHASE 1 COMPLETE

**Your task:**
1. Open TASK.md
2. Add your answers below the questions (replace `*[Your answers here]*`)
3. Save TASK.md
4. Run `/spec` again to continue

**Example of answered questions in TASK.md:**
```markdown
## Clarifying Questions
Please answer these questions to refine the specification:

1. **Scale**: What's the expected load?
2. **Constraints**: What are the hard limits?
[...questions...]

We expect about 1000 concurrent users with 50 req/sec peak.
Budget is $5000, timeline is 2 months with 3 developers.
Must integrate with existing PostgreSQL and Stripe APIs.
Users are non-technical business analysts.
Success = 50% reduction in report generation time.
API endpoints should be configurable, algorithms can be hardcoded.
Likely to add webhook support and batch processing within 6 months.
```

---

# PHASE 2: CONTEXTUAL REFINEMENT
*This section executes only when answers are found in TASK.md*

## 7. Read Context & User Answers

**Read TASK.md to extract:**
- Original task description
- Investigation summary from Phase 1
- Questions with user's answers

**Process the answers to understand:**
- Concrete scale and performance requirements
- Actual timeline and resource constraints
- Specific integration points and APIs
- User personas and success metrics

## 8. Targeted Refinement Research

**Launch Phase 2 research based on user's specific answers:**

```
Task 1: "Refined solution research based on user requirements:
- Use gemini --prompt to find solutions proven at [user's scale]
- Research [specific integrations] mentioned by user
- Find patterns that fit [timeline/budget] constraints
- Look for [specific features] user plans to add
Be extremely specific to their exact requirements."

Task 2: "Technical validation for user's context:
- Use Context7 MCP for [specific libraries] that fit requirements
- Verify performance at [stated load] levels
- Check compatibility with [mentioned integrations]
- Validate feasibility within [stated timeline]
Only recommend what's achievable with their constraints."

Task 3: "Risk assessment for user's specific situation:
- Identify risks specific to [their scale/timeline]
- Find common failures with [their tech stack]
- Assess complexity for [their team size]
- Evaluate maintenance burden given constraints
Be realistic about what could go wrong."
```

## 9. Final Specification Generation

**Append the refined specification to TASK.md:**

```markdown

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

### Dependencies (Explicit Documentation)
- **External Systems**: [list all system dependencies with versions/contracts]
- **Libraries/Frameworks**: [required dependencies with version constraints]
- **Infrastructure**: [database, message queues, caches, etc.]
- **Third-party Services**: [APIs, SaaS platforms, external integrations]

### Assumptions (Make Implicit Explicit)
- **Environment**: [deployment platform, resource availability, network topology]
- **Scale**: [expected load, growth patterns, performance baselines]
- **Users**: [technical level, usage patterns, device capabilities]
- **Team**: [skill level, availability, knowledge constraints]

### Constraints Discovered
- **Technical**: [existing system boundaries found]
- **Resource**: [realistic time/space limits]
- **Integration**: [API contracts, data formats]
- **Operational**: [deployment, monitoring, maintenance requirements]

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


## 10. Validation & Next Steps

**The Hoare Test: "There are two ways of constructing a software design: One way is to make it so simple that there are obviously no deficiencies."**

🎯 **SIMPLICITY TENET VALIDATION**: Prefer the simplest design that solves the problem completely.
🎯 **PRODUCT VALUE FIRST VALIDATION**: Every approach must justify existence through demonstrable user value.
🎯 **EXPLICIT OVER IMPLICIT VALIDATION**: Surface and document all assumptions, dependencies, and constraints.

Validate the specification:
- Can this fail silently? → Document failure modes
- What happens at the boundaries? → Define edge cases
- **Is this the simplest solution?** → Justify every layer of complexity
- **Could we solve this with fewer moving parts?** → Challenge each abstraction
- **Would a newcomer understand this design?** → Test for obviousness
- **How does this directly benefit users?** → Articulate clear user value proposition
- **What user problems does this solve?** → Verify real user need exists
- **Would users notice if we removed features/complexity?** → Eliminate vanity engineering
- **Are all dependencies explicitly documented?** → List every external system dependency
- **What assumptions are we making?** → Surface environment, scale, and user assumptions
- **Are integration contracts clear?** → Define all interfaces and data flows explicitly
- **What could break if assumptions change?** → Identify hidden coupling and constraints
- Would Dijkstra approve? → Ensure mathematical precision

**Next Command**: Run `/plan` to decompose this specification into actionable tasks

Remember: **A good specification is not when there is nothing left to add, but when there is nothing left to take away.**

## Workflow Summary

**Phase 1 (Initial Investigation):**
1. Read TASK.md and ultrathink
2. Conduct parallel research
3. Evaluate architecture alternatives
4. Append investigation summary to TASK.md
5. Append clarifying questions to TASK.md
6. STOP and wait for user to add answers

**Phase 2 (Post-Answer Refinement):**
1. Read TASK.md with user's answers
2. Conduct targeted research based on answers
3. Refine approach with concrete constraints
4. Append refined specification to TASK.md

**Key Innovation**: The specification evolves through natural language dialogue within TASK.md itself - no JSON, no temp files, just a living document that tells its own story.

## Implementation Notes

**Phase 1 appends to TASK.md:**
```markdown
## Investigation Summary
- Key findings from research
- Architecture tradeoffs discovered
- Existing patterns identified

## Clarifying Questions
Please answer these questions to refine the specification:
1. Scale: What's the expected load?
2. Constraints: What are the hard limits?
[...more questions...]

*[Your answers here]*
```

**Phase 2 appends to TASK.md:**
```markdown
## Refined Specification

### Selected Approach
[Chosen architecture based on answers]

### Requirements
[Functional and non-functional requirements]

### Success Criteria
[Measurable outcomes]
```

The entire specification process becomes a readable narrative in TASK.md.
