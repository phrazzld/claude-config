Execute the next available task from TODO.md.

# EXECUTE

Grab next task from TODO.md → Think about approach → Do the work → Mark complete

<!-- METRICS: Execution typically takes 20-30 seconds with pattern-scout assistance
     Previous baseline: 45-60 seconds with manual complexity assessment
     To track: Add timing around task execution and log to metrics.md -->

## PROCESS

1. **Find next task**: Look for first `[~]` (in-progress) or `[ ]` (not started) task in TODO.md
2. **Mark in-progress**: Update `[ ]` to `[~]` 
3. **Think before acting**: 
   - Consider the approach and plan implementation
   - For implementation tasks, invoke `pattern-scout` to find similar code
   - Identify relevant files and existing patterns to follow
4. **Do the work**: Implement what the task describes
5. **Mark complete**: Update `[~]` to `[x]` when done

## PATTERN DISCOVERY

When working on implementation tasks, invoke pattern-scout subagent to find similar code:
- Shows existing patterns with file:line references  
- Identifies the best template to follow
- Updates knowledge.md with genuinely useful new patterns

**How to invoke**: Use Task tool with subagent_type: "general-purpose" and prompt to act as pattern-scout from /Users/phaedrus/.claude/agents/pattern-scout.md

## WORK LOG

For complex tasks or when discovering important context, add a work log entry directly under the task in TODO.md:

```markdown
- [~] Implement user authentication
  ```
  Work Log:
  - Found existing auth pattern in services/auth.ts
  - Need to follow JWT token approach from api/middleware
  - Database schema already has user table, just needs session table
  - Blocked by: need to clarify token expiry requirements
  ```
```

This work log serves as:
- Scratchpad for discoveries and context
- Record of decisions made
- Place to note blockers or questions
- Memory for if task is resumed later

## POST-EXECUTION LEARNING

After completing or blocking on a task, invoke the lesson-harvester to extract learnings:

**When to harvest lessons:**
- Task completed successfully (what worked?)
- Task blocked or failed (what went wrong?)
- Unexpected complexity discovered
- Elegant solution found
- Time estimate significantly off

**How to invoke**: Use Task tool with subagent_type: "general-purpose" and prompt to act as lesson-harvester from /Users/phaedrus/.claude/agents/lesson-harvester.md, providing:
- Task description and outcome
- What worked or didn't work
- Time taken vs expected
- Any patterns discovered or bugs encountered

The lesson-harvester will:
- Extract reusable lessons that are impactful and non-obvious
- Update knowledge.md with valuable patterns, gotchas, questions, and estimation insights
- Track success/failure patterns
- Build institutional knowledge

## NOTES

- Always think through the approach before diving into implementation
- If task includes context or detailed steps, follow them
- If blocked, mark as `[!]` with explanation in work log and move to next task
- Only preserve work logs that contain valuable context for future reference
- Commit changes after completion if appropriate
- Invoke lesson-harvester for significant learnings