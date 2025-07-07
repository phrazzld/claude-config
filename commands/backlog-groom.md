Organize, prioritize, and enhance BACKLOG.md using parallel expert analysis from 8 specialized perspectives.

# GROOM

Organize, prioritize, and enhance @BACKLOG.md by launching 8 parallel expert agents who analyze the project from their unique perspectives and generate targeted improvements.

## 1. Prepare Context

**Read foundational documents**:
- Read current @BACKLOG.md to understand existing tasks and structure
- Read project-specific leyline documents in `./docs/leyline/` if they exist
- Note current project architecture, tech stack, and recent changes
- Identify any existing priority indicators or categories

## 2. Parallel Expert Analysis

Launch 8 expert agents using the Task tool to analyze the project and generate backlog items:

```
Task 1: "Creative/Product Innovation Agent - Think hard about innovative possibilities. Analyze the project codebase and @BACKLOG.md. Generate 3-5 innovative feature ideas that could dramatically improve user experience or unlock new capabilities. Consider:
- Emerging patterns in the codebase that suggest new possibilities
- User pain points that could be addressed creatively
- Opportunities for delightful surprises or '10x better' experiences
- Integration opportunities with modern tools/services
Each item should include: Priority (HIGH/MEDIUM/LOW), estimated complexity, and innovation rationale.
Format: `- [ ] [PRIORITY] [FEATURE] Description | Innovation: why this is game-changing`"

Task 2: "Security Audit Agent - Think very hard about security vulnerabilities and risks. Conduct thorough security analysis of the codebase and @BACKLOG.md. Generate 3-5 security improvements. Examine:
- Authentication and authorization patterns
- Data validation and sanitization practices  
- Dependency vulnerabilities
- Secrets management and configuration security
- API security and rate limiting needs
Each item should include: Priority (HIGH for vulnerabilities, MEDIUM for hardening, LOW for best practices), and security impact.
Format: `- [ ] [PRIORITY] [SECURITY] Description | Risk: what threat this addresses`"

Task 3: "Codebase Simplification Agent - Think about code complexity and simplification opportunities. Analyze code complexity and @BACKLOG.md. Generate 3-5 simplification opportunities. Look for:
- Over-engineered solutions that could be simplified
- Duplicate code or logic that could be consolidated
- Complex abstractions that add little value
- Unused or barely-used code that could be removed
- Convoluted flows that could be streamlined
Each item should include: Priority based on maintenance burden, and simplification impact.
Format: `- [ ] [PRIORITY] [SIMPLIFY] Description | Impact: lines removed or complexity reduced`"

Task 4: "Gordian Reimagining Agent - Ultrathink! Challenge fundamental assumptions in the codebase and @BACKLOG.md. Generate 3-5 radical simplifications by questioning 'why do we even need this?'. Consider:
- Features that could be entirely removed without real impact
- Architectural patterns that could be dramatically simplified
- Third-party dependencies that could be eliminated
- Whole subsystems that could be replaced with simpler alternatives
- 'Sacred cows' that no longer serve their purpose
Format: `- [ ] [PRIORITY] [GORDIAN] Description | Breakthrough: what assumption this challenges`"

Task 5: "Developer Experience Agent - Think about developer pain points and workflow friction. Analyze developer workflow and @BACKLOG.md. Generate 3-5 DX improvements. Focus on:
- Build and test speed optimizations
- Better error messages and debugging tools
- Development environment setup simplification
- Documentation gaps that slow developers
- Tooling that could accelerate common tasks
Each item should include: Priority based on developer pain, and time savings estimate.
Format: `- [ ] [PRIORITY] [DX] Description | Time saved: estimated hours per week`"

Task 6: "Maintainability Agent - Think hard about long-term code health and technical debt. Assess long-term code health and @BACKLOG.md. Generate 3-5 maintainability improvements. Evaluate:
- Test coverage gaps and test quality issues
- Code that's hard to understand or modify
- Missing documentation for complex areas
- Architectural debt that compounds over time
- Monitoring and observability gaps
Each item should include: Priority based on maintenance risk, and maintainability score improvement.
Format: `- [ ] [PRIORITY] [MAINTAIN] Description | Debt: what future pain this prevents`"

Task 7: "Leyline Philosophy Alignment Agent - Think hard about philosophy violations and misalignments. Read leyline philosophy docs and analyze codebase against principles. Generate 3-5 alignment tasks for violations of:
- Simplicity and minimalism principles
- Explicitness over magic
- Testability and contract clarity
- Single responsibility and modularity
- Performance and resource efficiency
Each item should include: Specific principle violated and correction needed.
Format: `- [ ] [HIGH] [ALIGN] Description | Principle: which tenet this upholds`"

Task 8: "Performance Optimization Agent - Think hard about performance bottlenecks and optimization opportunities. Profile potential bottlenecks and analyze @BACKLOG.md. Generate 3-5 performance improvements. Consider:
- Database query optimization opportunities
- Caching strategies for expensive operations
- Algorithm efficiency improvements
- Resource usage optimization
- Startup time and lazy loading opportunities
Each item should include: Priority based on user impact, and expected performance gain.
Format: `- [ ] [PRIORITY] [PERF] Description | Gain: expected improvement metrics`"
```

## 3. Synthesis and Consolidation

**Process all expert outputs**:
- Collect all generated items from the 8 agents
- Identify overlapping suggestions and consolidate
- Resolve conflicts between different perspectives
- Balance innovation with stability
- Ensure alignment with project goals

**Prioritization matrix**:
```
HIGH Priority:
- Security vulnerabilities
- Critical performance issues  
- Major DX blockers
- Philosophy alignment violations

MEDIUM Priority:
- Valuable features
- Code simplifications
- Maintainability improvements
- Non-critical optimizations

LOW Priority:
- Nice-to-have features
- Minor optimizations
- Style improvements
- Future-proofing
```

## 4. Update BACKLOG.md

**Merge expert recommendations**:
- Add new items to appropriate sections
- Update priorities based on expert consensus
- Remove completed or obsolete items
- Add cross-references between related items
- Ensure consistent formatting

**Structure template**:
```markdown
# BACKLOG

## Critical Priority
[Items marked HIGH by multiple experts or security/performance critical]

## High Value
[Items with strong rationale from 2+ experts]

## Technical Debt
[Simplification and maintainability items]

## Future Considerations
[Innovation and nice-to-have items]

## Completed
[Archive of recently completed items]
```

## 5. Document Grooming Summary

Create concise summary:
```markdown
## Grooming Summary [Date]

### Items Added
- X security improvements (Y critical)
- X simplification opportunities
- X innovation features
- X DX enhancements

### Key Themes
- [Primary concern across experts]
- [Secondary pattern identified]
- [Unexpected discovery]

### Recommended Focus
[Top 3 items to tackle next based on expert consensus]
```

## Success Criteria

✓ All 8 experts provide perspective-specific analysis
✓ 24-40 total items generated (3-5 per expert)
✓ Clear rationale for each priority assignment
✓ Consolidated list balances all perspectives
✓ BACKLOG.md is actionable and well-organized