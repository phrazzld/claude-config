Generate a comprehensive code review using a two-phase approach: thinktank multi-model analysis followed by independent Claude review, then synthesis of all findings into superior collective intelligence.

## WORKFLOW

**1. Context Preparation**
- **Leyline Pre-Processing**: Query relevant leyline documents for review standards:
  - Tenets for code quality, security, and maintainability principles
  - Bindings for review methodology and synthesis approaches
  - Internalize standards that guide comprehensive review process
- Get current branch name and identify all changed files
- Determine appropriate base branch (master/main)
- Count changed files for context

**2. Phase 1: Thinktank Multi-Model Analysis**
- Create `REVIEW-CONTEXT.md` with comprehensive context:
  ```markdown
  # Code Review Context

  ## PR Details
  Branch: [current branch name]
  Base Branch: [master/main]
  Files Changed: [count of changed files]

  ## Changed Files List
  [List all changed files with brief descriptions]

  ## Full Diff
  [Complete output of git diff base_branch]
  ```
- **Run Dual Thinktank Analysis**:
  - **Diff-focused review** (bugs and functional issues):
    ```bash
    thinktank-wrapper --template review-diff --inject REVIEW-CONTEXT.md --model-set high_context --include-leyline [changed files]
    ```
  - **Philosophy-alignment review** (standards and patterns):
    ```bash
    thinktank-wrapper --template review --inject REVIEW-CONTEXT.md --model-set high_context --include-leyline ./
    ```
- Locate and preserve thinktank synthesis outputs as `THINKTANK_DIFF_REVIEW.md` and `THINKTANK_PHILOSOPHY_REVIEW.md`

**3. Phase 2: Independent Review**
- **CRITICAL**: Perform analysis WITHOUT reading thinktank outputs first
- **Think very hard** about code changes with focus on areas thinktank might miss:
  - Integration points and cross-cutting concerns
  - Subtle logic errors and edge cases
  - User experience and API design implications
  - Testing strategy adequacy and test quality
  - Documentation clarity and completeness
  - Performance implications in real-world scenarios
  - Security considerations beyond obvious vulnerabilities
- **Independent Analysis Methodology**:
  - Read diff line-by-line with fresh perspective
  - Check adherence to leyline document principles
  - Evaluate consistency with codebase patterns
  - Identify potential bugs, race conditions, error handling gaps
  - Consider architectural implications and design trade-offs
  - Assess maintainability and future modification ease
- Create `CLAUDE_INDEPENDENT_REVIEW.md` with structured findings:
  - Executive summary of key concerns
  - Critical issues (blocker/high/medium/low severity)
  - Unique insights not covered by standard automated analysis
  - Recommendations for improvement with specific action items
  - Positive aspects and good practices observed

**4. Phase 3: Superior Synthesis**
- **Read all review outputs completely**:
  - `THINKTANK_DIFF_REVIEW.md` - functional issues and bugs
  - `THINKTANK_PHILOSOPHY_REVIEW.md` - standards and patterns
  - `CLAUDE_INDEPENDENT_REVIEW.md` - independent analysis
- **Apply synthesis methodology**:
  - Identify unique insights each source contributed
  - Map areas where sources agree vs. disagree
  - Resolve contradictions through reasoned analysis
  - Eliminate redundancy while preserving all valuable findings
  - Integrate different organizational approaches into coherent structure
- **Think very hard** about creating synthesis that is demonstrably superior:
  - Preserve strongest, most actionable insights from all sources
  - Create clearer categorization and prioritization
  - Resolve conflicting recommendations with reasoned decisions
  - Add connecting insights that emerge from combining multiple perspectives
  - Ensure final review is more comprehensive and actionable than any individual source
- Create final `CODE_REVIEW.md` that represents collective intelligence:
  - Comprehensive summary of all changes and their implications
  - Unified issue taxonomy with clear severity and action priorities
  - Synthesized recommendations that combine multiple AI perspectives
  - Clear action plan for addressing findings
  - Recognition of positive aspects and architectural decisions

**5. Cleanup**
- Remove temporary files: `REVIEW-CONTEXT.md`, individual thinktank outputs, Claude independent review
- Preserve only the final synthesized `CODE_REVIEW.md`

## Key Principles
- Maintain true independence between thinktank and Claude analysis phases
- Synthesis must be demonstrably superior to any individual review
- Focus on actionable findings with clear severity and priority
- Balance comprehensive coverage with practical recommendations
- Leverage collective AI intelligence while avoiding redundancy
