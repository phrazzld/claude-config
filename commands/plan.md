Break down work into executable chunks. No wishful thinking allowed.

# PLAN

Channel Torvalds: "Talk is cheap. Show me the code."

## The Torvalds Test

*"If it's not needed for THIS pull request, it's not a TODO."*

Every TODO must be executable today, not someday.

## 1. Read the Spec

**What would Torvalds prioritize?**
- Read @TASK.md or @SPEC.md
- Find what actually needs to work NOW
- Ignore future dreams and nice-to-haves
- Focus on what breaks if missing

## 2. Decompose Ruthlessly

**The YAGNI Principle: You Aren't Gonna Need It**

Break down into atomic, executable tasks:
- Each task = one commit
- Each commit = working code
- No task bigger than 2 hours
- If it's complex, it's multiple tasks

## 3. Apply The Torvalds Test

For each potential TODO, ask:
1. Will the code break without this? → TODO
2. Will users notice if this is missing? → TODO
3. Is this required for the next PR? → TODO
4. Everything else? → BACKLOG

## 4. Write TODO.md

**The Carmack Structure: Simple, Direct, Actionable**

```markdown
# TODO: [Feature Name]

## Phase 1: Make it Work [Today]
- [ ] Core functionality that must exist
- [ ] Critical error handling
- [ ] Basic tests to prove it works

## Phase 2: Make it Right [This Week]
- [ ] Refactor obvious problems
- [ ] Add proper validation
- [ ] Complete test coverage

## Phase 3: Make it Fast [If Needed]
- [ ] Performance optimization
- [ ] Caching layer
- [ ] Advanced features
```

## 5. Write BACKLOG.md

**The Graveyard of Good Ideas**

```markdown
# BACKLOG: Future Considerations

## Maybe Someday
- Nice UI improvements
- Advanced features nobody asked for
- Optimizations for problems we don't have
- Clever abstractions we don't need
```

## The Three Laws of TODOs

1. **A TODO without a deadline is a wish**
2. **A TODO without clear success criteria is confusion**
3. **A TODO you can't start today is a BACKLOG item**

## Output Validation

Before finalizing, apply the Torvalds Test to every item:
- Can I code this today? ✓
- Will the PR fail without it? ✓
- Is the success criteria binary? ✓

If any answer is "no" → Move to BACKLOG

Remember: **Perfect is the enemy of shipped. Ship working code, iterate later.**