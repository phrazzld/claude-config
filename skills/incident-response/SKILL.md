---
name: incident-response
description: |
  Investigate, fix, postmortem, prevent.
  Full incident lifecycle from bug report to systemic prevention.
  Use when: production down, critical bug, incident response, post-incident review.
  Composes: /investigate, /fix, /postmortem, /codify-learning.
argument-hint: <bug-report>
effort: max
---

# /incident-response

Fix the fire. Then prevent the next one.

## Role

Incident commander running the response lifecycle.

## Objective

Resolve the incident described in `$ARGUMENTS`. Fix it, verify it, learn from it, prevent recurrence.

## Latitude

- Multi-AI investigation: Codex (stack traces), Gemini (research), Thinktank (validate hypothesis)
- Create branch immediately: `fix/incident-$(date +%Y%m%d-%H%M)`
- Demand observable proof — never trust "should work"

## Workflow

1. **Investigate** — `/investigate $ARGUMENTS` (creates INCIDENT.md with timeline, evidence, root cause)
2. **Branch** — `fix/incident-$(date +%Y%m%d-%H%M)` from main
3. **Fix** — `/fix "Root cause from investigation"` (Codex delegation + verify)
4. **Verify** — Observable proof: log entries, metrics, database state. Mark UNVERIFIED until confirmed.
5. **Postmortem** — `/postmortem` (blameless: summary, timeline, 5 Whys, follow-ups)
6. **Prevent** — If systemic: create prevention issue, optionally `/autopilot` it
7. **Codify** — `/codify-learning` (regression test, agent update, monitoring rule)

## Output

Incident resolved, postmortem filed, prevention issue created (if applicable).
