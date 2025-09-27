Conduct a comprehensive review of the codebase to identify opportunities for improvement across all dimensions.

# GROOM

Step back and see the whole system. What would make this better?

## The Discovery Principle

*"The best problems to solve are the ones you find, not the ones you're given."* - Every Senior Engineer

Look for opportunities, not just problems. Think holistically about what would improve the product, the codebase, and the development experience.

## 1. Start Fresh

First, clean up any existing backlog. Archive what's done, remove what's obsolete, and group what remains by theme. This gives you a clean slate to work with.

Ask yourself: "Would I actually work on this in the next quarter?" If not, it probably doesn't belong in the active backlog.

## 2. Comprehensive Codebase Audit

Use the helper agent to conduct a thorough quality analysis. Ask it to examine the codebase from multiple angles - security, performance, maintainability, test coverage, dependencies.

You're looking for anything that affects the health and velocity of the system. The agent should identify specific issues and opportunities, not vague concerns. Each finding should be actionable - something a developer could pick up and work on tomorrow.

## 3. Consider Development Principles

As you review the codebase, think about where fundamental principles are being violated.

Is there unnecessary complexity that could be simplified? Are there tightly coupled modules that should be independent? Is there hidden behavior that should be explicit? Would a new developer struggle to understand certain areas?

These principle violations often compound over time. A confusing abstraction in a core module affects everything built on top of it. Tightly coupled components make changes risky and slow. Hidden dependencies create debugging nightmares.

When you find these issues, consider their ripple effects. Sometimes fixing a fundamental problem in the architecture is worth more than adding three new features.

## 4. Technology-Specific Considerations

Different technologies have their own patterns and pitfalls.

In TypeScript, are you bypassing the type system with 'any' types? In Go, are errors being ignored when they should be handled? In React, is state management clear and predictable? In your database layer, are queries optimized and migrations safe?

Security concerns cut across all technologies. Authentication bugs, authorization gaps, unvalidated inputs - these issues have real consequences and deserve attention regardless of where they appear.

When you find issues that violate both general principles and technology-specific best practices, they're usually worth addressing sooner rather than later. They tend to cause problems from multiple angles.

## 5. Think About Impact and Priority

Now comes the judgment call - what matters most?

Consider multiple dimensions: Will this improve the user experience? Will it make development faster? Will it prevent future problems? Will it reduce operational burden?

Some items are obviously critical - security vulnerabilities, data loss risks, broken core functionality. These go to the top of the list.

Beyond the critical issues, use your engineering instincts. A performance improvement that affects every user might matter more than a new feature that helps a few. A refactoring that unblocks three other features might be worth doing first. A fix that prevents weekly firefighting could save more time than it costs.

Don't overthink the prioritization. You know what matters. Trust your judgment about what would make the biggest positive impact on the product and the team.

## 6. Include Clear Next Steps

For each backlog item, briefly describe not just what the problem is, but how to approach fixing it.

If something is overly complex, the fix might be to remove abstractions rather than add them. If modules are tightly coupled, identify where to draw boundaries. If behavior is hidden, surface it in function signatures or return values.

The goal is to make each backlog item actionable. A developer should be able to pick it up and know where to start. They don't need step-by-step instructions, just enough context to approach the problem effectively.

## 7. Organize Your Findings

Structure your backlog in a way that makes sense for the team. Group related items together. Note any dependencies between tasks. Be clear about the value and effort of each item.

A simple, effective structure might look like:

```markdown
# BACKLOG.md

## Immediate Concerns
Things that need attention right now - security issues, broken functionality, critical performance problems.

## High-Value Improvements
Changes that would significantly improve user experience, developer velocity, or system reliability.

## Technical Debt Worth Paying
Refactorings and cleanups that would make future development easier and faster.

## Nice to Have
Improvements that would be valuable but aren't urgent - optimizations, new features, quality-of-life improvements.

## Completed/Archived
Track what's been done and what's been deliberately decided against.
```

Use whatever organization makes sense for your context. The goal is clarity and actionability.

## What Success Looks Like

You've done a good job if:
- Each item is clear and actionable - a developer could pick it up and start working
- The most important items are obvious - the team knows what to tackle first
- There's a good mix of quick wins and important long-term improvements
- The backlog reflects the real needs of both users and developers

The backlog should feel like a map of opportunities, not a list of complaints. It should energize the team about what's possible, not overwhelm them with what's broken.