Find bugs by thinking, not by guessing.

# DEBUG

Channel Kernighan: "The most effective debugging tool is still careful thought, coupled with judiciously placed print statements."

## The Kernighan Principle

*"Debugging is twice as hard as writing the code in the first place."*

If you wrote clever code, you're not smart enough to debug it. Write simple code.

## 1. Understand the Problem

**What would Kernighan ask first?**
- Read @ISSUE.md carefully
- What changed recently? (90% of bugs are in new code)
- Can you reproduce it reliably?
- What's the simplest failing case?

## 2. Form a Hypothesis

**The Pike Philosophy: "Don't guess, measure"**

Before touching code:
- What do you think is broken?
- Why do you think that?
- How will you prove it?
- What will you do if you're wrong?

### 🎯 Observability First

**Make the System Visible**:
Don't debug in the dark. Add instrumentation to see what's actually happening. Use logging, metrics, and tracing to understand system behavior. Make the invisible visible before trying to fix it.

**Observability Strategy**:
- Add strategic logging at key decision points
- Instrument the data flow through the system
- Capture state at critical transitions
- Log inputs and outputs of failing functions
- Use structured logging for better searchability

**What to Observe**:
- Input values that trigger the bug
- State changes during execution
- Timing and sequence of operations
- Resource usage at failure point
- Error propagation paths

## 3. Systematic Investigation

### 🎯 Explicit Debugging Documentation

**Document Actual vs Expected**:
Before diving into code, explicitly document what you expect to happen versus what actually happens. Clear documentation of the discrepancy guides your investigation and prevents assumptions.

**Explicit Bug Documentation**:
- **Expected Behavior**: What should happen according to requirements
- **Actual Behavior**: What is actually happening (be specific)
- **Difference**: Precisely where reality diverges from expectation
- **Reproduction Steps**: Exact steps to trigger the issue
- **Environment**: Specific conditions where bug occurs

**Hypothesis Documentation**:
Write down your hypothesis before testing it. Document why you think this is the cause. Record what evidence supports or refutes your hypothesis. Keep a log of what you've tried and learned.

**The Binary Search Method:**

Use systematic approaches to narrow down the problem:
- Find when it broke using git history
- Find where it breaks using search tools
- Find why it breaks using targeted logging
- Document each finding explicitly

## 4. Common Bug Patterns

**The Thompson Test: "When in doubt, use brute force"**

Check the usual suspects:
1. **Off-by-one**: Boundaries, loops, array indices
2. **Null/undefined**: Missing checks, race conditions
3. **State mutations**: Shared state, side effects
4. **Async issues**: Race conditions, promise chains
5. **Type mismatches**: String vs number, implicit conversions

## 5. Fix Strategy

**The Ritchie Rule: "The only way to learn a new programming language is by writing programs in it"**

### 🎯 Simplicity in Debug Solutions

**Choose the Simplest Fix**:
When debugging, prefer the simplest solution that solves the problem. Avoid the temptation to refactor or optimize while fixing bugs. Complex fixes often introduce new bugs. Save architectural improvements for separate tasks.

**Simplicity Guidelines**:
- Fix the bug with minimal code changes
- Avoid clever workarounds when a straightforward fix exists
- Don't add abstractions to fix a concrete problem
- Resist the urge to fix unrelated issues you notice
- Keep the fix focused on the actual problem

**Simple Fix Checklist**:
- Is this the smallest change that fixes the bug?
- Can I explain the fix in one sentence?
- Am I fixing just this bug or redesigning the system?
- Will another developer understand this fix immediately?
- Have I avoided adding complexity to work around the issue?

**Root Cause Documentation**:
- **What**: The specific failure mechanism
- **Where**: Exact file and line number
- **Why**: The actual reason (not symptoms)
- **When**: Conditions that trigger the bug

**Fix Approach**:
- Implement the minimal change that fixes the issue
- No clever refactoring while debugging
- Add a test that captures this specific bug
- Document why this simple fix is sufficient

**Verification**:
- Bug reproduces reliably before the fix
- Bug is eliminated after the fix
- No new bugs introduced by the change
- Test prevents regression of this issue

## 6. Post-Mortem Questions

**Channel Lamport: "A distributed system is one in which the failure of a computer you didn't even know existed can render your own computer unusable"**

Ask yourself:
- Why didn't tests catch this?
- What similar bugs might exist?
- How can we prevent this class of bugs?
- Is the fix simpler than the bug?

## The Three Laws of Debugging

1. **It's always your code** (until proven otherwise)
2. **The bug is not where you think it is** (check your assumptions)
3. **Read the error message** (yes, the whole thing)

Remember: **The best debugger is a fresh pair of eyes and a good night's sleep.**