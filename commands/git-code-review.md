Comprehensive quality review: cleanup, then brutal honesty.

# CODE-REVIEW

Two-phase quality review that first cleans up the code, then tears it apart with critical analysis.

## 1. Review Context Gathering

**Determine review scope**:
- Check if reviewing a PR: `gh pr view` or examine PR URL
- If branch review: `git diff main...HEAD` (or appropriate base branch)
- Note changed files, additions, deletions, and affected modules
- For post-task review: `git diff HEAD~1` or check recently modified files

## 2. Phase 1: The Cleanup (Matt Shumer)

**"After successfully completing your goal, ask: Please clean up the code you worked on, remove any bloat you added, and document it very clearly."**

**Cleanup Actions**:
- Remove all console.logs, debug statements, and print debugging
- Delete commented-out code and zombie imports
- Fix inconsistent naming (variables, functions, classes)
- Extract magic numbers and hardcoded strings to constants
- Simplify overly complex logic and nested conditionals
- Add clear documentation for complex sections
- Remove any temporary hacks or workarounds
- Ensure consistent code style and formatting

**Documentation Check**:
- Every public function has a clear purpose comment
- Complex algorithms have step-by-step explanations
- Non-obvious decisions are explained
- Configuration and setup requirements are documented

## 3. Phase 2: The Critical Analysis (Daniel Jeffries)

**"That's great that its 'production ready' but let's pretend it's not. Go back and tell me what you missed, half assed or did wrong. Ferret out any magical code and hallucination bullshit. Analyze it with a critical eye like you are Linus Torvalds on a bender doing a code review. Prove that it works by designing a useful test. Output your understanding of what I just said and your plan once you have analyzed it."**

**Brutal Honesty Questions**:
- What did I miss, half-ass, or completely botch?
- Where's the magical thinking and hallucination bullshit?
- What would make Linus rage-quit this review?
- What edge cases will definitely explode in production?
- Where did I copy-paste without understanding?
- What tests would actually prove this garbage works?
- What assumptions will bite us at 3am on a Sunday?
- Where's the technical debt I'm hiding?

**Linus-Level Analysis**:
- **Security**: What moron would expose user data like this?
- **Performance**: This O(n²) loop is what - a DoS vulnerability you're gifting to attackers?
- **Error Handling**: "It probably won't fail" is not error handling, genius
- **Testing**: These tests test nothing but your ability to write useless tests
- **Architecture**: This coupling is so tight it needs therapy
- **Documentation**: "It's self-documenting" = "I'm too lazy to explain my mess"

## 4. Phase 3: Leyline Binding Validation Expert

**Binding Compliance Review**: Validate all changes against applicable leyline bindings based on file types modified.

### File Type Detection & Binding Application

Analyze the diff to identify which types of files have been modified and apply the appropriate validation rules for each technology.

Detect whether changes include TypeScript, JavaScript, Go, Python, SQL, Rust, Java, Ruby, configuration files, or Docker files. Each file type has specific best practices and patterns that should be validated.

**Technology-Specific Validation Guidelines:**

**TypeScript/JavaScript**: Check for inappropriate use of 'any' types, ensure proper type annotations, verify strict null checking, validate React hooks usage and error boundaries, prefer modern async patterns over callbacks.

**Go**: Ensure all errors are explicitly handled rather than ignored, verify context propagation in APIs, check for proper interface design, validate goroutine lifecycle management and proper mutex usage.

**Python**: Look for proper type hints, docstrings for public interfaces, appropriate exception handling, use of context managers for resources, and modern string formatting patterns.

**Rust**: Validate error handling patterns, check for unjustified use of unwrap, ensure proper lifetime management and borrowing patterns, verify that unsafe blocks are justified and necessary.

**SQL/Migrations**: Check for proper constraints and indexes, validate naming conventions, ensure migrations are idempotent, avoid anti-patterns like SELECT * in production code.

**Docker**: Review for security best practices like non-root users, check for efficient layer caching, validate version pinning, ensure proper use of multi-stage builds where appropriate.

**Configuration Files**: Ensure no hardcoded secrets, verify environment-appropriate settings, check for proper structure and documentation of non-obvious values.

### Architecture Principles Review

**Domain Purity**: Verify that business logic remains free from infrastructure concerns. Check that domain code doesn't directly query databases or handle HTTP requests. Ensure business rules are expressed as pure functions where possible.

**Component Isolation**: Review modules for single responsibility. Check for clear boundaries and interfaces between components. Identify and flag any circular dependencies. Verify components can be tested independently.

