# CLAUDE

Sacrifice grammar for the sake of concision.

## Software Design Philosophy

**Foundation**: Informed by John Ousterhout's "A Philosophy of Software Design" - managing complexity is the primary challenge in software engineering.

### Complexity Management
- **The Enemy**: Complexity is anything that makes software hard to understand or modify
- **Two Sources**: Dependencies (linkages between components) + Obscurity (non-obvious information)
- **Zero Tolerance**: Fight accumulating complexity with every decision

### Module Design
- **Deep Modules**: Simple interfaces hiding powerful implementations
- **Value Formula**: Module worth = Functionality - Interface Complexity
- **Watch For**: Shallow modules where interface ≈ implementation complexity
- **Layer Discipline**: Each abstraction layer must change vocabulary and concepts

### Information Architecture
- **Hide Implementation**: Internal details stay internal
- **Expose Intention**: Interfaces define "what" not "how"
- **Detect Leakage**: If implementation changes break callers, you have leakage
- **Design for Misuse**: Make interfaces hard to use incorrectly

### Strategic Programming
- **Time Investment**: Dedicate 10-20% to design improvement, not just feature completion
- **Tactical vs Strategic**: Recognize when taking shortcuts vs investing in future velocity
- **Comments as Design**: Document reasoning, invariants, and intent code cannot express
- **Red Flags**: Watch for `Manager`/`Util`/`Helper` names, pass-through methods, config overload

## Engineering Discipline

**Test-First Thinking**: Generate test lists during planning. Write tests before implementation for core logic, algorithms, and production code with clear requirements. Prototype-first for exploration, then TDD the real implementation.

**Coverage Standards**: Target 80%+ patch coverage (new code only). Use GitHub Actions for PR comments. Branch coverage > line coverage. Don't chase absolute percentages.

**Small PRs**: Target 50-200 lines, max 400. Break down via vertical slicing, architectural layers, or feature flags. Use `git-spr` for stacking when needed. Auto-label all PRs with size.

**Architectural Decisions**: Create ADR (Architecture Decision Record) when decision is costly to reverse, has multiple viable alternatives, or affects team workflow. Plain markdown in `/docs/adr/`, MADR Light template. Never delete, only supersede.

**Documentation Discipline**: Update docs in same PR as code changes. Use `lychee` for link checking, `Vale` for style. Check freshness via git log. Living documentation > static docs.

## Essential Tools

**Code Analysis:**
* Use `ast-grep` for semantic code search and structural pattern matching
  ```bash
  ast-grep --lang typescript -p 'function $NAME($$$) { $$$ }'
  ast-grep --lang rust -p 'impl $TRAIT for $TYPE'
  ```

**AI Image Generation:**
* Skill: `gemini-imagegen` - Text-to-image generation, editing, multi-turn refinement
  ```bash
  # Generate image from text prompt
  ~/.claude/skills/gemini-imagegen/scripts/generate_image.py "prompt" output.png

  # Edit existing image
  ~/.claude/skills/gemini-imagegen/scripts/edit_image.py input.png "instruction" output.png

  # Interactive refinement session
  ~/.claude/skills/gemini-imagegen/scripts/multi_turn_chat.py
  ```
* Models: `gemini-2.5-flash-image` (fast, 1024px) | `gemini-3-pro-image-preview` (4K, pro quality)
* Requires: `GEMINI_API_KEY` environment variable (in `~/.secrets`)

**AI Research Assistant:**
* Use `gemini` CLI for web-grounded research, codebase investigation, and sophisticated reasoning
  ```bash
  # Quick research with web grounding
  gemini "What are best practices for React Server Components in Next.js 15?"

  # Deep codebase investigation
  gemini "Analyze this codebase architecture and identify technical debt"

  # Investigate with multimodal input
  gemini "Explain this architecture diagram" < diagram.png

  # Non-interactive mode for scripts
  gemini --prompt "Summarize breaking changes in Node.js 22" > summary.txt
  ```
* **Key Capabilities:**
  - **Google Search Grounding**: Real-time access to current docs, best practices, error solutions
  - **Codebase Investigator**: Autonomous architecture mapping, dependency tracing, root-cause analysis
  - **1M Token Context**: Analyze entire large codebases in single session
  - **Multimodal**: Process images, PDFs, diagrams, screenshots
  - **Shell Interpolation**: `!{command}` injects live shell output into prompts (in GEMINI.md)
* **When to Use Gemini CLI:**
  - Need current web-grounded information (latest framework docs, emerging patterns)
  - Investigating unfamiliar or complex codebases holistically
  - Require sophisticated reasoning with Gemini 3 Pro's advanced capabilities
  - Analyzing visual artifacts (architecture diagrams, UI screenshots)
  - Research that benefits from Google Search backing
* **When to Stay in Claude:**
  - Making code edits (Claude's Edit tool is superior)
  - File operations within known codebases
  - Following established project patterns
  - Tasks requiring Claude's specialized agents/skills
* **Integration Pattern**: Use Gemini as research assistant → bring findings back to Claude for implementation
* Free tier: 60 req/min, 1000 req/day with personal Google account

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
