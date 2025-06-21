# GORDIAN

## GOAL
Identify opportunities for radical simplification and creative destruction in the codebase through outside-the-box thinking, and create GitHub issues for the most promising opportunities.

## 1. Prepare Context
- Fetch current GitHub issues to understand existing tasks:
  ```bash
  gh issue list --state open --json number,title,body,labels --limit 100
  ```
- Create `GORDIAN-CONTEXT.md` with the following content:
  ```markdown
  # Radical Simplification Context

  ## Current Issues
  [Include output from GitHub issues list]

  ## Request
  Identify components in the codebase that could benefit from radical simplification or creative destruction.
  ```

## 2. Generate Gordian Opportunities
- **Leyline Pre-Processing**: Focus on simplification-oriented principles:
  - Query tenets emphasizing simplicity, orthogonality, and eliminating complexity
  - Identify bindings that enforce minimalism and clean architecture
  - Internalize radical simplification patterns from the leyline knowledge base
- ***Think very hard*** about radical simplification opportunities by:
  - **Existence justification**: Challenge why each component/abstraction exists - could it be eliminated entirely?
  - **Radical simplification**: Identify opportunities to replace complex systems with dramatically simpler solutions
  - **Architectural transformation**: Consider paradigm shifts that could eliminate entire categories of complexity
  - **Quality automation**: Find ways to automate quality/testing that remove manual overhead
  - **Assumption challenging**: Question fundamental assumptions about requirements, constraints, and architecture
- Apply transformative thinking to "cut the Gordian knot" - seek solutions that make problems disappear rather than solving them incrementally
- Focus on eliminating unnecessary complexity at its root, not just managing it
- Balance boldness with practicality - solutions should be revolutionary but achievable

## 3. Create GitHub Issues
- For each radical simplification opportunity, create a GitHub issue with appropriate details and labels

## DESCRIPTION
Inspired by Elon Musk's observation that "the number one mistake great engineers make is optimizing something that shouldn't exist" and the legend of Alexander cutting the Gordian Knot instead of untangling it. This command identifies components that:

1. Should be eliminated rather than optimized
2. Could be radically simplified with unconventional approaches
3. Are unnecessarily complex, tightly coupled, or difficult to maintain
4. Present opportunities to "cut the knot" rather than wrestling with its complexity

The output will provide specific, actionable recommendations for simplification and creative destruction.
