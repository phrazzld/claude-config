# Claude Commands

Streamlined command library for Claude Code CLI, providing an integrated development workflow from ideation to deployment with compounding quality improvements.

## Core Workflow Commands (42 Total)

### 🚀 Development Pipeline

**Meta-commands** (consolidated workflows):

| Command | Flow |
|---------|------|
| `/autopilot` | discover → spec → design → build → PR |
| `/deliver $N` | spec → design → build → PR → CI (for known issue) |
| `/ship` | PR → CI (for manual builds) |

**Granular commands** (when you need control):

```
/prime → /product → /architect → /plan → /execute → /git-pr
```

1. **autopilot.md** - Full autonomous: discover highest-priority issue → deliver → PR
2. **deliver.md** - End-to-end issue delivery with CI verification (chains: product → architect → build → git-pr → ci)
3. **ship.md** - Post-build shipping: create PR and wait for CI
4. **prime.md** - Gather context from repository files (README, CLAUDE.md, package.json)
5. **product.md** - Product specification with user interviews and success metrics
6. **architect.md** - Transform PRD into DESIGN.md with modules, pseudocode, data flow
7. **plan.md** - Convert architecture into actionable TODO items with Grug complexity review
8. **flesh.md** - Transform skeletal TODOs into executable specifications with parallel research
9. **execute.md** - Adaptive task execution with Carmack + Ousterhout quality review
10. **git-pr.md** - Create pull requests with auto-generated descriptions

### 📊 Analysis & Debugging

- **debug.md** - Intelligent specialist routing based on bug category (database/API/test/error/state/dependency/security/performance)
- **ci.md** - CI failure analysis and resolution task generation
- **verify.md** - Pre-commit bypass validation
- **ultrathink.md** - Steve Jobs/Ousterhout design review for risky plans
- **gates.md** - Quality gate checklist before merging or pushing
- **groom.md** - Comprehensive 15-agent parallel audit (8 specialists + 7 personas) with competitive intelligence

### 🔄 Git Worktrees (Parallel Development)

- **git-worktree-create.md** - Create isolated worktree with environment setup
- **git-worktree-review.md** - Review GitHub PRs in isolated worktrees
- **git-worktree-cleanup.md** - Remove stale worktrees safely

### 📚 Learning Codification (Compounding Quality)

- **codify.md** - Transform learnings into executable artifacts (code, tests, skills, commands, agents, docs)
  - Integrated into `/execute`, `/debug`, `/git-respond` with auto-prompts
  - Supported by 4 agents: learning-codifier, pattern-extractor, skill-builder, agent-updater

### 🔍 Simplification & Quality

- **simplify.md** - 4-perspective complexity reduction (Grug + Ousterhout + Fowler + Metz)
- **performance.md** - Performance optimization opportunities
- **security.md** - Security audit with OWASP focus
- **aesthetic.md** - UI/UX review and design improvements
- **observe.md** - Observability gaps and monitoring needs

### 📋 Task Management

- **backlog-groom.md** - Parallel expert backlog generation with 8 specialized agents
- **plan.md** - Architecture-to-task conversion with Grug complexity review
- **flesh.md** - Expand TODO items with deep analysis and parallel research
- **ticket.md** - Convert plans into prioritized TODO.md items
- **tighten.md** - Slim TODO.md to execution-ready scope only
- **skill-bootstrap.md** - Capture missing domain knowledge before building

### 🔀 Git Operations

- **git-merge-main.md** - Merge main branch with conflict resolution
- **git-respond.md** - Handle PR feedback with codification auto-prompt
- **git-push.md** - Quality gate workflow before pushing
- **git-simple-push.md** - Quick push without quality gates

### 🔧 Configuration & Sync

- **sync-configs.md** - Sync agents, commands, and philosophy to Codex CLI and Gemini CLI
  - Syncs all 15 agents to ~/.codex/agents/ and ~/.gemini/system-instructions/
  - Syncs commands with full prompt engineering preserved
  - Maintains consistent quality bar across all 3 CLIs

### 📚 Documentation & Reflection

- **distill.md** - Combined CLAUDE.md distillation + refresh workflow (≤100 lines, always current)
- **carmack.md** - Carmack-style first-principles reset with built-in chill/reflect ritual

