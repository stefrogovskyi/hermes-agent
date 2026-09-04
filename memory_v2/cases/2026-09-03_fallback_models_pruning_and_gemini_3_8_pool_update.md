# Case: Fallback Models Pool Maintenance — Tencent HY3 Removal & Gemini 3.8 Flash Audit

**Date:** 2026-09-03  
**Domain:** `ai_infra` / `ops_infrastructure`

## Context
В ночном отчете мониторинга моделей модель `tencent/hy3:free` продолжала отображаться как недоступная. Стефан запросил детальный разбор пула моделей: почему модель оставалась в списке, изменился ли размер пула бесплатных моделей и какие актуальные изменения произошли на рынке.

## Root Cause
- `tencent/hy3:free` являлась промо-моделью от Nous Research. Провайдер официально завершил бесплатный промо-период (HTTP 404: "This model's free period has ended. Please select a different model").
- В скрипте `fallback_monitor.py` модель опрашивалась для мониторинга статуса, создавая информационный шум в отчетах.

## Solution & Actions Taken
1. **Очистка пула:** Модель `tencent/hy3:free` полностью удалена из списков мониторинга `fallback_monitor.py` и активных конфигураций.
2. **Аудит рынка и обновление каталога:**
   - Зафиксированы ушедшие с бесплатного доступа модели: `tencent/hy3:free`, `mistralai/mistral-nemo`, `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free`, `z-ai/glm-5.2:free`.
   - Подтверждена интеграция флагмана Google: `google/gemini-3.8-flash`.
   - Проверены и подтверждены стабильно доступные модели в пуле Nous: `step-3.7-flash:free`, `solar-pro4:free`, `longcat-2.0:free`, `laguna-s-2.1:free`, `ling-3.0-flash-fin:free`.
3. Вкладка `Models` в реестре Google Таблицы синхронизирована с актуальными временными метками проверки по Киеву.

## Key Takeaways
- Промо-модели с истекшим сроком бесплатного использования должны оперативно вычищаться из скриптов мониторинга, чтобы не искажать статистику доступности пула.
