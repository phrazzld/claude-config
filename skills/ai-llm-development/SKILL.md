---
name: ai-llm-development
description: |
  Apply modern AI/LLM development best practices. Invoke when:
  - Building AI features or integrating LLMs into applications
  - Selecting models (don't memorize - learn to find current ones)
  - Writing or reviewing prompts (context engineering > prompt tweaking)
  - Designing RAG pipelines, tool use, or agentic systems
  - Optimizing costs (caching, model routing, token limits)
  - Evaluating LLM outputs (LLM-as-judge, test datasets)
  - Deploying AI features to production (error handling, observability)
  KEY: The landscape changes monthly. Learn HOW to find current solutions.
---

# AI/LLM Development

## Core Philosophy

**Context Engineering > Prompt Engineering**: Optimize entire LLM configuration, not just wording.

**Simplicity First**: 80% of use cases need single LLM call, not multi-agent systems.

**Currency Over Memory**: Models deprecate in 6-12 months. Learn to find current ones via leaderboards.

**Empiricism**: Benchmarks guide; YOUR data decides. Test top 3-5 models with your prompts.

## Decision Trees

### Model Selection
```
Task type → Find relevant benchmark → Check leaderboards → Test top 3 empirically
Coding: SWE-bench | Reasoning: GPQA | General: Arena Elo
```
See: `references/model-selection.md`

### Architecture Complexity
```
1. Single LLM Call (start here - 80% stop here)
2. Sequential Calls (workflows)
3. LLM + Tools (function calling)
4. Agentic System (LLM controls flow)
5. Multi-Agent (only if truly needed)
```
See: `references/architecture-patterns.md`

### Vector Storage
```
<1M vectors → Postgres pgvector or Convex
1-50M vectors → Postgres with pgvectorscale
>50M + <10ms p99 → Dedicated (Qdrant, Weaviate)
```

## Key Optimizations

- **Prompt Caching**: 60-90% cost reduction. Static content first.
- **Structured Outputs**: Native JSON Schema. Zero parsing failures.
- **Model Routing**: Simple→cheap model, Complex→expensive model.
- **Hybrid RAG**: Vector + keyword search = 15-25% better than pure vector.

See: `references/prompt-engineering.md`, `references/production-checklist.md`

## Stack Defaults (TypeScript/Next.js)

- **SDK**: Vercel AI SDK (streaming, React hooks, provider-agnostic)
- **Provider**: OpenRouter (400+ models, easy A/B testing, fallbacks)
- **Vectors**: Postgres pgvector (95% of use cases, $20-50/month)
- **Observability**: Simple logging or Langfuse (self-hosted)

## Scripts

- `scripts/validate_llm_config.py <dir>` - Scan for LLM anti-patterns

## References

- `references/model-selection.md` - Leaderboards, search strategies, red flags
- `references/prompt-engineering.md` - Caching, structured outputs, CoT, model-specific styles
- `references/architecture-patterns.md` - Complexity ladder, RAG, tool use, caching
- `references/production-checklist.md` - Cost, errors, security, observability, evaluation
