---
description: Audit LLM infrastructure quality - model routing, prompt testing, observability, security, cost
---

Audit and improve LLM-specific quality infrastructure.

# LLM-GATES

Channel AI engineering rigor: critically examine LLM infrastructure and identify improvements.

## The North Star

> **"Deploy a prompt change Friday afternoon and turn your phone off."**
>
> If you can't do this, LLM quality gates are missing. This command finds what's blocking confident AI deployments.

## The LLM Quality Principle

"Are we testing prompts, routing intelligently, and observing production?"

Traditional quality gates (linting, tests, CI/CD) don't catch LLM-specific failures: prompt regressions, model degradation, hallucinations, jailbreaks, cost explosions. This command audits whether LLM-specific checks are in place.

**The Friday Afternoon Test for LLM Apps:**
- Prompt changes tested before merge
- Model fallbacks handle provider outages
- Production traces debug any failure
- Security scans catch jailbreaks
- Cost alerts prevent surprise bills

## The Prompt Engineering Maturity Model

| Level | Maturity | Signs |
|-------|----------|-------|
| 0 | Ad-hoc | Prompts in code strings, no tests, "looks good" QA |
| 1 | Versioned | Prompts in separate files, Git-tracked, manual testing |
| 2 | Tested | Automated evals, regression suite, pre-deploy checks |
| 3 | **CI/CD** ⭐ | Pipeline integration, A/B tests, model pinning |
| 4 | Observable | Production monitoring, continuous improvement, alerts |

**Target: Level 3-4 for production apps.**

## Five Pillars of LLM Quality

### 1. Model Selection & Routing

**Detect current setup:**
```bash
# Search for model configs
**/*aiProviders*.{ts,js,py}
**/*llm*config*.{yaml,json,ts,js,py}
.env, .env.local (look for OPENAI_API_KEY, ANTHROPIC_API_KEY, OPENROUTER_API_KEY)
```

**Critical questions:**
- Are we using OpenRouter or similar for multi-model access?
- Do we have fallback chains for reliability?
- Is there cost-based routing (cheap model for simple, expensive for complex)?
- Are models pinned to versions (not "gpt-4" but "gpt-4-0125-preview")?
- Can we A/B test model changes?

**Red flags:**
- Single provider lock-in (only OpenAI keys)
- No fallback chains (one provider down = app down)
- Model strings hardcoded throughout codebase
- No cost tracking or routing
- Using latest model aliases (drift risk)

**Recommended tools:**
- **OpenRouter** (recommended): 400+ models, A/B testing, fallbacks, unified billing
- **LiteLLM**: Self-hosted proxy, 100+ providers, full control
- **Helicone**: Observability + gateway combo

**Output:**
```markdown
### Model Selection & Routing
- **Current state**: [OpenRouter configured / Single provider / Hardcoded models]
- **Providers detected**: [OpenAI, Anthropic, OpenRouter, etc.]
- **Fallback chains**: [Yes/No]
- **Cost routing**: [Yes/No]
- **Model pinning**: [Yes/No - list unpinned models]
- **Recommendation**: [Set up OpenRouter with fallbacks and cost routing]
```

### 2. Prompt Testing & CI/CD

**Detect current setup:**
```bash
# Look for evaluation configs
promptfooconfig.{yaml,json}
.promptfoo/
**/*.promptfoo.yaml

# GitHub Actions for prompts
.github/workflows/*prompt*.yml
.github/workflows/*eval*.yml
.github/workflows/*llm*.yml
```

**Critical questions:**
- Is Promptfoo or similar evaluation framework configured?
- Do prompts get tested before merge (GitHub Action)?
- Is there a regression test suite (golden examples)?
- Are security tests running (red teaming)?
- Do we have quality thresholds that block bad prompts?

**Red flags:**
- No `promptfooconfig.yaml` in repo
- No GitHub Action for prompt evaluation
- Prompts changed without any testing
- No security/red team testing
- No factuality or RAG evaluation

