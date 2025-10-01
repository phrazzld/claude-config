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

*Generated: [Date]*
*Approach: [Selected Architecture]*

---

## Executive Summary

**Problem**: [1-2 sentences describing the user problem being solved]

**Solution**: [1-2 sentences describing the proposed solution]

**User Value**: [Clear statement of how users benefit]

**Success Criteria**: [Primary metric for success]

---

## User Context

### Target Users
- **Who**: [User personas from answers]
- **Technical Level**: [From user answers]
- **Use Case**: [Primary scenarios]

### User Problems Being Solved
1. [Specific user problem 1]
2. [Specific user problem 2]
3. [Specific user problem 3]

### Expected User Benefits
- [Measurable benefit 1]
- [Measurable benefit 2]
- [Measurable benefit 3]

---

## Requirements

### Functional Requirements (What it MUST do)

**Core Functionality**:
- [ ] [Invariant 1: Specific, testable requirement]
- [ ] [Invariant 2: Specific, testable requirement]
- [ ] [Invariant 3: Specific, testable requirement]

**User Interactions**:
- [ ] [User flow 1]
- [ ] [User flow 2]
- [ ] [Error handling scenario]

**Integration Points**:
- [ ] [System integration 1 from user answers]
- [ ] [System integration 2 from user answers]
- [ ] [Data exchange requirement]

### Non-Functional Requirements (How well it must perform)

**Performance** (Based on user scale requirements):
- Throughput: [X requests/sec from user answers]
- Latency: [P95 < Y ms]
- Concurrent Users: [Z users from user answers]
- Data Volume: [Expected scale from user answers]

**Scalability**:
- Initial capacity: [Current needs]
- Growth plan: [6-month projection from user answers]
- Scaling strategy: [Horizontal/vertical approach]

**Security**:
- Authentication: [Method based on user context]
- Authorization: [Access control model]
- Data protection: [Encryption, PII handling]
- Threat model: [Key threats identified]

**Reliability**:
- Availability: [Target uptime]
- Failure modes: [How system degrades]
- Recovery: [RTO/RPO from user constraints]

**Maintainability**:
- Code organization: [Module structure]
- Testing strategy: [Coverage and approach]
- Documentation: [What needs docs]
- Operational complexity: [Deployment, monitoring]

---

## Architectural Design

### Selected Approach
**[Architecture Name]**: [Brief description]

**Rationale**:
- **Simplicity**: [Why this is the simplest solution that works]
- **User Value**: [How this maximizes user benefits]
- **Explicitness**: [How this makes behavior obvious]
- **Constraints**: [How this fits timeline/budget/team]

### Alternative Approaches Considered

| Approach | User Value | Simplicity | Risk | Why Not Selected |
|----------|-----------|------------|------|------------------|
| [Option 1] | [Score] | [Score] | [Score] | [Reason] |
| [Option 2] | [Score] | [Score] | [Score] | [Reason] |

### System Architecture

**High-Level Components**:
```
[ASCII diagram or description of major components]

Component 1 (Interface: simple) ──> Component 2 (Interface: simple)
       │                                    │
       └──> Shared Data Store <─────────────┘
```

**Module Boundaries** (Deep Module Design):
- **[Module 1]**:
  - Interface: [Simple, focused API]
  - Responsibility: [Single, clear purpose]
  - Hidden complexity: [What implementation details are internal]
- **[Module 2]**:
  - Interface: [Simple, focused API]
  - Responsibility: [Single, clear purpose]
  - Hidden complexity: [What implementation details are internal]

**Abstraction Layers**:
- **Layer 1 (Top)**: [User-facing abstraction]
- **Layer 2 (Middle)**: [Business logic abstraction - different from Layer 1]
- **Layer 3 (Bottom)**: [Infrastructure abstraction - different from Layer 2]

*Note: Each layer changes vocabulary and abstraction level - no pass-through methods*

### Technology Stack

**Languages/Frameworks**:
- [Technology 1]: [Version, rationale]
- [Technology 2]: [Version, rationale]

