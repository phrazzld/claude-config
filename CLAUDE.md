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
