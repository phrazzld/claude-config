Transform vague ideas into precise specifications through deep investigation and clarification.

# SPEC

Channel Dijkstra's precision: "The question of whether a computer can think is no more interesting than the question of whether a submarine can swim."

## The Dijkstra Principle

*"Simplicity is prerequisite for reliability."*

A specification isn't about what you want to build - it's about what must work.

## Workflow Detection

**First, check if continuing from Phase 1:**
```bash
if [ -f ".spec-context.json" ]; then
  echo "Found existing spec context. Continuing to Phase 2..."
  # Jump to Phase 2: Contextual Refinement
else
  echo "Starting fresh specification investigation..."
  # Continue with Phase 1
fi
```

---

# PHASE 1: INVESTIGATION & CLARIFICATION

## 1. Task Analysis & Deep Investigation

**What would Dijkstra specify?**
- Read @TASK.md with a critical eye
- Extract invariants that must hold
- Define preconditions and postconditions
- Identify edge cases before features

**Ultrathink: The Investigation Phase**
- What are the core problems we're actually solving?
- What are 3-5 fundamentally different approaches?
- What are the tradeoffs between simplicity and flexibility?
- Where are the natural system boundaries?
- What constraints are real vs. assumed?
- What would this look like if built from scratch today?
- What existing solutions can we learn from or build upon?

## 2. Parallel Research & Architecture Exploration

**Gather intelligence through comprehensive parallel research:**

```
Task 1: "Research current best practices for the task in TASK.md:
- Use gemini --prompt for industry patterns and 2025 standards
- Find proven architectural approaches and their tradeoffs
- Identify common failure modes and how to prevent them
- Security vulnerabilities and mitigation strategies
- Performance bottlenecks and optimization patterns
Focus on production-proven solutions with real-world validation."

Task 2: "Find relevant documentation using Context7 MCP:
- Resolve library IDs for potential technology choices
- Compare APIs and capabilities of alternative solutions
- Extract configuration patterns and best practices
- Note version constraints, breaking changes, and migration paths
- Identify ecosystem maturity and community support
Prioritize battle-tested libraries with strong documentation."

Task 3: "Explore alternative architectures and implementations:
- Use ast-grep to find similar patterns in the codebase
- Research competing approaches (monolith vs microservices, sync vs async, etc.)
- Evaluate different toolchains and build systems
- Consider data flow patterns (event-driven, request-response, streaming)
- Assess integration complexity with existing systems
Bring back 3-5 concrete alternatives with pros/cons."
```

## 3. Design Brainstorming & Evaluation

**Channel Thompson's simplicity while exploring alternatives:**

### Pattern Discovery
- Grep codebase for existing patterns we can leverage
- Find what already works and why
- Identify reusable components and abstractions
- Note architectural decisions we must respect

### Alternative Approaches (Generate 3-5)
For each approach, consider:
- **Approach Name**: Brief description
- **Complexity**: Implementation and maintenance burden
- **Performance**: Expected throughput, latency, resource usage
- **Scalability**: How it handles growth
- **Risk**: What could go wrong
- **Time**: Realistic implementation estimate

### Evaluation Matrix
| Approach | Simplicity | Performance | Maintainability | Risk | Time |
|----------|------------|-------------|-----------------|------|------|
| Option 1 | High/Med/Low | Score | Score | Score | Estimate |
| Option 2 | ... | ... | ... | ... | ... |

