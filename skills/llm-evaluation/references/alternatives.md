# Evaluation Tools Comparison

## Quick Decision Guide

| Need | Recommendation |
|------|----------------|
| Best CI/CD integration | **Promptfoo** |
| End-to-end platform | **Braintrust** |
| Open-source, research-backed | **DeepEval** |
| LangChain ecosystem | **LangSmith** |
| Unified evals + observability | **Braintrust** or **Maxim AI** |

## Tool Comparison

### Promptfoo (Recommended)

**Best for**: CI/CD integration, security testing, open-source

**Strengths**:
- GitHub Action with PR comments
- Red teaming and OWASP compliance
- CLI-first, works offline
- 100% open-source
- Comprehensive assertion library

**Weaknesses**:
- No hosted dashboard (DIY observability)
- No built-in collaboration features
- Requires more setup than hosted solutions

**Pricing**: Free (open-source)

**Setup**:
```bash
npx promptfoo@latest init
npx promptfoo@latest eval
```

### Braintrust

**Best for**: End-to-end platform (evals + observability + CI/CD)

**Strengths**:
- Production traces → eval cases with one click
- CI/CD integration with PR comments
- Built-in observability dashboard
- Team collaboration features
- Unified platform (no tool sprawl)

**Weaknesses**:
- Not open-source
- Pricing scales with usage
- Vendor lock-in potential

**Pricing**: Free tier, then usage-based

**Setup**:
```bash
npm install braintrust
npx braintrust eval
```

### DeepEval

**Best for**: Research-backed metrics, open-source

**Strengths**:
- Modular, research-backed evaluation metrics
- Strong focus on accuracy metrics
- Python-native
- Active development
- Enterprise platform (Confident AI)

**Weaknesses**:
- Python-only (no TypeScript SDK)
- Less CI/CD focused
- Smaller community than Promptfoo

**Pricing**: Open-source (paid platform: Confident AI)

**Setup**:
```bash
pip install deepeval
deepeval test run
```

### LangSmith

**Best for**: LangChain users, enterprise

**Strengths**:
- Deep LangChain integration
- Built-in tracing and observability
- Team collaboration
- Enterprise features

**Weaknesses**:
- Tied to LangChain ecosystem
- Commercial (limited free tier)
- Can be expensive at scale

**Pricing**: Free tier, then paid plans

**Setup**:
```python
from langsmith import evaluate
evaluate(my_app, data="dataset-name")
```

### Maxim AI

**Best for**: Agent systems, multi-agent evaluation

**Strengths**:
- Agent simulation and evaluation
- Full development lifecycle coverage
- Strong multi-agent support
- Experimentation features

**Weaknesses**:
- Newer platform (less proven)
- Smaller community
- Commercial

**Pricing**: Contact sales

### Arize Phoenix

**Best for**: Observability-first, open-source

**Strengths**:
- Strong observability features
- Open-source
- Good visualization
- Drift detection

**Weaknesses**:
- Less focused on CI/CD
- More observability than evaluation
- Requires more setup

**Pricing**: Open-source

## Feature Matrix

| Feature | Promptfoo | Braintrust | DeepEval | LangSmith |
|---------|-----------|------------|----------|-----------|
| Open Source | ✅ Full | ❌ | ✅ Full | ❌ |
| GitHub Action | ✅ Native | ✅ | ⚠️ DIY | ✅ |
| PR Comments | ✅ | ✅ | ❌ | ✅ |
| Red Teaming | ✅ Built-in | ⚠️ Limited | ⚠️ Limited | ⚠️ Limited |
| OWASP Compliance | ✅ | ❌ | ❌ | ❌ |
| Observability | ❌ | ✅ Built-in | ⚠️ Via Confident | ✅ Built-in |
| Team Collab | ❌ | ✅ | ⚠️ Paid | ✅ |
| Self-Hostable | ✅ | ❌ | ✅ | ❌ |
| Python SDK | ✅ | ✅ | ✅ Native | ✅ |
| TypeScript SDK | ✅ Native | ✅ | ❌ | ✅ |

## Migration Paths

### Promptfoo → Braintrust

If you need:
- Built-in observability dashboard
- Team collaboration features
- Trace → eval case workflow

### Promptfoo → DeepEval

If you need:
- Python-native tooling
- Research-backed accuracy metrics
- Confident AI enterprise features

### LangSmith → Promptfoo

If you need:
- Open-source solution
- Better CI/CD integration
- Security testing (red teaming)

## Recommendation by Use Case

**Startup / Small Team**:
- Start with Promptfoo (free, powerful)
- Add Langfuse for observability
- Graduate to Braintrust if collaboration needed

**Enterprise**:
- Braintrust or LangSmith for full platform
- Or Promptfoo + Langfuse (self-hosted) for control

**Research / Academia**:
- DeepEval for metrics
- Promptfoo for testing

**LangChain Users**:
- LangSmith if already invested
- Or Promptfoo + LangSmith for best of both

## Cost Comparison (Rough)

| Tool | Free Tier | ~10K evals/month | ~100K evals/month |
|------|-----------|------------------|-------------------|
| Promptfoo | Unlimited | $0 | $0 |
| Braintrust | 1K evals | ~$50 | ~$200 |
| DeepEval | Unlimited | $0 | $0 |
| LangSmith | 5K traces | ~$100 | ~$400 |

*Note: Costs exclude LLM API costs, which are separate.*
