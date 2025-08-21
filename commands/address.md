Address code review feedback and architectural decisions by analyzing reviews, checking ADR alignment, and creating actionable tasks.

# ADDRESS

Process code review feedback (typically in `CODE_REVIEW.md` or `CODE_REVIEW_*.md` files) and verify architectural alignment.

## 1. Code Review Analysis

Think very hard about the code review. Identify:
- Legitimate merge-blockers that must be addressed
- Issues within scope for this branch and pull request
- Suggestions that can be deferred to future work

What would John Carmack do? Focus on:
- Correctness over cleverness
- Performance where it matters
- Simplicity and maintainability
- Clear boundaries and responsibilities

## 2. Architecture Decision Review

If this implementation involved architectural decisions (check for relevant ADRs in docs/adr/):

**Invoke adr-architect subagent** to review implementation against ADRs:
- Compare actual implementation with documented decisions
- Identify any divergences and their justifications
- Document outcomes vs expectations
- Capture lessons learned for future decisions
- Update ADR status if needed

**How to invoke**: Use Task tool with subagent_type: "general-purpose" and prompt to act as adr-architect from /Users/phaedrus/.claude/agents/adr-architect.md for reviewing the implementation against relevant ADRs.

## 3. ADR Update Actions

If the adr-architect review identified divergences or important outcomes:

**Update the ADR file directly**:
1. Add a "Review Notes" section to the relevant ADR with:
   - Date of review
   - What actually happened vs expectations
   - Justification for any divergences
   - Actual trade-offs observed

2. Update ADR status if needed:
   - Keep as "Accepted" if implementation aligned
   - Change to "Deprecated" if approach proved unworkable
   - Mark as "Superseded" if a new approach is needed (create new ADR)

3. Update memory/adr-outcomes.md with:
   - Decision type and brief description
   - Success/Mixed/Failure outcome
   - Key lessons learned
   - Reusable pattern or anti-pattern identified

**Example ADR Review Notes addition**:
```markdown
## Review Notes (Added 2024-XX-XX)

**Implementation Review**: The decision to use native subagents proved successful.
- **Alignment**: 95% - minor deviation in memory file format
- **Unexpected Benefits**: Reduced command file sizes by 50%
- **Challenges**: Initial learning curve for subagent invocation patterns
- **Recommendation**: Continue with this pattern, document invocation examples
```

## 4. Task Generation

Synthesize findings into discrete, well-defined, narrowly-scoped, highly-detailed, context-rich, atomic, and actionable task items in TODO.md:

**For Code Review Items**:
- Create tasks for all merge-blockers
- Include context from the review
- Reference specific files and line numbers
- Prioritize by impact and risk

**For ADR Alignment Issues**:
- Create tasks to fix any unjustified implementation divergences
- If ADR needs fundamental change, create task for new ADR
- Ensure memory updates are completed
- Consider if additional ADRs are needed for uncovered decisions

## 5. Deferral Documentation

For all other issues not being addressed:
- Explain why they're out of scope for this branch
- Document in BACKLOG.md if they have future value
- Note any technical debt being accepted
- Ensure reviewers understand the rationale
