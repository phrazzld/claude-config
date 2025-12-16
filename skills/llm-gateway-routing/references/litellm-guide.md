# LiteLLM Self-Hosted Guide

## Installation

```bash
# Basic install
pip install litellm

# With proxy (recommended)
pip install litellm[proxy]

# With all extras
pip install litellm[extra_proxy]
```

## Quick Start

### Command Line

```bash
# Start proxy with single model
litellm --model gpt-4o

# With config file
litellm --config config.yaml

# With specific port
litellm --config config.yaml --port 4000
```

### Docker

```dockerfile
# docker-compose.yml
version: '3.8'
services:
  litellm:
    image: ghcr.io/berriai/litellm:main-latest
    ports:
      - "4000:4000"
    volumes:
      - ./config.yaml:/app/config.yaml
    environment:
      - LITELLM_MASTER_KEY=sk-master-...
    command: --config /app/config.yaml
```

## Configuration

### Basic Config

```yaml
# config.yaml
model_list:
  # OpenAI
  - model_name: gpt-4o
    litellm_params:
      model: openai/gpt-4o
      api_key: sk-...

  # Anthropic
  - model_name: claude
    litellm_params:
      model: anthropic/claude-3-5-sonnet-latest
      api_key: sk-ant-...

  # Azure OpenAI
  - model_name: azure-gpt4
    litellm_params:
      model: azure/gpt-4
      api_base: https://your-resource.openai.azure.com
      api_key: ...
      api_version: "2024-02-15-preview"
```

### Load Balancing

```yaml
model_list:
  # Same model_name = load balanced
  - model_name: fast-model
    litellm_params:
      model: openai/gpt-4o-mini
      api_key: sk-openai-...

  - model_name: fast-model
    litellm_params:
      model: anthropic/claude-3-5-haiku
      api_key: sk-ant-...

  - model_name: fast-model
    litellm_params:
      model: google/gemini-flash-1.5
      api_key: ...

router_settings:
  routing_strategy: simple-shuffle  # or latency-based-routing
```

### Fallbacks

```yaml
model_list:
  - model_name: primary
    litellm_params:
      model: anthropic/claude-3-5-sonnet-latest

router_settings:
  fallbacks:
    primary:
      - openai/gpt-4o
      - google/gemini-pro-1.5
  num_retries: 3
  timeout: 30
```

### Cost Tracking

```yaml
litellm_settings:
  success_callback: ["langfuse"]  # Log to Langfuse
  max_budget: 100  # $100/month max
  budget_duration: monthly

general_settings:
  database_url: postgresql://user:pass@localhost/litellm
```

### Rate Limiting

```yaml
litellm_settings:
  # Global rate limits
  max_requests_per_minute: 1000
  max_tokens_per_minute: 100000

# Per-user limits
user_rate_limit:
  rpm: 60
  tpm: 10000
```

### Caching

```yaml
litellm_settings:
  cache: true
  cache_params:
    type: redis
    host: localhost
    port: 6379
    ttl: 3600  # 1 hour

# Or in-memory
litellm_settings:
  cache: true
  cache_params:
    type: local
```

### Authentication

```yaml
general_settings:
  master_key: sk-master-...  # Admin key

# Generate user keys via API
# POST /key/generate
# {
#   "models": ["gpt-4o", "claude"],
#   "max_budget": 10,
#   "duration": "30d"
# }
```

## API Usage

### Chat Completions

```bash
curl http://localhost:4000/v1/chat/completions \
  -H "Authorization: Bearer sk-master-..." \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

### Embeddings

```bash
curl http://localhost:4000/v1/embeddings \
  -H "Authorization: Bearer sk-master-..." \
  -H "Content-Type: application/json" \
  -d '{
    "model": "text-embedding-3-small",
    "input": "Hello world"
  }'
```

### Health Check

```bash
curl http://localhost:4000/health
```

### Model List

```bash
curl http://localhost:4000/v1/models \
  -H "Authorization: Bearer sk-master-..."
```

## Admin API

### Generate API Key

```bash
curl -X POST http://localhost:4000/key/generate \
  -H "Authorization: Bearer sk-master-..." \
  -H "Content-Type: application/json" \
  -d '{
    "models": ["gpt-4o", "claude"],
    "max_budget": 50,
    "duration": "30d",
    "metadata": {"user": "john@example.com"}
  }'
```

### List Keys

```bash
curl http://localhost:4000/key/list \
  -H "Authorization: Bearer sk-master-..."
```

### Delete Key

```bash
curl -X DELETE http://localhost:4000/key/delete \
  -H "Authorization: Bearer sk-master-..." \
  -d '{"keys": ["sk-user-..."]}'
```

### Get Spend

```bash
curl http://localhost:4000/spend/logs \
  -H "Authorization: Bearer sk-master-..."
```

## Python SDK

```python
from litellm import completion

# Direct call (no proxy)
response = completion(
    model="anthropic/claude-3-5-sonnet-latest",
    messages=[{"role": "user", "content": "Hello!"}]
)

# Via proxy
import openai
client = openai.OpenAI(
    base_url="http://localhost:4000",
    api_key="sk-master-..."
)
response = client.chat.completions.create(
    model="claude",  # Mapped in config
    messages=[{"role": "user", "content": "Hello!"}]
)
```

## Observability Integration

### Langfuse

```yaml
litellm_settings:
  success_callback: ["langfuse"]

environment_variables:
  LANGFUSE_PUBLIC_KEY: pk-...
  LANGFUSE_SECRET_KEY: sk-...
  LANGFUSE_HOST: https://us.cloud.langfuse.com
```

### OpenTelemetry

```yaml
litellm_settings:
  success_callback: ["otel"]

environment_variables:
  OTEL_EXPORTER_OTLP_ENDPOINT: http://localhost:4317
```

## Production Deployment

### Kubernetes

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: litellm
spec:
  replicas: 3
  template:
    spec:
      containers:
        - name: litellm
          image: ghcr.io/berriai/litellm:main-latest
          ports:
            - containerPort: 4000
          env:
            - name: LITELLM_MASTER_KEY
              valueFrom:
                secretKeyRef:
                  name: litellm-secrets
                  key: master-key
          volumeMounts:
            - name: config
              mountPath: /app/config.yaml
              subPath: config.yaml
```

### Health Checks

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 4000
  initialDelaySeconds: 10
  periodSeconds: 5

readinessProbe:
  httpGet:
    path: /health
    port: 4000
  initialDelaySeconds: 5
  periodSeconds: 3
```

## Comparison: OpenRouter vs LiteLLM

| Feature | OpenRouter | LiteLLM |
|---------|------------|---------|
| Hosting | Managed | Self-hosted |
| Setup | Instant | Requires infra |
| Cost | Per-token markup | Free (+ API costs) |
| Control | Limited | Full |
| Privacy | Data through their servers | Your servers |
| Admin | Web dashboard | API / DB |
| Caching | ❌ | ✅ Built-in |
| Rate limiting | ❌ | ✅ Built-in |

**Use OpenRouter when**: Fast setup, no infra management, okay with data routing.

**Use LiteLLM when**: Need full control, privacy requirements, complex routing, cost optimization.
