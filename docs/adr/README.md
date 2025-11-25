# Architecture Decision Records

This directory contains Architecture Decision Records (ADRs) for the project.

## What is an ADR?

An Architecture Decision Record captures an important architectural decision made along with its context and consequences. ADRs help us:

- Document why decisions were made
- Learn from past decisions
- Onboard new team members
- Track the evolution of our architecture
- Review decisions against actual outcomes

## How to Create an ADR

1. Copy `template.md` to a new file named `ADR-XXX-brief-description.md`
   - XXX is the next sequential number (001, 002, etc.)
   - Use lowercase with hyphens for the description

2. Fill out all sections of the template

3. Set initial status to "Proposed"

4. After team review and acceptance, update status to "Accepted"

## Automated ADR Creation (Bash Function)

For faster ADR creation, add this function to your `~/.zshrc` or `~/.bashrc`:

```bash
# ADR Helper - Auto-numbers and templates new ADRs
adr() {
  local title="$1"
  local adr_dir="${2:-docs/adr}"

  if [ -z "$title" ]; then
    echo "Usage: adr \"Brief decision title\" [adr_directory]"
    echo "Example: adr \"Use PostgreSQL for primary database\""
    return 1
  fi

  # Create ADR directory if it doesn't exist
  mkdir -p "$adr_dir"

  # Find next ADR number
  local last_num=$(ls "$adr_dir"/ADR-*.md 2>/dev/null | \
    sed 's/.*ADR-0*\([0-9]*\)-.*/\1/' | \
    sort -n | \
    tail -1)
  local next_num=$((last_num + 1))

  # Format number with leading zeros
  local num_padded=$(printf "%03d" $next_num)

  # Convert title to filename-friendly format
  local slug=$(echo "$title" | \
    tr '[:upper:]' '[:lower:]' | \
    sed 's/[^a-z0-9]/-/g' | \
    sed 's/--*/-/g' | \
    sed 's/^-//;s/-$//')

  local filename="$adr_dir/ADR-$num_padded-$slug.md"
  local date=$(date +%Y-%m-%d)

  # Create ADR from template
  cat > "$filename" << EOF
# ADR-$num_padded: $title

Date: $date
Status: proposed

## Context and Problem Statement

[What problem requires this decision? What are the current constraints?]

## Considered Options

* **Option 1**: [Name and brief description]
  - Pros: [Benefits]
  - Cons: [Downsides]

* **Option 2**: [Name and brief description]
  - Pros: [Benefits]
  - Cons: [Downsides]

* **Option 3**: [Name and brief description]
  - Pros: [Benefits]
  - Cons: [Downsides]

## Decision Outcome

**Chosen**: [Selected option]

**Rationale**: [Why this option? Consider: simplicity, user value, explicitness, maintainability]

### Consequences

**Good**:
- [Positive outcome 1]
- [Positive outcome 2]

**Bad**:
- [Cost or downside 1]
- [Trade-off 2]

**Neutral**:
- [Neutral consequence that requires attention]

## Implementation Notes

[Technical details, migration strategy, rollout plan]

## Follow-up Actions

- [ ] [Action item 1]
- [ ] [Action item 2]

## References

- [Related documentation]
- [External resources]
- [Related ADRs]
EOF

  echo "Created: $filename"

  # Open in editor (uses EDITOR env var, defaults to vim)
  ${EDITOR:-vim} "$filename"
}
```

**Usage**:
```bash
# Create new ADR (auto-numbers and opens in editor)
adr "Use PostgreSQL for primary database"

# Specify custom ADR directory
adr "Adopt React Query for data fetching" "documentation/decisions"
```

**Features**:
- Auto-numbers ADRs sequentially (ADR-001, ADR-002, etc.)
- Converts title to URL-friendly slug
- Uses MADR Light template format
- Opens in your default editor immediately
- Creates ADR directory if missing

After editing, commit the ADR with your changes:
```bash
git add docs/adr/ADR-003-*.md
git commit -m "docs: add ADR-003 for database choice"
```

## ADR Lifecycle

1. **Proposed**: Decision is under consideration
2. **Accepted**: Decision has been agreed upon and will be/is implemented
3. **Deprecated**: Decision is no longer recommended but may still be in use
4. **Superseded**: Decision has been replaced by another ADR (reference the new one)

## Integration with Workflow

- ADRs are proposed during `/spec` command by the `adr-architect` subagent
- ADRs are reviewed during `/address` command after implementation
- The `adr-architect` maintains memory of outcomes in `agents/memory/adr-outcomes.md`

## Current ADRs

| Number | Title | Status | Date |
|--------|-------|--------|------|
| (None yet) | | | |

## Review Schedule

ADRs should be reviewed:
- After implementation is complete
- When considering similar decisions
- During major refactoring
- Quarterly for active ADRs