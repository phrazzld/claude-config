# DISTILL (AND KEEP CLAUDE.md ALIVE)

Single command to both shrink and refresh CLAUDE.md. Target ≤100 lines of razor-sharp, repo-specific direction that actually reflects how we work *today*.

## 1. Baseline Scan
- Read README.md, existing CLAUDE.md, recent TODO/TASK logs, leyline docs
- Identify what makes this repo unique (tooling, workflows, constraints)
- Note stale guidance, unused tools, or missing practices

## 2. Extract the Signal
- Keep only guidance Claude needs to operate here; drop generic advice
- Promote patterns that repeatedly deliver value (command chains, tooling combos)
- Document invariants, pitfalls, or project-specific quality bars

## 3. Refresh The Content
- Evaluate each CLAUDE.md section (philosophy, tools, reasoning budgets, workflows)
- Ask for every line: still true? still used? needs a newer example?
- Add any new tools or principles that have become standard

## 4. Distill To ≤100 Lines
- Collapse redundancy, prefer imperative sentences
- Reference files/workflows instead of restating their contents
- Highlight only the top-tier tools (rg, ast-grep, Task, etc.) with live examples

## 5. Quality Bar
- [ ] Repository-specific, zero fluff
- [ ] Examples use real commands we run
- [ ] Dead tools/info removed
- [ ] New instructions easy to scan (headers, bullets, short sentences)
- [ ] Final line count ≤100

Deliverable: refreshed CLAUDE.md that feels like a living operations brief, not an archive.
