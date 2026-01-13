---
description: Consult thinktank expert council for multi-model perspectives
argument-hint: "<query>" [path...]
---

# COUNCIL

> Many minds. One synthesis. Better decisions.

Delegate analysis to thinktank's expert council for multi-model perspectives.

## Usage

```
/council "Review this auth implementation for security issues" ./src/auth
/council "Evaluate this architecture for scalability" ./src
/council "What are the tradeoffs of this approach?"
```

## Process

### 1. Frame the Question

Convert the query into focused instructions:
- Clear question/task
- Specific focus areas
- Expected output format

### 2. Scope the Context

Determine target files:
- Use paths from args if provided
- Otherwise use current working context
- Keep scope focused (fewer files = better synthesis)

### 3. Create Instructions File

Write temp instructions (e.g., `/tmp/council-instructions.md`):

```markdown
# Expert Review Request

## Question
{{query}}

## Focus Areas
- [Specific aspects to evaluate]
- [Potential concerns to address]

## Requested Output
For each perspective, provide:
1. Key observations
2. Concerns or risks
3. Recommendations
4. Confidence level (high/medium/low)

Conclude with synthesized recommendations highlighting consensus and divergent views.
```

### 4. Run Thinktank

```bash
thinktank /tmp/council-instructions.md {{paths}} --synthesis
```

**Model group selection:**
- Default: `workhorses` for reasoning-heavy tasks
- `--model cheap` for quick validation
- Large codebases: consider `a-milli` group

### 5. Synthesize Results

Read thinktank output and distill:

**Consensus Points** (all models agree):
- [Finding that multiple models identified]

**Divergent Views** (models disagree - needs attention):
- [Area where models had different opinions]

**Actionable Recommendations**:
1. [Prioritized action item]
2. [Secondary action]

## When to Use

- **Code Review**: Get diverse perspectives on implementation quality
- **Architecture Decisions**: Validate design before committing
- **Security Audit**: Comprehensive vulnerability assessment
- **Performance Analysis**: Multiple optimization perspectives
- **Design Patterns**: Evaluate pattern choices
- **Technical Decisions**: When there's no obvious right answer

## Output

Report synthesized council findings:
- Consensus points (high confidence)
- Divergent views (investigate further)
- Prioritized recommendations
- Next steps

## Example

```
/council "Is this error handling approach robust?" ./src/api/handlers.ts

→ Creates instructions focusing on error handling patterns
→ Runs thinktank with synthesis mode
→ Reports:
  - Consensus: Missing retry logic for transient failures
  - Divergent: Some models suggest circuit breaker, others prefer backoff
  - Recommendation: Add exponential backoff, consider circuit breaker for external APIs
```
