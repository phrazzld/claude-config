Find bugs by thinking, not guessing.

# DEBUG

Channel Kernighan: "The most effective debugging tool is still careful thought, coupled with judiciously placed print statements."

## The Kernighan Principle

"Debugging is twice as hard as writing the code in the first place. Therefore, if you write the code as cleverly as possible, you are, by definition, not smart enough to debug it."

Write simple code. You'll thank yourself later.

## Understand the Problem

Read ISSUE.md carefully. What changed recently? (90% of bugs are in new code.) Can you reproduce it reliably? What's the simplest failing case?

## Form a Hypothesis

**Before touching code**, think through:
- What do you think is broken?
- Why do you think that?
- How will you prove it?
- What if you're wrong?

**Don't debug blind**—make the system visible first:
- Add strategic logging at key decision points
- Instrument data flow through the system
- Capture state at critical transitions
- Log inputs/outputs of failing functions
- Use structured logging for searchability

## Document Explicitly

Before diving into code, write down:
- **Expected behavior**: What should happen per requirements
- **Actual behavior**: What's actually happening (be specific)
- **Difference**: Where reality diverges from expectation
- **Reproduction steps**: Exact steps to trigger issue
- **Environment**: Specific conditions where bug occurs

Write your hypothesis before testing it. Document evidence supporting or refuting it. Keep a log of what you tried and learned.

## Systematic Investigation

**Binary search the problem space**:
- **When**: Find when it broke using git history
- **Where**: Find where it breaks using search tools
- **Why**: Find why it breaks using targeted logging

**Check usual suspects**:
1. Off-by-one: boundaries, loops, array indices
2. Null/undefined: missing checks, race conditions
3. State mutations: shared state, side effects
4. Async issues: race conditions, promise chains
5. Type mismatches: string vs number, implicit conversions

## Fix With Simplicity

**Choose the simplest fix that solves the problem completely**. Don't refactor or optimize while fixing bugs—complex fixes introduce new bugs. Save architectural improvements for separate tasks.

- Fix with minimal code change
- Avoid clever workarounds when straightforward fix exists
- Don't add abstractions to fix concrete problem
- Resist fixing unrelated issues you notice
- Keep focused on actual problem

**Can you explain the fix in one sentence?** If not, simplify.

## Root Cause Documentation

Document what you found:
- **What**: The specific failure mechanism
- **Where**: Exact file and line number
- **Why**: The actual reason (not symptoms)
- **When**: Conditions that trigger the bug

Add a test that captures this specific bug. Verify the bug reproduces before the fix, disappears after, and no new bugs introduced.

## Post-Mortem

Ask yourself:
- Why didn't tests catch this?
- What similar bugs might exist?
- How can we prevent this class of bugs?
- Is the fix simpler than the bug?

## Three Laws of Debugging

1. **It's always your code** (until proven otherwise)
2. **The bug is not where you think it is** (check your assumptions)
3. **Read the error message** (yes, the whole thing)

Remember: **The best debugger is a fresh pair of eyes and a good night's sleep.**
