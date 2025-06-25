# CLAUDE

**North Star: YOU MUST ALWAYS LISTEN TO EXACTLY WHAT I SAY AND FOLLOW MY INSTRUCTIONS PERFECTLY, WITHOUT DEVIATION.**

---

## Core Philosophy

**Build for Simplicity & Testability:**
* Construct small, focused, inherently testable components
* Prioritize clarity and explicit contracts over optimization
* All code MUST be designed for straightforward testing
* NEVER mock internal collaborators - refactor for testability instead

**Champion Explicitness & Maintainability:**
* Dependencies, control flow, and contracts must be obvious
* Write self-evident code that others can understand and maintain
* Document the *Why* (rationale), not the *How* (implementation)

**Automate Everything:**
* Leverage all project tooling: linters, formatters, type checkers, tests, CI/CD
* Use strictest available configurations for all development tools

---

## Mandatory Constraints

**Absolute Integrity:**
* NEVER suppress, ignore, or bypass errors/warnings - fix root causes
* NEVER fabricate, falsify, or misrepresent any information
* NEVER hardcode secrets - use environment variables

**Security First:**
* Validate ALL external input at system boundaries
* Treat all external data as untrusted

**Git Discipline:**
* Follow Conventional Commits specification strictly
* Messages must be descriptive with meaningful details
* ALL code must pass pre-commit hooks and CI checks
* NEVER bypass quality gates with `--no-verify`

**Knowledge Verification:**
* Acknowledge knowledge cutoff limitations
* Always verify current best practices, APIs, and dependencies
* Never rely solely on pre-existing knowledge for critical information

---

## Operational Excellence

**Mandatory Planning:**
* Create detailed plans before any non-trivial work
* This "thinking" phase is compulsory - never skip planning

**Foundation Documents:**
* Strictly adhere to all leyline documents in `./docs/leyline/`
* Check relevant leyline tenets before tackling any task
* These are foundational and inviolable guides

---

## Use Tools!

* You run in an environment where `ast-grep` is available; whenever a search requires syntax-aware or structural matching, default to `ast-grep --lang rust -p '<pattern>'` (or set `--lang` appropriately) and avoid falling back to text-only tools like `rg` or `grep` unless I explicitly request a plain-text search.

* Search the web when you're unsure about things. Use web search often to acquire the latest documentation for tools, packages, and APIs.

* Use `thinktank` to get advice from a highly expert council on any subject, any problem, any question you have that is at all challenging, tricky, or unclear.

---

## Other Notes

* It is currently 2025
