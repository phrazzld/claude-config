Transform vague ideas into precise specifications.

# SPEC

Channel Dijkstra's precision: "The question of whether a computer can think is no more interesting than the question of whether a submarine can swim."

## The Dijkstra Principle

*"Simplicity is prerequisite for reliability."*

A specification isn't about what you want to build - it's about what must work.

## 1. Task Decomposition

**What would Dijkstra specify?**
- Read @TASK.md with a critical eye
- Extract invariants that must hold
- Define preconditions and postconditions
- Identify edge cases before features
- Ultrathink for mathematical precision

## 2. Research & Discovery

**Gather intelligence through parallel research:**

```
Task 1: "Research current best practices for the task in TASK.md:
- Use gemini --prompt for industry patterns and 2025 standards
- Find proven architectural approaches
- Identify common failure modes
- Security and performance considerations
Focus on what works in production, not what's trendy."

Task 2: "Find relevant documentation using Context7 MCP:
- Resolve library IDs for identified technologies
- Extract critical APIs and configuration patterns
- Note version constraints and gotchas
Only recommend battle-tested solutions."
```

## 3. Pattern Analysis

**Channel Thompson's simplicity:**
- Grep codebase for existing patterns
- Find what already works here
- Don't reinvent what exists
- Reuse before you build

## 4. Specification Structure

**The Knuth approach: "Beware of bugs in the above code; I have only proved it correct, not tried it."**

```markdown
## Requirements
### Functional (What it MUST do)
- [ ] Invariant 1: [specific, testable]
- [ ] Invariant 2: [measurable outcome]

### Non-Functional (How well it must do it)
- Performance: [specific metrics]
- Security: [threat model]
- Reliability: [failure modes]

## Constraints
- Technical: [existing system boundaries]
- Resource: [time/space limits]
- Business: [non-negotiables]

## Implementation Strategy
### Phase 1: Core Functionality
- Minimal viable solution
- Focus on invariants

### Phase 2: Hardening
- Edge cases
- Error handling
- Performance optimization

## Success Criteria
- [ ] All invariants hold
- [ ] Performance within bounds
- [ ] No security vulnerabilities
- [ ] Tests pass
```

## 5. Validation Questions

**The Hoare Test: "There are two ways of constructing a software design: One way is to make it so simple that there are obviously no deficiencies."**

Ask yourself:
- Can this fail silently?
- What happens at the boundaries?
- Is this the simplest solution that works?
- Would Dijkstra approve?

## Output

A SPEC.md that would make Dijkstra nod:
- Mathematically precise requirements
- Clear invariants and constraints
- Testable success criteria
- No wishful thinking

Remember: **A good specification is not when there is nothing left to add, but when there is nothing left to take away.**