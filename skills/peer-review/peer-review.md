# /peer-review

Multi-provider adversarial science review. Attacks experimental methodology, citations, logic,
and data integrity before publication. Provider variance is the core design principle — Anthropic
cannot grade its own homework.

## When to use

- Before publishing any experiment deliverables
- After generating paper.md or findings.md
- When you want to stress-test a hypothesis verdict
- As a final gate before creating a PR for publication artifacts

## Input

Target path — either:
- An experiment family: `experiments/prompt-injection-boundary-tags/`
- A specific round: `experiments/prompt-injection-boundary-tags/rounds/round7/`

The skill will locate `report/paper.md`, `report/findings.md`, `data/*.csv`, and `design.md`.

## Process

### Phase 1: Parallel Adversarial Reviews (4 providers)

Launch all 4 reviews simultaneously. Each writes its findings to a temp file.

#### Reviewer 1: Methodology Critic (OpenAI via Codex)

**Provider rationale:** Different training data and safety biases from the authoring model.

```bash
codex exec --full-auto "$(cat <<'PROMPT'
You are a hostile methodology reviewer. Your job is to find every flaw in this experiment's
design. Read the following files and attack the experimental methodology:

Files to read:
- [design.md path]
- [paper.md path]
- [findings.md path]

Attack vectors:
1. Sample size adequacy — are N values sufficient for claimed effect sizes?
2. Statistical test selection — are tests appropriate for the data distribution?
3. Control conditions — are there confounds? Missing baselines?
4. Simulation validity — if simulated, does the simulation model faithfully represent
   the phenomenon? Are risk multipliers justified?
5. Generalizability — can conclusions extend beyond the tested models/conditions?
6. Cherry-picking — are unfavorable results downplayed or omitted?

For each finding, rate: FATAL / MAJOR / MINOR / NOTE
Output a structured markdown report.
PROMPT
)" --output-last-message /tmp/peer-review-methodology.md 2>/dev/null
```

#### Reviewer 2: Citation Verifier (Google via Gemini)

**Provider rationale:** Web-grounded search is native. Verifies references exist and claims
match cited work.

```bash
gemini "$(cat <<'PROMPT'
You are a citation and prior art verifier. Read this paper and verify every claim against
the literature.

Paper: [paste paper.md content or provide path]

Tasks:
1. For every citation — verify it exists (search the web). Report any phantom references.
2. For every claim like "prior work shows X" — verify the cited work actually shows X.
3. Check if the novelty claim holds — search for work published after the paper's
   references that might invalidate the novelty statement.
4. Check for missing citations — important related work the authors should have cited.
5. Verify venue and year accuracy for all references.

For each finding, rate: FATAL / MAJOR / MINOR / NOTE
Output a structured markdown report.
PROMPT
)" > /tmp/peer-review-citations.md 2>/dev/null
```

#### Reviewer 3: Logic Auditor (Anthropic via Task tool subagent)

**Provider rationale:** Strong at logical reasoning and long-document analysis.

Use the Task tool with subagent_type="general-purpose":
```
Prompt: "You are a logic auditor. Read these files: [paper.md], [findings.md], [design.md].

Trace every conclusion back to its supporting data. Flag:
1. Logical leaps — conclusions not supported by presented evidence
2. Reversed causality — correlation presented as causation
3. Scope creep — conclusions that exceed what the data can support
4. Internal contradictions — findings section says X, discussion says Y
5. Missing alternative explanations — could another factor explain the result?
6. Hedging inconsistency — strong claims in abstract, weak evidence in results

For each finding, rate: FATAL / MAJOR / MINOR / NOTE
Output a structured markdown report."
```

#### Reviewer 4: Data Integrity Reviewer (Anthropic via Task tool subagent)

**Provider rationale:** Needs tool access (Read, Bash) to recompute numbers from raw CSVs.

Use the Task tool with subagent_type="general-purpose":
```
Prompt: "You are a data integrity auditor. You have access to Read and Bash tools.

Files:
- Raw data: [data/*.csv paths]
- Paper: [paper.md]
- Findings: [findings.md]

Tasks:
1. Read the CSV data files. Compute summary statistics independently.
2. Compare your computed numbers against every number cited in the paper and findings.
3. Flag any discrepancy — wrong mean, wrong N, wrong percentage, wrong CI.
4. Check that charts/figures match the underlying data.
5. Verify that the scoring methodology described matches the actual scorer behavior
   (read shared/scoring/scorer.py if referenced).
6. Check for data leakage between train/test conditions (if applicable).

For each discrepancy, rate: FATAL / MAJOR / MINOR / NOTE
Output a structured markdown report with your recomputed values."
```

