---
description: Execute plan with Ousterhout principles - deep modules, strategic design
---

# OBJECTIVE
Execute the plan in full. Your goal is not just functional correctness, but system design excellence. Adhere to Ousterhout principles religiously.

# CORE PHILOSOPHY (NON-NEGOTIABLE)
1. Strategic vs. Tactical: Reject "tactical programming" (short-sighted fixes/hacks). Invest time to find the best long-term design.
2. Deep Modules: Prioritize modules that provide powerful functionality through simple interfaces.
3. Complexity Management: Pull complexity downwards. Handle edge cases internally; do not expose them to the caller.

# INSTRUCTIONS
1. ANALYZE: Before writing code, analyze the plan. Identify where complexity can be reduced.
2. REASON: If a requested step encourages a shallow interface or data leakage, refactor the plan to align with deep module design.
3. EXECUTE: Implement the solution.
4. VERIFY: Ensure the code is cleaner than when you found it.

# CONSTRAINT
If a strategic fix requires a massive deviation from the scope, pause and ask for clarification. Otherwise, proceed with the strategic implementation.
