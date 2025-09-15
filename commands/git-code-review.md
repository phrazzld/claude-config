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

## 4. Categorize Findings

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

**Add all BLOCKERS with Linus-level clarity**:
```markdown
## Code Review Blockers - [Branch/PR Name] [Date]

- [ ] [CRITICAL] Fix SQL injection in user search - currently concatenating user input like it's 1999
- [ ] [CRITICAL] Add ANY tests for payment processing - zero coverage on code handling actual money
- [ ] [CRITICAL] Fix O(n²) algorithm in notifications - will melt server with >1000 users
- [ ] [CRITICAL] Handle network timeouts - currently just praying the network never fails
```

## 6. Output Summary

```markdown
## Review Summary

### What I Half-Assed
- [Honest admission of shortcuts taken]
- [Features that barely work]
- [Code I copied without understanding]

### Magical Thinking & Hallucination Bullshit
- [Assumptions that are definitely wrong]
- [Code that works by accident]
- [Things I pretended to understand]

### What Would Make Linus Rage
- [The absolutely broken garbage]
- [Security holes you could drive a truck through]
- [Performance disasters waiting to happen]

### Tests That Would Actually Prove It Works
- [Specific test cases that would expose the bugs]
- [Edge cases I'm definitely not handling]
- [Load tests that would break everything]

### Merge Decision: [BLOCKED/APPROVED]
[Clear explanation of why this should or shouldn't merge]
```

## Success Criteria

✓ Code is cleaned up and properly documented
✓ Brutal honest assessment completed
✓ All magical thinking exposed
✓ BLOCKERS identified with clear explanations
✓ TODO.md updated with critical items
✓ No sugar-coating or false confidence