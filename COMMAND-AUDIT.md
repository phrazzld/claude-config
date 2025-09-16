# Command Verbosity Audit Report

## Summary
Current average: 73 lines
Target average: <100 lines (already met, but outliers need attention)
Total commands: 35
Commands over 100 lines: 10 (need urgent reduction)

## Critical Findings

### 1. backlog-groom.md (227 lines → Target: 80 lines)
**Major Issues**:
- References 6+ deleted agents (security-scanner, quality-auditor, etc.)
- Excessive duplication in expert analysis sections
- Overly detailed step-by-step instructions

**Reduction Strategy**:
- Replace all deleted agent references with single helper.md invocation
- Condense repetitive analysis sections into single quality checklist
- Use persona mindset instead of verbose instructions
- Remove unnecessary examples and redundant explanations

### 2. spec.md (210 lines → Target: 80 lines)
**Major Issues**:
- Overly detailed examples for every pattern
- Redundant explanations of basic concepts
- Verbose formatting instructions

**Reduction Strategy**:
- Keep only one example per pattern type
- Remove basic concept explanations (users know what a spec is)
- Condense formatting to simple template
- Replace verbose instructions with "What would Dijkstra specify?"

### 3. plan.md (192 lines → Target: 80 lines)
**Major Issues**:
- Excessive detail on task breakdown methodology
- Repetitive phase descriptions
- Verbose success criteria for each phase

**Reduction Strategy**:
- Simplify to: Analyze → Break down → Prioritize → Write
- Remove redundant phase explanations
- Use single success metric: "Can execute immediately?"
- Add Torvalds Test prominently

### 4. docs-sync.md (174 lines → Target: 60 lines)
**Major Issues**:
- Too many examples of documentation patterns
- Verbose explanations of sync strategies
- Repetitive section structures

**Reduction Strategy**:
- Single template for all doc types
- Remove sync strategy explanations (just do it)
- Condense to: Find docs → Check accuracy → Update → Verify

### 5. setup-mcp.md (169 lines → Target: 60 lines)
**Major Issues**:
- Overly detailed MCP server explanations
- Redundant configuration examples
- Verbose troubleshooting guide

**Reduction Strategy**:
- Link to official docs instead of explaining MCP
- Single configuration template
- Move troubleshooting to separate doc or remove

## Commands That Are Good As-Is
- gates.md (103 lines): Perfect balance of detail and brevity
- execute.md (57 lines): Concise and effective
- carmack.md (56 lines): Pure philosophy, no fluff

## Quick Wins (Already Good, Minor Tweaks)
- tighten.md (134 lines → 100): Slight example reduction
- debug.md (122 lines → 80): Remove redundant agent references
- git-code-review.md (126 lines → 80): Condense review categories

## Deletion Candidates
- shatter.md (1 line): Empty/broken command
- git-simple-push.md (1 line): Duplicate of git-push.md
- ticket.md (4 lines): Unclear purpose
- verify.md (5 lines): Too minimal to be useful

## Persona Energy Opportunities
Commands that would benefit from persona invocations:
- plan.md: "What would Torvalds put in a TODO?"
- spec.md: "Channel Dijkstra's precision"
- debug.md: "Think like Kernighan debugging"
- gates.md: Already has it! (Carmack, Kent Beck, Torvalds, Knuth)

## Implementation Priority
1. **URGENT**: Fix backlog-groom.md (references deleted agents)
2. **HIGH**: Reduce spec.md, plan.md, docs-sync.md
3. **MEDIUM**: Trim setup-mcp.md, debug.md, git-code-review.md
4. **LOW**: Minor tweaks to remaining verbose commands

## Success Metrics
- Remove all references to deleted agents
- Average command length: <100 lines ✓
- No command over 150 lines (currently 5 violate this)
- Every command has clear persona energy where appropriate
- Preserve all critical error-prevention details