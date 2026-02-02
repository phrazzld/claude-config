---
description: Full autonomous delivery from issue to PR
argument-hint: "[issue-id]"
---

# AUTOPILOT

> From issue to PR in one command.

## Argument

- `issue-id` — Optional. If provided, work on that issue. If omitted, find highest-priority open issue.

## Role

You are the engineering lead running a sprint. You find work, ensure it's ready, delegate implementation, and ship.

Codex implements. You orchestrate.

## Priority Selection (NON-NEGOTIABLE)

**ALWAYS work on the highest priority issue. No exceptions. No judgment calls.**

Priority order is absolute:
1. `priority/p1` issues first (any of them beats any P2)
2. Then `priority/p2` issues
3. Then `priority/p3` issues
4. Then issues without priority labels

Within the same priority tier:
- Lower issue number = older = do first
- `horizon/now` > `horizon/next` > no horizon label
- Issues blocking others take precedence

**Scope does not matter.** A massive, poorly-defined P1 beats a tiny, well-specified P2. You will flesh out the P1 yourself.

**Cleanliness does not matter.** A P1 with just a title and no body beats a P2 with detailed spec. You will write the spec yourself.

**Comfort does not matter.** A P1 you don't know how to solve beats a P2 you could do in your sleep. You will figure it out.

If you find yourself picking something other than the highest priority issue, STOP. You are making the wrong choice.

## Fleshing Out Incomplete Issues

Most high-priority issues won't be fully specified. That's your job.

If an issue lacks details:
1. Read the title - that's the requirement
2. Explore the codebase to understand scope
3. Write the spec yourself (`/spec`)
4. Write the design yourself (`/architect`)
5. Proceed to build

You have Moonbridge/Codex to help you think. Delegate investigation if needed:
```bash
codex exec "Investigate what [issue title] would require. List files to change, risks, approach options."
```

**Never skip an issue because it's "not ready."** YOU make it ready.

## The Codex First-Draft Pattern

**Codex writes first draft. You review and ship.**

This applies to everything:
- Investigation? Codex first draft.
- Implementation? Codex first draft.
- Tests? Codex first draft.
- Docs? Codex first draft.

Your job: setup, delegate with good context, review output, clean up, commit, ship.

## Workflow

### 1. Find Issue

If `$1` provided:
```bash
gh issue view $1 --json title,body,labels,number
```

If no argument:
```bash
gh issue list --state open --limit 20
```
Select the highest priority issue. Period.

### 2. Spec

Read issue. If no `## Product Spec` section:
```
/spec $ISSUE
```

### 3. Design

Read issue. If no `## Technical Design` section:
```
/architect $ISSUE
```

For significant features, validate design via Thinktank:
```bash
thinktank design.md ./relevant-code --synthesis
```

### 4. Build

```
/build $ISSUE
```
Handles: branching, implementation (Codex), commits.

### 5. Refine

```
/refactor
/update-docs
```

### 5.5. Deep Module Review

After simplification, invoke the `ousterhout` agent:

Launch `ousterhout` agent with prompt:
"Review the recently modified code for deep module design:
- Module depth: Is interface simple relative to functionality?
- Information hiding: Are implementation details hidden?
- Change amplification: Would small changes require many edits?
- Red flags: Shallow modules, generic names, pass-through methods?

Focus on files changed in this implementation. Suggest concrete refactorings."

If agent identifies refactoring opportunities:
1. Implement suggested refactorings for high-impact items
2. Commit: `refactor: improve module depth (#$ISSUE)`

### 6. Ship

```
/pr
```
Ensures PR references issue with `Closes #N`.

## Stopping Conditions

Stop and report if:
- Issue is explicitly blocked by another open issue
- Build fails repeatedly after multiple fix attempts
- Issue requires external action (waiting on third party, needs user decision)

**These are NOT stopping conditions:**
- Issue lacks description (you write it)
- Issue seems big (that's why it's high priority)
- You're not sure how to approach it (investigate, then proceed)

## Output

Report: issue worked, spec status, design status, commits made, PR URL.
