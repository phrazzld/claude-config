---
description: Multi-model expert review with synthesis
argument-hint: "<query>" [file...]
---

# THINKTANK

Invoke thinktank CLI for multi-model perspectives on any question.

## Arguments

- `query` — The question or review request (required)
- `file...` — Optional file paths to include as context

## What This Does

1. **Frame question** — Write clear instructions to temp file
2. **Gather context** — Include specified files or branch diff
3. **Run thinktank** — Multiple models analyze in parallel
4. **Synthesize** — Report consensus vs. divergent views

## Execution

```bash
# Write instructions
cat > /tmp/thinktank-query.md << 'EOF'
# Review Request

## Question
$ARGUMENTS

## Requested Output
1. Key observations
2. Concerns or risks
3. Recommendations
4. Confidence level (high/medium/low)

Conclude with synthesis: consensus points and divergent views.
EOF

# Run thinktank with synthesis
thinktank /tmp/thinktank-query.md $FILES --synthesis
```

## Usage Examples

```
/thinktank "Is this auth implementation secure?" ./src/auth
/thinktank "What are the tradeoffs of this architecture?"
/thinktank "Review this PR for issues" $(git diff main --name-only)
```

## Output

Report:
- **Consensus** — What all models agree on
- **Divergent** — Where models disagree (investigate further)
- **Recommendations** — Prioritized actions