### Phase 2: Cross-Model Synthesis via thinktank

After all 4 reviews complete, feed them into thinktank for multi-model synthesis:

```bash
thinktank "$(cat <<'PROMPT'
You have received 4 adversarial peer reviews of a scientific experiment from different
AI providers. Your job is to synthesize them into a single, authoritative review.

Reviews:
1. Methodology (from OpenAI): [/tmp/peer-review-methodology.md]
2. Citations (from Google): [/tmp/peer-review-citations.md]
3. Logic (from Anthropic): [/tmp/peer-review-logic.md]
4. Data Integrity (from Anthropic): [/tmp/peer-review-data.md]

Tasks:
1. De-duplicate — merge findings that multiple reviewers flagged
2. Resolve disagreements — if reviewers contradict, explain both positions
3. Assign final severity — FATAL / MAJOR / MINOR / NOTE with consensus rationale
4. Catch blind spots — flag anything ALL 4 reviewers missed
5. Assess overall publication readiness

Output format:
## Findings (severity-ranked)
### FATAL
### MAJOR
### MINOR
### NOTES

## Reviewer Concordance
[Where did providers agree? Disagree?]

## Blind Spot Analysis
[What might all reviewers have missed?]

## Verdict
PUBLISH / REVISE AND RESUBMIT / MAJOR REVISION REQUIRED
PROMPT
)" --file /tmp/peer-review-methodology.md \
  --file /tmp/peer-review-citations.md \
  --file /tmp/peer-review-logic.md \
  --file /tmp/peer-review-data.md \
  --synthesis > /tmp/peer-review-synthesis.md 2>/dev/null
```

### Phase 3: Final Report

Write `{target_path}/report/peer_review.md`:

```markdown
# Peer Review: [Experiment Name]

**Date**: [YYYY-MM-DD]
**Target**: [path reviewed]
**Verdict**: [PUBLISH / REVISE AND RESUBMIT / MAJOR REVISION REQUIRED]

## Review Panel

| Phase | Provider | Role | Tool |
|-------|----------|------|------|
| 1 | OpenAI (GPT-5.2 Codex) | Methodology Critic | codex exec |
| 1 | Google (Gemini 3 Pro) | Citation Verifier | gemini CLI |
| 1 | Anthropic (Claude) | Logic Auditor | Task subagent |
| 1 | Anthropic (Claude) | Data Integrity | Task subagent |
| 2 | Multi-model ensemble | Synthesis | thinktank |

## Findings

### FATAL
[Findings that block publication. Must be resolved.]

### MAJOR
[Significant issues that weaken the work. Should be resolved.]

### MINOR
[Small issues. Nice to fix but not blocking.]

### NOTES
[Suggestions for improvement. No action required.]

## Reviewer Concordance

[Where did providers agree? Where did they disagree? What does disagreement tell us?]

## Provider Attribution

[For each finding — which provider(s) flagged it. Helps calibrate reviewer quality over time.]

## Blind Spot Analysis

[What might all reviewers have missed? Structural limitations of AI peer review.]

## Action Items

- [ ] [FATAL-1]: [specific fix needed]
- [ ] [MAJOR-1]: [specific fix needed]
- ...
```

## Provider Coverage

| Provider | Phase | Role | Why |
|----------|-------|------|-----|
| OpenAI | 1 | Methodology | Different training data, different blind spots |
| Google | 1 | Citations | Native web-grounded search |
| Anthropic | 1 | Logic + Data | Strong reasoning, tool access for recomputation |
| Multi-model | 2 | Synthesis | Ensemble catches single-model blind spots |

No single provider dominates. The authoring model (Anthropic) handles logic/data where it
excels, but methodology and citation verification come from independent providers.

## Output

The skill produces:
1. `{target_path}/report/peer_review.md` — the final review
2. Temp files cleaned up after synthesis

## Limitations

- AI reviewers cannot catch domain-expertise gaps (e.g., "this statistical test requires
  normality assumption the authors didn't verify") as reliably as human domain experts
- Citation verification depends on web search quality — paywalled papers may not be verifiable
- The review is adversarial by design — it optimizes for finding flaws, not praising strengths
- Provider availability may vary — if a provider is down, note the gap in the report
