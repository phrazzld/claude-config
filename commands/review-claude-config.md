---
description: Audit Claude Code config (commands, skills, agents, hooks) against best practices
argument-hint: "[focus: skills|commands|agents|hooks|all|<name>]"
---
# REVIEW-CLAUDE-CONFIG

Audit Claude Code configuration for quality, overlap, and gaps.

## Role

Senior architect auditing Claude Code extensibility layer.

## Objective

1. Find structural issues (missing frontmatter, oversized files, poor triggers)
2. Find semantic issues (overlap, misclassification, weak philosophy)
3. Suggest improvements, consolidations, expansions
4. Prioritize by impact

## Quality Checklist

### Skills (`~/.claude/skills/`)
- [ ] Frontmatter: `name` (≤64 chars), `description` (~100 words, trigger-rich)
- [ ] SKILL.md lean (<100 lines) OR uses references/
- [ ] Trigger terms: action verbs, domain nouns, tool names, problem phrases
- [ ] Has philosophy section (why, not just how)
- [ ] Has anti-patterns (what NOT to do)
- [ ] No semantic overlap with other skills

### Commands (`~/.claude/commands/`)
- [ ] Frontmatter: `description`, optional `argument-hint`, `allowed-tools`
- [ ] Clear phases with completion criteria
- [ ] Orchestrates workflow (doesn't duplicate skill knowledge)

### Agents (`~/.claude/agents/`)
- [ ] Clear role definition
- [ ] Appropriate tool restrictions
- [ ] No overlap with skills or commands

### Hooks (`~/.claude/hooks/`)
- [ ] Executable and tested
- [ ] Clear purpose in filename
- [ ] Appropriate trigger events

## Process

1. **Inventory** - List all artifacts with line counts
2. **Structural audit** - Check each against checklist above
3. **Quality audit** - Evaluate triggers, philosophy, examples
4. **Overlap detection** - Find semantic duplicates or near-duplicates
5. **Gap analysis** - Compare coverage to user's tech stack (from CLAUDE.md)
6. **Report** - Talk through findings conversationally

## Output

Group findings by:
1. **Fixes needed** - Specific issues with specific artifacts
2. **Consolidation candidates** - Artifacts to merge
3. **Expansion opportunities** - New artifacts worth creating
4. **Priorities** - What to fix first

Offer to implement changes after reporting.

## Reference Standards

- `~/.claude/skills/skill-builder/` - Meta skill defining skill quality
- `~/.claude/skills/llm-communication/` - Principles for LLM instructions
