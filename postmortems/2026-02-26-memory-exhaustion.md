# Postmortem: Memory Exhaustion from Vitest Watch Mode + Agent Spawning

**Date**: 2026-02-26
**Severity**: High (machine near-crash, forced terminal kill)
**Duration**: Unknown (accumulated over multiple sessions)
**Status**: Resolved

## Summary

The machine reached 60+ GB memory usage on a 36 GB system, forcing a manual terminal kill. Dozens of zombie Node/Vitest processes were each consuming 2+ GB. Three independent factors combined into a memory cascade: (1) 12 repositories configured with bare `vitest` as their test script, which runs in watch mode and never exits, (2) Moonbridge MCP spawning up to 6 parallel AI agents simultaneously, each with their own Node process trees, and (3) the `fast-feedback.py` hook firing SWC/tsc/eslint on every file edit with no throttling or deduplication.

## Timeline

| Time | Event |
|------|-------|
| Ongoing (days) | Each Claude Code session that ran `pnpm test` in any of 12 repos left a vitest watch process alive |
| Ongoing | `fast-feedback.py` fired tsc/eslint on every Edit/Write, spawning short-lived but frequent Node processes |
| Ongoing | Moonbridge parallel agent spawning created bursts of 6+ concurrent heavy processes |
| ~2026-02-26 | Memory pressure crossed critical threshold (~60 GB), system became unresponsive |
| 2026-02-26 | User force-killed terminal, identified root causes, planned hardening |
| 2026-02-27 02:44Z | All 7 phases of hardening implemented and verified |

## Root Cause

**Vitest's default behavior is watch mode.** When `package.json` has `"test": "vitest"` (no `run` subcommand), vitest starts in interactive watch mode, holding a persistent Node process open indefinitely. The `stop-quality-gate.py` hook runs `pnpm test` at end-of-turn, meaning every Claude Code session in a TS repo spawned a zombie vitest watcher that was never cleaned up.

This was amplified by two force multipliers:
- **Moonbridge** could spawn 6 parallel agents, each potentially triggering their own test runs
- **fast-feedback.py** fired tsc/eslint on every single file write, adding continuous process churn

## 5 Whys

1. **Why did memory spike?** Dozens of vitest watch processes accumulated across sessions.
2. **Why were watch processes accumulating?** `pnpm test` ran `vitest` (watch mode) and the process was never killed when Claude Code sessions ended.
3. **Why did `pnpm test` run watch mode?** 12 package.json files had `"test": "vitest"` without the `run` subcommand. Vitest defaults to watch in TTY-like environments.
4. **Why wasn't `CI=true` set?** The quality gate hook ran subprocess without setting CI environment, and vitest only auto-detects CI from the env var.
5. **Why were there no guardrails?** No skill, hook, or convention documented that `vitest` scripts must use `run`. The failure mode is silent (process starts, test passes, process stays alive in background).

## What Went Well

- User recognized the pattern (not first occurrence) and immediately planned systematic hardening
- Fix addressed all three root causes, not just the primary one
- Belt-and-suspenders approach: fixed package.json scripts AND added CI=true to hooks
- Codified the learning into skill, CLAUDE.md, and auto-memory to prevent regression
- Moonbridge removal was a pragmatic simplification rather than patching around its resource behavior

## What Went Wrong

- **No process monitoring**: No hook or check detected runaway memory or zombie processes
- **No vitest convention**: 12 repos independently had the same misconfiguration with no shared standard
- **Moonbridge resource model was invisible**: No visibility into how many processes Moonbridge agents spawned
- **fast-feedback was redundant**: It duplicated stop-quality-gate's job but ran 10-100x more often, adding process churn with no unique value
- **Accumulation over days**: The problem built gradually across sessions, making it hard to attribute to any single action

## Follow-up Actions

| Action | Status | Notes |
|--------|--------|-------|
| Fix all 12 package.json: `vitest` → `vitest run` | Done | Phase 1 |
| Add `CI=true` to stop-quality-gate subprocess env | Done | Phase 2 |
| Add pool limits to volume's vitest.config.ts | Done | Phase 3 |
| Remove fast-feedback.py hook | Done | Phase 4 |
| Uninstall Moonbridge from all config + skills | Done | Phase 5 |
| Add memory safety section to vitest skill | Done | Phase 6 |
| Add vitest safety rules to CLAUDE.md staging | Done | Phase 7 |
| Record incident in auto-memory | Done | Phase 7 |
| Add pool limits to brainrot + sploot vitest configs | Done | `forks`, `maxForks: 4` |
| Audit for other test runners that might watch-mode | Done | Found whetstone `jest --watchAll`, fixed |
| Augment session-health-check with orphan vitest detection | Done | Warns + suggests `pkill -f vitest` |

## Lessons

1. **Default behaviors kill you silently.** Vitest's watch-mode default is reasonable for interactive dev but catastrophic in automated contexts. Always verify what a command's default mode is before putting it in a hook.

2. **Redundant hooks aren't free.** fast-feedback and stop-quality-gate covered the same ground. The "extra safety" of fast-feedback actually made things worse by multiplying process spawns.

3. **MCP servers are resource-opaque.** Moonbridge could spawn arbitrary processes with no visibility into resource consumption. Prefer tools where you can see and bound the blast radius (CLI commands, Task tool with known process model).

4. **Conventions need enforcement, not just documentation.** Having 12 repos independently misconfigured the same way proves the fix needs to be at the tool/hook level, not just "remember to add `run`."
