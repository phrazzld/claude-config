# Leyline Tenets - Core Development Principles

This document defines the canonical vocabulary and phrasing for core development tenets referenced throughout Claude Code commands. Use these exact definitions for consistency.

**Philosophical Foundation**: These tenets are informed by John Ousterhout's "A Philosophy of Software Design" - see [docs/ousterhout-principles.md](./ousterhout-principles.md) for detailed integration guidance.

## Core Tenets

### Simplicity
**Definition**: Prefer the simplest solution that solves the problem completely.

**Ousterhout Extension**: Complexity is anything that makes software hard to understand or modify. It comes from two sources: **dependencies** (linkages between components) and **obscurity** (when important information is not obvious). Zero tolerance for accumulating complexity.

**Key Phrases**:
- "Choose boring over clever"
- "Simplicity is prerequisite for reliability"
- "The simplest thing that could possibly work"
- "Every line of code is a liability"
- "Complexity = dependencies + obscurity" (Ousterhout)

**Application**: Remove unnecessary abstractions, avoid premature optimization, delete code that doesn't pay rent, choose proven solutions over experimental ones. Evaluate every design decision by whether it increases or decreases dependencies and obscurity.

### Modularity
**Definition**: Build independent, focused components with clear boundaries.

**Ousterhout Extension**: **Deep modules** provide powerful functionality through simple interfaces. Module value = functionality - interface complexity. Avoid **shallow modules** where interface complexity nearly equals implementation complexity.

**Key Phrases**:
- "Single responsibility principle"
- "Loose coupling, high cohesion"
- "Components testable in isolation"
- "Clear interfaces between modules"
- "Deep modules: simple interface, powerful implementation" (Ousterhout)
- "Different layers, different abstractions" (Ousterhout)

**Application**: Break complex systems into manageable parts, define explicit contracts, minimize dependencies, enable parallel development. When creating abstractions, ask "What complexity am I actually hiding?" Ensure each layer provides a simpler abstraction than the one below it.

### Explicitness
**Definition**: Make behavior obvious - explicit over implicit.

**Ousterhout Extension**: Practice **information hiding** - hide implementation details while making interfaces clear. Watch for **information leakage** - when design choices leak out forcing callers to know implementation details. Interfaces should define 'what' not 'how'.

**Key Phrases**:
- "Surface hidden dependencies"
- "No magic, no surprises"
- "Visible in function signatures"
- "Document assumptions clearly"
- "Hide implementation, expose intention" (Ousterhout)
- "Hard to misuse by design" (Ousterhout)

**Application**: Avoid global state, make dependencies visible, use descriptive names, document non-obvious decisions, prefer return values over side effects. Hide implementation details behind clear interfaces. In code review, ask "If I change this implementation, will calling code break?" If yes, you have information leakage.

### Maintainability
**Definition**: Write for the developer who will modify this in six months.

**Ousterhout Extension**: Adopt **strategic programming** - invest 10-20% of development time in improving system design, not just completing features. Recognize the difference between **tactical** (quick fixes) and **strategic** (long-term design) work. Write comments that capture what code cannot: reasoning, invariants, units, and contracts.

**Key Phrases**:
- "Future-you will thank present-you"
- "Code is read more than written"
- "Self-documenting code"
- "Obvious extension points"
- "Strategic over tactical programming" (Ousterhout)
- "Comments document intent, not mechanics" (Ousterhout)

**Application**: Use clear naming, maintain consistent patterns, document complex logic, create obvious places for changes, optimize for readability. Dedicate time to leaving code better than you found it. Write comments that explain why, not what. Recognize when you're taking shortcuts vs investing in design.

### Observability
**Definition**: Make system behavior visible rather than guessing.

**Key Phrases**:
- "Don't debug in the dark"
- "Measure, don't guess"
- "Make the invisible visible"
- "Strategic instrumentation"

**Application**: Add logging at decision points, capture state transitions, trace data flow, monitor resource usage, instrument for debugging.

## Secondary Tenets

### Automation
**Definition**: If it can be automated, it should be automated.

**Key Phrases**:
- "Automate repetitive tasks"
- "Machines are better at repetition"
- "Scripts over documentation"
- "Quality gates, not manual reviews"

### Testability
**Definition**: Design systems to be verifiable and validated.

**Key Phrases**:
- "Test seams and boundaries"
- "Isolation and mockability"
- "Test behavior, not implementation"
- "Coverage with confidence"

### Design Never Done
**Definition**: Accept that design evolves with understanding.

**Key Phrases**:
- "First iteration, not final solution"
- "Plan for refactoring"
- "Learn and iterate"
- "Assumptions will change"

## Usage Guidelines

1. **Consistency**: Always use the canonical definition when introducing a tenet
2. **Context**: Add context-specific examples relevant to the command
3. **Brevity**: Keep tenet reminders concise - link here for full details
4. **Relevance**: Only include tenets that directly apply to the task

## Design Red Flags (Ousterhout)

When reviewing code, watch for these red flags that indicate tenet violations:

1. **Information Leakage**: Implementation details visible through interface (violates Explicitness + Modularity)
2. **Temporal Decomposition**: Code organized by execution order rather than functionality (violates Modularity)
3. **Over-exposure / Generic Names**: Classes named `Manager`, `Util`, `Helper`, `Context` (violates all tenets)
4. **Pass-through Methods**: Methods that only call another method with same signature (violates Modularity - shallow module)
5. **Configuration Overload**: Dozens of exposed parameters (violates Simplicity + Explicitness)
6. **Shallow Modules**: Interface complexity ≈ implementation complexity (violates Modularity)

See [docs/ousterhout-principles.md](./ousterhout-principles.md) for detailed examples and detection guidance.

## Cross-References

When discussing tenets across commands, use these standard cross-references:
- "See also: Simplicity principles in /spec command"
- "Related: Modularity approach in /plan command"
- "Compare: Explicitness validation in /git-code-review"
- "Reference: Maintainability guidelines in /execute"
- "Deep dive: Ousterhout's Philosophy in docs/ousterhout-principles.md"

---

*These tenets guide principled development without prescribing implementation. They're north stars, not rigid rules.*