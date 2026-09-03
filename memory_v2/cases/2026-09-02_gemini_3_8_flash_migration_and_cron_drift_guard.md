# Case: Gemini 3.8 Flash Ecosystem Migration & Cron Inference Drift Guard

**Date:** 2026-09-02  
**Domain:** `ai_infra` / `agent_club`  
**Tags:** `gemini-3.8-flash`, `cron`, `drift_guard`, `archie`, `claude-sonnet-5`, `model_routing`

---

## 1. Контекст и Симптом
1. Google выпустила модель нового поколения `Gemini 3.8 Flash`. Стефан дал указание проверить доступность и активировать её как основную модель в экосистеме Hermes Stevenson.
2. После смены глобальной модели кластера на `gemini-3.8-flash` вечерний крон-джоб `853cf3c5ef02` (Daily Ecosystem Registry Sync & Evening Report) пропустил запуск с ошибкой:
   > `⚠️ Cron 'Daily Ecosystem Registry Sync & Evening Report (22:00 Kiev)' failed: Skipped to prevent unintended spend: global inference config drifted since this job was created.`
3. Возник вопрос по Archie (`@WordCraftBot`): как именно распределяются модели между интерактивным чатом и генерацией блогов.

## 2. Корень проблемы (Root Cause)
1. **Drift Guard в Hermes:** Встроенная защита `Inference Config Drift Guard` сравнивает текущую конфигурацию модели/провайдера с baseline/snapshot, зафиксированным в момент создания крон-задачи в `jobs.json`. При смене глобальной конфигурации все незапиненные задачи блокируются, чтобы защитить баланс пользователя от непредвиденных трат.
2. **Архитектура Archie:** Archie сконфигурирован для создания глубоких текстов без AI-маркеров. Для него требуется сохранять связку с `Claude Sonnet 5` (Anthropic PRO), даже когда общая экосистема работает на Gemini.

## 3. Решение (Fix)
1. **Активация Gemini 3.8 Flash:** Модель протестирована через прямой Google API и переведена в статус основной (`provider: gemini`, `model: gemini-3.8-flash`) в `/opt/hermes/config.yaml`.
2. **Преодоление Drift Guard во всех 36 кронах:**
   - Проведена тотальная ревизия всех 36 крон-задач во всех 7 файлах расписаний кластера.
   - Обновлен baseline snapshot конфигурации (`last_inference_config` / hash) для задач, использующих дефолтную модель.
   - Критические специализированные задачи явно запинены к их целевым моделям.
3. **Фиксация маршрутизации моделей для Archie:**
   - Интерактивный диалог в Telegram (@WordCraftBot): строго `Claude Sonnet 5`.
   - Крон-задачи Archie по написанию блогов: строго зафиксированы на `claude-sonnet-5`.

## 4. Урок и правило
- При глобальном изменении модели экосистемы в `config.yaml` ОБЯЗАТЕЛЬНО производить превентивный аудит и обновление snapshot конфигурации во всех файлах `jobs.json`, предотвращая сбои `drift_skip`.
- Любой агент с индивидуальными требованиями к стилистике (Archie) должен иметь явную фиксацию модели в своем `config.yaml` и в промптах крон-задач.
