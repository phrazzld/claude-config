Transform vague ideas into precise specifications through deep investigation and direct clarification.

# SPEC

Channel Dijkstra's precision: "The question of whether a computer can think is no more interesting than the question of whether a submarine can swim."

## The Dijkstra Principle

*"Simplicity is prerequisite for reliability."*

A specification isn't about what you want to build - it's about what must work.

## The Ousterhout Lens

*"The greatest limitation in writing software is our ability to understand the systems we are creating."*

When specifying solutions, apply these design principles:

**Design Twice**: Before committing to an approach, explore 2-3 fundamentally different alternatives. The best design often emerges from comparing options.

**Deep Module Thinking**: Specify interfaces first. The best modules have simple interfaces hiding powerful implementations. Ask: "What complexity can this module hide from its users?"

**Information Hiding**: What implementation details should stay internal? What must be exposed? Define clear boundaries between what callers need to know (interface) and what they shouldn't (implementation).

**Strategic Specification**: This isn't just documenting features - it's investing in future velocity by creating clear abstractions that reduce system complexity.

See [docs/tenets.md](../docs/tenets.md) and [docs/ousterhout-principles.md](../docs/ousterhout-principles.md) for detailed guidance.

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
**Simplicity**: Prefer the simplest solution that solves the problem completely.
**Product Value First**: Every approach must justify existence through demonstrable user value.
**Explicitness**: Make behavior obvious - explicit over implicit. Surface and document all assumptions, dependencies, and constraints.
For each approach, explicitly identify: dependencies on existing systems, assumptions about environment/users/scale, constraints and limitations, integration requirements, and potential side effects on other systems.
Evaluate each approach against user/business outcomes - reject technically interesting but low-value solutions.
Focus on production-proven solutions with real-world validation and clear user benefits."

Task 2: "Find relevant documentation using Exa MCP:
- Search for documentation and code examples for potential technology choices
- Compare APIs and capabilities of alternative solutions
- Extract configuration patterns and best practices
- Note version constraints, breaking changes, and migration paths
- Identify ecosystem maturity and community support
**Simplicity**: Prefer the simplest solution that solves the problem completely.
**Product Value First**: Every technology choice must serve demonstrable user value.
**Explicitness**: Make behavior obvious - explicit over implicit. Surface and document all assumptions, dependencies, and constraints.
For each technology choice, explicitly document: runtime dependencies, configuration requirements, assumptions about infrastructure/environment, integration constraints, breaking change risks, and compatibility requirements.
Evaluate libraries based on user benefits they enable, not feature richness or technical novelty.
Prioritize battle-tested libraries that directly support user-valuable functionality."

Task 3: "Explore alternative architectures and implementations:
- Use ast-grep to find similar patterns in the codebase
- Research competing approaches (monolith vs microservices, sync vs async, etc.)
- Evaluate different toolchains and build systems
- Consider data flow patterns (event-driven, request-response, streaming)
- Assess integration complexity with existing systems
**Simplicity**: Prefer the simplest solution that solves the problem completely.
**Product Value First**: Every architectural choice must demonstrate clear user value.
**Explicitness**: Make behavior obvious - explicit over implicit. Surface and document all assumptions, dependencies, and constraints.
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
**Simplicity**: Prefer the simplest solution that solves the problem completely.
**Product Value First**: Every approach must justify existence through demonstrable user value.
**Explicitness**: Make behavior obvious - explicit over implicit. Surface and document all assumptions, dependencies, and constraints.

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

**Preliminary Recommendation**: [Selected approach with justification using tenet decision matrix - prioritize user value, simplicity, and explicitness while managing implementation risk]

## 5. Generate Clarifying Questions

**Synthesize research into focused questions:**

Based on the investigation, generate 5-10 critical questions that will refine the specification. Focus on:

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
10. **[Add 2-4 context-specific questions based on research findings]**

## 6. Ask User Directly

**Present questions directly to the user for immediate answers:**

Display investigation summary and questions in a clear, conversational format:

