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
- Get specific file:line references with confidence scores
- Update pattern memory for future searches

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

**Generate clarifying questions**:
Based on the initial task and research findings, create a bunch of high impact and useful yes/no questions that would clarify requirements:

```markdown
## Clarifying Questions for [Task Title]

### Scope & Features
1. Should this feature support [specific capability]?
2. Do we need [specific integration] in the initial version?
3. Should the implementation handle [edge case/scenario]?

### Technical Approach
4. Should we use [technology A] or [technology B] for [component]?
5. Do we need to maintain backward compatibility with [existing system]?
6. Should this be implemented as [approach A] or [approach B]?

### Performance & Scale
7. Do we need to support [specific performance target]?
8. Should this handle [scale requirement] in the initial version?
9. Is [caching/optimization strategy] required?

### Security & Compliance
10. Does this need [specific security measure]?
11. Should we implement [authentication/authorization] requirements?
12. Are there [compliance/regulatory] considerations?

### User Experience
13. Should the interface support [specific UX pattern]?
14. Do we need [accessibility features] in the initial version?
15. Should this include [user feedback/monitoring] capabilities?
```

Ask these questions to the user and get their answers. Incorporate the answers into the TASK.md description, then rinse and repeat this process from the top. Do this a couple times, until the TASK.md file is crystal clear and we've fleshed out the spec and mitigated most of the uncertainty.

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

### Technology Stack
- **Frontend**: [Framework choice] because [rationale]
- **Backend**: [Framework/language choice] because [rationale]
- **Database**: [Database choice] because [rationale]
- **External Services**: [Service choices] because [rationale]

### Design Patterns
- **Architecture Pattern**: [Choice] because [rationale]
- **Data Flow**: [Pattern] because [rationale]
- **Integration Pattern**: [Approach] because [rationale]

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