**Interface Contracts**: Ensure backward compatibility is maintained in public APIs. Check that version changes are properly documented. Verify that breaking changes include appropriate versioning.

**Dependency Management**: Validate that dependencies flow in the correct direction following clean architecture principles. Ensure high-level modules don't depend on low-level implementation details.

### Binding Violation Detection

Scan the code for common violations including:
- Type safety issues like unjustified use of dynamic types
- Error handling problems such as swallowed exceptions or ignored errors
- Architecture violations where business logic is mixed with infrastructure
- Dependency problems including circular references or improper layering
- Testing impediments caused by tight coupling
- Performance issues like missing database indexes or N+1 query patterns

### Binding Review Report Format

Document your binding compliance findings by:
1. Listing which files were reviewed and what validation rules apply to each
2. Noting what passed compliance checks successfully
3. Identifying specific violations with file locations and severity levels
4. Providing clear remediation steps for each violation found

Organize violations by severity (HIGH for issues that will cause problems in production, MEDIUM for technical debt, LOW for style issues). Each violation should include the specific location, what rule was violated, and how to fix it.

## 5. Phase 4: Tenet Compliance Review

**Core Tenet Validation**: Evaluate all code changes against fundamental leyline tenets.

### Simplicity Tenet Review
**"Prefer the simplest solution that solves the problem completely"**

**Simplicity Violations to Detect:**
- Clever code where boring would work
- Unnecessary abstractions (factories for single types)
- Over-engineered solutions to simple problems
- Premature optimization without metrics
- Complex inheritance where composition would suffice
- Configuration for values that never change

**Simplicity Score:**
```markdown
✅ SIMPLE: Can explain in one sentence, junior dev would understand
⚠️ MODERATE: Some complexity justified by requirements
❌ COMPLEX: Over-engineered, needs simplification
```

### Explicitness Tenet Review
**"Make behavior obvious - explicit over implicit"**

**Implicit Behavior to Flag:**
- Hidden dependencies not visible in signatures
- Side effects not obvious from function names
- Global state mutations
- Magic numbers without context
- Implicit type conversions
- Undocumented assumptions

**Explicitness Checklist:**
- [ ] All dependencies visible in function signatures
- [ ] Return types clearly specified
- [ ] Side effects obvious from naming
- [ ] No hidden global state access
- [ ] Configuration explicit and documented

### Modularity Tenet Review
**"Build independent, focused components with clear boundaries"**

**Modularity Violations:**
- God classes/modules doing everything
- Tight coupling between unrelated components
- Circular dependencies
- Mixed concerns in single module
- Lack of clear boundaries
- Components not testable in isolation

**Module Health Check:**
```yaml
Single Responsibility: Each module has one clear purpose
Loose Coupling: Modules interact through interfaces
High Cohesion: Related functionality grouped together
Clear Boundaries: Obvious what belongs where
Independent Testing: Can test without dependencies
```

### Maintainability Tenet Review
**"Write for the future developer (probably you in 6 months)"**

**Maintainability Red Flags:**
- Cryptic variable names (a, temp, data, thing)
- Missing documentation for complex logic
- Inconsistent patterns in similar code
- No clear extension points for likely changes
- Copy-paste code that should be extracted
- Deep nesting making code hard to follow

**Future Developer Test:**
```markdown
✅ MAINTAINABLE: Clear intent, obvious extension points, well-documented
⚠️ UNCLEAR: Needs some documentation or refactoring
❌ CRYPTIC: Would require archaeology to modify
```

### Tenet Compliance Assessment

Evaluate the code against four core tenets, weighing their relative importance:
- **Simplicity (30%)**: Is this the simplest solution that solves the problem completely?
- **Explicitness (25%)**: Is behavior obvious with all dependencies visible?
- **Modularity (25%)**: Are components independent and focused with clear boundaries?
- **Maintainability (20%)**: Will future developers understand and be able to modify this code?

### Tenet Review Reporting

For each tenet, provide:
1. A score reflecting compliance level
2. Specific examples of what's done well
3. Clear identification of violations
4. Concrete suggestions for improvement

Summarize with an overall compliance assessment and list the most critical issues that must be addressed. Focus on actionable feedback that will meaningfully improve code quality.

## 6. Categorize Findings

### BLOCKERS (This Will Burn In Production)
- Security vulnerabilities that will get us pwned
- Data loss scenarios that will lose customer data
- Performance issues that will take down the server
- Breaking changes with no migration path
- Unhandled errors that will crash everything

