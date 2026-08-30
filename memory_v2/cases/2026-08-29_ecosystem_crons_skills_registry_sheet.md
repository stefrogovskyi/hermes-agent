# Case: Ecosystem Crons & Skills Google Sheet Registry & Fallback Monitor Fix

**Дата:** 2026-08-29
**Домен:** `ai_infra` / `ops_infrastructure`

## Контекст
1. **Google Sheet Registry:** Стефан поставил задачу создать и ежедневно актуализировать единую Google Таблицу (`Hermes Ecosystem`) со всеми кронами и кастомными скиллами всех агентов системы.
2. **Models Tab & Timestamping:** На отдельной вкладке `Models` необходимо вести реестр доступных LLM-моделей с меткой времени последнего обновления (Киевское время).
3. **Nous API 401 & Fallback Monitor Fix:** При выполнении крона `Daily Fallback Models Health-Check & Auto-Discovery` произошел сбой из-за ошибки 401 при вызове провайдера Nous и некроссплатформенных путей в `fallback_monitor.py`.

## Решение и Результат
1. **Google Sheet Registry (`Hermes Ecosystem`):**
   - Создана таблица `Hermes Ecosystem` (ID сохранен в `ecosystem_registry_sheet.json`).
   - Заполнены вкладки с описанием всех кронов и скиллов по всем профилям агентов (Hermes, Richard, Alistair, Liz, Callum, Ben, Harrison, Archie, Aeon).
   - На вкладку `Models` добавлен выгруженный список доступных моделей с таймстампом обновления по Киеву.
   - Зарегистрирован ежедневный крон `Sync Ecosystem Crons & Skills Registry to Google Sheet` (`0 21 * * *`).

2. **Fix `fallback_monitor.py` & Nous API:**
   - Обновлен `fallback_monitor.py`: добавлена кроссплатформенная обработка путей (Windows / Linux), принудительное декодирование UTF-8 для `stdout/stderr` и правильная обработка ответов Nous API / OpenRouter.
   - Кеш моделей сохранен в `models_dev_cache.json` (43 проверенные модели).

## Ключевые Правила
- Таблицы и реестры экосистемы ведутся автоматически через Google Sheets API (`google_token.json`).
- Любые скрипты мониторинга модели/кронов обязаны использовать `Path` из `pathlib` для совместимости Windows (`Desktop-mst5pt7`) и Linux (`Servarica VPS`).
