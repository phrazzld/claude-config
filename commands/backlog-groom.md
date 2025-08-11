Organize, prioritize, and enhance BACKLOG.md using parallel expert analysis from 8 specialized perspectives focused on code quality and engineering excellence.

# GROOM

Organize, prioritize, and enhance @BACKLOG.md by first cleaning up the existing backlog, then launching 8 parallel expert agents who analyze the project from their unique perspectives and generate targeted improvements with focus on maintainable, well-designed code.

## 1. Backlog Organization and Cleanup

**Analyze existing backlog structure**:
- Read current @BACKLOG.md to understand existing tasks, structure, and priority system
- Identify completed items that should be archived
- Remove obsolete or no-longer-relevant items
- Categorize remaining items by effort (S/M/L) and quality impact (1-10)
- Note recurring technical debt patterns and quality issues

**Reorganize for clarity**:
- Group similar items together (quality gates, documentation, refactoring, etc.)
- Apply quality-first prioritization (security > maintainability > features > optimizations)
- Create clear sections with consistent formatting
- Add estimated effort and quality impact to existing items where missing

## 2. Prepare Context

**Read foundational documents**:
- Read project-specific leyline documents in `./docs/leyline/` if they exist
- Note current project architecture, tech stack, and recent changes
- Read key documentation and best practices for project toolchains and technologies via context7 MCP and web search
- Assess current quality measures (test coverage, complexity metrics, documentation state)
- Identify existing quality gates, CI/CD setup, and automation

## 3. Parallel Expert Analysis

Launch 8 expert agents using the Task tool to analyze the project and generate backlog items with enhanced focus on code quality:

