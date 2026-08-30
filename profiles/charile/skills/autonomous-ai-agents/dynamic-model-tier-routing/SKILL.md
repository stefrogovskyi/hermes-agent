---
name: dynamic-model-tier-routing
description: Use to route tasks across model tiers to save tokens.
---

# Dynamic Model Tier Routing (LLM Intelligence Tier Router)

## Overview
This skill allows Hermes agents to dynamically and seamlessly select the appropriate model tier based on prompt complexity, saving API costs and tokens while providing sub-second latency for casual chats and maximum reasoning depth for complex multi-step tasks.

**Status:** Disabled by default. Only activate upon explicit user direction.

## Model Tiers & 35-Model Distribution

### 🔴 Tier 3: Heavy Reasoning & Deep Architecture (Deep Thinking, 70B-671B, Opus/Sonnet, Extended Logic)
- **Use Cases:** Архитектура систем, поиск сложных багов, аудит контрактов, тяжелая математика, оркестрация параллельных субагентов.
- **Characteristics:** Глубокая цепочка рассуждений (Extended Thinking), максимальный вес параметров (70B-671B / Opus).
- **Models:**
  1. `deepseek-ai/DeepSeek-R1` (huggingface)
  2. `claude-opus-5` (anthropic)
  3. `claude-opus-4` (anthropic)
  4. `claude-sonnet-5` (anthropic)
  5. `claude-fable-5` (anthropic)
  6. `gpt-4o` (openai)
  7. `deepseek/deepseek-chat` (openrouter)
  8. `deepseek-ai/DeepSeek-V3` (huggingface)
  9. `nousresearch/hermes-3-llama-3.1-405b` (openrouter)
  10. `meta-llama/Llama-3.3-70B-Instruct` (huggingface)
  11. `meta-llama/llama-3.3-70b-instruct` (openrouter)
  12. `nousresearch/hermes-3-llama-3.1-70b` (openrouter)
  13. `Qwen/Qwen2.5-72B-Instruct` (huggingface)
  14. `qwen/qwen-2.5-72b-instruct` (openrouter)
  15. `nvidia/nemotron-3-super-120b-a12b:free` (openrouter)

### 🟡 Tier 2: Standard Workhorse (Balanced Default, 24B-32B, Multi-turn, Coding & Research)
- **Use Cases:** Стандартная разработка, сводки, написание писем, поиск по базе знаний, анализ документов, регулярные задачи.
- **Characteristics:** Высокая точность выполнения инструкций, оптимальный баланс скорости и глубины.
- **Models:**
  1. `google/gemini-3.7-flash` (google — default)
  2. `google/gemini-2.5-pro` (google)
  3. `google/gemini-3.6-flash` (google)
  4. `Qwen/Qwen2.5-Coder-32B-Instruct` (huggingface)
  5. `mistralai/mistral-small-24b-instruct-2501` (openrouter)
  6. `minimax-m2.7` (gonka24)
  7. `kimi-k2.6` (gonka24)
  8. `google/gemma-4-31b-it:free` (openrouter)
  9. `google/gemma-4-26b-a4b-it:free` (openrouter)
  10. `minimax/minimax-m3:free` (openrouter)
  11. `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free` (openrouter)

### 🟢 Tier 1: Light & Free (Casual Chit-Chat, Quick Q&A, Short Status, Sub-second)
- **Use Cases:** Приветствия, шутки, короткие реплики, уточнение статуса, перевод простых фраз, повседневный диалог.
- **Characteristics:** Ультра-быстрый ответ (<1s), нулевое потребление дорогого контекста.
- **Models:**
  1. `gpt-4o-mini` (openai)
  2. `stepfun/step-3.7-flash:free` (nous)
  3. `upstage/solar-pro4:free` (nous)
  4. `tencent/hy3:free` (nous)
  5. `meituan/longcat-2.0:free` (nous)
  6. `poolside/laguna-s-2.1:free` (nous)
  7. `poolside/laguna-xs-2.1:free` (nous)
  8. `mistralai/mistral-nemo` (openrouter)
  9. `meta-llama/Llama-3.1-8B-Instruct` (huggingface)
  10. `google/gemini-2.5-flash` (google)

## Toggle Control
- **Activate Dynamic Routing:** User command: *"Включи динамический роутинг моделей"* / *"Активируй умный выбор моделей"*.
  - Sets `routing.dynamic_tiers: true` in agent state.
  - Dynamically routes prompt execution to the optimal tier.
- **Deactivate (Default State):** User command: *"Выключи динамический роутинг"* / *"Работай только на основной модели"*.
  - Restores fixed execution strictly on primary default model (`google/gemini-3.7-flash`).

## Classification Heuristics
1. **Length & Structure:** <15 words + no code + conversational markers -> **Tier 1 (Light/Free)**
2. **Tool / Terminal / File Tasks:** Multi-file edits, code generation, web research -> **Tier 2 (Standard Workhorse)**
3. **Reasoning Triggers:** "Спроектируй архитектуру", "глубокий аудит", "реши сложную задачу", "step-by-step math", multi-agent delegation -> **Tier 3 (Heavy Reasoning)**
