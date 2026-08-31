# 35-Model Fallback Cascade & 3-Tier Dynamic Routing Architecture

## Overview
A resilient, 35+ model fallback chain distributed across 7 independent providers (OpenAI, Google, Hugging Face Router, OpenRouter, Nous Portal, Mistral AI, Gonka24), integrated with an automated daily 03:00 Kyiv liveness monitor and auto-discovery daemon.

## Provider Endpoints & Authentication
1. **Google Direct:** API key in `GEMINI_API_KEY` / `GOOGLE_API_KEY`. Free tier covers 15 RPM / 1M TPM.
2. **OpenAI Direct:** API key in `OPENAI_API_KEY` (`https://api.openai.com/v1`).
3. **Hugging Face Router:** API key in `HF_TOKEN` (`https://router.huggingface.co/v1`). Registered as custom provider `huggingface` in `config.yaml`.
4. **Nous Portal:** OAuth token in `auth.json` (`providers.nous.access_token`) calling `https://inference-api.nousresearch.com/v1`.
5. **OpenRouter:** API key in `OPENROUTER_API_KEY` (`https://openrouter.ai/api/v1`). Includes `:free` pool and paid micro-billing models.
6. **Gonka24:** API key in `GONKA24_API_KEY` (`https://api.gonka24.com/v1`) for decentralized GPU compute with 204.8k context.

## 3-Tier Model Classification
- **🔴 Tier 3: Heavy Reasoning & Deep Architecture:** `deepseek-ai/DeepSeek-R1`, `claude-opus-5`, `claude-sonnet-5`, `gpt-4o`, `deepseek/deepseek-chat` (671B), `nousresearch/hermes-3-llama-3.1-405b`, `meta-llama/Llama-3.3-70B-Instruct`, `Qwen/Qwen2.5-72B-Instruct`, `nvidia/nemotron-3-super-120b-a12b:free`, `google/gemini-2.5-pro`.
- **🟡 Tier 2: Standard Workhorse:** `google/gemini-3.7-flash` (default), `google/gemini-3.6-flash`, `Qwen/Qwen2.5-Coder-32B-Instruct`, `mistralai/mistral-small-24b-instruct-2501`, `minimax-m2.7`, `kimi-k2.6`, `google/gemma-4-31b-it:free`.
- **🟢 Tier 1: Light & Free Tier:** `gpt-4o-mini`, `stepfun/step-3.7-flash:free`, `upstage/solar-pro4:free`, `tencent/hy3:free`, `meituan/longcat-2.0:free`, `poolside/laguna-s-2.1:free`, `mistralai/mistral-nemo`, `meta-llama/Llama-3.1-8B-Instruct`, `google/gemini-2.5-flash`.

## Daily Liveness & Auto-Discovery Daemon
- **Script:** `/opt/hermes/scripts/fallback_monitor.py`
- **Cron Schedule:** `0 0 * * *` UTC (03:00 AM Kyiv time).
- **Execution:** Concurrently pings all models across all 7 providers, discovers newly released `:free` models on OpenRouter & Nous Portal, removes permanently deprecated 404 models, updates `config.yaml` across all profiles, and sends a daily Telegram status report.
