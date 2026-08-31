# Gonka AI / Gonka24 Broker Integration Notes

## Overview
Gonka AI (`gonka.ai`) is a decentralized AI inference protocol that aggregates GPU compute power (H100, A100, RTX 4090) across independent nodes to run open-source SOTA LLMs.

## Gonka24 Broker Details (`gonka24.com`)
- **API Endpoint:** `https://api.gonka24.com/v1`
- **Authentication:** `Authorization: Bearer GONKA24_API_KEY` (env variable `GONKA24_API_KEY` in `.env`)
- **OpenAI Compatibility:** 100% compliant with standard `chat.completions` and `tools` (Function Calling).

## Models Catalog (as of August 2026)
1. **`minimax-m2.7`**
   - Context Window: 204,800 tokens
   - Max Output Tokens: 16,384 tokens
   - Verified Response Latency: ~11.9s on cold start
2. **`kimi-k2.6`**
   - Context Window: 204,800 tokens
   - Max Output Tokens: 16,384 tokens

## Hermes `config.yaml` Wire
```yaml
model:
  providers:
    gonka24:
      api_key_env: GONKA24_API_KEY
      base_url: https://api.gonka24.com/v1
      models:
        - minimax-m2.7
        - kimi-k2.6

fallback_providers:
  - model: poolside/laguna-s-2.1:free
    provider: nous
  - model: google/gemma-4-31b-it:free
    provider: openrouter
  - model: minimax-m2.7
    provider: gonka24
  - model: kimi-k2.6
    provider: gonka24
```
