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

## 3. Systematic Investigation

**The Binary Search Method:**

```bash
# Find when it broke
git log --oneline -20  # What changed?
git bisect start       # When did it break?

# Find where it breaks
grep -r "error_pattern" .  # Where's the symptom?
rg "function_name" --type py  # Where's the cause?

# Find why it breaks
print("HERE 1")  # Yes, really
console.log({state})  # State at failure point
```

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

```markdown
## Root Cause
- What: [Specific failure]
- Where: [file:line]
- Why: [Actual reason]
- When: [Conditions that trigger]

## Fix
- Minimal change that fixes the issue
- No clever refactoring while debugging
- Add test to prevent regression

## Verification
- [ ] Bug reproduces before fix
- [ ] Bug gone after fix
- [ ] No new bugs introduced
- [ ] Test captures the issue
```

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