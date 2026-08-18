# Case: SQLite WAL Mode Transition & Interrupted Turn Recovery

- **Дата:** 2026-08-04
- **Домен:** memory_systems
- **Симптом:** Падение `session storage could not be written (the transcript would have been lost on restart)` и блокировка `state.db` («database is locked»). В `crash_journal.json` зафиксировано прерывание хода.
- **Гипотеза:** Стандартный режим журнала SQLite (delete/rollback) блокировал всю базу данных на чтение и запись при одновременных обращениях от шлюза, процессов ботов и фоновых крон-задач.
- **Корень:** Множественные независимые процессы Hermes (Gateway, Watchdogs, Cron) обращались к `state.db` без WAL и с низким `busy_timeout`.
- **Фикс:**
  1. Все 19 файлов баз данных SQLite в директории `AppData\Local\hermes\` переведены в режим WAL (`PRAGMA journal_mode=WAL;`) с `PRAGMA busy_timeout=10000;`.
  2. Создан механизм `hermes_turn_recovery.py` и статус `IN_FLIGHT` в `session_state.json`, фиксирующий начало хода и автоматически восстанавливающий незавершенные задачи при перезапуске системы.
- **Рефлексия:** Для всех SQLite баз данных мультипроцессного агента режим WAL и `busy_timeout >= 10s` являются обязательным стандартом архитектуры.