```
# Investigation Summary

Based on research, here are the key findings:
- [Finding 1: Industry pattern discovered]
- [Finding 2: Architectural tradeoff identified]
- [Finding 3: Existing codebase pattern found]
- [Finding 4: Risk or constraint discovered]

# Preliminary Approach

I'm leaning toward [recommended approach] because:
- [Reason 1: Simplicity/User Value/Explicitness]
- [Reason 2: Fits constraints]
- [Reason 3: Proven pattern]

# Clarifying Questions

To write a precise specification, I need answers to these questions:

1. **Scale**: What's the expected load? (concurrent users, requests/sec, data volume)

2. **Constraints**: What are the hard limits? (budget, timeline, team size, existing systems)

3. **Integration**: What systems must this integrate with? Are there API contracts or data formats to follow?

4. **Users**: Who will use this? What's their technical level and context?

5. **Success Metrics**: How will we know this is working? What KPIs matter?

6. **User Value**: What specific user problems are we solving? How will this improve their experience?

7. **Flexibility**: What aspects need to be configurable vs. hardcoded?

8. **Evolution**: What features are likely next? What should we design for extensibility?

9. [Context-specific question 1]

10. [Context-specific question 2]

Please provide answers so I can write a detailed PRD.
```

## 🛑 STOP HERE - Wait for User Answers

Once user provides answers, continue to Phase 2.

---

# PHASE 2: PRD GENERATION

*Execute this phase after receiving user's answers*

## 7. Synthesize Answers

**Process user responses:**
- Extract concrete requirements from answers
- Identify scale, performance, and constraint parameters
- Map to specific technology choices and architectural decisions
- Note any new risks or considerations revealed

## 8. Targeted Refinement Research

**Conduct focused research based on user's specific context:**

```
Task 1: "Validate approach against user requirements:
- Use gemini --prompt to verify [recommended approach] works at [user's scale]
- Research [specific integrations] mentioned by user
- Find examples of [approach] with [user's tech stack]
- Validate feasibility within [user's timeline/budget]"

Task 2: "Deep dive on implementation details:
- Use Exa MCP to find production examples of [selected pattern]
- Research [specific libraries/frameworks] needed
- Find configuration examples for [user's use case]
- Identify potential gotchas with [user's constraints]"

Task 3: "Risk and mitigation planning:
- Identify failure modes specific to [user's scale/context]
- Research common issues with [selected approach + user's stack]
- Find testing strategies that fit [user's team/timeline]
- Plan for [user's evolution requirements]"
```

## 9. Write Comprehensive PRD to TASK.md

**Replace TASK.md contents with detailed Product Requirements Document:**