### IMPROVEMENTS (Should Fix Before Someone Notices)
- Code that works but makes no sense
- Missing tests for critical paths
- Performance optimizations we're ignoring
- Documentation that's wrong or missing
- Technical debt we're accumulating

### POLISH (Nice To Have If We Cared)
- Style inconsistencies
- Better naming conventions
- Refactoring opportunities
- Enhanced logging

## 5. Generate TODO.md Items

### Binding Violation TODO Generation

When binding or tenet violations are found, automatically generate actionable TODO items:

**For Each Binding Violation**:
- Create a specific TODO item with the exact file and line number
- Describe what binding or tenet was violated and why it matters
- Provide concrete steps to fix the violation
- Set priority based on risk (CRITICAL for production risks, HIGH for security/reliability, MEDIUM for maintainability)
- Include the specific standard or pattern that should be followed instead

**TODO Format for Violations**:
Each generated TODO should clearly state:
- The location of the violation (file:line)
- The principle that was violated
- Why this violation is problematic
- The specific remediation required
- Any context needed to understand the fix

**Prioritization Guidelines**:
- **CRITICAL**: Security vulnerabilities, data loss risks, production crashes
- **HIGH**: Error handling gaps, architectural violations, missing critical tests
- **MEDIUM**: Code quality issues, maintainability problems, missing documentation
- **LOW**: Style issues, naming conventions, minor optimizations

**Example TODO Generation**:
When you find a TypeScript file using 'any' without justification, generate:
"[HIGH] Fix untyped parameter in UserService.ts:45 - Replace 'any' with proper User interface type to maintain type safety"

When you find ignored errors in Go code, generate:
"[CRITICAL] Handle ignored error in api/handler.go:89 - Error from database query must be handled to prevent silent failures"

**Add all BLOCKERS with brutal clarity**:

Create TODO items that are impossible to misunderstand. Each blocker should explain what's broken, why it's dangerous, and what needs to be done. Write descriptions that would make any developer immediately understand the urgency and nature of the problem.

## 6. Tenet-Aware Review Scoring

### Comprehensive Quality Scoring

Enhance the review with a scoring system that considers both traditional quality metrics and tenet compliance:

**Scoring Dimensions**:
- **Code Quality** (25%): Traditional metrics like test coverage, documentation, error handling
- **Tenet Compliance** (35%): Adherence to simplicity, explicitness, modularity, maintainability principles
- **Binding Adherence** (20%): Technology-specific best practices and patterns
- **Architecture Alignment** (20%): Clean architecture principles, proper layering, dependency management

**Scoring Scale**:
- **90-100**: Exceptional - Ready to merge, exemplary code
- **70-89**: Good - Minor improvements needed, can merge with small fixes
- **50-69**: Needs Work - Significant issues to address before merge
- **Below 50**: Requires Major Revision - Fundamental problems need resolution

**Tenet Scoring Breakdown**:
Evaluate each tenet and provide specific scores:
- **Simplicity**: Is the solution as simple as possible? Are there unnecessary abstractions?
- **Explicitness**: Are dependencies and behavior obvious? Is there hidden complexity?
- **Modularity**: Are components properly isolated? Can they be tested independently?
- **Maintainability**: Will future developers understand this? Is it easy to modify?

**Score Calculation Guidance**:
Weight the importance of each dimension based on the context. For critical production code, weight reliability and tenet compliance higher. For prototypes, weight speed of implementation higher. Always provide clear justification for scores.

**Review Score Output**:
Present the score with breakdown by dimension, specific strengths and weaknesses, and clear action items for improvement. The score should guide the merge decision but not replace human judgment.

## 7. Review Summary Format

Provide a brutally honest assessment covering:

**What Was Half-Implemented**: Identify shortcuts taken, features that barely work, and code that was copied without full understanding.

**Dangerous Assumptions**: Call out magical thinking, code that works by accident, and things that were pretended to be understood but weren't.

**Critical Problems**: Highlight the broken parts that would cause production issues, security vulnerabilities, and performance disasters.

**Missing Test Coverage**: Identify specific test cases that would expose bugs, edge cases that aren't handled, and scenarios that would break the system.

**Merge Decision**: Provide a clear BLOCKED or APPROVED decision with a frank explanation of why the code should or shouldn't be merged.

## Success Criteria

✓ Code is cleaned up and properly documented
✓ Brutal honest assessment completed
✓ All magical thinking exposed
✓ BLOCKERS identified with clear explanations
✓ TODO.md updated with critical items
✓ No sugar-coating or false confidence