Brainstorm design, architecture, UI/UX, and implementation approaches for the task described in @TASK.md using parallel expert analysis.

# PLAN

Read the task from @TASK.md and conduct comprehensive brainstorming across design patterns, architecture, UI/UX, technology choices, and implementation strategies using parallel research and expert analysis.

## 1. Context Gathering & Initial Research
- **Read @TASK.md** to understand the task requirements and constraints
- **Check ./docs/leyline/** for project-specific development philosophies if available
- **Launch parallel research agents** for comprehensive context:
  ```
  Task 1: "Use gemini --prompt to research current best practices and patterns for [task type] in 2025"
  Task 2: "Use Context7 MCP to find documentation for potentially relevant libraries/frameworks/services"
  Task 3: "Analyze existing codebase to understand current patterns, tech stack, and architectural decisions"
  Task 4: "Use gemini to research common pitfalls, performance considerations, and security implications for [task domain]"
  ```

## 2. Multi-Perspective Brainstorming (Parallel Execution)
- **Launch parallel expert analysis** covering all aspects:
  ```
  Task 1: "Architecture Expert: Evaluate patterns (monolith/microservices, event-driven, CQRS, etc.) and system design approaches"
  Task 2: "UI/UX Expert: Design user flows, interaction patterns, accessibility, and delightful experiences"
  Task 3: "Technology Evaluator: Compare frameworks, libraries, services (self-hosted vs SaaS), and toolchains"
  Task 4: "Performance Engineer: Consider caching strategies, database design, API optimization, and scalability"
  Task 5: "Security Architect: Analyze authentication, authorization, data protection, and compliance needs"
  Task 6: "Pragmatic Developer: Identify quickest path to MVP, existing code to leverage, and iterative approach"
  ```

## 3. Technology & Service Evaluation
- **Evaluate technology options** with pros/cons:
  - Frontend frameworks/libraries if UI involved
  - Backend frameworks and architectural patterns
  - Database choices (SQL/NoSQL, specific engines)
  - External services (payment, auth, analytics, etc.)
  - Infrastructure considerations (containerization, serverless, etc.)
- **Consider build vs buy** for each component
- **Assess integration complexity** with existing stack

## 4. Generate Comprehensive Brainstorm & Append to @TASK.md
- **Synthesize all findings** into coherent recommendations
- **Structure tradeoff analysis** for major decisions
- **Append to @TASK.md** with this format:
  ```markdown

  ---

  # Brainstorming & Analysis

  ## Research Findings

  ### Best Practices Research
  - [Key finding 1 from web research]
  - [Key finding 2 about current industry patterns]
  - [Relevant documentation/examples found]

  ### Codebase Analysis
  - Existing patterns we can leverage: [pattern at file:line]
  - Current tech stack constraints: [findings]
  - Similar implementations: [references]

  ## Architecture & Design Options

  ### Option 1: [Architecture Name]
  **Approach**: [Description]
  **Pros**:
  - [Advantage 1]
  - [Advantage 2]
  **Cons**:
  - [Drawback 1]
  - [Drawback 2]
  **Implementation effort**: [Low/Medium/High]

  ### Option 2: [Alternative Architecture]
  [Similar structure...]

  ## UI/UX Considerations
  - User flow: [Description or diagram reference]
  - Key interactions: [List]
  - Accessibility requirements: [WCAG compliance needs]
  - Mobile considerations: [Responsive/PWA/Native]

  ## Technology Recommendations

  ### Frontend (if applicable)
  - Recommended: [Framework/Library] because [reasons]
  - Alternative: [Option 2] if [conditions]

  ### Backend
  - Pattern: [REST/GraphQL/gRPC/etc.]
  - Framework: [Recommendation based on stack]
  - Key libraries: [List with justification]

  ### Data Layer
  - Database: [Choice] for [reasons]
  - Caching: [Strategy if needed]
  - Search: [Approach if needed]

  ### External Services
  - [Service type]: [Recommendation] vs [Alternative]
  - Integration approach: [SDK/API/Webhook]

  ## Implementation Strategy

  ### Recommended Approach
  [Synthesized recommendation based on all analysis]

  ### MVP Path
  1. [First deliverable - simplest working version]
  2. [Enhancement 1]
  3. [Enhancement 2]

  ### Risk Mitigation
  - [Risk 1]: [Mitigation strategy]
  - [Risk 2]: [Mitigation strategy]

  ## Performance & Scalability Notes
  - Expected load: [Analysis]
  - Bottlenecks to watch: [List]
  - Optimization opportunities: [Defer these for later]

  ## Security Considerations
  - Authentication: [Approach]
  - Authorization: [Pattern]
  - Data protection: [Requirements]
  - Compliance: [Any specific needs]
  ```

## 5. Next Steps Documentation
- **Validate brainstorming** with task requirements
- **Highlight key decisions** that need stakeholder input
- **Set up for implementation** by identifying first concrete steps
- **Document assumptions** made during brainstorming for future reference

