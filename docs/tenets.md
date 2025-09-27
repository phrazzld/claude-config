# Leyline Tenets - Core Development Principles

This document defines the canonical vocabulary and phrasing for core development tenets referenced throughout Claude Code commands. Use these exact definitions for consistency.

## Core Tenets

### Simplicity
**Definition**: Prefer the simplest solution that solves the problem completely.

**Key Phrases**:
- "Choose boring over clever"
- "Simplicity is prerequisite for reliability"
- "The simplest thing that could possibly work"
- "Every line of code is a liability"

**Application**: Remove unnecessary abstractions, avoid premature optimization, delete code that doesn't pay rent, choose proven solutions over experimental ones.

### Modularity
**Definition**: Build independent, focused components with clear boundaries.

**Key Phrases**:
- "Single responsibility principle"
- "Loose coupling, high cohesion"
- "Components testable in isolation"
- "Clear interfaces between modules"

**Application**: Break complex systems into manageable parts, define explicit contracts, minimize dependencies, enable parallel development.

### Explicitness
**Definition**: Make behavior obvious - explicit over implicit.

**Key Phrases**:
- "Surface hidden dependencies"
- "No magic, no surprises"
- "Visible in function signatures"
- "Document assumptions clearly"

**Application**: Avoid global state, make dependencies visible, use descriptive names, document non-obvious decisions, prefer return values over side effects.

### Maintainability
**Definition**: Write for the developer who will modify this in six months.

**Key Phrases**:
- "Future-you will thank present-you"
- "Code is read more than written"
- "Self-documenting code"
- "Obvious extension points"

**Application**: Use clear naming, maintain consistent patterns, document complex logic, create obvious places for changes, optimize for readability.

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

## Cross-References

When discussing tenets across commands, use these standard cross-references:
- "See also: Simplicity principles in /spec command"
- "Related: Modularity approach in /plan command"
- "Compare: Explicitness validation in /git-code-review"
- "Reference: Maintainability guidelines in /execute"

---

*These tenets guide principled development without prescribing implementation. They're north stars, not rigid rules.*