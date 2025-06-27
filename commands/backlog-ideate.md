# BACKLOG-IDEATE

## GOAL
Generate innovative, project-specific ideas and add them to local BACKLOG.md by analyzing current project context, architecture, and opportunities for enhancement.

## 1. Project Context Analysis
- Read local BACKLOG.md to understand current tasks, direction, and avoid duplication
- Read project-specific leyline documents in `./docs/leyline/` if they exist
- Analyze current project structure, technologies, and architectural patterns
- Identify current project's domain, purpose, and user base
- Review existing features and functionality gaps

## 2. Create Context File
- Create `IDEATE-CONTEXT.md` with information about current project and ideation goals:
  ```markdown
  # Ideation Context

  ## Current Project State
  [Brief description of current project's purpose, architecture, and key technologies]

  ## Current BACKLOG.md Status
  [Include key items from existing backlog to understand direction and avoid duplication]

  ## Project Strengths & Opportunities
  [Identify what's working well and areas with enhancement potential]

  ## Ideation Focus Areas
  [Specify areas where new ideas would be most valuable for THIS project:
  - New features that align with project purpose
  - Developer experience improvements for current tech stack
  - Performance optimizations for current architecture
  - User experience enhancements for current functionality]
  ```

## 3. Generate Ideas Through Deep Analysis
- **Leyline Pre-Processing**: Read leyline documents to anchor ideation:
  - Query tenets related to innovation, user value, and sustainable development
  - Identify bindings that guide feature development and architectural evolution
  - Internalize principles that balance innovation with simplicity and maintainability
- **Think very hard** about innovative ideas that would benefit THIS SPECIFIC PROJECT:
  - **Gap analysis**: Consider missing functionality that would enhance current project value
  - **Developer experience**: Identify opportunities to improve development workflow for current tech stack
  - **Performance opportunities**: Brainstorm optimizations specific to current architecture and usage patterns
  - **User experience**: Think about features that would delight users within current project scope
  - **Automation possibilities**: Identify manual processes in current project that could be automated
  - **Integration opportunities**: Consider how current project could integrate with other tools/systems
  - **Architectural enhancements**: Think about evolutionary improvements to current project structure
  - **Domain-specific innovations**: Generate ideas specific to current project's problem domain
  - **Technology leverage**: Consider how to better leverage current tech stack capabilities
  - **Simplification through addition**: Ideas that add value while reducing overall complexity

## 4. Prioritize and Categorize Ideas
- **Innovation vs. Effort matrix**: Evaluate each idea based on:
  - Impact potential for current project and its users
  - Implementation complexity within current architecture
  - Alignment with project philosophy and leyline principles
  - Dependencies on existing work or external factors
  - Resource requirements and technical feasibility
- **Categorize ideas** by type and priority:
  - Quick wins (high impact, low effort) for current project
  - Strategic improvements (high impact, higher effort)
  - Experimental features (uncertain impact, worth exploring)
  - Infrastructure enhancements (foundational improvements)

## 5. Add Ideas to BACKLOG.md
- **Format**: Add ideas using standard BACKLOG.md format:
  ```
  - [ ] [PRIORITY] [FEATURE/ENHANCE] Specific innovation description
  ```
- **Organization**: 
  - Add high-impact, achievable ideas to appropriate priority sections
  - Add experimental or longer-term ideas to "Ideas & Future Considerations" section
- **Specificity**: Each idea should be:
  - Tailored to current project context and constraints
  - Include clear value proposition for current users/developers
  - Reference current architecture or components where relevant
  - Specify expected benefits and success criteria

## 6. Document Ideation Process
- Update `IDEATE-CONTEXT.md` with ideation results and rationale
- Include:
  * Summary of idea categories and priorities
  * Rationale for high-priority selections
  * Notes about project-specific constraints or opportunities
  * Future ideation directions based on current analysis

