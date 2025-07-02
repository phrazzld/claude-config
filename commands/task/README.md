# Task Management Commands

Task planning and breakdown workflows.

## Commands

- **plan.md** - Select a task from @BACKLOG.md and create detailed breakdown in @TASK.md using parallel expert analysis.
- **ready.md** - Convert @TASK.md implementation plan into discrete, actionable @TODO.md entries.

## Usage

```bash
/task/plan        # Plan task from backlog with detailed breakdown
/task/ready       # Convert task plan to actionable TODO items
```

## Workflow Integration

Task commands bridge planning and execution:
1. **plan** - Moves items from @BACKLOG.md → @TASK.md with comprehensive analysis
2. **ready** - Converts @TASK.md → @TODO.md with discrete, actionable items

This creates the flow: BACKLOG.md → TASK.md → TODO.md → Execution