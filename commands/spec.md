Transform vague ideas into precise specifications through deep investigation and direct clarification.

# SPEC

Channel Dijkstra's precision: "The question of whether a computer can think is no more interesting than the question of whether a submarine can swim."

## Your Mission

You're defining what to build before building it. Read the initial request (usually TASK.md), investigate deeply, explore alternatives, then ask clarifying questions. Don't jump to solutions—understand the problem space first.

### Design Principles

**Design Twice**: Explore 2-3 fundamentally different alternatives before committing. The best design emerges from comparison, not your first idea.

**Deep Modules**: Great modules = simple interface hiding powerful implementation. Ask: "What complexity can this module hide from users?" Module Value = Functionality - Interface Complexity.

**Information Hiding**: Define clear boundaries—what callers need to know (interface) vs. shouldn't know (implementation). If changing implementation breaks callers, details are leaking.

**Strategic Specification**: Invest 10-20% in design that reduces future complexity, not just feature completion. Tactical specs create debt; strategic specs pay dividends.

## Investigation & Architecture

**Parallel Research** - Launch multiple research angles simultaneously:
- Use `gemini --prompt` for industry patterns and proven approaches (2025 best practices)
- Use Exa MCP for technical documentation, API comparisons, version constraints
- Use `ast-grep` to find similar patterns in this codebase
- Grep for existing utilities, conventions, and reusable components

**Think deeply about alternatives**:
- What are 3-5 fundamentally different approaches to this problem?
- What are the tradeoffs between simplicity and flexibility?
- Where are the natural system boundaries?
- What constraints are real vs. assumed?
- What would this look like built from scratch today?

**Evaluation Framework**:
- **User Value** (40%): Does this solve real user problems? Reject if unclear or theoretical.
- **Simplicity** (30%): Is this the simplest viable solution? Prefer obvious over clever.
- **Explicitness** (20%): Are dependencies and assumptions clear? No hidden complexity.
- **Risk** (10%): What could realistically go wrong? Prefer proven over experimental.

For each approach, explicitly document: dependencies on existing systems, assumptions about environment/users/scale, integration requirements, potential side effects.

## Clarifying Questions

Based on your investigation, generate 5-8 critical questions that will refine the specification:

**Must Answer**:
- **Scale**: Expected load (users, requests/sec, data volume)
- **Constraints**: Hard limits (budget, timeline, team size, existing systems)
- **Integration**: What systems must this work with? API contracts?
- **Success**: How will we measure this worked? What metrics matter?
- **User Value**: What specific user problems are we solving?

**Design Questions**:
- **Flexibility**: What needs to be configurable vs. hardcoded?
- **Evolution**: What features are likely in 6 months?
- [Add 2-3 context-specific questions based on research findings]

**Present directly to the user** in conversational format—show investigation summary, preliminary approach with reasoning, then your questions. Don't create intermediate files.

## 🛑 Wait for User Answers

Once user provides answers, continue to PRD generation.

## Writing the PRD

After receiving answers, conduct targeted refinement research validating your recommended approach against user's specific context (scale, integrations, constraints). Then write a comprehensive but concise PRD to TASK.md:

**Executive Summary** (4-6 lines):
Problem, solution, user value, success criteria

**User Context**:
Who uses this, problems being solved, measurable benefits

**Requirements**:
- Functional: What it must do
- Non-Functional: Performance, security, reliability, maintainability

**Architecture Decision**:
- Selected Approach: Name, description, rationale (simplicity, user value, explicitness)
- Alternatives Considered: Table showing value, simplicity, risk, why not chosen
- Module Boundaries: Each module's interface, responsibility, hidden complexity
- Abstraction Layers: How each layer changes vocabulary

**Dependencies & Assumptions**:
Make everything explicit—external systems, scale expectations, team constraints, environment requirements. No hidden assumptions.

**Implementation Phases**:
- Phase 1 MVP: Core features proving value
- Phase 2 Hardening: Edge cases, optimization, monitoring
- Phase 3 Future: Planned improvements (6-month horizon)

**Risks & Mitigation**:
What could go wrong, how we'll handle it (table: risk, likelihood, impact, mitigation)

**Key Decisions**:
For each major decision: what, alternatives, rationale (user value, simplicity, explicitness), tradeoffs

Keep the PRD tight—if you can't explain a section in 2 paragraphs, it's probably too complex.

## Quality Validation

Before finalizing, check:
- **Deep modules**: Simple interfaces hiding powerful implementations?
- **Information hiding**: No leakage—implementation changes don't break callers?
- **Different abstractions**: Each layer changes vocabulary and abstraction level?
- **Strategic design**: Investing in future velocity, not just feature completion?

**Red Flags to Avoid**:
- Premature abstraction (wait for 3+ pattern repetitions)
- Information leakage (returning raw DB rows exposes schema)
- Temporal decomposition (organizing by step1, step2 instead of functionality)
- Generic names (Manager, Util, Helper without domain context)
- Pass-through layers (each abstraction should transform, not just forward)

## Present Summary

After writing TASK.md, provide concise summary:
- Approach selected and why
- User value delivered
- Timeline estimate
- Key decisions and complexity assessment

**Next**: Run `/plan` to break this down into implementation tasks.

Remember: "A good specification is not when there's nothing left to add, but nothing left to take away."
