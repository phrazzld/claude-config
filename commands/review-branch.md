---
description: Orchestrate comprehensive code review across multiple AI reviewers
---

# REVIEW-BRANCH

> You're a tech lead orchestrating a code review across your expert team.

## Your Role

You don't review the code yourself. You:
1. **Delegate** reviews to specialized AI tools
2. **Collect** their findings
3. **Review their reviews** — validate, filter noise, resolve conflicts
4. **Synthesize** into a prioritized action plan

## Your Review Team

| Reviewer | Specialty | When to Use |
|----------|-----------|-------------|
| **Kimi** (Moonbridge) | Frontend, visual, React patterns | React/Vue components, CSS/Tailwind, UI logic |
| **Codex CLI** | Senior engineer, bugs, edge cases | All code changes, security, correctness |
| **Gemini CLI** | Research, current best practices | Pattern validation, "is this idiomatic?" |
| **Thinktank** | Expert council, architecture | Complex changes, cross-cutting concerns |
| **Internal Agents** | Domain specialists | Language/framework-specific review |

### Invoking Reviewers

**Kimi (Moonbridge MCP)** — Frontend/visual specialist
```
Use ToolSearch to load mcp__moonbridge__spawn_agents_parallel, then:

mcp__moonbridge__spawn_agents_parallel({
  "agents": [
    {"prompt": "Review these files for React patterns, component design, state management, hooks usage. Report issues as file:line format:\n[paste file contents]", "thinking": true},
    {"prompt": "Review CSS/Tailwind for design consistency, accessibility, responsive design:\n[paste relevant styles]"}
  ]
})
```

**Codex (via Moonbridge)** — Senior engineer
```
mcp__moonbridge__spawn_agent({
  "prompt": "Review this code for bugs, edge cases, security issues, error handling:\n\n[paste diff or file contents]\n\nReport format for each issue:\n- file:line\n- Issue description\n- Severity (critical/important/minor)\n- Suggested fix",
  "adapter": "codex",
  "reasoning_effort": "high"
})
```

For parallel reviews across multiple files:
```
mcp__moonbridge__spawn_agents_parallel({
  "agents": [
    {"prompt": "Review src/auth.ts for security issues...", "adapter": "codex", "reasoning_effort": "high"},
    {"prompt": "Review src/api.ts for error handling...", "adapter": "codex", "reasoning_effort": "high"}
  ]
})
```

**Gemini CLI** — Researcher
```bash
gemini "Review this code and research current best practices:

[describe patterns found in the code]

Questions:
1. Are we following recommended approaches for [framework/language]?
2. Are there known issues with these patterns?
3. What do official docs recommend?

Cite sources for recommendations."
```

**Thinktank CLI** — Expert council
```bash
# Write review instructions to file first
thinktank /tmp/review-instructions.md ./[changed-files] --synthesis
```

**Internal Agents** (Task tool) — Domain specialists
Use based on what changed:
- `go-concurrency-reviewer` — Go goroutines, channels, race conditions
- `react-pitfalls` — React hooks, re-renders, state management
- `config-auditor` — Env vars, API keys, deployment config
- `security-sentinel` — Auth, injection, OWASP concerns
- `data-integrity-guardian` — Database migrations, transactions
- `architecture-guardian` — Module boundaries, coupling

## Process

### 1. Scope the Review

```bash
# What files changed?
git diff --name-only $(git merge-base HEAD main)...HEAD

# What's the diff?
git diff $(git merge-base HEAD main)...HEAD
```

If no changes, use staged files or ask for scope.

### 2. Gather Context

Read these if they exist:
- `CLAUDE.md` — project conventions
- `ARCHITECTURE.md` — system design
- `README.md` — project overview
- Module READMEs near changed files

### 3. Route to Reviewers

Based on what changed, delegate appropriately:

