---
name: openclaw-gateway
description: Use when configuring OpenClaw gateways, models and bots.
---

# OpenClaw Gateway Orchestration

OpenClaw is a lightweight TypeScript/Node.js multi-channel AI gateway and autonomous agent daemon created by Peter Steinberger.

## 1. Core Architecture & Files
- **App Directory:** `/opt/openclaw/app` (git repo `openclaw/openclaw`)
- **CLI Executable:** `/usr/local/bin/openclaw` -> `/opt/openclaw/app/dist/entry.js`
- **Configuration:** `~/.openclaw/openclaw.json` (validated via `openclaw config validate`)
- **Auth Profiles:** `~/.openclaw/auth/auth-profiles.json`
- **Systemd Unit:** `/etc/systemd/system/openclaw.service` (port 18789 loopback)

## 2. Telegram Pairing & Approval Flow
When OpenClaw receives a message from an unauthenticated user, it requires pairing approval:
```bash
# Approve pairing for user ID
openclaw pairing approve telegram <PAIRING_CODE>
```
This registers the sender ID in `commands.ownerAllowFrom` in `openclaw.json`.

## 3. Model Fallback Pipeline & Low-Latency Tuning
To avoid rate limits (429) or token authentication errors (401) without hanging:
1. **Primary & Fallbacks Schema:**
   In `~/.openclaw/openclaw.json`:
   ```json
   {
     "agents": {
       "defaults": {
         "model": {
           "primary": "openrouter/nvidia/nemotron-3.5-lightning:free",
           "fallbacks": [
             "openrouter/nvidia/nemotron-3-nano-30b-a3b:free",
             "openrouter/google/gemma-4-26b-a4b-it:free",
             "openrouter/google/gemma-4-31b-it:free",
             "openrouter/poolside/laguna-s-2.1:free",
             "openrouter/openai/gpt-oss-20b:free",
             "huggingface/meta-llama/Llama-3.3-70B-Instruct",
             "huggingface/Qwen/Qwen2.5-72B-Instruct",
             "nvidia/nvidia/nemotron-3.5-lightning-30b-a3b",
             "nvidia/nvidia/llama-3.3-nemotron-super-49b-v1.5",
             "nvidia/nvidia/nemotron-3-super-120b-a12b",
             "nvidia/nvidia/nemotron-mini-4b-instruct",
             "nvidia/meta/llama-3.1-8b-instruct",
             "gonka24/deepseek-v4-flash-0731",
             "gonka24/kimi-k2.6",
             "gonka24/minimax-m2.7"
           ]
         },
         "models": {
           "openrouter/nvidia/nemotron-3.5-lightning:free": {},
           "huggingface/meta-llama/Llama-3.3-70B-Instruct": {},
           "nvidia/nvidia/nemotron-3.5-lightning-30b-a3b": {},
           "gonka24/deepseek-v4-flash-0731": {}
         },
         "timeoutSeconds": 10
       }
     },
     "models": {
       "providers": {
         "openrouter": {
           "timeoutSeconds": 6
         },
         "huggingface": {
           "baseUrl": "https://router.huggingface.co/v1",
           "timeoutSeconds": 8
         },
         "nvidia": {
           "baseUrl": "https://integrate.api.nvidia.com/v1",
           "timeoutSeconds": 8
         },
         "gonka24": {
           "baseUrl": "https://api.gonka24.com/v1",
           "timeoutSeconds": 8,
           "models": [
             {"id": "deepseek-v4-flash-0731", "name": "DeepSeek V4 Flash"},
             {"id": "kimi-k2.6", "name": "Kimi K2.6"},
             {"id": "minimax-m2.7", "name": "MiniMax M2.7"}
           ]
         }
       }
     }
   }
   ```
2. **Provider Key Ingestion & Auth Profiles:**
   Ensure environment variables (`OPENROUTER_API_KEY`, `HF_TOKEN`/`HUGGINGFACE_API_KEY`, `NVIDIA_API_KEY`, `GONKA24_API_KEY`) are injected into systemd unit `openclaw.service`, `/opt/hermes/.env`, and `~/.openclaw/auth/auth-profiles.json`.
   Note: OpenClaw CLI strictly requires custom OpenAI-compatible providers (like `gonka24`) to explicitly declare a `models: [{id, name}]` array inside `models.providers.<name>`, otherwise schema validation fails. Custom top-level keys like `env: {}` or misplaced `fallbacks` are rejected — always structure them within `model: { primary, fallbacks: [] }` and `models: { ... }`.

## 4. Diagnostics & Verification
- `openclaw gateway health` — Check gateway response time.
- `openclaw channels status` — Check Telegram polling connection.
- `journalctl -u openclaw -n 25 --no-pager` — Monitor live inbound/outbound event logs.
