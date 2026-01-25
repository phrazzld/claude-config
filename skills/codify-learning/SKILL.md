---
name: codify-learning
description: |
  CODIFY-LEARNING
---

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

## The Codex First-Draft Pattern

**Codex creates the artifact. You review and commit.**

```bash
codex exec "CODIFY: Create [artifact type] for [learning]. Follow patterns in ~/.claude/skills/. Output to [path]." \
  --output-last-message /tmp/codex-codify.md 2>/dev/null
```

## Execution

1. Review session: What problems did we solve?
2. Identify repeatable pattern or insight
3. Delegate artifact creation to Codex
4. Review and refine Codex's output
5. Commit with message: "chore(knowledge): codify {learning}"

## Output

Artifact created and committed. Describe what was codified and where.
