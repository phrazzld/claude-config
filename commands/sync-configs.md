---
description: Sync Claude Code configuration to Codex CLI and Gemini CLI
---

# SYNC-CONFIGS

Synchronize your AI-assisted development workflow configuration from Claude Code (canonical source) to Codex CLI and Gemini CLI.

## Your Mission

Read Claude Code configuration and generate adapted versions for Codex and Gemini, ensuring consistent philosophy and workflow while respecting each tool's unique strengths.

## Process

### 1. Audit Current State

First, examine what exists:

```bash
# Claude Code (source)
ls -la ~/.claude/CLAUDE.md
ls ~/.claude/commands/*.md | wc -l
ls ~/.claude/skills/*/SKILL.md | wc -l

# Codex CLI (target)
cat ~/.codex/AGENTS.md | wc -l
ls ~/.codex/prompts/*.md 2>/dev/null | wc -l

# Gemini CLI (target)
cat ~/.gemini/GEMINI.md | wc -l
ls ~/.gemini/commands/*.toml 2>/dev/null | wc -l
```

### 2. Generate AGENTS.md for Codex

Adapt the core philosophy from CLAUDE.md into AGENTS.md format. Key adaptations:

**Structure**:
- AGENTS.md should be concise but complete
- Include Ousterhout framework
- Include persona definitions
- Include red flags checklist
- Reference Codex-specific tools (rg, ast-grep)

**Content to port**:
- Software Design Philosophy section
- Complexity Management principles
- Module Design guidance
- Red flags (Manager/Util/Helper, pass-throughs, etc.)
- Persona vocabulary (Carmack, Jobs, Torvalds, Hara, Ousterhout)

**Write to**: `~/.codex/AGENTS.md`

### 3. Generate GEMINI.md for Gemini

Create a comprehensive GEMINI.md (currently empty). Key adaptations:

**Structure**:
- Similar depth to CLAUDE.md
- Leverage Gemini strengths: shell interpolation `!{cmd}`, multimodal, Google grounding
- Include full Ousterhout framework
- Include persona definitions

**Content to port**:
- Full Software Design Philosophy
- Complexity Management
- Module Design
- Red flags checklist
- Persona vocabulary
- Tool usage guidance (adapted for Gemini capabilities)

**Write to**: `~/.gemini/GEMINI.md`

### 4. Port Core Commands

Identify commands that should exist in all three tools:

**Core workflow** (always sync):
- prime, spec, plan, execute, ship
- ultrathink, carmack, aesthetic
- quality-check, triage, observe
- flesh, architect, debug

**Claude-specific** (don't sync):
- Commands that heavily use subagents
- Commands that depend on Claude-specific skills

**Adaptation rules**:

For **Codex** (prompts/*.md):
- Keep markdown format
- Add YAML frontmatter with name, description, aliases, enabled
- Reference Codex tools (rg, ast-grep, gemini CLI for research)
- Remove Claude-specific skill references

For **Gemini** (commands/*.toml):
- Convert to TOML format
- Use shell interpolation: `!{cat TODO.md}`, `!{ls -F}`
- Use `{{args}}` for arguments
- Keep prompts concise but complete

### 5. Apply Sync Policy

**SYNC** (must be consistent):
- Ousterhout principles as default lens
- Red flags checklist
- Persona definitions (Carmack, Jobs, Torvalds, Hara, Ousterhout)
- Core workflow commands
- Commit/PR standards
- Testing philosophy

**DIVERGE** (preserve tool strengths):
- **Claude**: Full subagent ecosystem, skill library, MCP integrations
- **Codex**: Reasoning effort settings, simpler execution model
- **Gemini**: Shell interpolation, multimodal analysis, Google grounding

### 6. Generate Sync Report

Output a clear report:

```markdown
## Sync Report

### Base Configuration
- AGENTS.md: [UPDATED/CREATED/UNCHANGED] - [line count] lines
- GEMINI.md: [UPDATED/CREATED/UNCHANGED] - [line count] lines

### Commands Synced

| Command | Codex | Gemini | Notes |
|---------|-------|--------|-------|
| ultrathink | ✅ | ✅ | |
| carmack | ✅ | ✅ | |
| execute | ✅ | ✅ | |
| ... | | | |

### Commands Skipped (Claude-specific)
- [command]: [reason]

### Manual Attention Needed
- [any issues or warnings]

### Next Steps
1. Review generated files
2. Test commands in each tool
3. Run `/sync-configs` again after significant Claude Code changes
```

## Adaptation Guidelines

### Philosophy Adaptation

When porting philosophy content:

1. **Preserve the core** - Ousterhout principles, complexity focus, red flags
2. **Adapt the examples** - Use tool-appropriate references
3. **Maintain the tone** - Concise, direct, zero fluff
4. **Include personas** - Define Carmack/Jobs/Torvalds/Hara/Ousterhout vocabulary

### Command Adaptation

When porting commands:

1. **Preserve ALL richness** - Same personas, examples, red flags, philosophy, output formats
2. **Adapt the mechanics** - Shell interpolation for Gemini, tool refs for Codex
3. **NEVER strip content** - Gemini TOML should have identical depth to Claude md (only format changes)
4. **Test the output** - Verify commands work in target tool

**CRITICAL**: The Gemini TOML format can hold just as much content as Claude markdown. Converting format does NOT mean reducing content. A 400-line Claude command should become a 400-line Gemini command. Every persona quote, every red flag, every example must transfer.

**Anti-pattern to AVOID**: Stripping rich Claude prompts down to bare-bones Gemini commands. This destroys the prompt engineering that makes commands effective.

### TOML Format for Gemini

**CORRECT (Rich, complete prompt engineering):**

```toml
description = "Deep critical evaluation of plans for simplicity and system health"
prompt = """
# ULTRATHINK

> **THE MASTERS OF SIMPLICITY**
>
> **Steve Jobs**: "Simple can be harder than complex..."
> **John Ousterhout**: "The most fundamental problem in computer science is problem decomposition..."
> **John Carmack**: "It's done when it's right..."

You're an IQ 155 principal architect who's seen 50+ systems collapse under their own complexity...

## Your Mission
[Full mission with context question]

## The Ousterhout Framework

### 1. Complexity Analysis
[Full framework with bullet points, red flags]

### 2. Module Depth Evaluation
[Full evaluation criteria with formula, examples]

[... ALL sections from Claude version ...]

## Red Flags Checklist
- [ ] Shallow modules
- [ ] Information leakage
[... complete list ...]

## Output Format
[Full structured output template]

## Philosophy
[Rich closing philosophy section]
"""
```

**WRONG (Stripped down, lost all value):**

```toml
description = "Evaluate plans"
prompt = """
# ULTRATHINK

> Simple is better

Review the plan for issues.

## Process
1. Check complexity
2. Find problems
3. Report findings
"""
```

The first example preserves all prompt engineering. The second destroys it. **Always use the first pattern.**

## When to Run

- After significant changes to Claude Code commands
- After adding new skills you want everywhere
- After updating CLAUDE.md philosophy sections
- Periodically to catch drift

## Example Sync

Running `/sync-configs` should:

1. Read ~/.claude/CLAUDE.md → generate adapted AGENTS.md and GEMINI.md
2. Read ~/.claude/commands/ultrathink.md → generate:
   - ~/.codex/prompts/ultrathink.md (adapted)
   - ~/.gemini/commands/ultrathink.toml (converted)
3. Report what changed

The goal: run `codex` or `gemini` and get the same quality bar, same philosophy, same workflow - just adapted for each tool's strengths.
