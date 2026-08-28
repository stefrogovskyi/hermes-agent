---
name: dynamic-model-tier-routing
description: Use to route tasks across model tiers to save tokens.
---

# Dynamic Model Tier Routing (LLM Intelligence Tier Router)

## Overview
This skill allows Hermes agents to dynamically and seamlessly select the appropriate model tier based on prompt complexity, saving API costs and tokens while providing sub-second latency for casual chats and maximum reasoning depth for complex multi-step tasks.

**Status:** Disabled by default. Only activate upon explicit user direction.

## Model Tiers

### 🟢 Tier 1: Light & Free Tier (Casual / Chit-Chat / Quick Q&A)
- **Use Cases:** Приветствия, шутки, короткие реплики, уточнение статуса, перевод простых фраз, повседневный диалог.
- **Characteristics:** Ультра-быстрый ответ (<1s), нулевое потребление дорогого контекста.
- **Active Models:** `google/gemini-3.6-flash`, `gpt-4o-mini`, `stepfun/step-3.7-flash:free` (Nous), `upstage/solar-pro4:free` (Nous).

### 🟡 Tier 2: Standard Tier (Balanced Default Workhorse)
- **Use Cases:** Стандартная разработка, сводки, написание писем, поиск по базе знаний, анализ документов, регулярные задачи.
- **Characteristics:** Высокая точность выполнения инструкций, оптимальный баланс скорости и глубины.
- **Active Models:** `google/gemini-3.7-flash` (Основная дефолтная модель), `deepseek/deepseek-chat`, `nousresearch/hermes-3-llama-3.1-70b`.

### 🔴 Tier 3: Heavy Reasoning & Deep Architecture Tier (Multi-Step & Complex Logic)
- **Use Cases:** Архитектура систем, поиск сложных багов, аудит контрактов, тяжелая математика, оркестрация параллельных субагентов.
- **Characteristics:** Глубокая цепочка рассуждений (Extended Thinking), максимальный вес параметров (70B-671B / Opus).
- **Active Models:** `deepseek-ai/DeepSeek-R1`, `claude-sonnet-5` / `claude-opus-5` (Anthropic), `gpt-4o` (OpenAI), `nousresearch/hermes-3-llama-3.1-405b`.

## Toggle Control
- **Activate Dynamic Routing:** User command: *"Включи динамический роутинг моделей"* / *"Активируй умный выбор моделей"*.
  - Sets `routing.dynamic_tiers: true` in agent state.
  - Dynamically routes prompt execution to the optimal tier.
- **Deactivate (Default State):** User command: *"Выключи динамический роутинг"* / *"Работай только на основной модели"*.
  - Restores fixed execution strictly on primary default model (`google/gemini-3.7-flash`).

## Classification Heuristics
1. **Length & Structure:** <15 words + no code + conversational markers -> **Tier 1 (Light/Free)**
2. **Tool / Terminal / File Tasks:** Multi-file edits, code generation, web research -> **Tier 2 (Standard Gemini 3.7)**
3. **Reasoning Triggers:** "Спроектируй архитектуру", "глубокий аудит", "реши сложную задачу", "step-by-step math", multi-agent delegation -> **Tier 3 (Reasoning/R1/Sonnet/Opus)**
