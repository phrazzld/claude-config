# CI/CD Integration Guide

## GitHub Actions

### Basic Setup

```yaml
# .github/workflows/llm-eval.yml
name: 'LLM Evaluation'

on:
  pull_request:
    paths:
      - 'prompts/**'
      - 'src/**/*prompt*'
      - 'promptfooconfig.yaml'

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

      - name: Cache Promptfoo
        uses: actions/cache@v4
        with:
          path: ~/.promptfoo
          key: ${{ runner.os }}-promptfoo-${{ hashFiles('promptfooconfig.yaml') }}

      - name: Run Evaluation
        uses: promptfoo/promptfoo-action@v1
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          OPENROUTER_API_KEY: ${{ secrets.OPENROUTER_API_KEY }}
```

### With Before/After Comparison

```yaml
jobs:
  evaluate:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Need full history for comparison

      - uses: actions/setup-node@v4
        with:
          node-version: '20'

      # Evaluate current branch
      - name: Evaluate PR
        run: npx promptfoo@latest eval -o pr-results.json
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}

      # Evaluate base branch
      - name: Checkout base
        run: git checkout ${{ github.base_ref }}

      - name: Evaluate Base
        run: npx promptfoo@latest eval -o base-results.json
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}

      # Compare results
      - name: Compare
        run: npx promptfoo@latest diff base-results.json pr-results.json > comparison.md

      - name: Comment PR
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const comparison = fs.readFileSync('comparison.md', 'utf8');
            github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: `## LLM Evaluation Results\n\n${comparison}`
            });
```

### Quality Gate (Fail on Regression)

```yaml
jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Evaluation
        run: npx promptfoo@latest eval -o results.json
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}

      - name: Check Results
        run: |
          FAILURES=$(jq '.results.stats.failures' results.json)
          if [ "$FAILURES" -gt 0 ]; then
            echo "❌ $FAILURES test(s) failed!"
            jq '.results.results[] | select(.success == false)' results.json
            exit 1
          fi
          echo "✅ All tests passed!"
```

### Security Scan

```yaml
name: 'LLM Security Scan'

on:
  pull_request:
    paths: ['prompts/**']
  schedule:
    - cron: '0 0 * * 0'  # Weekly

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Red Team Scan
        run: npx promptfoo@latest redteam run
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}

      - name: Generate Report
        run: npx promptfoo@latest redteam report --output security-report.html

      - name: Upload Report
        uses: actions/upload-artifact@v4
        with:
          name: security-report
          path: security-report.html
```

## GitLab CI

```yaml
# .gitlab-ci.yml
llm-evaluation:
  image: node:20
  stage: test
  script:
    - npx promptfoo@latest eval -o results.json
    - |
      FAILURES=$(jq '.results.stats.failures' results.json)
      if [ "$FAILURES" -gt 0 ]; then
        exit 1
      fi
  artifacts:
    reports:
      junit: results.xml
    paths:
      - results.json
  only:
    changes:
      - prompts/**
      - promptfooconfig.yaml
```

## Azure Pipelines

```yaml
# azure-pipelines.yml
trigger:
  paths:
    include:
      - prompts/*
      - promptfooconfig.yaml

pool:
  vmImage: 'ubuntu-latest'

steps:
  - task: NodeTool@0
    inputs:
      versionSpec: '20.x'

  - script: npx promptfoo@latest eval -o results.json
    displayName: 'Run LLM Evaluation'
    env:
      OPENAI_API_KEY: $(OPENAI_API_KEY)

  - script: |
      FAILURES=$(jq '.results.stats.failures' results.json)
      if [ "$FAILURES" -gt 0 ]; then
        echo "##vso[task.complete result=Failed;]Tests failed"
      fi
    displayName: 'Check Results'
```

## Quality Gate Patterns

### Minimum Pass Rate

```yaml
# promptfooconfig.yaml
evaluateOptions:
  threshold: 0.9  # 90% pass rate required
```

### Critical Tests

```yaml
tests:
  - description: "Critical - Auth flow"
    vars: { ... }
    assert: [ ... ]
    options:
      critical: true  # Fail entire suite if this fails
```

### Cost Budget

```yaml
evaluateOptions:
  maxCost: 1.00  # Max $1 per evaluation run
```

### Timeout

```yaml
evaluateOptions:
  timeout: 300000  # 5 minute timeout per test
```

## Secrets Management

### GitHub Secrets

1. Go to repo Settings → Secrets and variables → Actions
2. Add secrets:
   - `OPENAI_API_KEY`
   - `ANTHROPIC_API_KEY`
   - `OPENROUTER_API_KEY`

### Environment-Specific

```yaml
jobs:
  evaluate:
    environment: production  # Use production secrets
    steps:
      - run: npx promptfoo@latest eval
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY_PROD }}
```

## Caching Strategies

### GitHub Actions Cache

```yaml
- uses: actions/cache@v4
  with:
    path: |
      ~/.promptfoo
      node_modules/.cache/promptfoo
    key: ${{ runner.os }}-promptfoo-${{ hashFiles('promptfooconfig.yaml') }}
    restore-keys: |
      ${{ runner.os }}-promptfoo-
```

### Self-Hosted Runner with Redis

```yaml
evaluateOptions:
  cache: true
  cacheType: redis
  cacheRedisUrl: redis://localhost:6379
```

## Notification Patterns

### Slack Notification on Failure

```yaml
- name: Notify Slack
  if: failure()
  uses: slackapi/slack-github-action@v1
  with:
    payload: |
      {
        "text": "❌ LLM Evaluation Failed in ${{ github.repository }}",
        "blocks": [
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "PR: ${{ github.event.pull_request.html_url }}"
            }
          }
        ]
      }
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

## Matrix Testing

### Multiple Models

```yaml
jobs:
  evaluate:
    strategy:
      matrix:
        model: [gpt-4o-mini, claude-3-5-haiku, gemini-flash]
    steps:
      - run: npx promptfoo@latest eval --provider ${{ matrix.model }}
```

### Multiple Prompt Versions

```yaml
jobs:
  evaluate:
    strategy:
      matrix:
        prompt: [v1, v2, v3]
    steps:
      - run: npx promptfoo@latest eval --prompts prompts/${{ matrix.prompt }}.txt
```