**Recommended tools:**
- **Promptfoo** (recommended): Best CI/CD integration, security testing, open-source
- **Braintrust**: End-to-end platform (evals + observability)
- **DeepEval**: Open-source, research-backed metrics

**Promptfoo quick setup:**
```bash
# Initialize (no global install needed)
npx promptfoo@latest init

# Run evaluation
npx promptfoo@latest eval -c promptfooconfig.yaml

# Run security scan
npx promptfoo@latest redteam run
```

**GitHub Action template:**
```yaml
name: 'Prompt Evaluation'
on:
  pull_request:
    paths: ['prompts/**', 'src/**/*prompt*']
jobs:
  evaluate:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - uses: actions/cache@v4
        with:
          path: ~/.promptfoo
          key: ${{ runner.os }}-promptfoo-${{ hashFiles('promptfooconfig.yaml') }}
      - uses: promptfoo/promptfoo-action@v1
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

**Output:**
```markdown
### Prompt Testing & CI/CD
- **Current state**: [Promptfoo configured / No evaluation / Manual testing only]
- **Eval framework**: [Promptfoo / Braintrust / None]
- **CI/CD integration**: [GitHub Action / None]
- **Test coverage**: [X test cases / None]
- **Security testing**: [Red team enabled / None]
- **Recommendation**: [Set up Promptfoo with GitHub Action]
```

### 3. Production Observability

**Detect current setup:**
```bash
# Langfuse configuration
langfuse.config.*
**/*langfuse*.{ts,js}
.env (LANGFUSE_*)

# Other observability
**/*helicone*.{ts,js}
**/*braintrust*.{ts,js}
**/*langsmith*.{ts,js}
```

**Critical questions:**
- Is Langfuse or similar LLM observability configured?
- Can we trace any LLM call in production?
- Is cost tracking enabled (know spend per user/request)?
- Are there alerts for error spikes, cost spikes, latency?
- Can we debug "why did this LLM call fail?"

**Red flags:**
- No LLM tracing in production
- Can't answer "why did this fail?"
- No cost tracking (surprise bills possible)
- No alerts for LLM-specific issues
- Logs don't include prompt/response

**Recommended tools:**
- **Langfuse** (recommended): Self-hostable, generous free tier, production-ready
- **Helicone**: Proxy-based, simple setup, cost optimization
- **Braintrust**: Unified evals + observability
- **LangSmith**: LangChain ecosystem, commercial

**Langfuse quick setup:**
```bash
# Install
pnpm add langfuse

# Configure (in code)
import { Langfuse } from "langfuse";
const langfuse = new Langfuse({
  publicKey: process.env.LANGFUSE_PUBLIC_KEY,
  secretKey: process.env.LANGFUSE_SECRET_KEY,
});
```

**Output:**
```markdown
### Production Observability
- **Current state**: [Langfuse configured / No tracing / Logs only]
- **Observability tool**: [Langfuse / Helicone / None]
- **Trace coverage**: [All calls / Partial / None]
- **Cost tracking**: [Yes/No]
- **Alerts configured**: [Yes/No]
- **Recommendation**: [Set up Langfuse with cost alerts]
```

### 4. Security & Compliance

**Detect current setup:**
```bash
# Security scanning
promptfooconfig.yaml (check for redteam section)
**/*guardrail*.{ts,js,py}
**/*safety*.{ts,js,py}

# PII handling
**/*redact*.{ts,js,py}
**/*sanitize*.{ts,js,py}
```

**Critical questions:**
- Is red team testing configured (jailbreak, injection, PII)?
- Are there guardrails for harmful outputs?
- Is PII redacted from prompts/logs?
- Do we have compliance reports (OWASP, NIST)?
- Are there input validation checks?

**Red flags:**
- No security testing for prompts
- User input goes directly to LLM (injection risk)
- PII in prompts/responses logged
- No output filtering for harmful content
- No compliance reporting

**Security testing with Promptfoo:**
```bash
# Run red team scan
npx promptfoo@latest redteam run