```markdown
# [Feature/Project Name]

*Generated: [Date] | Approach: [Selected Architecture]*

---

## Executive Summary

**Problem**: [1-2 sentences]
**Solution**: [1-2 sentences]
**User Value**: [Clear benefit statement]
**Success Criteria**: [Primary metric]

---

## User Context

- **Who**: [User personas]
- **Problems**: [Specific issues being solved]
- **Benefits**: [Measurable improvements]

---

## Requirements

### Functional (What it MUST do)
- [ ] [Core functionality requirements]
- [ ] [User interactions and flows]
- [ ] [Integration points with existing systems]

### Non-Functional (How well it performs)
**Performance**: Throughput, latency, concurrent users, data volume
**Security**: Authentication, authorization, data protection, threats
**Reliability**: Availability targets, failure modes, recovery
**Maintainability**: Code org, testing, documentation

---

## Architecture

### Selected Approach
**[Name]**: [Description]

**Rationale**: Simplicity, user value, explicitness, constraints

**Alternatives Considered**:
| Approach | Value | Simplicity | Risk | Why Not |
|----------|-------|------------|------|---------|
| [Option] | [Score] | [Score] | [Score] | [Reason] |

### System Design

**Components**: [High-level component diagram or description]

**Module Boundaries** ([Deep modules](../docs/ousterhout-principles.md)):
- **[Module]**: Interface, responsibility, hidden complexity

**Abstraction Layers**: [Top layer] → [Middle layer] → [Bottom layer]
*Each layer changes vocabulary and abstraction level*

**Technology Stack**:
- Languages/Frameworks: [Tech + version + rationale]
- Libraries: [Key dependencies]
- Infrastructure: Database, caching, storage

---

## Dependencies & Assumptions

**Dependencies**:
- External systems: [APIs, versions, contracts]
- Libraries: [Critical dependencies + versions]
- Infrastructure: [Compute, storage, network requirements]

**Assumptions**:
- Environment: [Deployment platform, resources]
- Scale: [Initial load, growth, peak patterns]
- Users: [Technical level, devices, usage patterns]
- Team: [Size, skills, timeline]

**Constraints**:
- Technical: [Existing system limitations]
- Resource: [Budget, timeline, team capacity]
- Operational: [Deployment processes, compliance]

---

## Implementation

### Phase 1: MVP
- [ ] [Core features proving value]
- Success: [Primary flows work, tests pass, baseline met]
- Time: [Estimate]

### Phase 2: Hardening
- [ ] [Edge cases, optimization, monitoring, docs]
- Success: [All scenarios handled, targets met, review complete]
- Time: [Estimate]

### Phase 3: Future Extensions
- [Planned improvements based on 6-month projection]
- Design considerations: [Extensibility vs hardcoded decisions]

---

## Testing

**Unit**: Core logic, business rules (80%+ coverage)
**Integration**: System interactions, API contracts
**E2E**: Critical user flows, error scenarios
**Performance**: Load, stress, soak tests

**Environments**: Test data strategy, staging setup, CI/CD automation

---

## Success Metrics

**User Value** (Primary): [Key user-facing metrics with targets]
**Technical** (Secondary): Performance, reliability, error rates
**Business**: ROI, outcomes, adoption
**Measurement**: Instrumentation approach, tooling, reporting

---

## Risks & Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| [Technical] | H/M/L | H/M/L | [Plan] |
| [Timeline] | H/M/L | H/M/L | [Plan] |
| [Operational] | H/M/L | H/M/L | [Plan] |

---

## Key Decisions

**[Decision Name]**: What, alternatives, rationale (user value, simplicity, explicitness), tradeoffs

---

## Validation

**Ousterhout**: Deep modules? Info hiding? No leakage? Different abstractions? Strategic design?
**Tenets**: Simplicity? User value? Explicitness? Maintainability? Observability?
**Dijkstra**: Invariants? Edge cases? Failure modes?

See [docs/tenets.md](../docs/tenets.md) and [docs/ousterhout-principles.md](../docs/ousterhout-principles.md)

---

## Next Steps

1. Review PRD with stakeholders
2. Get approval
3. Run `/plan` for implementation tasks

*"A good specification is not when there is nothing left to add, but when there is nothing left to take away."*
```

## 10. Present PRD Summary

After writing TASK.md, provide concise summary to user:

```
✅ Specification Complete

I've written a comprehensive PRD to TASK.md covering:

**Approach**: [Selected architecture]
**User Value**: [Key benefits]
**Timeline**: [Phase 1: X weeks, Phase 2: Y weeks]
**Key Decisions**: [Major choice 1, Major choice 2]

**Complexity Assessment**:
- Dependencies: [Count and criticality]
- Risk Level: [Low/Medium/High]
- Confidence: [High/Medium based on research]

**Next**: Run `/plan` to break this down into implementation tasks.

Any questions or changes to the approach?
```

---

## Workflow Summary

**Single Continuous Flow**:
1. Read TASK.md (user's initial request)
2. Ultrathink and conduct parallel research
3. Evaluate 3-5 architectural alternatives
4. Generate focused clarifying questions
5. **Ask user directly** (conversational, not file-based)
6. **Wait for user's answers**
7. Conduct targeted research based on answers
8. **Write comprehensive PRD to TASK.md** (replacing original content)
9. Present summary to user

**Key Innovation**: Direct conversation for clarification, then comprehensive documentation in TASK.md. No intermediate file states, no manual editing required.

---

*For complete tenet definitions and vocabulary, see [docs/tenets.md](../docs/tenets.md)*
