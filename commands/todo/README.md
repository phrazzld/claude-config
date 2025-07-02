# TODO Execution Commands

Task execution and resolution workflows.

## Commands

- **execute.md** - Execute the next available task from TODO.md with adaptive context gathering and planning.
- **resolve.md** - Resolve merge conflicts methodically and cautiously to unblock stuck tasks.

## Usage

```bash
/todo/execute     # Execute next available task with status tracking
/todo/resolve     # Resolve merge conflicts and unblock tasks
```

## Workflow Integration

TODO commands handle task execution and problem resolution:
- **execute** processes @TODO.md tasks with proper status markers: `[ ]` → `[~]` → `[x]`
- **resolve** unblocks stuck tasks and handles conflicts

These commands complete the workflow: BACKLOG.md → TASK.md → TODO.md → **Execution**