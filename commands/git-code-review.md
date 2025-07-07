Conduct comprehensive code review using parallel expert analysis to identify merge blockers and improvement opportunities.

# REVIEW-CODE

Perform thorough code review of the current PR/branch using 8 specialized experts who identify critical blockers and enhancement opportunities.

## 1. Review Context Gathering

**Determine review scope**:
- Check if reviewing a PR: `gh pr view` or examine PR URL
- If branch review: `git diff main...HEAD` (or appropriate base branch)
- Note changed files, additions, deletions, and affected modules
- Identify review priorities based on change scope

**Prepare review environment**:
- Ensure latest changes are pulled
- Run any existing tests to establish baseline
- Note any CI/CD status if available

## 2. Parallel Expert Code Review

Launch 8 expert reviewers using the Task tool. Each expert examines the changes and categorizes findings as BLOCKERS (must-fix) or IMPROVEMENTS (nice-to-have):

```
Task 1: "Security Review Expert - Think very hard about security implications of the changes. Examine:
- Authentication/authorization changes
- Input validation and sanitization
- Potential injection vulnerabilities
- Secrets or sensitive data exposure
- Dependency security issues
- CORS/CSP/security header changes
Categorize each finding as:
BLOCKER: Security vulnerabilities, auth bypasses, data exposure
IMPROVEMENT: Security hardening, defense in depth
Format: `[BLOCKER/IMPROVEMENT] Description | Risk: specific threat`"

Task 2: "Code Quality Expert - Think hard about code maintainability and clarity. Review:
- Code readability and naming conventions
- Function/class complexity (cyclomatic complexity)
- DRY violations and code duplication
- SOLID principle adherence
- Magic numbers and hardcoded values
- Code organization and structure
Categorize findings as:
BLOCKER: Severe readability issues, major DRY violations, unmaintainable code
IMPROVEMENT: Minor refactoring, naming improvements, style consistency
Format: `[BLOCKER/IMPROVEMENT] Description | Impact: maintenance burden`"

Task 3: "Testing Expert - Think hard about test coverage and quality. Analyze:
- Missing tests for new functionality
- Edge case coverage
- Test quality and assertions
- Mocking and test isolation
- Integration test needs
- Performance test requirements
Categorize findings as:
BLOCKER: Zero test coverage for critical paths, broken tests
IMPROVEMENT: Additional edge cases, test refactoring, coverage gaps
Format: `[BLOCKER/IMPROVEMENT] Description | Coverage: what's missing`"

Task 4: "Performance Expert - Think hard about efficiency and scalability. Investigate:
- Algorithm complexity (O(n²) or worse)
- Database query efficiency (N+1, missing indexes)
- Memory leaks or excessive allocation
- Caching opportunities
- Async/parallel processing potential
- Resource usage patterns
Categorize findings as:
BLOCKER: O(n²)+ algorithms, severe memory leaks, obvious N+1 queries
IMPROVEMENT: Caching opportunities, minor optimizations
Format: `[BLOCKER/IMPROVEMENT] Description | Impact: performance metric`"

Task 5: "Architecture Expert - Think hard about design patterns and system structure. Evaluate:
- Coupling and cohesion
- Layer violations
- Design pattern appropriateness
- API contract changes
- Backward compatibility
- Scalability considerations
Categorize findings as:
BLOCKER: Breaking changes without migration, severe coupling, layer violations
IMPROVEMENT: Better patterns, decoupling opportunities, future-proofing
Format: `[BLOCKER/IMPROVEMENT] Description | Design: principle violated`"

Task 6: "Error Handling Expert - Think about robustness and failure scenarios. Check:
- Exception handling completeness
- Error message quality
- Graceful degradation
- Retry logic appropriateness
- Logging and observability
- User-facing error experiences
Categorize findings as:
BLOCKER: Unhandled exceptions, data loss on errors, poor error recovery
IMPROVEMENT: Better error messages, enhanced logging, retry strategies
Format: `[BLOCKER/IMPROVEMENT] Description | Failure: scenario not handled`"

Task 7: "Documentation Expert - Think about knowledge transfer and clarity. Review:
- Code comments for complex logic
- API documentation completeness
- README updates for new features
- Architecture decision records
- Configuration documentation
- Migration guides if needed
Categorize findings as:
BLOCKER: Missing critical setup docs, undocumented breaking changes
IMPROVEMENT: Better comments, enhanced examples, clarifications
Format: `[BLOCKER/IMPROVEMENT] Description | Gap: what's missing`"

Task 8: "API Design Expert - Think hard about interface design and usability. Assess:
- API consistency and conventions
- Request/response schema design
- Versioning strategy
- Rate limiting and quotas
- Error response formats
- REST/GraphQL best practices
Categorize findings as:
BLOCKER: Breaking API changes, inconsistent schemas, missing versioning
IMPROVEMENT: Better naming, enhanced responses, consistency fixes
Format: `[BLOCKER/IMPROVEMENT] Description | API: design issue`"
```

## 3. Synthesis and Categorization

**Consolidate all findings**:
- Collect all BLOCKER findings from experts
- Collect all IMPROVEMENT findings from experts
- Remove duplicates while preserving unique perspectives
- Prioritize based on severity and impact

**Validation criteria for blockers**:
- Security vulnerabilities
- Data loss risks
- Breaking changes without migration
- Severe performance regressions
- Unhandled critical errors
- Zero test coverage for critical paths

## 4. Generate TODO.md Items

**Create high-priority tasks for all blockers**:
```markdown
## Code Review Blockers - [Branch/PR Name] [Date]

- [ ] [HIGH] Fix SQL injection vulnerability in user search | Security: user input directly concatenated
- [ ] [HIGH] Add tests for payment processing logic | Testing: 0% coverage on critical financial path
- [ ] [HIGH] Fix O(n²) algorithm in notification system | Performance: will not scale beyond 1000 users
- [ ] [HIGH] Handle network timeout in API client | Error: data loss on connection failure
```

## 5. Generate BACKLOG.md Items

**Add improvements to backlog with appropriate sections**:
```markdown
## Code Review Improvements - [Branch/PR Name] [Date]

### Performance Optimization
- [ ] [MEDIUM] Add caching for user preferences API | Performance: reduce 90% of repeated queries
- [ ] [LOW] Consider pagination for admin dashboard | Performance: currently loads all records

### Code Quality
- [ ] [MEDIUM] Refactor UserService to reduce complexity | Quality: cyclomatic complexity of 15
- [ ] [LOW] Rename variables for clarity in data processor | Quality: improve readability

### Testing
- [ ] [LOW] Add edge case tests for date parsing | Testing: enhance robustness
- [ ] [LOW] Consider property-based testing for validators | Testing: catch more edge cases
```

## 6. Review Summary

**Generate actionable summary**:
```markdown
## Review Summary for [Branch/PR Name]

### Merge Decision: BLOCKED/APPROVED

### Critical Blockers (4)
1. Security vulnerability in authentication
2. Missing tests for payment flow
3. Performance regression in search
4. Data loss risk on errors

### Improvement Opportunities (8)
- 3 performance optimizations
- 2 code quality enhancements
- 2 testing improvements
- 1 documentation update

### Commendations
- Excellent error handling in module X
- Well-structured API design
- Comprehensive test coverage in module Y
```

## Success Criteria

✓ All 8 experts complete their specialized review
✓ Clear distinction between blockers and improvements
✓ Blockers are actionable and specific
✓ TODO.md updated with high-priority blockers
✓ BACKLOG.md updated with improvement opportunities
✓ Summary provides clear merge decision