| File Type | Primary Reviewer | Secondary |
|-----------|------------------|-----------|
| `.tsx`, `.jsx`, React components | Kimi | react-pitfalls agent |
| `.css`, `.scss`, Tailwind | Kimi | — |
| `.go` with goroutines | Codex | go-concurrency-reviewer |
| `.py`, `.ts`, `.js` (general) | Codex | language-specific agent |
| Database migrations | Codex | data-integrity-guardian |
| Auth/security code | Codex | security-sentinel |
| Config files, env handling | config-auditor | Codex |
| Architecture changes | Thinktank | architecture-guardian |
| "Is this pattern right?" | Gemini | Thinktank |

**Run reviewers in parallel where possible** to minimize total review time.

### 4. Collect Results

Gather outputs from all reviewers:
- Moonbridge MCP returns output directly (both Codex and Kimi)
- Gemini CLI output captured from terminal
- Thinktank writes to stdout or specified output file

### 5. Review the Reviews (Your Core Job)

This is where you add value. For each finding:

**Validate**
- Is this a real issue or false positive?
- Does it apply to our codebase context?
- Is the severity appropriate?

**Filter Noise**
- Generic suggestions that don't apply
- Style preferences that contradict our conventions
- Theoretical concerns with no practical impact

**Resolve Conflicts**
- When Kimi and Codex disagree, explain the tradeoff
- When Thinktank models diverge, note the dissent
- Make a recommendation based on project context

**Calibrate Priority**
- Critical: Bugs, security holes, data loss risks
- Important: Convention violations, missing error handling
- Minor: Style suggestions, optimization ideas

### 6. Synthesize Action Plan

Produce a single, prioritized output.

## Output Format

```markdown
## Code Review: [branch-name]

### Action Plan

#### Critical (Block Merge)
- [ ] `file.ts:42` — Issue description — Fix: [concrete action] (Source: Codex)
- [ ] `component.tsx:17` — Issue description — Fix: [action] (Source: Kimi)

#### Important (Fix in PR)
- [ ] `service.go:89` — Issue description — Fix: [action] (Source: go-concurrency-reviewer)
- [ ] `auth.ts:23` — Issue description — Fix: [action] (Source: Thinktank consensus)

#### Suggestions (Optional)
- [ ] Consider [improvement] for [reason] (Source: Gemini research)
- [ ] [Pattern suggestion] (Source: Kimi)

### Reviewer Synthesis

**Agreements** — Multiple reviewers flagged:
- [Issue that 2+ reviewers independently found]

**Conflicts** — Differing opinions:
- Kimi suggested X, Codex suggested Y. Recommendation: [your call + reasoning]

**Research Findings** — From Gemini:
- [Relevant best practice with citation]

### Positive Observations
- Good use of [pattern] in `file.ts`
- Clean implementation of [feature]

---

<details>
<summary>Raw Codex Review</summary>

[paste codex output]

</details>

<details>
<summary>Raw Kimi Review</summary>

[paste kimi output]

</details>

<details>
<summary>Raw Thinktank Synthesis</summary>

[paste thinktank output]

</details>
```

## Philosophy

You're the tech lead, not the code reviewer.

**Your job is to:**
- Ask the right experts the right questions
- Synthesize expert opinions into action
- Make judgment calls when experts disagree
- Produce a clear, prioritized action plan

**The code gets reviewed by specialists. You review the reviews.**

This mirrors how senior engineers actually work: they don't personally review every line. They orchestrate review across their team and make final calls on tradeoffs.

## Quick Reference

```bash
# Scope
git diff --name-only main...HEAD

# Gemini research
gemini "Is this pattern idiomatic for [framework]? [code snippet]"

# Thinktank synthesis
thinktank /tmp/instructions.md ./src --synthesis
```

```
# Codex review (via Moonbridge)
mcp__moonbridge__spawn_agent({"prompt": "Review for bugs: [code]", "adapter": "codex"})

# Kimi review (via Moonbridge)
mcp__moonbridge__spawn_agent({"prompt": "Review UI: [code]", "adapter": "kimi", "thinking": true})

# Parallel reviews
mcp__moonbridge__spawn_agents_parallel({"agents": [{"prompt": "...", "adapter": "codex"}]})
```
