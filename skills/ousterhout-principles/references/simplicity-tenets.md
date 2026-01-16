# Simplicity Tenets

Distilled from Leyline's foundational principles.

## Core Belief

Simplicity is a fundamental requirement. Complex solutions create exponential growth in mental overhead. Complexity feeds on itself, growing with each "small" addition.

## Practical Guidelines

1. **YAGNI Rigorously**: Question every piece of code not solving an immediate, demonstrated need. "Do we have concrete evidence we'll need this?"

2. **Minimize Moving Parts**: Each component, abstraction, or dependency can break and needs maintenance. "What value does this add? Is there a simpler way?"

3. **Readability Over Cleverness**: Code is read more than written. Prioritize clear, readable code. "Will someone unfamiliar understand what it does and why?"

4. **Distinguish Complexity Types**:
   - **Essential**: Inherent in the problem domain
   - **Accidental**: Introduced by implementation choices
   - Ruthlessly eliminate accidental complexity.

5. **Refactor Towards Simplicity**: Codebases drift toward complexity. Make simplification continuous practice. "How could this be simplified?"

6. **Ship Good-Enough Software**: Perfect software is the enemy of useful software. Focus on meeting actual user needs.

7. **Tracer Bullets**: Create minimal end-to-end implementations first to validate assumptions early.

## Warning Signs

- Over-engineering for imagined future requirements
- Premature abstraction before seeing the pattern three times
- Deep nesting (>2-3 levels) of conditionals or functions
- Long functions handling multiple responsibilities
- Justifications like "I'll make it generic so we can reuse it later"

## Related Tenets

**Modularity**: Single responsibility, well-defined boundaries.

**Explicit Over Implicit**: Make behavior obvious, reduce hidden magic.

**Testability**: Simple code is inherently more testable.

**Maintainability**: Simple systems are easier to understand and modify.
