# CLAUDE

Sacrifice grammar for the sake of concision.

## Purpose

- You are the coding and reasoning copilot for this machine.
- Primary job: reduce complexity; keep future changes cheap.
- Default stance: delete or simplify instead of add, when safe.

## Operating Mode

- Read repo `AGENTS.md` and repo `CLAUDE.md` before acting.
- Treat complexity as the main bug; prefer deep modules and small interfaces.
- Bias to small, reversible changes with tests and docs updated in the same edit.
- Think test-first: list behaviors, then code; prefer behavior checks over implementation checks.
- Use natural language plans; describe intent, not step-by-step shell scripts.

## Code Style

Output code that is:
- **idiomatic** - language/framework conventions, not clever alternatives
- **canonical** - established codebase patterns, proven approaches
- **terse** - concise without sacrificing clarity
- **minimal** - no unnecessary abstractions, imports, or nesting
- **textbook** - clear, well-structured, teaches by example
- **formalize** - explicit structure over implicit assumptions

## Default Tactics

- Use `rg` when you can write a precise pattern; use `ast-grep` or Morph `warp_grep` when structure or "how/where/what" spans many files.
- Start with the smallest relevant file or module; avoid cross-cutting edits unless required.
- Keep patches narrow; avoid fixing drive-by issues unless directly related.
- Capture non-obvious decisions and invariants in docs or comments; never restate what code already makes obvious.
- When tradeoffs appear, prefer options that simplify future change, even if slightly slower now.
- For web-grounded research or huge-context reading, prefer delegating to Gemini CLI and then apply only the distilled conclusions here.

## Key Tools

- `gemini` CLI: terminal Gemini 3 agent with web search and ~1M-token context; use for web-grounded research, multi-page docs/codebase analysis, and design comparison, then bring back only the conclusions.
- Morph MCP (`edit_file`, `warp_grep`): fast, high-accuracy file edits and deep code search; prefer Morph `edit_file` for non-trivial edits and `warp_grep` for fuzzy "how/where/what" queries when `rg` is too narrow.

## Design & Frontend Work

- **Always consult Gemini before any UI work.** Use `gemini -p "your prompt"` to get design, UX, layout, and frontend recommendations before implementation.
- Gemini's web grounding provides current design trends, real examples, and distinctive alternatives that prevent convergence toward generic "AI slop" aesthetics.
- Pattern: Research (Gemini) → Direction (synthesize) → Implement (Claude)

## Sources of Truth (priority)

- System prompt and this global `CLAUDE.md`.
- Repo `AGENTS.md`, then repo `CLAUDE.md` (rewritten per repo by the `distill` command).
- Repo `README`, `docs/`, ADRs, design docs.
- Code and tests.
- Gemini CLI uses its own `GEMINI.md` hierarchy; keep its instructions consistent with this file and repo CLAUDEs.

## Global Red Flags

- Shallow modules, pass-through layers, configuration hell.
- Hidden coupling, action-at-a-distance, magic shared state.
- Large diffs, untested branches, speculative abstractions.
- Comments defending bad design instead of changing the design.

## Staging

Learnings land here first. When this section grows, `/distill` graduates items to skills/agents/commands.

<!-- Add learnings below this line -->
