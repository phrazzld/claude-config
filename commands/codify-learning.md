---
description: Extract patterns from session into executable artifacts
---

# CODIFY-LEARNING

Transform learnings from this session into permanent, executable knowledge.

Run at the end of workflows to capture insights.

## Artifact Hierarchy (Most to Least Executable)

1. **Code** — Reusable function, hook, utility
2. **Test** — Regression test capturing the bug pattern
3. **Skill** — Knowledge Claude applies automatically
4. **Command** — Workflow automation
5. **Agent** — Specialized reviewer with enforcement rules
6. **Documentation** — ADR, runbook, or inline comment

## What This Does

1. **Reflect** — What did we learn? What pattern emerged?
2. **Classify** — Which artifact type best captures this?
3. **Create** — Write the artifact
4. **Verify** — Ensure it works and is discoverable

## Decision Tree

```
Did we fix a bug?
  → Could it happen again? → Write regression TEST
  → Is it a pattern? → Extract to CODE utility

Did we learn a new pattern?
  → Is it domain knowledge? → Create SKILL
  → Is it a workflow? → Create COMMAND
  → Is it enforcement? → Update AGENT

Did we make a design decision?
  → Write ADR in docs/
```

## Execution

1. Review session: What problems did we solve?
2. Identify repeatable pattern or insight
3. Create appropriate artifact
4. Commit with message: "chore(knowledge): codify {learning}"

## Output

Artifact created and committed. Describe what was codified and where.
