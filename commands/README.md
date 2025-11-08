# Claude Commands

Streamlined command library for Claude Code CLI, providing an integrated development workflow from ideation to deployment.

## Core Workflow Commands (23 Total)

### 🚀 Development Pipeline

The main development flow follows this progression:

```
/prime → /spec → /architect → /plan → /flesh → /execute → /git-pr
```

1. **prime.md** - Gather context from repository files (README, CLAUDE.md, package.json)
2. **spec.md** - Research and specification generation with parallel experts
3. **architect.md** - Transform PRD into DESIGN.md with modules, pseudocode, data flow
4. **plan.md** - Convert architecture into actionable TODO items
5. **flesh.md** - Transform skeletal TODOs into executable specifications with parallel research
6. **execute.md** - Adaptive task execution with complexity-based reasoning
7. **git-pr.md** - Create pull requests with auto-generated descriptions

### 📊 Analysis & Debugging

- **debug.md** - Adaptive debugging with 8 domain experts using confidence scoring
- **ci.md** - CI failure analysis and resolution task generation
- **verify.md** - Pre-commit bypass validation
- **ultrathink.md** - Steve Jobs/Ousterhout design review for risky plans
- **gates.md** - Quality gate checklist before merging or pushing

### 📋 Task Management

- **backlog-groom.md** - Parallel expert backlog generation with 8 specialized agents
- **plan.md** - Architecture-to-task conversion
- **flesh.md** - Expand TODO items with deep analysis and parallel research
- **ticket.md** - Convert plans into prioritized TODO.md items
- **tighten.md** - Slim TODO.md to execution-ready scope only
- **skill-bootstrap.md** - Capture missing domain knowledge before building

### 🔀 Git Operations

- **git-merge-main.md** - Merge main branch with conflict resolution
- **git-respond.md** - Handle PR feedback and reviews
- **git-push.md** - Quality gate workflow before pushing
- **git-simple-push.md** - Quick push without quality gates

### 📚 Documentation & Reflection

- **distill.md** - Combined CLAUDE.md distillation + refresh workflow (≤100 lines, always current)
- **carmack.md** - Carmack-style first-principles reset with built-in chill/reflect ritual

### 🛠️ Utilities

- **spec.md / architect.md / ultrathink.md** embed the Steve Jobs ultrathink mindset so every stage feels inevitable
- **ticket.md + tighten.md** keep TODO.md actionable and lean

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
- `/flesh` - 3 research experts for TODO expansion
- `/debug` - 8 domain experts with confidence assessment
- `/backlog-groom` - 8 specialized backlog agents

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
/flesh                    # Expand complex TODOs before execution
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
/distill                  # Shrink + refresh CLAUDE.md into a 100-line living brief
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
4. **Stress test designs**: Run `/ultrathink` before building risky features
5. **Document learnings**: Refresh CLAUDE.md via `/distill` after major work

## Command Philosophy

- **Single Purpose**: Each command does one thing well
- **Composable**: Commands work together in workflows
- **Transparent**: Live logging shows what's happening
- **Adaptive**: Complexity-based reasoning allocation
- **Parallel**: Multi-expert analysis when beneficial
- **Reality Distortion Mindset**: Spec → Architect → Plan → Execute → Ultrathink all embed the Steve Jobs ultrathink ritual for simplicity, iteration, and elegance
