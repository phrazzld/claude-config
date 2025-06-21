# SCOPE

## GOAL
Analyze and right-size `TODO.md`, breaking it into manageable pieces if needed to avoid unwieldy pull requests.

## FLOW

### 1. Gather Context
- Read PLAN.md
- Read TODO.md
- Find relevant leyline documents

### 2. Analyze Scope and Complexity
- **Think very hard** about the scope and complexity of TODO.md:
  - Analyze the total number of tasks and their complexity
  - Consider the interconnectedness of tasks
  - Evaluate if the changes would result in a reviewable PR
  - Think about logical groupings of related functionality
  - Consider the risk of introducing bugs with too many changes
  - Assess whether the scope aligns with single-responsibility principle
  - Identify natural breaking points if the scope is too large
- Create `SCOPE-RESULT.md` with your analysis including:
  - Assessment of current scope (appropriate/too large)
  - If too large, recommended split approach
  - Logical groupings for separate PRs
  - Dependencies between proposed splits

### 3. Execute Splitting (If Needed)
- If SCOPE-RESULT.md recommends splitting:
  - Create SCOPE-CONTEXT.md with the following content:
    ```markdown
    # Scope Splitting Context

    Based on the scope analysis, split TODO.md into multiple focused todo files.

    ## Source Plan
    [Include PLAN.md content]

    ## Source TODO
    [Include TODO.md content]

    ## Scope Analysis Results
    [Include SCOPE-RESULT.md content]

    ## Output Requirements
    1. Create separate plan files (TODO-1.md, TODO-2.md, etc.)
    2. Each todo file must be independently implementable
    ```
  - **Think very hard** about how to split the tasks effectively:
    - Group related tasks that should be implemented together
    - Ensure each split is independently testable and deployable
    - Maintain logical coherence within each split
    - Consider dependencies and order splits appropriately
    - Ensure no split is still too large for a manageable PR
    - Think about the review process and keeping changes focused
    - Create clear boundaries between splits
  - Generate the split TODO files based on your analysis
  - Write each plan to `TODO-{n}.md` files
  - Rename original to `TODO-ORIGINAL.md`
  - Create `TODO-INDEX.md` listing all generated plans

### 4. Review & Clean Up
- Present results to user
  - If not split: "TODO scope is appropriate - proceed with ticket command"
  - If split: "TODO split into N parts: [list file names]"
- Remove temporary files (SCOPE-CONTEXT.md)