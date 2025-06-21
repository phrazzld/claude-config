# WHITEBOARD

## GOAL
Generate creative technical brainstorming for a GitHub issue, exploring multiple approaches from conventional to innovative "cut the Gordian knot" solutions.

## 1. Select Issue
- List GitHub issues to select one for brainstorming:
  ```bash
  gh issue list --state open --json number,title,labels --limit 20
  ```
- View details of the selected issue:
  ```bash
  gh issue view [issue-number] --json number,title,body,labels
  ```

## 2. Create Context
- Create `WHITEBOARD-CONTEXT.md` containing the selected GitHub issue details

## 3. Generate Ideas
- **Leyline Pre-Processing**: Gather creative problem-solving context:
  - Query tenets that encourage innovation and alternative approaches
  - Identify bindings that provide architectural flexibility patterns
  - Internalize principles for evaluating solution trade-offs and complexity
- ***Think very hard*** about creative technical brainstorming by exploring the full solution spectrum:
  - **Deep problem analysis**: Clarify the core problem beyond literal description, identify essential vs accidental complexity, challenge unstated assumptions
  - **Solution spectrum exploration**: Generate comprehensive range of solutions including:
    - Conventional approaches with standard patterns
    - Incremental improvements to existing patterns
    - Alternative paradigms or architectural styles
    - Innovative simplifications that "cut the Gordian knot"
    - Blue sky ideas with breakthrough potential
  - **For each approach**, provide concept summary, implementation outline, key decisions, unique advantages, and honest drawbacks
  - **Comparative analysis**: Create complexity vs value matrix, analyze tradeoffs across development effort, performance, maintainability, testing, security
  - **Opinionated recommendation**: Select approach that best balances requirements, philosophy alignment, minimal complexity, extensibility, and maximum value
- Focus on intellectual curiosity and creative exploration of technical potential
- Ensure ideas range from safe/conventional to innovative/risky options

## 4. Update Issue
- Consider commenting on the GitHub issue with the brainstorming results:
  ```bash
  gh issue comment [issue-number] --body "[Summary of brainstorming results]"
  ```