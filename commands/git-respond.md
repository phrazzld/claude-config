# RESPOND

Systematically analyze all PR review feedback and comments, categorize them by priority and scope, and create actionable responses for immediate and future work.

## 1. Review Analysis
- **Goal:** Comprehensively evaluate all PR comments and feedback.
- **Actions:**
    - Read through all comments, suggestions, and review feedback on the open pull request.
    - Think critically about each comment's legitimacy, scope, and impact.
    - Assess technical merit, alignment with project goals, and implementation complexity.
    - Consider reviewer expertise and context behind each suggestion.

## 2. Categorize Feedback
- **Goal:** Classify comments into actionable categories based on urgency and scope.
- **Categories:**
    - **Critical/Merge-blocking:** Issues that must be addressed before merge
    - **In-scope improvements:** Enhancements that fit this branch's purpose
    - **Follow-up work:** Valid suggestions for future iterations
    - **Low priority/Not applicable:** Comments that don't warrant immediate action

## 3. Create Action Plans
- **For immediate work (Critical + In-scope):**
    - Create discrete, well-defined, narrowly-scoped tasks in @TODO.md
    - Each task should be highly detailed, context-rich, atomic, and actionable
    - Include specific file paths, line numbers, and implementation details
    - Prioritize by merge-blocking status and implementation effort

- **For follow-up work:**
    - Incorporate valid suggestions into @BACKLOG.md with proper context
    - Include rationale for deferring and estimated effort/complexity
    - Link back to original PR comments for reference

- **For low priority/rejected feedback:**
    - Document reasoning for not addressing immediately
    - Consider: erroneous suggestions, out-of-scope changes, low ROI improvements
    - Provide clear justification to inform future discussions

## 4. Document Decisions
- **Goal:** Create transparent record of feedback handling decisions.
- **Actions:**
    - Summarize analysis approach and decision criteria
    - For each comment category, explain rationale and next steps
    - Ensure all feedback is acknowledged and appropriately addressed