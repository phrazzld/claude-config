---
name: retro
description: |
  Implementation feedback capture. Appends effort accuracy, scope changes,
  and blockers to {repo}/.groom/retro.md. Read by /groom for planning.
  Invoked by /done and /pr, or manually via /retro append.
argument-hint: "append"
effort: low
---

# /retro

Capture implementation feedback for future grooming sessions.

## Philosophy

When implementation reveals that an issue was underscoped, that signal should
persist. `/retro` captures these signals so `/groom` can adjust future scoping.

## Storage

```
{repo}/.groom/retro.md
```

Created automatically if missing. Appended to, never overwritten.

## Format

```markdown
# Implementation Retrospective

## Entry: #{issue} — {title} ({date})

**Effort:** predicted {predicted} → actual {actual}
**Scope changes:** {what changed from original issue}
**Blockers:** {what blocked progress}
**Pattern:** {reusable insight for future scoping}

---
```

## Subcommands

### `/retro append`

Interactive capture. Ask:

1. Which issue did you just finish? (issue number)
2. What was the predicted effort? (from effort label)
3. What was the actual effort?
4. Did scope change during implementation? How?
5. What blocked you?
6. What should future grooming sessions know?

Then append to `{repo}/.groom/retro.md`.

### Automated Append (from /done and /pr)

When invoked programmatically by `/done` or `/pr`, accept structured data:

```
/retro append --issue 42 --predicted m --actual l --scope "Added retry logic not in original spec" --blocker "Webhook signature verification undocumented" --pattern "Webhook issues always need retry logic"
```

Append without interactive prompts.

## How /groom Uses Retro

During Phase 1, `/groom` reads `retro.md` and extracts patterns:

- **Effort calibration:** "Payment issues consistently take 1.5x estimates"
- **Scope patterns:** "Webhook issues always need retry logic added during implementation"
- **Blocker patterns:** "External API docs are frequently wrong — always verify with web research"
- **Domain insights:** "Bitcoin wallet issues require manual testing on regtest"

These patterns inform:
- Effort estimates (adjust based on historical accuracy)
- Issue scoping (include commonly-missed concerns upfront)
- Boundary statements (prevent known scope creep patterns)
- Research priorities (investigate known problem areas proactively)

## Related

- `/done` — Appends retro signals after session retrospective
- `/pr` — Appends retro signals when opening PR
- `/groom` — Reads retro.md during Phase 1 (Context)
