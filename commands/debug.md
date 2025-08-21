Debug complex issues using parallel native subagents for comprehensive root cause analysis.

# DEBUG

Conduct comprehensive root cause analysis of the issue in ISSUE.md using native subagents who provide specialized analysis.

<!-- METRICS: Parallel subagent analysis takes 2-3 minutes
     Previous baseline: 5-10 minutes with sequential analysis
     Performance gain: 60% faster with parallel execution
     To track: Log subagent invocation times and bug memory hits -->

## 1. Initial Issue Analysis

**Read and classify the issue**:
- Read ISSUE.md thoroughly
- Extract symptoms, error messages, logs, stack traces
- Identify affected systems and reproduction steps
- Note keywords that suggest issue domain
- Generate initial "issue fingerprint"

## 2. Parallel Expert Analysis

Launch specialized debugging subagents in parallel. Each expert assesses relevance and provides targeted analysis:

**Invoke these subagents**:
1. `bug-historian` - Check if we've seen this pattern before (has memory)
2. `performance-detective` - Assess performance issues (bottlenecks, resources)
3. `logic-detective` - Analyze code logic and business rules
4. `integration-detective` - Investigate system integration problems

Additional analysis if needed:
- Flakiness patterns (race conditions, intermittent failures)
- Security concerns (auth, vulnerabilities, exposure)
- Data integrity (validation, corruption, constraints)
- Configuration issues (env vars, deployment settings)

**How to invoke subagents**:
Use the Task tool with subagent_type: "general-purpose" and prompt each to act as their respective subagent from /Users/phaedrus/.claude/agents/[agent-name].md

## 3. Evidence Synthesis

**Build evidence matrix from ALL experts**:
- Include both positive findings and elimination reasoning
- Value "not my domain" explanations as debugging evidence
- Look for convergence and divergence patterns
- Identify cross-domain issues

**Process of elimination**:
- Which domains were confidently ruled out?
- What does this tell us about the issue?
- How do elimination findings support positive findings?

## 4. Fallback Analysis

If all experts report low confidence (<30%), apply general debugging techniques:
- **Five Whys**: Iteratively ask "why" to drill to root cause
- **Ishikawa/Fishbone**: Map cause-and-effect relationships
- **Binary search**: Systematically narrow problem scope
- **Differential analysis**: Compare working vs broken states

## 5. Root Cause Determination

**Synthesize findings**:
- Primary hypothesis based on highest confidence expert(s)
- Supporting evidence from other domains
- Contradicting evidence and how to reconcile
- Confidence level in root cause determination

## 6. Solution Development

**Generate action plan based on evidence**:
```markdown
## Debug Analysis for [Issue Title]

### Expert Analysis Matrix

| Expert | Confidence | Assessment | Key Finding |
|--------|------------|------------|-------------|
| Bug Historian | X% | [Found/New] | [Previous solution or new pattern] |
| Performance | X% | [Domain fit] | [Key finding or elimination] |
| Logic | X% | [Domain fit] | [Key finding or elimination] |
| Integration | X% | [Domain fit] | [Key finding or elimination] |

### Synthesis

**Primary Finding**: [Highest confidence domain]
- [Root cause identified]
- [Supporting evidence]
- [How elimination of other domains confirms this]

**Process of Elimination Value**:
- [Domain] ruled out → [What this tells us]
- [Domain] ruled out → [What this tells us]

### Root Cause
[Clear statement of the root cause]

### Recommended Actions

#### Immediate Fix
- [ ] [Specific action to fix the issue]
- [ ] [Additional required changes]

#### Validation  
- [ ] [Tests to verify the fix]
- [ ] [Checks to ensure no regression]

#### Prevention
- [ ] [Changes to prevent recurrence]
- [ ] [Monitoring or alerts to add]
```

## 7. Post-Debug Learning

After resolving the issue, invoke lesson-harvester to capture debugging insights:

**How to invoke**: Use Task tool with subagent_type: "general-purpose" and prompt to act as lesson-harvester from /Users/phaedrus/.claude/agents/lesson-harvester.md, providing:
- The issue description and root cause
- Which expert analysis was most accurate
- Time to resolution vs severity
- Any new bug patterns discovered
- Debugging techniques that worked

The lesson-harvester will:
- Update bugs.md with new patterns if bug-historian missed them
- Score expert effectiveness for future debugging
- Extract reusable debugging strategies
- Note prevention opportunities

## Success Criteria

- Bug historian checks memory first for known patterns
- All relevant experts provide confidence assessment
- Both positive and negative findings are synthesized
- Evidence matrix clearly shows convergence/divergence
- Root cause has supporting evidence from multiple angles
- Elimination reasoning strengthens positive findings
- Bug historian updates memory with new patterns found
- Lesson-harvester captures debugging insights after resolution