## Agent Architecture (15 Total)

### 8 Domain Specialists

1. **complexity-archaeologist** - Ousterhout red flags, shallow modules, information leakage
2. **data-integrity-guardian** - Database migrations, transactions, referential integrity
3. **api-design-specialist** - REST/GraphQL design, HTTP semantics, error responses
4. **test-strategy-architect** - Test pyramid, coverage, behavior vs implementation testing
5. **error-handling-specialist** - Error boundaries, async handling, graceful degradation
6. **state-management-analyst** - State architecture, race conditions, stale closures
7. **dependency-health-monitor** - Security audits, bundle size, version management
8. **documentation-quality-reviewer** - Comment quality, JSDoc, ADRs, changelog
9. **infrastructure-guardian** - Quality gates, logging, error tracking, CI/CD, design systems

### 7 Master Personas

10. **grug** - Complexity demon hunter ("complexity very, very bad")
11. **carmack** - Direct implementation + shippability ("Focus is deciding what NOT to do")
12. **jobs** - Craft + simplicity + excellence ("Simple can be harder than complex")
13. **torvalds** - Pragmatic engineering ("Talk is cheap. Show me the code")
14. **ousterhout** - Deep modules + information hiding ("Deep modules manage complexity")
15. **fowler** - Refactoring + code smells ("Code for humans, not computers")
16. **beck** - TDD + simple design ("Red. Green. Refactor")

## Agent Composition Patterns

Commands intelligently compose agents based on context:

### /execute - Implementation Quality
- **Carmack** (direct implementation, YAGNI)
- **Ousterhout** (module depth, information hiding)
- Parallel invocation for final quality check

### /plan - Complexity Analysis
- **Grug** (detect complexity demon, premature abstraction)
- Validates plan before proceeding to implementation

### /simplify - Multi-Perspective Reduction
- **Grug** (complexity demon detection)
- **Ousterhout** (module depth analysis)
- **Fowler** (code smell identification)
- **Metz** (abstraction value assessment)
- 4 agents in parallel for comprehensive simplification

### /debug - Intelligent Specialist Routing
- **Database bugs** → data-integrity-guardian
- **API bugs** → api-design-specialist
- **Test bugs** → test-strategy-architect
- **Error bugs** → error-handling-specialist
- **State bugs** → state-management-analyst
- **Dependency bugs** → dependency-health-monitor
- **Security bugs** → security-sentinel
- **Performance bugs** → performance-oracle

### /product - Product Specification
- User interviews via AskUserQuestion (context, scope, success, edge cases)
- Research: users, pain points, competitive landscape
- Structured spec: Problem, Users, User Stories, Success Metrics, Non-Goals

### /groom - Comprehensive 15-Agent Audit
- All 8 specialists + all 7 personas in parallel
- Cross-validation signals (3+ agents flagging = critical priority)
- Persona consensus (Grug + Carmack + Jobs agree → strong signal)
- Gemini CLI competitive intelligence research

## Key Features

### Adaptive Complexity

The `/execute` command assesses task complexity and allocates reasoning accordingly:
- **SIMPLE** (0-2 files): Direct execution
- **MEDIUM** (3-5 files): Think mode
- **COMPLEX** (6+ files): Think hard mode
- **VERY_COMPLEX** (system-wide): Ultrathink mode

### Parallel Processing

Multiple commands use the Task tool for concurrent expert analysis:
- `/product` - User interviews + product spec
- `/flesh` - 3 research experts for TODO expansion
- `/debug` - Specialist routing (1-2 agents based on bug type)
- `/groom` - 15 agents (8 specialists + 7 personas)
- `/simplify` - 4 agents (Grug + Ousterhout + Fowler + Metz)

### Learning Codification

Every unit of work improves codebase quality through codification:
- **Hierarchy**: Code > Tests > Skills > Commands > Agents > Docs > Philosophy
- **Auto-prompts**: `/execute`, `/debug`, `/git-respond` prompt for codification
- **Dedicated command**: `/codify` for manual codification workflow
- **4 agents**: learning-codifier, pattern-extractor, skill-builder, agent-updater

### Live Progress Tracking

Commands update TODO.md in real-time with:
- Timestamps and complexity assessment
- Context discovery logs
- Approach decisions
- Learnings and blockers

