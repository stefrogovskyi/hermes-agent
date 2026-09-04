# Case: OpenClaw 2.0 Nous Research Provider Integration & Auth Recovery

**Date:** 2026-09-03  
**Domain:** `agent_club` / `ai_infra` / `ops_infrastructure`

## Context
Клоу Стивенсон (`@clawstevensonbot` / OpenClaw 2.0) начал сыпать 5 критических ошибок:
1. `nous/upstage/solar-pro4:free` → ❌ нет провайдера nous
2. `nous/meituan/longcat-2.0:free` → ❌ нет провайдера nous
3. `nous/poolside/laguna-s-2.1:free` → ❌ нет провайдера nous
4. `openrouter/nvidia/nemotron...` → ❌ 429 Rate limit exceeded
5. `openrouter/minimax/minimax-m3:free` → ❌ 400 Context Length / Timeout 45s

Стефан обратил внимание, что у нас активна подписка Nous Research, и OpenClaw обязан иметь полноценный доступ ко всем моделям Nous наравне с остальными агентами кластера.

## Root Cause
- В OpenClaw 2.0 провайдер Nous не был зарегистрирован в `openclaw.json` и локальной базе авторизации `openclaw-agent.sqlite`. Запросы с префиксом `nous/` сразу отклонялись как неизвестный провайдер.
- Использовался устаревший временный `agent_key`, возвращавший HTTP 401 Unauthorized, в то время как основной портальный токен подписки (`access_token`) был 100% активен и отдавал HTTP 200 OK.
- Бесплатный шлюз OpenRouter перегружался дневными квотами (429) и не справлялся с длинным контекстом промпта на Minimax (400).

## Solution & Architecture
1. **Регистрация провайдера Nous:** Добавлен провайдер `nous` с валидным базовым URL и актуальным портальным токеном подписки в конфигурацию OpenClaw.
2. **Фолбэк-цепочка:** Обновлена цепочка фолбэков OpenClaw с приоритетом прямого доступа к проверенным моделям подписки Nous (`step-3.7-flash:free`, `solar-pro4:free`, `longcat-2.0:free`, `laguna-s-2.1:free`, `ling-3.0-flash-fin:free`).
3. **Валидация и перезапуск:** Конфигурация проверена через `openclaw config validate`, сервис `openclaw.service` перезапущен, проверен статус каналов (`openclaw channels status` — Telegram: connected, running).

## Key Takeaways
- Все агенты экосистемы должны использовать единый активный токен подписки Nous Research.
- При появлении ошибок «нет провайдера» в OpenClaw необходимо проверять регистрацию в `openclaw.json` и sqlite-хранилище профилей авторизации.