**Libraries/Dependencies**:
- [Library 1]: [Version, purpose, why chosen]
- [Library 2]: [Version, purpose, why chosen]

**Infrastructure**:
- Database: [Type, scale considerations]
- Caching: [If needed, approach]
- Message Queue: [If needed, approach]
- Storage: [File storage, object storage]

**Rationale**: [Why this stack serves users best, fits constraints, minimizes complexity]

---

## Dependencies & Assumptions

### Explicit Dependencies
**External Systems**:
- [System 1]: [API version, contract, SLA]
- [System 2]: [API version, contract, SLA]

**Libraries/Services**:
- [Dependency 1]: [Version constraint, criticality]
- [Dependency 2]: [Version constraint, criticality]

**Infrastructure Requirements**:
- Compute: [Specification]
- Storage: [Specification]
- Network: [Requirements]

### Documented Assumptions
**Environment**:
- Deployment platform: [From user answers]
- Network topology: [Assumptions about connectivity]
- Resource availability: [Compute/memory/storage]

**Scale**:
- Initial load: [From user answers]
- Growth rate: [Projection]
- Peak patterns: [Traffic characteristics]

**Users**:
- Technical capability: [From user answers]
- Device/browser support: [Compatibility matrix]
- Usage patterns: [How users will interact]

**Team**:
- Size: [From user answers]
- Skill level: [Capabilities]
- Timeline: [From user answers]

### Identified Constraints
**Technical**:
- [Existing system constraint 1]
- [Integration limitation 2]
- [Technology restriction 3]

**Resource**:
- Budget: [From user answers]
- Timeline: [From user answers]
- Team capacity: [From user answers]

**Operational**:
- Deployment process: [Existing practices to follow]
- Monitoring/alerting: [Existing tooling]
- Compliance: [Regulatory requirements]

---

## Implementation Strategy

### Phase 1: Core Functionality (MVP)
**Goal**: Minimal viable solution proving core value

**Scope**:
- [ ] [Core feature 1]
- [ ] [Core feature 2]
- [ ] [Critical integration 1]
- [ ] [Basic error handling]

**Success Criteria**:
- [ ] [Primary user flow works]
- [ ] [Integration test passes]
- [ ] [Performance baseline met]

**Estimated Time**: [Based on user timeline]

### Phase 2: Hardening & Polish
**Goal**: Production-ready, robust implementation

**Scope**:
- [ ] [Edge case handling from research]
- [ ] [Error recovery patterns]
- [ ] [Performance optimization]
- [ ] [Monitoring/observability]
- [ ] [Documentation]

**Success Criteria**:
- [ ] [All error scenarios handled]
- [ ] [Performance targets met]
- [ ] [Security scan passes]
- [ ] [Code review complete]

**Estimated Time**: [Based on user timeline]

