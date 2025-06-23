# Setup Review Command - Generate Multi-Agent Code Review Command

Generate a project-specific `/project:review` command that creates comprehensive code reviews using parallel expert analysis.

**Usage**: `/user:setup-review-command`

## Implementation Instructions

Create a project-specific "review" command that leverages multiple expert programming personas through Task tool subagents to generate comprehensive code reviews.

### Command Generation Process

1. **Analyze Project Context**
   - Read the current project structure and technology stack
   - Check package.json, go.mod, Cargo.toml, requirements.txt, etc.
   - Identify primary languages and frameworks
   - Detect architectural patterns and conventions

2. **Select Expert Reviewers**
   Based on detected technologies, select 4-5 experts including:
   - **John Carmack** (always included): Performance, algorithms, first principles
   - **Language-Specific Experts**:
     - JavaScript/React: Dan Abramov, Kent C. Dodds, Sarah Drasner
     - Go: Rob Pike, Russ Cox, Mat Ryer
     - Python: Guido van Rossum, Raymond Hettinger, David Beazley
     - Rust: Graydon Hoare, Steve Klabnik, Carol Nichols
     - Ruby: DHH, Matz, Aaron Patterson
     - Java: Brian Goetz, Joshua Bloch, Venkat Subramaniam
   - **Domain Experts**:
     - Security: Troy Hunt, Bruce Schneier, OWASP perspectives
     - Architecture: Martin Fowler, Uncle Bob, Eric Evans
     - Testing: Kent Beck, Michael Feathers, Lisa Crispin
     - DevOps: Kelsey Hightower, Jessie Frazelle, Mitchell Hashimoto

   ### Phase 1: Parallel Expert Review
   Launch subagents using the Task tool for independent analysis. Make sure each one only conducts research and investigations and brainstorms, and outputs all responses directly to chat -- they should not make code changes and they should not use plan mode:

   **Task 1: John Carmack - Performance & Algorithms**
   - Prompt: "As John Carmack, review the code diff in REVIEW-CONTEXT.md focusing on algorithmic efficiency, performance optimization, and first principles engineering. Consider computational complexity, memory usage, and mathematical elegance. What could be more elegant or performant?"

   [Project-specific expert tasks based on detected stack]

   ### Phase 2: Superior Synthesis
   1. Read all expert subagent reviews

   2. Create final `CODE_REVIEW.md`:
      ```markdown
      # Code Review: [Branch Name]

      ## Executive Summary
      [High-level overview combining all perspectives]

      ## Critical Issues
      ### 🚨 Blockers
      [Issues that must be fixed before merge]

      ### ⚠️ High Priority
      [Important issues that should be addressed]

      ### 📝 Medium Priority
      [Improvements worth considering]

      ## Architectural Impacts
      [Long-term implications from multiple expert perspectives]

      ## Performance Considerations
      [Synthesis of performance-related findings]

      ## Security Analysis
      [Combined security insights]

      ## Positive Aspects
      [Good practices and improvements noted]

      ## Recommendations
      [Prioritized action items with clear next steps]
      ```

   ## Success Criteria
   - All expert perspectives represented
   - Synthesis demonstrates collective intelligence
   - Actionable recommendations with clear priorities
   - No redundant or conflicting advice

   Execute this comprehensive review process now.

4. **Project-Specific Customization**
   - Adapt expert selection to detected technologies
   - Include relevant linting/testing commands if found
   - Reference project-specific standards or conventions

5. **Create and Confirm**
   - Write the customized command to `.claude/commands/review.md`
   - Verify proper formatting and command availability
   - Confirm command is accessible as `/project:review`

Execute the review command generation now, creating a project-tailored multi-agent code review tool.
