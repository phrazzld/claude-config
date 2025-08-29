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
**Times referenced**: 2
**Last used**: 2025-08-28

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
**Times referenced**: 2
**Last used**: 2025-08-28

---

## AI-Driven Content Pipeline: Multi-Stage Validation Architecture
**ADR**: ADR-006
**Date**: 2025-08-24
**Outcome**: Pending Implementation
**Lessons**: Complex AI pipelines require security-first design (subprocess arrays, not shell strings), multi-source validation for accuracy, and human review queues for quality control; modular architecture enables independent optimization of pipeline stages
**Pattern**: For AI-assisted content creation, use composable CLI tools with secure subprocess execution, implement confidence thresholds and multi-stage validation, maintain human oversight for high-stakes content
**Times referenced**: 1
**Last used**: 2025-08-28

---

## KDP Image Processing: Sharp.js vs Alternatives
**ADR**: ADR-007
**Date**: 2025-08-28
**Outcome**: Pending Implementation
**Lessons**: Performance is critical for image validation pipelines; native libraries like Sharp.js provide 10-20x speed improvements over pure JS solutions, essential for batch cover processing and real-time validation feedback
**Pattern**: For image-intensive applications, prioritize native processing libraries over pure JS alternatives; bundle size concerns are secondary to performance in CLI/server contexts
**Times referenced**: 0
**Last used**: 2025-08-28

---

## EPUB Generation: Native vs Pandoc Enhancement
**ADR**: ADR-008
**Date**: 2025-08-28
**Outcome**: Pending Implementation
**Lessons**: When existing tools work well, enhancement often beats rewrite; Pandoc's mature EPUB generation plus targeted Sharp.js integration provides better ROI than custom EPUB implementation
**Pattern**: Prefer enhancing proven tools with targeted improvements over complete rewrites; composite solutions can leverage best-of-breed components
**Times referenced**: 0
**Last used**: 2025-08-28

---

## Publishing Validation: Multi-Stage Pipeline Architecture
**ADR**: ADR-009
**Date**: 2025-08-28
**Outcome**: Pending Implementation
**Lessons**: Complex validation requirements benefit from composable pipeline architecture; staged validation with progressive error reporting improves both extensibility and user experience over simple function chains
**Pattern**: For complex validation scenarios, implement composable pipelines with clear stage separation; invest in good error recovery and progressive feedback for better user experience
**Times referenced**: 0
**Last used**: 2025-08-28

---

## Error Recovery: Three-Tier Recovery System
**ADR**: ADR-010
**Date**: 2025-08-28
**Outcome**: Pending Implementation
**Lessons**: Automated error recovery significantly improves user experience but requires careful tier design; auto-fix should be conservative, semi-auto should require confirmation, manual should provide clear guidance
**Pattern**: Implement graduated error recovery: auto-fix for safe operations, semi-auto with confirmation for potentially destructive changes, manual with clear guidance for complex issues
**Times referenced**: 0
**Last used**: 2025-08-28

---

## Rate Limiting: Queue-Based Publishing Management
**ADR**: ADR-011
**Date**: 2025-08-28
**Outcome**: Pending Implementation
**Lessons**: External platform rate limits require proactive queue management; in-memory queues with persistent state provide good balance between performance and reliability for CLI tools
**Pattern**: For rate-limited external APIs, implement persistent queues with intelligent scheduling; hybrid in-memory + SQLite provides good performance with reliability
**Times referenced**: 0
**Last used**: 2025-08-28

---

## Cover Workflow: File-System Based Integration
**ADR**: ADR-012
**Date**: 2025-08-28
**Outcome**: Pending Implementation
**Lessons**: File-system based workflows provide intuitive interfaces for developers; staged directories (submitted/validated/rejected) with symlink integration offers transparency and seamless build system integration
**Pattern**: For developer-facing workflows, file-system interfaces often provide better UX than APIs; use staged directories for clear state transitions and symlinks for build system integration
**Times referenced**: 0
**Last used**: 2025-08-28

---

<!-- New ADR outcomes will be added below this line -->