# Generate compliance report
npx promptfoo@latest redteam report --output compliance.html
```

**OWASP Top 10 for LLMs:**
1. Prompt Injection
2. Insecure Output Handling
3. Training Data Poisoning
4. Model Denial of Service
5. Supply Chain Vulnerabilities
6. Sensitive Information Disclosure
7. Insecure Plugin Design
8. Excessive Agency
9. Overreliance
10. Model Theft

**Output:**
```markdown
### Security & Compliance
- **Current state**: [Red team configured / No security testing]
- **Security scanning**: [Promptfoo redteam / None]
- **PII handling**: [Redaction enabled / None]
- **Guardrails**: [Configured / None]
- **Compliance**: [OWASP/NIST reports / None]
- **Recommendation**: [Enable Promptfoo red team scanning]
```

### 5. Cost & Performance

**Detect current setup:**
```bash
# Cost tracking
**/*cost*.{ts,js,py}
**/*budget*.{ts,js,py}
**/*usage*.{ts,js,py}

# Performance monitoring
**/*latency*.{ts,js,py}
**/*metrics*.{ts,js,py}
```

**Critical questions:**
- Do we track cost per request/user?
- Are there token budgets (max_tokens limits)?
- Is latency monitored (p50, p95, p99)?
- Are there alerts for cost spikes?
- Is model routing optimized for cost?

**Red flags:**
- No cost tracking (can't answer "what's our LLM spend?")
- No token limits (runaway costs possible)
- No latency monitoring (slow responses undetected)
- No cost alerts (surprise bills)
- All requests go to most expensive model

**Cost optimization strategies:**
- **Model routing**: Simple queries → cheap models, complex → expensive
- **Token limits**: Set max_tokens to prevent runaway responses
- **Caching**: Cache common queries (prompt caching, response caching)
- **Batching**: Batch requests where possible

**Output:**
```markdown
### Cost & Performance
- **Current state**: [Cost tracking enabled / No tracking]
- **Cost tracking**: [Per-request / Per-user / None]
- **Token budgets**: [Configured / None]
- **Latency monitoring**: [p50/p95/p99 tracked / None]
- **Cost alerts**: [Configured / None]
- **Model routing**: [Cost-optimized / Static]
- **Recommendation**: [Set up cost tracking with alerts]
```

## Quality Gate Standards

### Pre-commit (< 5s)
- Prompt file syntax validation
- Secret scan (no API keys in prompts)
- Basic injection pattern detection

### Pre-push (< 15s)
- Quick regression suite (5-10 golden test cases)
- Cost estimate check (token budget)
- Latency baseline check

### CI/CD (< 5 min)
- Full evaluation suite (50-100+ test cases)
- Red team security scan (OWASP top 10)
- Before/after comparison (regression detection)
- Compliance report generation

### Production
- Continuous trace monitoring (Langfuse)
- Cost alerts (>2x daily average)
- Error rate alerts (>5% failures)
- Latency alerts (p95 > SLA)

## Your Approach

### 1. Scan Repository

Look for:
```bash
# Model configs
**/*aiProviders*.{ts,js,py}
**/*llm*config*.{yaml,json,ts,js,py}
.env, .env.local

# Promptfoo
promptfooconfig.{yaml,json}
.github/workflows/*prompt*.yml

# Langfuse
langfuse.config.*
**/*langfuse*.{ts,js}

# Security
**/*guardrail*.{ts,js,py}
**/*redact*.{ts,js,py}
```

### 2. Audit Each Pillar

For each of the five pillars:
1. Detect current state
2. Identify gaps
3. Prioritize improvements
4. Generate CLI commands

### 3. Generate Improvement Plan

Prioritize by impact:
- **Critical**: No testing, no observability, no security
- **High**: Missing CI/CD, no cost tracking, single provider
- **Medium**: Missing fallbacks, no latency monitoring, incomplete traces
- **Low**: Optimization opportunities, nice-to-haves

## Output Format

```markdown
## LLM Infrastructure Audit

