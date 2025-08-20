# ADR-001: Native Subagents with Persistent Memory

**Date**: 2025-01-20
**Status**: Accepted
**Deciders**: Development team, Claude Code architecture discussion

## Context

The existing Claude Code workflow used the Task tool with inline prompts to create parallel "agents" for complex operations like debugging, specification, and backlog grooming. This approach had several limitations:

- No persistent memory between invocations
- Verbose inline prompts cluttering command files
- No learning from past experiences
- Duplicated logic across commands
- Difficult to maintain consistency across different Task invocations

The introduction of native subagent support in Claude Code presented an opportunity to redesign this architecture for better maintainability and capability.

## Decision

We will convert from Task tool patterns to native subagents with persistent memory systems. Specifically:

1. Create dedicated subagent files in `/agents/` directory
2. Implement memory systems in `/agents/memory/` for agents that learn
3. Use YAML frontmatter for agent configuration
4. Invoke subagents via Task tool with standardized pattern
5. Limit total subagents to 10-12 focused agents
6. Only add memory to agents where learning provides value

## Consequences

### Positive
- **Persistent Learning**: Agents remember patterns, bugs, and decisions across sessions
- **Cleaner Commands**: Command files reduced by 30-70% in size
- **Maintainability**: Centralized agent definitions easier to update
- **Compounding Value**: System gets smarter over time through memory
- **Consistency**: Standardized invocation and memory patterns

### Negative
- **Migration Effort**: Requires converting all existing Task patterns
- **Complexity**: Memory management adds new layer to maintain
- **Testing Challenge**: Need real files to test agents (TASK.md, ISSUE.md)
- **Learning Curve**: Team needs to understand new invocation patterns

### Neutral
- Change from inline prompts to file-based agent definitions
- Introduction of memory pruning and maintenance considerations
- Shift from stateless to stateful agent operations

## Options Considered

### Option 1: Keep Task Tool Patterns (Status Quo)
**Description**: Continue using inline Task tool prompts in commands
**Pros**: 
- No migration needed
- Already working
- Simple, self-contained
**Cons**: 
- No learning/memory
- Verbose command files
- Duplicate logic

### Option 2: Native Subagents WITHOUT Memory
**Description**: Convert to native subagents but keep them stateless
**Pros**: 
- Cleaner than inline prompts
- Easier to maintain
- No memory complexity
**Cons**: 
- Miss learning opportunity
- No improvement over time
- Repeated mistakes

### Option 3: Native Subagents WITH Memory (Chosen)
**Description**: Native subagents with selective persistent memory
**Pros**: 
- Learning and improvement
- Clean architecture
- Compounding value
**Cons**: 
- Memory management overhead
- More complex implementation
- Storage considerations

## Implementation Notes

- Start with high-value commands (debug, spec, execute)
- Create memory only for agents that truly benefit (bug-historian, pattern-scout, adr-architect)
- Use simple markdown format for memory files
- Implement confidence scoring (0-100%) for agent outputs
- Batch agent invocations where possible for performance
- Document clear invocation patterns in each command

Memory structure:
```
/agents/
  ├── [agent-name].md      # Agent definition
  └── memory/
      ├── bugs.md          # Bug patterns and solutions
      ├── patterns.md      # Code patterns and locations
      └── adr-outcomes.md  # Decision outcomes
```

## Review Notes

[To be filled after initial implementation period]

**Review Date**: [Pending]
**Actual Outcomes**:
- [To be assessed]

**Lessons Learned**:
- [To be documented]

**Recommendation**: [To be determined]