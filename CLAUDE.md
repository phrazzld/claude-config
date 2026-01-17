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

### 2026-01-16: External Integration Debugging

**Check config before code.** When external services (Stripe, Clerk, etc.) fail in production:
1. First verify env vars are set on production deployment: `./scripts/verify-env.sh --prod-only`
2. Then check service logs and dashboards
3. Only then consider code changes

Root cause is often missing config, not code bugs. Code analysis can burn hours when `env list` would reveal the problem in seconds.

**Dev ≠ Prod is a footgun.** Separate deployments mean env vars must be set twice. The `--prod` flag is easy to forget. Always verify:
```bash
CONVEX_DEPLOYMENT=prod:... npx convex env list | grep <SERVICE>
```

**Don't over-engineer under pressure.** When debugging production issues, resist the urge to build sophisticated solutions before confirming the diagnosis. Simpler is better until proven otherwise.

### 2026-01-17: Environment Variable Hygiene

**Trailing whitespace kills.** Env vars with `\n` or trailing spaces cause cryptic errors:
- "Invalid character in header content" (HTTP headers)
- Webhook signature mismatches
- Silent authentication failures

**Rules:**
1. Use `printf '%s' 'value'` not `echo` when setting secrets via CLI
2. Always trim: `value=$(echo "$var" | tr -d '\n')`
3. Validate format before use: `[[ "$key" =~ ^sk_(live|test)_ ]]`

**Cross-platform parity.** Shared tokens (webhook secrets, auth tokens) must match across:
- Vercel environment
- Convex environment
- Local .env.local

Verify parity: tokens set on one platform but not the other cause silent failures.

**CLI environment gotcha.** `CONVEX_DEPLOYMENT=prod:xxx npx convex data` may return dev data.
Always use `npx convex run --prod` flag or verify via Convex Dashboard.

### 2026-01-17: DEBUG MODE — Incident Investigation Protocol

**OODA-V Framework.** When debugging production issues, follow this loop:

1. **OBSERVE** — Gather raw data before forming hypotheses
   - Check logs first: "Is the request hitting our server?"
   - If no logs, it's network/routing/redirects, NOT application code
   - Run basic reachability checks: `curl -I <endpoint>`

2. **ORIENT** — Generate hypotheses with specific tests
   - List 3 hypotheses ranked by likelihood
   - For each: "What test would disprove this?"
   - Include the simple checks (curl, logs) before code analysis

3. **DECIDE** — Pick highest-likelihood hypothesis

4. **ACT** — Implement minimal fix

5. **VERIFY** — (MANDATORY) No fix is complete without observables
   - Show the log entry that proves delivery
   - Show the metric change (e.g., pending_webhooks decreased)
   - "Confidence: LOW until verified"

**Anti-patterns to avoid:**
- Agreeing a fix "should work" without seeing proof
- Declaring resolved before metrics confirm
- Endorsing plausible explanations without running tests
- Stopping at first "looks like the cause" without verification
- Treating configuration inspection as equivalent to runtime behavior

**Verification gate for incidents:**
```
VERIFIED = saw_log_entry AND metric_changed AND (database_state_correct OR not_applicable)
```

If verification fails → revert if needed → loop back to OBSERVE.

**Skills for incident debugging:**
- `/stripe-health` — Webhook endpoint diagnostics
- `/verify-fix` — Mandatory verification checklist