**Recommendation**: [Selected approach with justification based on Dijkstra's simplicity principle]

## 4. Clarifying Questions Generation

**Generate concrete questions to refine the specification:**

### Critical Questions (Must answer before proceeding)
1. **Scale**: What's the expected load? (users, requests/sec, data volume)
2. **Constraints**: What are the hard limits? (budget, timeline, team size)
3. **Integration**: What systems must this work with? What are their APIs?
4. **Users**: Who exactly will use this? What's their technical level?
5. **Success**: How will we measure success? What metrics matter?

### Design Questions (Shape the architecture)
6. **Flexibility**: What needs to be configurable vs. hardcoded?
7. **Evolution**: What features are likely to be added in 6 months?
8. **[Add 1-3 context-specific questions based on research findings]**

### Save Context for Phase 2

**Store investigation findings and questions:**
```bash
cat > .spec-context.json << 'EOF'
{
  "timestamp": "$(date -Iseconds)",
  "task": "[original task from TASK.md]",
  "research_findings": {
    "best_practices": "[summarized findings from research]",
    "architecture_options": "[evaluated approaches with tradeoffs]",
    "constraints_discovered": "[technical limitations found]",
    "existing_patterns": "[relevant patterns in codebase]"
  },
  "questions": [
    "Scale: What's the expected load?",
    "Constraints: What are the hard limits?",
    "[...all questions listed above...]"
  ],
  "preliminary_recommendation": "[initial approach based on research]"
}
EOF
```

## 🛑 STOP HERE - PHASE 1 COMPLETE

**✋ DO NOT PROCEED FURTHER. Present the questions above to the user and wait for their responses.**

### Instructions for User

**Please provide answers to the questions above.** You can respond in any format:
- Numbered list (e.g., "1. We expect 1000 users...")
- Prose addressing each point
- Skip questions that don't apply

**Example response:**
```
1. Scale: ~100 concurrent users, 50 requests/sec peak
2. Constraints: 3 week timeline, 2 developers, $1000 budget
3. Integration: Existing PostgreSQL database, Stripe API
4. Users: Technical developers familiar with CLI tools
5. Success: 90% reduction in manual process time
6. Flexibility: API keys configurable, algorithm hardcoded
7. Evolution: Likely adding webhook support, batch processing
```

**After you provide answers**, run `/spec` again and I'll continue with Phase 2 to create a refined specification based on your input.

---

# PHASE 2: CONTEXTUAL REFINEMENT
*This section executes only when .spec-context.json exists with user answers*

## 5. Load Context & User Answers

**Retrieve saved investigation context:**
```bash
if [ ! -f ".spec-context.json" ]; then
  echo "ERROR: No context found. Please run /spec first to generate questions."
  exit 1
fi

context=$(cat .spec-context.json)
echo "Resuming specification from $(echo $context | jq -r .timestamp)"
```

**Process user answers:**
- Map answers to original questions
- Update constraints with concrete values
- Refine architecture based on scale/timeline
- Adjust approach for stated integrations

## 6. Targeted Refinement Research

**Launch Phase 2 research based on user's specific answers:**

```
Task 1: "Refined solution research based on user requirements:
- Use gemini --prompt to find solutions proven at [user's scale]
- Research [specific integrations] mentioned by user
- Find patterns that fit [timeline/budget] constraints
- Look for [specific features] user plans to add
Be extremely specific to their exact requirements."

Task 2: "Technical validation for user's context:
- Use Context7 MCP for [specific libraries] that fit requirements
- Verify performance at [stated load] levels
- Check compatibility with [mentioned integrations]
- Validate feasibility within [stated timeline]
Only recommend what's achievable with their constraints."

Task 3: "Risk assessment for user's specific situation:
- Identify risks specific to [their scale/timeline]
- Find common failures with [their tech stack]
- Assess complexity for [their team size]
- Evaluate maintenance burden given constraints
Be realistic about what could go wrong."
```

## 7. Final Specification Generation

**Create the refined specification incorporating all context:**

```markdown
# TASK
[Original task description preserved at top]

## Refined Specification

### Selected Approach
[Chosen architecture with justification]

### Requirements
#### Functional (What it MUST do)
- [ ] Invariant 1: [specific, testable]
- [ ] Invariant 2: [measurable outcome]

#### Non-Functional (How well it must do it)
- Performance: [specific metrics based on research]
- Security: [threat model from security analysis]
- Reliability: [failure modes and recovery]

### Constraints Discovered
- Technical: [existing system boundaries found]
- Resource: [realistic time/space limits]
- Integration: [API contracts, data formats]

### Implementation Strategy
#### Phase 1: Core Functionality
- Minimal viable solution
- Focus on critical path

#### Phase 2: Hardening
- Edge cases identified in research
- Error handling patterns
- Performance optimization opportunities

### Success Criteria
- [ ] All invariants hold
- [ ] Performance meets targets
- [ ] Security scan passes
- [ ] Integration tests pass

### Key Decisions
- [Decision 1]: [Rationale]
- [Decision 2]: [Rationale]

### Open Questions (if any remain)
- [Unresolved question needing user input]
```

### Cleanup
```bash
# Remove context file after successfully updating TASK.md
rm -f .spec-context.json
echo "Specification complete and context cleaned up."
```

## 8. Validation & Next Steps

**The Hoare Test: "There are two ways of constructing a software design: One way is to make it so simple that there are obviously no deficiencies."**

Validate the specification:
- Can this fail silently? → Document failure modes
- What happens at the boundaries? → Define edge cases
- Is this the simplest solution? → Justify complexity
- Would Dijkstra approve? → Ensure mathematical precision

**Next Command**: Run `/plan` to decompose this specification into actionable tasks

Remember: **A good specification is not when there is nothing left to add, but when there is nothing left to take away.**

## Workflow Summary

**Phase 1 (Initial Investigation):**
1. Read TASK.md and ultrathink
2. Conduct parallel research
3. Evaluate architecture alternatives
4. Generate clarifying questions
5. Save context and STOP for user input

**Phase 2 (Post-Answer Refinement):**
1. Load saved context and user answers
2. Conduct targeted research based on answers
3. Refine approach with concrete constraints
4. Update TASK.md with final specification
5. Clean up temporary files

**Key Innovation**: The specification evolves through dialogue, not guesswork.