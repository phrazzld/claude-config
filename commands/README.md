# Claude Commands

Streamlined command library for Claude Code CLI, providing an integrated development workflow from ideation to deployment.

## Core Workflow (20 Commands)

### 🚀 Development Pipeline

The main development flow follows this progression:

```
/prime → /spec → /plan → /execute → /git-pr → /git-code-review
```

1. **prime.md** - Gather context from repository files (README, CLAUDE.md, package.json)
2. **spec.md** - Research and specification generation with parallel experts
3. **plan.md** - Convert specifications to actionable TODO items
4. **execute.md** - Adaptive task execution with complexity-based reasoning
5. **git-pr.md** - Create pull requests with auto-generated descriptions
6. **git-code-review.md** - Multi-expert code review generating TODOs and backlog items

### 📊 Analysis & Debugging

- **debug.md** - Adaptive debugging with 8 domain experts using confidence scoring
- **audit.md** - Security audit documentation

### 📋 Backlog Management

- **backlog-groom.md** - Parallel expert backlog generation with 8 specialized agents

### 🔀 Git Operations

- **git-merge-main.md** - Merge main branch with conflict resolution
- **git-respond.md** - Handle PR feedback and reviews
- **git-push.md** - Quality gate workflow before pushing
- **git-simple-push.md** - Quick push without quality gates

### 🧠 Meta Commands

- **meta-carmack.md** - John Carmack-inspired technical problem-solving
- **meta-chill.md** - Structured reflection and stress reduction
- **meta-update-claude.md** - Session-based CLAUDE.md refinement

### 📚 Documentation

- **docs-sync.md** - Extract patterns from work logs and update documentation

### ⚙️ Setup Commands

- **setup-mcp.md** - Configure MCP integrations
- **setup-context7.md** - Set up Context7 documentation access
- **setup-playwright.md** - Configure Playwright testing

## Key Features

### Adaptive Complexity

The `/execute` command assesses task complexity and allocates reasoning accordingly:
- **SIMPLE** (0-2 files): Direct execution
- **MEDIUM** (3-5 files): Think mode
- **COMPLEX** (6+ files): Think hard mode
- **VERY_COMPLEX** (system-wide): Ultrathink mode

### Parallel Processing

Multiple commands use the Task tool for concurrent expert analysis:
- `/spec` - 3 research experts (web, docs, codebase)
- `/debug` - 8 domain experts with confidence assessment
- `/backlog-groom` - 8 specialized backlog agents
- `/git-code-review` - 8 review experts

### Live Progress Tracking

Commands update TODO.md in real-time with:
- Timestamps and complexity assessment
- Context discovery logs
- Approach decisions
- Learnings and blockers

## Workflow Examples

### Feature Development
```bash
/prime                    # Understand the codebase
/spec                     # Research and specify the feature
/plan                     # Break down into TODO items
/execute                  # Work through tasks adaptively
/git-pr                   # Create pull request
```

### Debugging Session
```bash
/debug                    # Launch parallel debugging experts
/execute                  # Fix identified issues
/git-push                 # Push fixes with quality checks
```

### Documentation Update
```bash
/docs-sync                # Extract patterns and update docs
/meta-update-claude       # Refine CLAUDE.md with session insights
```

## File Conventions

- **@TODO.md** - Active task queue with live progress logs
- **@TASK.md** - Detailed task specifications
- **@BACKLOG.md** - Project ideas and future work
- **@ISSUE.md** - Problem descriptions for debugging
- **@CLAUDE.md** - Project-specific instructions

## Best Practices

1. **Start with context**: Use `/prime` to understand the codebase
2. **Research thoroughly**: Use `/spec` for complex features
3. **Track everything**: Let commands update TODO.md automatically
4. **Review comprehensively**: Use `/git-code-review` before merging
5. **Document learnings**: Run `/docs-sync` after major work

## Command Philosophy

- **Single Purpose**: Each command does one thing well
- **Composable**: Commands work together in workflows
- **Transparent**: Live logging shows what's happening
- **Adaptive**: Complexity-based reasoning allocation
- **Parallel**: Multi-expert analysis when beneficial