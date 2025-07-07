Debug complex issues using adaptive parallel expert analysis that dynamically responds to issue characteristics.

# DEBUG

Conduct comprehensive root cause analysis of the issue in @ISSUE.md using parallel domain experts who assess relevance and provide targeted or elimination-based insights.

## 1. Initial Issue Analysis

**Read and classify the issue**:
- Read @ISSUE.md thoroughly
- Extract symptoms, error messages, logs, stack traces
- Identify affected systems and reproduction steps
- Note keywords that suggest issue domain
- Generate initial "issue fingerprint"

## 2. Adaptive Expert Analysis

Launch 8 parallel domain experts using the Task tool. Each expert assesses relevance and provides analysis accordingly:

```
Task 1: "Performance Expert - Assess if the issue in @ISSUE.md relates to performance (0-100% confidence). 
HIGH confidence (>70%): Investigate bottlenecks, resource usage, slow queries, algorithm complexity, memory leaks, CPU spikes, I/O blocking, caching issues.
LOW confidence (<30%): Explain what performance indicators are MISSING and why this appears to be a different type of issue.
MEDIUM confidence (30-70%): Check key performance indicators and note ambiguous signals.
Keywords: slow, timeout, lag, memory, CPU, bottleneck, performance.
DO NOT modify code - output confidence score and analysis."

Task 2: "Logic Expert - Assess if the issue in @ISSUE.md relates to code logic/business rules (0-100% confidence).
HIGH confidence: Trace execution paths, identify incorrect conditionals, off-by-one errors, edge cases, null handling, state management bugs.
LOW confidence: Explain why logic appears sound and what other domain might be affected.
MEDIUM confidence: Investigate suspicious logic patterns while noting uncertainty.
Keywords: incorrect, wrong result, unexpected behavior, should be, supposed to.
DO NOT modify code - output confidence score and analysis."

Task 3: "Integration Expert - Assess if the issue in @ISSUE.md relates to system integration (0-100% confidence).
HIGH confidence: Investigate API failures, service communication, dependency conflicts, protocol mismatches, network issues, timeouts.
LOW confidence: Explain why integration layers appear healthy and suggest other domains.
MEDIUM confidence: Check integration points while noting ambiguity.
Keywords: API, service, connection, integration, dependency, communication.
DO NOT modify code - output confidence score and analysis."

Task 4: "Flakiness Expert - Assess if the issue in @ISSUE.md is intermittent/non-deterministic (0-100% confidence).
HIGH confidence: Investigate race conditions, timing dependencies, concurrency bugs, test flakiness, environmental variance, random failures.
LOW confidence: Explain why issue appears deterministic and consistent.
MEDIUM confidence: Look for subtle non-determinism patterns.
Keywords: sometimes, occasionally, flaky, intermittent, randomly, sporadic.
DO NOT modify code - output confidence score and analysis."

Task 5: "Security Expert - Assess if the issue in @ISSUE.md relates to security (0-100% confidence).
HIGH confidence: Investigate auth failures, vulnerabilities, data exposure, injection risks, privilege escalation, security misconfigurations.
LOW confidence: Explain why security appears intact and issue lies elsewhere.
MEDIUM confidence: Check security boundaries while noting uncertainty.
Keywords: unauthorized, forbidden, security, authentication, permission, access.
DO NOT modify code - output confidence score and analysis."

Task 6: "Data Expert - Assess if the issue in @ISSUE.md relates to data integrity/validation (0-100% confidence).
HIGH confidence: Investigate data corruption, validation failures, schema mismatches, encoding issues, data loss, integrity constraints.
LOW confidence: Explain why data layer appears healthy.
MEDIUM confidence: Check data flows and transformations.
Keywords: corrupt, invalid, data, validation, integrity, missing data.
DO NOT modify code - output confidence score and analysis."

Task 7: "Configuration Expert - Assess if the issue in @ISSUE.md relates to configuration/environment (0-100% confidence).
HIGH confidence: Investigate env variables, config files, deployment settings, version mismatches, missing dependencies, environment differences.
LOW confidence: Explain why configuration appears correct.
MEDIUM confidence: Check key configuration points.
Keywords: environment, config, deployment, setting, production, staging.
DO NOT modify code - output confidence score and analysis."

Task 8: "UX Expert - Assess if the issue in @ISSUE.md relates to user experience/interface (0-100% confidence).
HIGH confidence: Investigate UI bugs, accessibility issues, user workflow problems, confusing interactions, responsive design issues.
LOW confidence: Explain why this appears to be a backend/system issue.
MEDIUM confidence: Consider UX implications of technical issues.
Keywords: user, UI, interface, display, interaction, accessibility, workflow.
DO NOT modify code - output confidence score and analysis."
```

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
| Performance | 15% | NOT MY DOMAIN | No performance indicators; issue is binary failure |
| Logic | 85% | PRIMARY DOMAIN | Off-by-one error in array boundary check |
| Integration | 20% | NOT MY DOMAIN | All API calls succeeding; issue is internal |
| Flakiness | 10% | NOT MY DOMAIN | 100% reproducible with same input |
| Security | 25% | UNLIKELY | No auth involved in affected code path |
| Data | 40% | POSSIBLE FACTOR | Data validation might be too permissive |
| Configuration | 15% | NOT MY DOMAIN | Same config works in other environments |
| UX | 30% | SECONDARY IMPACT | Error not surfaced clearly to user |

### Synthesis

**Primary Finding**: Logic error with 85% confidence
- Off-by-one error in array indexing at module.js:45
- Elimination of performance/flakiness/integration confirms deterministic logic bug
- Data expert's finding suggests validation gap allowed bad input to reach buggy code

**Process of Elimination Value**:
- Performance ruled out → Not a scaling/resource issue
- Flakiness ruled out → Consistent reproduction path exists
- Integration ruled out → Problem is internal, not external

### Root Cause
Array index calculation fails when input length equals buffer size due to incorrect boundary condition.

### Recommended Actions

#### Immediate Fix
- [ ] Fix off-by-one error in array boundary check
- [ ] Add input validation to prevent edge case

#### Validation  
- [ ] Add unit test for boundary condition
- [ ] Test with inputs at size limits

#### Prevention
- [ ] Add stricter data validation layer
- [ ] Improve error messaging for users
```

## Success Criteria

- All 8 experts provide confidence assessment
- Both positive and negative findings are synthesized
- Evidence matrix clearly shows convergence/divergence
- Root cause has supporting evidence from multiple angles
- Elimination reasoning strengthens positive findings