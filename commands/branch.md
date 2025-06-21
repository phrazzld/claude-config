Create a new git worktree with a dedicated branch based on the current task from TASK.md, enabling parallel development without disrupting the main workspace.

## ANALYZE
- Check repository state and ensure working directory is clean
- Extract task description from TASK.md for branch naming
- Identify primary branch (main/master) and validate git repository health

## EXECUTE

### 1. Assess Current State
Verify we're in a clean git repository. Warn if uncommitted changes exist and allow user to proceed or abort.

### 2. Extract Task from TASK.md
Read TASK.md and extract the task description for branch naming. Exit with error if TASK.md doesn't exist.

### 3. Generate Branch Name
Create branch name using format: `feature/{sanitized-task-description}` where the task description is sanitized (lowercase, spaces to hyphens, special chars removed, truncated to 40 chars).

### 4. Create Worktree
Set up worktree in sister directory using format: `../{repo-name}__{branch-name}`. Fetch latest changes, create worktree with new branch based on primary branch (main/master), and set up upstream tracking.

### 5. Configure New Environment
Copy essential configuration files (.envrc, .env.example, .vscode/settings.json) from main worktree to new worktree to maintain development environment consistency.
