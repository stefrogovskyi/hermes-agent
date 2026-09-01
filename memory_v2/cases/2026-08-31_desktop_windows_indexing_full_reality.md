# Case: Windows Desktop File Indexing Integration into Daily Full Reality Indexer

**Date:** 2026-08-31  
**Domain:** `ops_infrastructure`  
**Tags:** `indexer`, `tailscale`, `windows_pc`, `fts5`, `google_drive`

---

## 1. Контекст и проблема
Ежедневный скрипт полнотекстовой индексации (`/opt/hermes/scripts/daily_full_indexer.py`) индексировал только знания локального VPS (`/opt/hermes`) и облачный Google Drive, оставляя локальные файлы ПК Стефана (Windows Desktop, Документы, Загрузки) вне общего поискового индекса FTS5.

## 2. Решение (Fix)
1. В `daily_full_indexer.py` добавлено сканирование Windows-десктопа Стефана (`Stefan@100.79.157.46`) через Tailscale SSH.
2. Автоматически сканируются директории:
   - `Desktop` (Рабочий стол)
   - `Documents` (Документы)
   - `Downloads` (Загрузки)
   - `AppData/Local/hermes/skills` и `memories`
3. Поддерживаются форматы: `.pdf`, `.docx`, `.xlsx`, `.txt`, `.md`, `.py`, `.json`, `.csv`.
4. Результаты объединяются с объектами VPS и Google Drive в единой базе полнотекстового поиска SQLite FTS5 (`/opt/hermes/state/full_reality_index.db`, >26,400 записей).
5. Реализована защита от сбоев: если ПК выключен или временно недоступен по Tailscale, индексер продолжит работу без ошибок и сохранит имеющиеся данные.

## 3. Результаты
- Проиндексировано с ПК 849+ локальных файлов на первом запуске.
- Изменения зафиксированы в git (`4f92911`) и протестированы вживую.
