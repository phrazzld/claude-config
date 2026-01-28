---
name: delegate
description: |
  Multi-AI orchestration primitive. Delegate to specialized AI tools, collect outputs, synthesize.
  Use when: analysis, review, audit, investigation tasks need multiple expert perspectives.
  Keywords: orchestrate, delegate, multi-ai, parallel, synthesis, consensus
---

# /delegate

> You orchestrate. Specialists do the work.

Reference pattern for invoking multiple AI tools and synthesizing their outputs.

## Your Role

You don't analyze/review/audit yourself. You:
1. **Route** — Send work to appropriate specialists
2. **Collect** — Gather their outputs
3. **Curate** — Validate, filter, resolve conflicts
4. **Synthesize** — Produce unified output

## Your Team

### Agentic Tools (Can Take Action)

**Codex MCP** — Senior engineer, security specialist
- Long-context understanding, reliable tool calling
- Best at: refactors, migrations, debugging, security review
- Invocation: `mcp__codex__spawn_agent({"prompt": "..."})`
- Parallel: `mcp__codex__spawn_agents_parallel({"agents": [...]})`

**Kimi MCP** — Visual/frontend specialist
- Native multimodal (vision + text), agent swarm architecture
- Best at: UI from designs, visual debugging, frontend patterns
- Invocation: `mcp__moonbridge__spawn_agent({"prompt": "...", "thinking": true})`
- Parallel: `mcp__moonbridge__spawn_agents_parallel({"agents": [...]})`

**Gemini CLI** — Researcher, deep reasoner
- Web grounding, thinking_level control, agentic vision
- Best at: current best practices, pattern validation, design research
- Invocation: `gemini "..."` (bash)

### Non-Agentic (Opinions Only)

**Thinktank CLI** — Expert council
- Multiple models respond in parallel, synthesis mode
- Best at: consensus, architecture validation, second opinions
- Invocation: `thinktank instructions.md ./files --synthesis` (bash)
- **Note**: Cannot take action. Use for validation, not investigation.

### Internal Agents (Task tool)

Domain specialists for focused review:
- `go-concurrency-reviewer`, `react-pitfalls`, `security-sentinel`
- `data-integrity-guardian`, `architecture-guardian`, `config-auditor`

## How to Delegate

Apply `/llm-communication` principles — state goals, not steps:

### To Agentic Tools (Codex, Kimi, Gemini)

Give them latitude to investigate:
```
"Investigate this stack trace. Find root cause. Propose fix with file:line."
```

NOT:
```
"Step 1: Read file X. Step 2: Check line Y. Step 3: ..."
```

### To Thinktank (Non-Agentic)

Provide context, ask for judgment:
```
"Here's the code and proposed fix. Is this approach sound?
What are we missing? Consensus and dissent."
```

### Parallel Execution

Run independent reviews in parallel:
- Multiple MCP calls in same message
- Multiple Task tool calls in same message
- Gemini + Thinktank can run concurrently (both bash)

## Curation (Your Core Job)

For each finding:

**Validate**: Real issue or false positive? Applies to our context?
**Filter**: Generic advice, style preferences contradicting conventions
**Resolve Conflicts**: When tools disagree, explain tradeoff, make recommendation

## Output Template

```markdown
## [Task]: [subject]

### Action Plan

#### Critical
- [ ] `file:line` — Issue — Fix: [action] (Source: [tool])

#### Important
- [ ] `file:line` — Issue — Fix: [action] (Source: [tool])

#### Suggestions
- [ ] [improvement] (Source: [tool])

### Synthesis

**Agreements** — Multiple tools flagged:
- [issue]

**Conflicts** — Differing opinions:
- [Tool A] vs [Tool B]: [your recommendation]

**Research** — From Gemini:
- [finding with citation]
```

## When to Use

- **Code review** — Multiple perspectives on changes
- **Incident investigation** — Agentic tools investigate, Thinktank validates fix
- **Architecture decisions** — Thinktank for consensus
- **Audit/check tasks** — Parallel investigation across domains

## Related

- `/llm-communication` — Prompt writing principles
- `/review-branch` — Example implementation
- `/thinktank` — Multi-model synthesis
- `/codex-coworker` — Codex delegation patterns