### Maturity Assessment
- **Current level**: X (Ad-hoc / Versioned / Tested / CI/CD / Observable)
- **Target level**: 3-4 (CI/CD + Observable)

### Model Selection & Routing
- **Current state**: [description]
- **Gaps**: [list]
- **Improvements**: [list with CLI commands]

### Prompt Testing & CI/CD
- **Current state**: [description]
- **Gaps**: [list]
- **Improvements**: [list with CLI commands]

### Production Observability
- **Current state**: [description]
- **Gaps**: [list]
- **Improvements**: [list with CLI commands]

### Security & Compliance
- **Current state**: [description]
- **Gaps**: [list]
- **Improvements**: [list with CLI commands]

### Cost & Performance
- **Current state**: [description]
- **Gaps**: [list]
- **Improvements**: [list with CLI commands]

## Generated TODOs
- [ ] [CRITICAL] [action with CLI command]
- [ ] [HIGH] [action with CLI command]
- [ ] [MEDIUM] [action with CLI command]
- [ ] [LOW] [action with CLI command]
```

## Quick Wins

### No Promptfoo? Start here:
```bash
# Initialize Promptfoo
npx promptfoo@latest init

# Run first evaluation
npx promptfoo@latest eval

# View results
npx promptfoo@latest view
```

### No Langfuse? Start here:
```bash
# Install
pnpm add langfuse

# Sign up at langfuse.com (free tier)
# Add to .env:
LANGFUSE_PUBLIC_KEY=pk-...
LANGFUSE_SECRET_KEY=sk-...
LANGFUSE_HOST=https://us.cloud.langfuse.com
```

### Single provider? Add OpenRouter:
```bash
# Sign up at openrouter.ai
# Add to .env:
OPENROUTER_API_KEY=sk-or-...

# Use with Vercel AI SDK:
import { createOpenAI } from "@ai-sdk/openai";
const openrouter = createOpenAI({
  baseURL: "https://openrouter.ai/api/v1",
  apiKey: process.env.OPENROUTER_API_KEY,
});
```

## Related Skills

Invoke these skills for detailed guidance:
- `llm-evaluation` - Promptfoo setup, CI/CD integration, assertions
- `llm-gateway-routing` - OpenRouter, LiteLLM, routing strategies
- `ai-llm-development` - Model selection, prompt engineering, production
- `langfuse-observability` - Tracing, cost tracking, debugging

## The Philosophy

LLM apps fail differently than traditional software:
- **Non-deterministic**: Same input → different outputs
- **Degradation**: Quality drifts as models update
- **Hallucination**: Confident but wrong answers
- **Injection**: Prompts can be hijacked
- **Cost explosion**: Token usage can spike unexpectedly

Traditional tests don't catch these. You need:
- **Evaluation suites** that test behavior, not exact outputs
- **Security scans** that find prompt injection vulnerabilities
- **Production traces** that show why calls failed
- **Cost monitoring** that alerts on spikes
- **Model routing** that falls back gracefully

### The Friday Afternoon Standard for LLM Apps

**Can you deploy a prompt change Friday at 5pm and turn your phone off?**

If NO:
- No prompt testing (regressions undetected)
- No security scans (jailbreaks possible)
- No observability (can't debug failures)
- No fallbacks (provider outage = app outage)
- No cost alerts (surprise bills possible)

If YES:
- Prompt changes tested in CI/CD
- Red team scans catch security issues
- Full traces for debugging
- Fallback chains handle outages
- Cost alerts prevent surprises

**LLM quality gates enable fearless AI deployments. That's the only metric that matters.**
