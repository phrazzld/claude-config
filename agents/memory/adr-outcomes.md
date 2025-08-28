# ADR Outcomes Memory

This file tracks architecture decisions and their real-world outcomes to inform future decisions.

## Structure

Each entry includes:
- **ADR**: Reference number
- **Date**: When decided
- **Outcome**: Success/Mixed/Failure
- **Lessons**: What we learned
- **Pattern**: Reusable insight
- **Times referenced**: How often this outcome is consulted
- **Last used**: When this pattern was last referenced (YYYY-MM-DD)

---

## Example Entry (Remove after first real ADR)

## Microservices: User Service Extraction
**ADR**: ADR-001
**Date**: 2024-01-15
**Outcome**: Mixed
**Lessons**: Extraction worked but added complexity for small team
**Pattern**: Consider team size when choosing architecture complexity
**Times referenced**: 0
**Last used**: Never

---

## Reading Status Model: Three-State to Two-State Simplification
**ADR**: ADR-001
**Date**: 2025-08-21
**Outcome**: Pending Implementation
**Lessons**: Complex status models in single-user systems often unnecessary; simplification preferred when business logic is clear
**Pattern**: For personal tools, favor binary states over multi-state models unless clear value justification exists
**Times referenced**: 0
**Last used**: 2025-08-21

---

## Command Injection: Shell Escaping vs Subprocess Arrays
**ADR**: ADR-002
**Date**: 2024-03-10
**Outcome**: Success
**Lessons**: Direct shell command construction with string concatenation led to vulnerabilities; switching to spawn() with argument arrays eliminated injection risks
**Pattern**: Never construct shell commands with user input via string concatenation; use subprocess with argument arrays for external tool integration
**Times referenced**: 1
**Last used**: 2025-08-22

---

## Monorepo: Jest vs Vitest for Test Infrastructure
**ADR**: ADR-003
**Date**: 2024-07-15
**Outcome**: Mixed
**Lessons**: Jest configuration in complex monorepos requires extensive setup for ES modules; Vitest works out of the box but lacks ecosystem maturity
**Pattern**: For greenfield projects, prefer Vitest for ESM-first monorepos; for existing Jest setups, investment in proper configuration usually pays off
**Times referenced**: 1
**Last used**: 2025-08-22

---

## API Design: God Functions vs Service Layer
**ADR**: ADR-004
**Date**: 2024-05-20
**Outcome**: Success
**Lessons**: Breaking down 500+ line API handlers into service layer improved testability dramatically; however, over-abstraction can hurt performance
**Pattern**: Use service layer pattern for complex business logic, but keep simple operations inline; aim for 50-100 line functions as sweet spot
**Times referenced**: 1
**Last used**: 2025-08-22

---

## Build Scripts: Centralized vs Distributed in Monorepo
**ADR**: ADR-005
**Date**: 2024-09-12
**Outcome**: Success
**Lessons**: Initially put all scripts in root package.json (90+ scripts); distributing to workspace-specific packages improved discoverability and reduced complexity
**Pattern**: In monorepos, co-locate scripts with their functionality; use root only for orchestration scripts
**Times referenced**: 1
**Last used**: 2025-08-22

---

## AI-Driven Content Pipeline: Multi-Stage Validation Architecture
**ADR**: ADR-006
**Date**: 2025-08-24
**Outcome**: Pending Implementation
**Lessons**: Complex AI pipelines require security-first design (subprocess arrays, not shell strings), multi-source validation for accuracy, and human review queues for quality control; modular architecture enables independent optimization of pipeline stages
**Pattern**: For AI-assisted content creation, use composable CLI tools with secure subprocess execution, implement confidence thresholds and multi-stage validation, maintain human oversight for high-stakes content
**Times referenced**: 0
**Last used**: 2025-08-24

---

<!-- New ADR outcomes will be added below this line -->