Transform a basic TASK.md into a comprehensive specification through parallel research and requirement clarification.

# SPEC

Read the initial TASK.md description and enhance it with detailed requirements, constraints, architecture decisions, and implementation strategy through comprehensive research.

## 1. Initial Task Analysis

**Read and understand the task**:
- Read @TASK.md thoroughly
- Extract core objectives and scope
- Identify domain and technology hints
- Note any explicit requirements or constraints
- Assess complexity and research needs
- Ultrathink

## 2. Parallel Research Pipeline

Launch specialized research using native subagents and Task tool:

### Pattern Discovery (Native Subagent)
Invoke `pattern-scout` to find similar implementations in the codebase:
- Search for existing patterns matching the task requirements
- Identify reusable components and implementation examples
- Get specific file:line references with implementation guidance
- Update knowledge.md with genuinely useful new patterns

**How to invoke**: Use Task tool with subagent_type: "general-purpose" and prompt to act as pattern-scout from /Users/phaedrus/.claude/agents/pattern-scout.md

### External Research (Task Agents)
```
Task 1: "Web Research Expert - Research the task described in TASK.md using gemini --prompt. Focus on:
- Current industry best practices and patterns for this type of task
- Latest technology choices and frameworks recommended in 2025
- Common implementation approaches and their trade-offs
- Performance considerations and scalability patterns
- Security best practices for this domain
- Real-world examples and case studies
- Ultrathink
Use multiple gemini queries to gather comprehensive insights. DO NOT modify files - output research findings directly."

Task 2: "Documentation Expert - Research relevant libraries and frameworks for the task in TASK.md using Context7 MCP. Focus on:
- Identify potentially relevant libraries/frameworks based on task description
- Use mcp__context7__resolve-library-id to find matching libraries
- Use mcp__context7__get-library-docs to get current documentation
- Extract key capabilities, APIs, configuration options, and best practices
- Note version compatibility and integration requirements
- Ultrathink
DO NOT modify files - output documentation findings directly."
```

## 3. Requirements Clarification

### Requirements Analysis (Native Subagent)
Invoke `requirements-oracle` to generate high-impact clarifying questions:
- Analyze task for ambiguities and hidden complexities
- Check knowledge.md for similar past projects and valuable question patterns
- Generate prioritized questions that prevent rework
- Track which questions reveal missing requirements
- Learn from question effectiveness for future projects

**How to invoke**: Use Task tool with subagent_type: "general-purpose" and prompt to act as requirements-oracle from /Users/phaedrus/.claude/agents/requirements-oracle.md

**Process**:
1. Get clarifying questions from requirements-oracle
2. Ask the critical and important questions to the user
3. Incorporate answers into the TASK.md description
4. Repeat if significant ambiguities remain
5. Update knowledge.md with valuable questions that prevent rework

Continue this cycle until the TASK.md is crystal clear and uncertainty is minimized.

## 4. Synthesis and Enhancement

**Enhance TASK.md with comprehensive specification**:
Append detailed sections to @TASK.md based on research findings:

```markdown

---

# Enhanced Specification

## Research Findings

### Industry Best Practices
[Key insights from web research about current approaches and patterns]

### Technology Analysis
[Framework/library recommendations from Context7 research with rationale]

### Codebase Integration
[Existing patterns to follow and reusable components identified]

## Detailed Requirements

### Functional Requirements
- [Requirement 1]: [Description with acceptance criteria]
- [Requirement 2]: [Description with acceptance criteria]
- [Requirement 3]: [Description with acceptance criteria]

### Non-Functional Requirements
- **Performance**: [Specific targets and constraints]
- **Security**: [Authentication, authorization, data protection needs]
- **Scalability**: [Expected load and growth considerations]
- **Availability**: [Uptime requirements and disaster recovery]

## Architecture Decisions

### Generate ADR (Native Subagent)
Invoke `adr-architect` to propose architecture decisions:
- Analyze requirements and constraints from research
- Check adr-outcomes.md for similar past decisions and outcomes
- Generate formal ADR with trade-offs and alternatives
- Include lessons from past architectural decisions

**How to invoke**: Use Task tool with subagent_type: "general-purpose" and prompt to act as adr-architect from /Users/phaedrus/.claude/agents/adr-architect.md

### Technology Stack
- **Frontend**: [Framework choice] because [rationale from ADR]
- **Backend**: [Framework/language choice] because [rationale from ADR]
- **Database**: [Database choice] because [rationale from ADR]
- **External Services**: [Service choices] because [rationale from ADR]

### Design Patterns
- **Architecture Pattern**: [Choice from ADR] because [rationale]
- **Data Flow**: [Pattern from ADR] because [rationale]
- **Integration Pattern**: [Approach from ADR] because [rationale]

### Proposed ADR
[Include the full ADR generated by adr-architect here]

## Implementation Strategy

### Development Approach
[Methodology, phases, and sequence of implementation]

### MVP Definition
1. [Core feature 1]
2. [Core feature 2]
3. [Core feature 3]

### Technical Risks
- **Risk 1**: [Description] → Mitigation: [Strategy]
- **Risk 2**: [Description] → Mitigation: [Strategy]
- **Risk 3**: [Description] → Mitigation: [Strategy]

## Integration Requirements

### Existing System Impact
[Systems that will be affected and integration points]

### API Design
[Endpoints, data formats, and integration patterns]

### Data Migration
[Any data migration or transformation needs]

## Testing Strategy

### Unit Testing
[Coverage requirements and testing frameworks]

### Integration Testing
[API testing, service communication validation]

### End-to-End Testing
[User workflow validation and acceptance criteria]

## Deployment Considerations

### Environment Requirements
[Infrastructure, dependencies, configuration]

### Rollout Strategy
[Deployment phases, feature flags, monitoring]

### Monitoring & Observability
[Metrics, logging, alerting requirements]

## Success Criteria

### Acceptance Criteria
[Specific, measurable criteria for completion]

### Performance Metrics
[KPIs and performance targets]

### User Experience Goals
[UX metrics and user satisfaction targets]

## Future Enhancements

### Post-MVP Features
[Features deferred to future iterations]

### Scalability Roadmap
[Long-term scaling and enhancement plans]
```

## 5. Validation

**Review enhanced specification**:
- Ensure all research findings are integrated
- Verify requirements are specific and testable
- Confirm architecture decisions have clear rationale
- Validate implementation strategy is feasible
- Check that success criteria are measurable

## 6. Post-Specification Learning

After completing the specification, invoke lesson-harvester to capture insights:

**How to invoke**: Use Task tool with subagent_type: "general-purpose" and prompt to act as lesson-harvester from /Users/phaedrus/.claude/agents/lesson-harvester.md, providing:
- Which clarifying questions proved most valuable
- Architecture patterns that emerged
- Research findings that changed the approach
- Complexity estimation accuracy
- Requirements that were initially missed

The lesson-harvester will:
- Update knowledge.md with high-value clarifications and successful architecture patterns
- Track specification accuracy for future estimates
- Note common requirement blind spots

