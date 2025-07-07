Review and refine CLAUDE.md to ensure it contains the most effective tools, patterns, and guidance.

# META UPDATE CLAUDE

Systematically review and update CLAUDE.md to keep it sharp, relevant, and immediately useful.

## Review Process

### 1. **Current State Analysis**
**Evaluate CLAUDE.md sections**:
- Development Philosophy
- Essential Tools (gemini, ast-grep, thinktank, Task)
- Reasoning Budget Control
- Any project-specific additions

### 2. **Tool Effectiveness Review**
**Assess each documented tool**:
- Is it still actively used?
- Are the examples current and helpful?
- Should it be promoted/demoted in the hierarchy?
- Are there new tools that deserve inclusion?

### 3. **Pattern Recognition**
**Identify recurring patterns worth documenting**:
- Successful command sequences
- Common tool combinations
- Effective reasoning strategies
- Workflow optimizations

### 4. **Update Guidelines**

**Structure principles**:
- Most-used tools at the top
- Concrete examples over abstractions
- Remove outdated or unused sections
- Keep it scannable and actionable

**Content principles**:
- Document what works, not what might work
- Prefer specific commands to general advice
- Include warnings for common pitfalls
- Update examples to reflect current usage

### 5. **Common Updates**

**Tool section updates**:
```markdown
## Essential Tools

**Research & Information:**
* gemini --prompt "specific technical question"
* WebSearch for current events/documentation

**Code Analysis:**
* ast-grep for semantic pattern matching
* rg (ripgrep) for fast text search
```

**Workflow patterns**:
```markdown
## Proven Workflows

**Feature Development:**
/spec → /plan → /execute → /git-pr

**Debugging:**
/debug → identify root cause → /execute fix

**Documentation:**
/docs-sync after major changes
```

### 6. **Quality Checklist**

Before saving updates:
- [ ] All tools have working examples
- [ ] Removed any unused sections
- [ ] Examples use actual commands
- [ ] Instructions are clear and concise
- [ ] No redundant information

**Remember**: CLAUDE.md should be a living reference that gets better through actual usage, not theoretical improvements.