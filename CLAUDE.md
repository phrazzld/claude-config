# CLAUDE

## Development Philosophy

* Consult `./docs/leyline/` for project-specific development philosophies and guidelines

## Essential Tools

**Research & Information:**
* Use `gemini --prompt` for web research, documentation lookup, and external information
  ```bash
  gemini --prompt "latest Next.js 15 routing changes"
  gemini --prompt "best practices for PostgreSQL indexing"
  ```

**Code Analysis:**
* Use `ast-grep` for semantic code search and structural pattern matching
  ```bash
  ast-grep --lang typescript -p 'function $NAME($$$) { $$$ }'
  ast-grep --lang rust -p 'impl $TRAIT for $TYPE'
  ```

**Expert Consultation:**
* Use `thinktank` CLI for expert advice on:
  - Code review and feedback
  - Task planning and architecture decisions
  - Security audits and vulnerability analysis
  - Complex problem solving
  ```bash
  # Create instructions.txt with your question/task
  thinktank instructions.txt ./src
  thinktank security-review.md ./auth --dry-run
  ```

**Parallel Execution:**
* Use the `Task` tool to launch multiple agents in parallel when actions operate in distinct, non-conflicting spaces:
  - Research from different perspectives or domains
  - Brainstorming ideas with independent expert viewpoints
  - Conducting investigations across separate code areas
  - Writing code/tests/docs in isolated modules
  ```bash
  # Example: Launch parallel research agents
  Task 1: "Research authentication patterns in codebase"
  Task 2: "Investigate API rate limiting best practices" 
  Task 3: "Analyze error handling conventions"
  ```

## Reasoning Budget Control

Claude has powerful reasoning capabilities that can be invoked with specific phrases:

**Reasoning Levels:**
* `think` - Basic reasoning for straightforward analysis
* `think hard` - Deeper analysis for complex problems
* `think very hard` - Extensive reasoning for intricate challenges  
* `ultrathink` - Maximum reasoning budget for the most complex tasks

**Usage Guidelines:**
* Use reasoning phrases when tasks require careful analysis, not for simple operations
* Match reasoning level to task complexity:
  - Simple refactoring, documentation → no explicit reasoning needed
  - Architecture decisions, debugging → `think` or `think hard`
  - System-wide changes, security analysis → `think very hard`
  - Fundamental reimagining, complex algorithms → `ultrathink`
* Place reasoning phrases before the analysis request for best results
* These phrases unlock deeper analytical capabilities and should be used judiciously