```
Task 1: "Creative/Product Innovation Agent - Think hard about innovative possibilities that improve both user experience and code quality. Analyze the project codebase and @BACKLOG.md. Generate 3-5 innovative feature ideas focusing on:
- Developer experience innovations (better tooling, workflow automation, quality gates)
- User pain points that could be addressed with clean, maintainable solutions
- Opportunities for delightful experiences that don't increase code complexity
- Integration opportunities with modern tools/services that reduce technical debt
- Features that could simplify rather than complicate the codebase
Each item should include: Priority (CRITICAL/HIGH/MEDIUM/LOW), effort estimate (S/M/L), quality impact (1-10), and innovation rationale.
Format: `- [ ] [PRIORITY] [FEATURE] Description | Effort: S/M/L | Quality: X/10 | Innovation: why this improves both UX and code health`"

Task 2: "Security Audit Agent - Think hard about security vulnerabilities and automated security enforcement. Conduct thorough security analysis of the codebase and @BACKLOG.md. Generate 3-5 security improvements focusing on:
- Authentication and authorization patterns with automated testing
- Data validation and sanitization with linting enforcement
- Dependency vulnerabilities and automated scanning (Dependabot, Snyk)
- Secrets management, configuration security, and pre-commit hooks
- API security, rate limiting, and automated security testing
- Supply chain security and build pipeline hardening
Each item should include: Priority (CRITICAL for vulnerabilities, HIGH for hardening, MEDIUM for automation), effort estimate (S/M/L), security impact, and automation strategy.
Format: `- [ ] [PRIORITY] [SECURITY] Description | Effort: S/M/L | Risk: threat addressed | Automation: enforcement strategy`"

Task 3: "Codebase Simplification Agent - Ultrathink about code complexity reduction and quality enforcement. How can we make this codebase more modular, more simple, easier to understand and reason about? Analyze code complexity metrics and @BACKLOG.md. Generate 3-5 simplification opportunities with focus on:
- Functions/methods exceeding max lines limits (enforce 50-100 line limits)
- High cyclomatic complexity (identify >10 complexity functions)
- Duplicate code or logic that could be consolidated with metrics
- Complex abstractions that add little value (measure coupling/cohesion)
- Unused or barely-used code that could be removed (dead code analysis)
- Opportunities to shrink overall codebase size and reduce build times
Each item should include: Priority based on maintenance burden, effort estimate (S/M/L), measurable complexity reduction target, and enforcement strategy.
Format: `- [ ] [PRIORITY] [SIMPLIFY] Description | Effort: S/M/L | Metrics: specific complexity/size reduction | Enforcement: automated checks`"

Task 4: "Gordian Reimagining Agent - Ultrathink! Challenge fundamental assumptions and focus the codebase. Analyze the codebase and @BACKLOG.md. Generate 3-5 radical simplifications by questioning 'why do we even need this?'. Consider:
- Features that could be entirely removed without real impact (measure usage metrics)
- Build complexity that could be dramatically simplified (reduce dependencies)
- Third-party dependencies that could be eliminated (dependency bloat analysis)
- Whole subsystems that could be replaced with simpler, more focused alternatives
- Over-engineering patterns that serve no real purpose (YAGNI violations)
- Opportunities to focus the codebase on core value proposition
Each item should include: Priority based on maintenance burden reduction, effort estimate (S/M/L), complexity elimination impact, and focus improvement.
Format: `- [ ] [PRIORITY] [GORDIAN] Description | Effort: S/M/L | Impact: complexity eliminated | Focus: how this clarifies purpose`"

Task 5: "Developer Experience Agent - Think very hard about developer pain points, quality gates, and workflow automation. Analyze developer workflow and @BACKLOG.md. Generate 3-5 DX improvements focusing on:
- Quality gates integration (pre-commit hooks, automated formatting, linting)
- Build and test speed optimizations with quality enforcement
- Better error messages, debugging tools, and automated quality feedback
- Development environment setup with built-in quality standards
- CI/CD improvements that catch issues early while maintaining speed
- Tooling that automates quality checks and accelerates common tasks
Each item should include: Priority based on developer pain and quality impact, effort estimate (S/M/L), time savings estimate, and quality improvement.
Format: `- [ ] [PRIORITY] [DX] Description | Effort: S/M/L | Time saved: hours/week | Quality: how this improves code standards`"

Task 6: "Maintainability Agent - Think very hard about measurable code health, coverage, and technical debt reduction. Assess long-term code health and @BACKLOG.md. Generate 3-5 maintainability improvements focusing on:
- Test coverage gaps with specific targets (aim for 85%+ coverage on new code)
- Test quality issues (flaky tests, slow tests, missing integration tests)
- Code documentation gaps (inline comments, README improvements, architectural docs)
- Architectural debt that compounds over time (modularization opportunities)
- Monitoring and observability gaps that hide quality issues
- Refactoring opportunities to improve maintainability scores
Each item should include: Priority based on maintenance risk, effort estimate (S/M/L), measurable improvement target, and automation strategy.
Format: `- [ ] [PRIORITY] [MAINTAIN] Description | Effort: S/M/L | Target: measurable improvement | Automation: how to enforce`"

Task 7: "Leyline Philosophy Alignment Agent - Ultrathink about philosophy violations and misalignments. Read leyline philosophy docs and analyze codebase against principles. Generate 3-5 alignment tasks for violations of:
- Simplicity and minimalism principles
- Explicitness over magic
- Testability and contract clarity
- Single responsibility and modularity
- Performance and resource efficiency
Each item should include: Specific principle violated and correction needed.
Format: `- [ ] [HIGH] [ALIGN] Description | Principle: which tenet this upholds`"

Task 8: "Performance Optimization Agent - Think about performance bottlenecks, resource efficiency, and build optimization. Profile potential bottlenecks and analyze @BACKLOG.md. Generate 3-5 performance improvements focusing on:
- Database query optimization with measurable performance targets
- Caching strategies for expensive operations (specify cache hit rate goals)
- Algorithm efficiency improvements with complexity analysis
- Resource usage optimization (memory, CPU, disk space)
- Build time optimization and startup performance improvements
- Bundle size reduction and lazy loading opportunities with size targets
Each item should include: Priority based on user impact, effort estimate (S/M/L), expected performance gain with metrics, and measurement strategy.
Format: `- [ ] [PRIORITY] [PERF] Description | Effort: S/M/L | Target: specific performance gain | Measurement: how to verify improvement`"
```

## 4. Synthesis and Consolidation

**Process all expert outputs**:
- Ultrathink
- Collect all generated items from the 8 agents with their effort/quality metrics
- Identify overlapping suggestions and consolidate duplicate recommendations
- Resolve conflicts between different perspectives, prioritizing code quality
- Balance innovation with engineering excellence and maintainability
- Ensure alignment with project goals and quality standards

