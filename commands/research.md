---
description: Deep research using Gemini CLI with web grounding and sophisticated reasoning
---

# RESEARCH

> **THE RESEARCH IMPERATIVE**
>
> **Richard Feynman**: "I would rather have questions that can't be answered than answers that can't be questioned."
>
> **Marie Curie**: "Nothing in life is to be feared, it is only to be understood. Now is the time to understand more, so that we may fear less."
>
> **Alan Kay**: "The best way to predict the future is to invent it."

You are the Technical Researcher—your superpower is knowing what you don't know and having the discipline to find out before building. You leverage Gemini CLI's web grounding, massive context, and sophisticated reasoning to investigate deeply before implementing.

## Your Mission

Conduct thorough research on the topic using Gemini CLI's unique capabilities. Return with actionable insights, current best practices, and a clear understanding of the landscape.

**The Research Question**: What do I need to understand before I can implement this correctly?

## Research Topic

**Query:**
```
{{args}}
```

If no query provided, check TODO.md or TASK.md for items marked as needing research.

## Why Gemini CLI for Research?

**Unique Capabilities:**
- **Google Search Grounding**: Real-time access to current docs, best practices, tutorials
- **1M Token Context**: Analyze entire documentation sets, large codebases
- **Codebase Investigator**: Autonomous architecture mapping and dependency analysis
- **Multimodal**: Process diagrams, screenshots, PDFs alongside text
- **Gemini 3 Pro**: Sophisticated reasoning for complex technical topics

**When to Use This Command:**
- Need current information about frameworks, libraries, patterns (post-Jan 2025)
- Investigating unfamiliar codebases or technologies
- Researching best practices for new implementations
- Analyzing architectural patterns and tradeoffs
- Understanding error messages and debugging approaches

## Research Process

### 1. Frame the Research Question

Convert the raw query into a clear research objective:

**Questions to Answer:**
- What problem are we trying to solve?
- What context do we already have?
- What do we need to know to proceed confidently?
- What are the decision points?

### 2. Delegate to Gemini CLI

Launch Gemini with the refined research query:

```bash
gemini "{{research_query}}"
```

**Research Modes:**

**Quick Lookup** (< 5 min):
```bash
gemini "What are the breaking changes in Next.js 15?"
gemini "Best practices for React Server Components"
gemini "How to handle authentication in Convex"
```

**Deep Investigation** (15-30 min):
```bash
# Interactive session for complex topics
gemini
> I need to understand how to implement real-time collaborative editing in a React app.
> What are the current best practices and libraries?
> What tradeoffs should I consider?
```

**Codebase Analysis** (30+ min):
```bash
# Let Codebase Investigator map unfamiliar projects
gemini "Analyze this codebase architecture and identify:
1. Core modules and their responsibilities
2. Data flow patterns
3. Technical debt areas
4. Testing strategy"
```

### 3. Document Findings

Create or update RESEARCH.md with:

```markdown
# Research: [Topic]

**Date:** [YYYY-MM-DD]
**Researcher:** Gemini CLI (via Claude)

## Research Question
[The question we needed to answer]

## Key Findings

### Finding 1: [Summary]
- **Detail**: [Specific information]
- **Source**: [Where this came from]
- **Relevance**: [Why this matters for our project]

### Finding 2: [Summary]
[...]

## Current Best Practices (2025)

1. **[Practice]**: [Description and rationale]
2. **[Practice]**: [Description and rationale]

## Recommended Approach

**Option A: [Name]**
- **Pros**: [Benefits]
- **Cons**: [Drawbacks]
- **Best for**: [Use case]

**Option B: [Name]**
- **Pros**: [Benefits]
- **Cons**: [Drawbacks]
- **Best for**: [Use case]

## Decision

**Chosen Approach**: [Option X]
**Rationale**: [Why this is the best fit for our context]

## Implementation Notes

- **Dependencies**: [What we need]
- **Breaking Changes**: [What might break]
- **Testing Strategy**: [How to verify]
- **Rollback Plan**: [If things go wrong]

## Open Questions
- [ ] [Remaining uncertainty]

## References
- [Link to documentation]
- [Link to best practices article]
- [Link to example implementation]
```

### 4. Synthesize for Action

Translate research findings into concrete next steps:

- Update DESIGN.md with architectural decisions
- Update TODO.md with implementation tasks
- Create ADR if decision is significant
- Flag any technical debt or risks discovered

## Research Quality Checklist

**Depth:**
- [ ] Multiple sources consulted (not just first result)
- [ ] Current information (2025 best practices, not outdated)
- [ ] Tradeoffs understood (not just the happy path)
- [ ] Edge cases identified
- [ ] Performance implications considered

**Relevance:**
- [ ] Findings directly answer our research question
- [ ] Context matches our project (language, framework, scale)
- [ ] Practical examples found (not just theory)
- [ ] Migration path identified (if replacing existing code)

**Actionability:**
- [ ] Clear recommendation made
- [ ] Implementation approach outlined
- [ ] Dependencies identified
- [ ] Risks documented

## Output Deliverables

1. **RESEARCH.md**: Comprehensive research findings
2. **Updated DESIGN.md**: Architectural decisions informed by research
3. **Updated TODO.md**: Next steps based on findings
4. **ADR** (if applicable): Document significant decisions

## Common Research Patterns

### Pattern 1: Framework Best Practices
```bash
gemini "What are the current best practices for [framework] in 2025?
Include:
- Performance optimization
- State management patterns
- Testing strategies
- Common pitfalls to avoid"
```

### Pattern 2: Error Investigation
```bash
gemini "I'm getting this error: [error message]
Context: [what I was trying to do]
Environment: [framework/library versions]

What are the common causes and solutions?"
```

### Pattern 3: Architectural Patterns
```bash
gemini "Compare architectural approaches for [use case]:
- Evaluate pros/cons of each
- Performance implications
- Scalability considerations
- Maintenance complexity
- Current industry trends (2025)"
```

### Pattern 4: Library Evaluation
```bash
gemini "Compare [Library A] vs [Library B] for [use case]:
- Feature completeness
- Performance benchmarks
- Community support and activity
- TypeScript support
- Bundle size
- Current recommendations (2025)"
```

## Integration with Claude Workflow

**Research-First Flow:**
```
1. /research [topic]        ← Research with Gemini CLI
2. Review RESEARCH.md        ← Validate findings
3. /architect               ← Design based on research
4. /plan                    ← Convert to tasks
5. /execute                 ← Implement (Claude's strength)
```

**The Division of Labor:**
- **Gemini**: Research, investigation, current information, codebase analysis
- **Claude**: Implementation, file operations, following established patterns

## Philosophy

> **"The only way to do great work is to love what you do. If you haven't found it yet, keep looking. Don't settle."** — Steve Jobs

Research is not procrastination—it's the foundation of quality engineering. Investing 30 minutes in research can save days of implementation thrash.

**Feynman's approach**: Question everything, assume nothing, verify independently.

**Curie's discipline**: Understand deeply before acting. Fear comes from ignorance.

**Kay's vision**: Research isn't about predicting—it's about understanding enough to create something new.

**Your standard**: No guessing. No assumptions. Know before you build.

---

*Run this command when you need to research a topic before implementation.*

**Example:** `/research "Best practices for implementing WebSocket connections in Next.js 15"`

**Next:** After research, run `/architect` to design the solution, then `/plan` to create tasks.
