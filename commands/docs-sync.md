Synchronize documentation with actual usage patterns and learnings from TODO.md work logs.

# DOCS-SYNC

Analyze work patterns, extract learnings, and update documentation to be tight, punchy, clear, accurate, and useful.

## 1. Extract Learnings from Work Logs

**Analyze TODO.md execution logs**:
- Think hard about patterns in TODO.md execution logs
- Extract key learnings, decisions, and discoveries
- Identify recurring challenges and solutions
- Note successful approaches and workflows
- Collect innovative techniques discovered during implementation

**Pattern categories to identify**:
- **Workflow patterns**: Successful task progressions
- **Technical patterns**: Repeated solutions, tools, approaches
- **Decision patterns**: Common reasoning, trade-offs
- **Error patterns**: Frequent blockers and their resolutions
- **Innovation patterns**: Creative solutions worth documenting

## 2. Scan Current Documentation State

**Comprehensive documentation audit**:
```
- Read all *.md files in commands/ directory
- Read CLAUDE.md for current guidance
- Read README.md for project overview
- Read any project-specific docs (docs/leyline/, etc.)
- Note documentation gaps and inconsistencies
```

**Assessment criteria**:
- **Accuracy**: Does documentation match actual implementation?
- **Completeness**: Are all commands and features documented?
- **Clarity**: Is language clear and unambiguous?
- **Usefulness**: Does it help users accomplish tasks?
- **Conciseness**: Can it be said with fewer words?

## 3. Synthesize Updates

**Think very hard about documentation improvements**:
- Merge extracted learnings with existing documentation
- Identify outdated information to remove
- Add newly discovered patterns and best practices
- Clarify ambiguous sections based on actual usage
- Streamline verbose explanations

**Documentation principles**:
- **Be direct**: Skip preambles, get to the point
- **Be specific**: Use concrete examples from work logs
- **Be actionable**: Focus on what users should DO
- **Be concise**: Every word should earn its place
- **Be current**: Reflect the latest patterns and tools

## 4. Update CLAUDE.md

**Enhance with work-derived insights**:
```markdown
# CLAUDE

## Essential Tools
[Update based on frequently used tools from logs]

## Proven Workflows
[Add successful patterns from TODO.md executions]

## Common Solutions
[Document recurring fixes and approaches]

## Key Learnings
[Insights that would help future work]
```

**Focus areas**:
- Tool usage patterns that proved effective
- Workflow combinations that work well
- Gotchas and their solutions
- Performance tips discovered
- Debugging strategies that succeeded

## 5. Update README.md

**Refresh project overview**:
```markdown
# Project Name

## Quick Start
[Most efficient path based on logs]

## Core Commands
[Organized by actual usage frequency]

## Workflows
[Real examples from successful executions]

## Recent Improvements
[Notable enhancements from TODO.md]
```

**Prioritize**:
- Most-used commands and workflows
- Clearest getting-started path
- Real examples over theoretical ones
- Practical tips from experience

## 6. Update Command Documentation

**For each command that was used**:
- Update examples with real ones from logs
- Add discovered edge cases
- Clarify ambiguous instructions
- Add performance notes if relevant
- Remove outdated information

**Documentation template**:
```markdown
Brief one-line description of what command does.

# COMMAND-NAME

Slightly expanded description focusing on the value provided.

## Usage
[Real example from logs]

## Key Points
- [Discovered insight 1]
- [Discovered insight 2]
- [Important gotcha]

## Success Patterns
[What worked well in practice]
```

## 7. Create Update Summary

**Document what changed**:
```markdown
## Documentation Sync Summary [Date]

### Patterns Extracted
- [Pattern 1]: [Brief description]
- [Pattern 2]: [Brief description]

### Major Updates
- CLAUDE.md: [What was added/changed]
- README.md: [What was added/changed]
- Commands: [Which ones were updated]

### Key Improvements
- [Clarity improvement 1]
- [New insight added]
- [Outdated info removed]
```

## Execution Flow

1. Read and analyze TODO.md for patterns
2. Scan all documentation files
3. Think very hard about improvements
4. Update CLAUDE.md with practical insights
5. Update README.md for clarity and usefulness
6. Update individual command docs as needed
7. Generate summary of changes

## Success Criteria

✓ Documentation reflects actual usage patterns
✓ Learnings from work logs are captured
✓ Language is tighter and more direct
✓ Examples are real, not theoretical
✓ Users can accomplish tasks faster
✓ No outdated or incorrect information remains