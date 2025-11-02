---
description: Smart workflow progression - determines and executes next logical action
---

# CONTINUE

Context-aware workflow dispatcher that analyzes current state and executes the appropriate next action.

## Mission

Eliminate "what command should I run next?" decisions. Analyzes your current workflow state and automatically executes the right next step.

## State Analysis

Check what exists and determine workflow position:

**Files to check**:
- TASK.md: Does it exist? Is it spec'd (detailed PRD with requirements, constraints)?
- DESIGN.md: Does it exist? Is it complete (architecture, modules, pseudocode)?
- TODO.md: Does it exist? Are there pending tasks `[ ]` or `[~]`? All complete `[x]`?
- Recent commits: Work recently committed? PR created?
- Git status: Branch state, uncommitted changes?

**Workflow states**:
- **IDLE**: No active work (no TASK.md or empty)
- **NEEDS_SPEC**: TASK.md exists but not detailed/spec'd
- **NEEDS_ARCHITECT**: TASK.md spec'd but no DESIGN.md
- **NEEDS_PLAN**: DESIGN.md exists but no TODO.md
- **IN_PROGRESS**: TODO.md has pending tasks
- **READY_FOR_PR**: All tasks complete, work committed
- **STALE_BRANCH**: Branch behind main

## Action Dispatch

Based on detected state, execute appropriate command:

### IDLE State
Report: "No active work. Create TASK.md with feature description or run /backlog-groom to find work."

### NEEDS_SPEC State
TASK.md exists but lacks detail (no clear requirements, success criteria, or constraints).

**Action**: Run /spec to refine TASK.md into comprehensive PRD.

### NEEDS_ARCHITECT State
TASK.md fully spec'd but no DESIGN.md exists.

**Action**: Run /architect to create DESIGN.md with architecture, module design, and pseudocode.

### NEEDS_PLAN State
DESIGN.md exists but no TODO.md exists.

**Action**: Run /plan to convert DESIGN.md architecture into actionable TODO.md tasks.

### IN_PROGRESS State
TODO.md exists with tasks marked `[ ]` (pending) or `[~]` (in-progress).

**Action**: Run /execute to work through next available task.

If multiple pending tasks remain, ask: "Continue executing remaining tasks?" If yes, keep running /execute until complete or blocked.

### READY_FOR_PR State
All TODO.md tasks marked `[x]` (complete) and work committed.

**Action**: Run /pr-ready to validate quality gates, then /git-pr to create pull request if ready.

### STALE_BRANCH State
Branch is behind main branch (detected via git status).

**Action**: Run /git-merge-main to update branch before proceeding with other actions.

## Blocking Conditions

If any blockers detected:
- Uncommitted changes in working directory → Ask: "Commit current work first?"
- Conflicting signals (e.g., TODO.md complete but TASK.md not spec'd) → Report ambiguity, suggest cleanup

## Notes

This command makes workflow progression automatic. Use it any time you're unsure what to do next.

**Pattern**: After completing any manual task, run `/continue` to see what's next.

## Success Criteria

User never needs to decide which command to run - `/continue` figures it out based on current state.