### Phase 3: Evolution (Future)
**Planned Extensions** (Based on user's 6-month projection):
- [Future feature 1 from user answers]
- [Future feature 2 from user answers]
- [Scalability improvements]

**Design Considerations**:
- [What we're designing for extensibility]
- [What we're intentionally hardcoding]
- [Where we expect change]

---

## Testing Strategy

### Test Pyramid

**Unit Tests** (Fast, focused):
- [ ] [Module 1: Core logic]
- [ ] [Module 2: Business rules]
- [ ] [Module 3: Utilities]
- Target: 80%+ coverage of business logic

**Integration Tests** (API contracts):
- [ ] [Integration 1 from user requirements]
- [ ] [Integration 2 from user requirements]
- [ ] [Database interactions]
- [ ] [External service mocking]

**End-to-End Tests** (User scenarios):
- [ ] [Critical user flow 1]
- [ ] [Critical user flow 2]
- [ ] [Error recovery scenario]

**Performance Tests**:
- [ ] Load test: [X req/sec sustained]
- [ ] Stress test: [Peak load + 50%]
- [ ] Soak test: [24hr stability]

### Test Data & Environments
- **Test Data**: [Strategy for realistic data]
- **Staging**: [Environment matching production]
- **CI/CD**: [Automated test runs]

---

## Success Metrics & KPIs

### User Value Metrics (Primary)
- [Metric 1 from user answers]: Target [X]
- [Metric 2 from user answers]: Target [Y]
- User satisfaction: Target [Z]

### Technical Metrics (Secondary)
- Performance: [Latency targets]
- Reliability: [Uptime target]
- Error rate: [< X% target]

### Business Metrics (From user context)
- [ROI metric from user answers]
- [Business outcome from user answers]
- [Adoption metric]

### How We'll Measure
- [Instrumentation approach]
- [Analytics tooling]
- [Reporting cadence]

---

## Risks & Mitigation

### Technical Risks
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| [Risk 1 from research] | High/Med/Low | High/Med/Low | [Specific mitigation plan] |
| [Risk 2 from research] | High/Med/Low | High/Med/Low | [Specific mitigation plan] |

### Timeline Risks
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| [Schedule risk] | High/Med/Low | High/Med/Low | [Buffer, scope reduction] |
| [Dependency risk] | High/Med/Low | High/Med/Low | [Early integration, mocking] |

### Operational Risks
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| [Deployment risk] | High/Med/Low | High/Med/Low | [Rollback plan, feature flags] |
| [Scale risk] | High/Med/Low | High/Med/Low | [Monitoring, auto-scaling] |

---

## Key Decisions & Rationale

### Decision 1: [Technology/Architecture Choice]
**Decision**: [What was decided]
**Options Considered**: [Alternatives]
**Rationale**: [Why this choice - user value, simplicity, explicitness]
**Trade-offs**: [What we're giving up]

### Decision 2: [Design Pattern Choice]
**Decision**: [What was decided]
**Options Considered**: [Alternatives]
**Rationale**: [Why this choice]
**Trade-offs**: [What we're giving up]

### Decision 3: [Scope/Feature Choice]
**Decision**: [What's in/out]
**Rationale**: [Based on user priorities, timeline, value]

---

## Leyline Binding Compliance

### Applicable Bindings for Implementation
Based on detected technologies and architecture:

**Core Bindings**:
- hex-domain-purity: [How we're maintaining domain purity]
- api-design: [Interface contracts defined]
- automated-quality-gates: [CI/CD checks]
- code-size: [Module size limits]

**Technology-Specific Bindings**:
- [Binding 1]: [Compliance approach]
- [Binding 2]: [Compliance approach]

**Validation Plan**:
- Code review checklist includes binding compliance
- Automated linting for applicable rules
- Manual review for architectural bindings

---

## Open Questions (If Any)

- [ ] [Unresolved question 1]: Needs [stakeholder] input
- [ ] [Unresolved question 2]: Requires [technical research]

*Note: These should be rare - most questions answered in clarification phase*

---

## Validation Checklist

**Ousterhout Validation**:
- [ ] **Deep Modules**: Are we creating simple interfaces hiding complex implementations?
- [ ] **Information Hiding**: Are implementation details truly hidden?
- [ ] **No Information Leakage**: Can we change internals without breaking callers?
- [ ] **Different Abstractions**: Does each layer change vocabulary/concepts?
- [ ] **Strategic Design**: Have we invested 10-20% time in design quality?

**Tenet Validation**:
- [ ] **Simplicity**: Is this the simplest solution that solves the problem completely?
- [ ] **User Value**: Does every feature clearly benefit users?
- [ ] **Explicitness**: Are all dependencies, assumptions, and constraints documented?
- [ ] **Maintainability**: Would a developer understand this in 6 months?
- [ ] **Observability**: Can we see what's happening in production?

**Dijkstra Validation**:
- [ ] All invariants explicitly stated?
- [ ] Edge cases defined?
- [ ] Failure modes documented?
- [ ] Mathematical precision in requirements?

---

## Next Steps

1. Review this PRD with stakeholders
2. Get approval on approach and constraints
3. Run `/plan` to decompose into actionable tasks
4. Begin Phase 1 implementation

**Ready for**: `/plan` command

---

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