### Git Worktrees

Separate Claude sessions for parallel development:
- Create isolated worktrees with `/git-worktree-create`
- Review PRs in isolation with `/git-worktree-review`
- Clean up safely with `/git-worktree-cleanup`

## Workflow Examples

### Consolidated Issue Delivery (Recommended)
```bash
/groom                    # Creates GitHub issues from 15-agent audit
/deliver 42               # Spec → Design → Build → PR → CI (one command)
                          # Await review
/git-respond              # Handle review feedback
```

### Full Autonomous (Discover + Deliver)
```bash
/autopilot                # Discovers highest-priority issue
                          # Runs spec → design → build → PR automatically
```

### Manual Build → Ship
```bash
# (write code manually)
/ship                     # Create PR + wait for CI
/git-respond              # Handle review feedback
```

### Granular Control (When Needed)
```bash
/prime                    # Understand the codebase
/product                  # Interview user, research, write product spec
/architect                # Design modules and interfaces
/plan                     # Break down with Grug complexity review
/execute                  # Work through with Carmack + Ousterhout review
/git-pr                   # Create pull request
/ci                       # Verify CI passes
```

### Debugging Session
```bash
/debug                    # Intelligent specialist routing
                          # Codification auto-prompt for bug patterns
/execute                  # Fix identified issues
/ship                     # PR + CI verification
```

### Codebase Grooming
```bash
/groom                    # 15-agent comprehensive audit
                          # Gemini CLI competitive intelligence
                          # Cross-validation signals
                          # Persona consensus
                          # Creates GitHub issues
```

### Parallel Development
```bash
/git-worktree-create feature/auth  # Create isolated worktree
# Navigate to worktree, new Claude session
/prime
/product
/plan
/execute
# Back to main
/git-worktree-cleanup              # Clean up when done
```

### Configuration Sync
```bash
/sync-configs             # Sync to Codex & Gemini CLIs
                          # 15 agents synced
                          # Commands adapted
                          # Philosophy preserved
```

## File Conventions

- **TODO.md** - Active task queue with live progress logs
- **TASK.md** - Detailed task specifications
- **BACKLOG.md** - Project ideas and future work
- **ISSUE.md** - Problem descriptions for debugging
- **CLAUDE.md** - Project-specific instructions
- **DESIGN.md** - Architecture from /architect
- **LEARNINGS.md** - Codified learnings for batch processing

## Best Practices

1. **Start with context**: Use `/prime` to understand the codebase
2. **Research thoroughly**: Use `/product` to interview users and define specs
3. **Track everything**: Let commands update TODO.md automatically
4. **Stress test designs**: Run `/ultrathink` before building risky features
5. **Codify learnings**: Accept codification prompts in `/execute`, `/debug`, `/git-respond`
6. **Groom regularly**: Run `/groom` monthly for 15-agent comprehensive audit
7. **Sync configs**: Run `/sync-configs` after agent/command changes
8. **Use worktrees**: Parallel development with isolated Claude sessions
9. **Leverage personas**: When Grug + Carmack + Jobs agree, listen closely

## Command Philosophy

- **Single Purpose**: Each command does one thing well
- **Composable**: Commands work together in workflows
- **Transparent**: Live logging shows what's happening
- **Adaptive**: Complexity-based reasoning allocation
- **Parallel**: Multi-agent analysis when beneficial
- **Compounding**: Every unit of work improves quality through codification
- **Persona-Driven**: 7 master personas bring timeless wisdom
- **Specialist-Augmented**: 8 domain specialists provide deep expertise
- **Reality Distortion Mindset**: Spec → Architect → Plan → Execute → Ultrathink embed Steve Jobs simplicity ritual

## Compounding Engineering Principles

From Every's compounding engineering flow:

1. **Git Worktrees**: Parallel development in separate Claude sessions
2. **Learning Codification**: Executable artifacts (code > tests > skills > commands > agents > docs)
3. **Agent Composition**: 15 perspectives (8 specialists + 7 personas) intelligently composed

**The Result**: Every unit of work makes future work easier, faster, and higher quality. Code review feedback becomes automated checks. Bugs become regression tests and preventive patterns. Design insights become reusable wisdom.