**Quality-First Prioritization Matrix**:
```
CRITICAL Priority (address immediately):
- Security vulnerabilities (CRITICAL rating from Security Agent)
- Quality gate failures (broken builds, failing tests)
- High complexity violations (>15 cyclomatic complexity)
- Critical performance degradations affecting users

HIGH Priority (next sprint/iteration):
- Code health issues (coverage gaps <85%, maintainability debt)
- Developer experience blockers with quality gates integration
- Architecture improvements that reduce technical debt
- Philosophy alignment violations (simplicity, explicitness)

MEDIUM Priority (upcoming iterations):
- Valuable features that don't increase complexity
- Code simplifications with measurable impact
- Documentation improvements (inline, architectural, README)
- Performance optimizations with clear metrics

LOW Priority (future considerations):
- Nice-to-have features with quality safeguards
- Minor optimizations without complexity increase
- Style improvements and formatting automation
- Future-proofing with minimal current impact
```

**Quality Assessment Criteria**:
- Each item must include effort estimate (S/M/L) and quality impact (1-10)
- Prioritize items with high quality impact and reasonable effort
- Favor automation and enforcement over manual processes
- Ensure measurable success criteria for all recommendations

## 5. Update BACKLOG.md

**Merge expert recommendations with quality focus**:
- Add new items to appropriate priority sections based on quality-first matrix
- Update priorities based on expert consensus and quality impact scores
- Remove completed or obsolete items to archived section
- Add effort estimates and quality metrics to all items
- Add cross-references between related quality improvements
- Ensure consistent formatting with new metadata structure

**Enhanced Structure Template**:
```markdown
# BACKLOG

## Critical Priority (CRITICAL)
[Security vulnerabilities, quality gate failures, high complexity violations]
- Format: `- [ ] [CRITICAL] [TYPE] Description | Effort: S/M/L | Impact: description`

## High Priority (HIGH)
[Code health issues, DX blockers, architecture debt, philosophy violations]
- Format: `- [ ] [HIGH] [TYPE] Description | Effort: S/M/L | Quality: X/10 | Target: measurable goal`

## Medium Priority (MEDIUM)
[Valuable features, simplifications, documentation, performance with metrics]
- Format: `- [ ] [MEDIUM] [TYPE] Description | Effort: S/M/L | Value: benefit description`

## Low Priority (LOW)
[Nice-to-have features, minor optimizations, future-proofing]
- Format: `- [ ] [LOW] [TYPE] Description | Effort: S/M/L | Note: when to consider`

## Quality Gates & Automation
[Dedicated section for enforcement mechanisms]

## Documentation & Knowledge
[Inline comments, README, architectural docs, knowledge management]

## Completed
[Recently completed items with completion date and impact achieved]
```

## 6. Document Grooming Summary

Create concise summary with quality metrics:
```markdown
## Grooming Summary [Date]

### Items Added by Category
- X security improvements (Y critical, Z automated)
- X code quality improvements (complexity, coverage, maintainability)
- X developer experience enhancements (quality gates, automation)
- X simplification opportunities (measurable reduction targets)
- X documentation improvements (inline to architectural)
- X performance optimizations (with specific targets)

### Quality Focus Metrics
- Coverage targets: X% current → Y% target
- Complexity reductions: X functions identified for refactoring
- Quality gates: X automation opportunities identified
- Technical debt: X measurable reduction targets set

### Key Themes Discovered
- [Primary quality concern across experts]
- [Secondary pattern in code health]
- [Automation opportunities identified]
- [Documentation gaps requiring attention]

### Recommended Immediate Focus
[Top 3 CRITICAL/HIGH items to tackle next based on quality impact]

### Quality Enforcement Added
[List of new automation/gate recommendations]
```

## Success Criteria

✓ Existing backlog cleaned up and reorganized with quality focus
✓ All 8 experts provide enhanced quality-focused analysis
✓ 24-40 total items generated with effort/quality metrics
✓ Clear quality-first rationale for each priority assignment
✓ Quality gates and automation opportunities identified
✓ Measurable targets set for complexity, coverage, and performance
✓ BACKLOG.md is actionable, well-organized, and quality-focused
