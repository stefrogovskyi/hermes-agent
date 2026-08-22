# Memory V2 Index — Hermes Long-Term Memory

Архитектура: подробные кейсы лежат в `cases/`, жёсткие правила в `principles/`.
При необходимости — читать ТОЛЬКО нужный case-файл (по индексу), не всю память целиком.
Старый `memory` tool (лимит 2200 симв) — только для кратких указателей на эту систему.

## Principles (жёсткие правила)
- `principles/00_hypothesis_fact.md` — гипотезу сначала ФАКТ, потом правка кода.
- `principles/01_self_recovery.md` — автономная фиксация+доделывание при падениях.
- `principles/02_windows_silent_automation.md` — фоновые процессы на Windows через `pythonw.exe` + `CREATE_NO_WINDOW` (0x08000000) + VBScript.

## Cases
| Дата | Тема | Файл | Ключевой урок |
| 2026-08-21 | Callum & Ben Frontend Deployments, SPA Routing & Enterprise AI Sales Showcase | cases/2026-08-21_callum_ben_frontend_routing_and_ai_sales_agent.md | Callum: 5-я вкладка поиска статей в блог-редакторе, рендеринг иконок и SPA-роутинг без 404 на staging; Ben: деплой промо-блока AI Sales Agent на Hostinger и стилизация меню. |
| 2026-08-19 | AgentOS Mission Control Upgrade & Kanban Unification | cases/2026-08-19_agentos_mission_control_upgrade_and_kanban_unification.md | Все 6 канбанов размещены на Vercel (`https://<agent>-kanban.vercel.app`), иконка Канбан исправлена на Lucide `kanban`, `server.py` использует `ReusableTCPServer`. |
| 2026-08-19 | Git Autosync & GitHub Push Protection Fix | cases/2026-08-19_git_autosync_github_push_protection_bypass.md | GitHub Push Protection блокирует пуш при обнаружении секретов в истории коммитов; расписание крона обновлено на `0 0 * * *` (03:00 Киев). |
| 2026-08-19 | Firecrawl PDF Inspector Skill Integration | cases/2026-08-19_firecrawl_pdf_inspector_skill_integration.md | Подключена библиотека Firecrawl `pdf-inspector` для классификации и OCR PDF; создан CLI обертка `pdf_inspect_cli.py` и скилл `productivity/pdf-inspector`. |
| 2026-08-18 | Cron Duplication on Desktop Wake & Explicit LLM Model Pinning | cases/2026-08-18_cron_duplicate_desktop_wake_and_model_pinning.md | Фоновые кроны 24/7 строго на VPS `stefan1`; все LLM-кроны обязан принудительно пинить к явной модели (`model: ...`) в конфигурации, чтобы предотвратить сбои при глобальной смене модели. |
| 2026-08-18 | Archie 4-Layer Anti-AI Copywriting, Audit & Point-Patch Pipeline | cases/2026-08-18_archie_4_layer_anti_ai_copywriting_and_audit.md | 3-этапный цикл Archie: глубокий человечный рерайт -> независимый 4-слойный аудит (плагиат n-gram >=6, AI-слова, структурные тики, факты) -> точечный патч замечаний. |
| 2026-08-16 | Odessa Safe Router & Telethon Userbot Session Watchdog | cases/2026-08-16_odessa_safe_router_and_telethon_userbot.md | Скилл `odessa-safe-router` сканирует группу «Не повредит, Одесса» через Telethon (`stefan_userbot.session`); добавлен крон-вахтёр (`0 */6 * * *`) с автобэкапом и алертом. |
| 2026-08-16 | Archie Anthropic PRO Auth & Anti-AI Copywriting Standard | cases/2026-08-16_archie_anti_ai_copywriting_and_anthropic_pro_auth.md | Подключение Anthropic PRO подписки (sk-ant...), 8-шаговый алгоритм копирайтинга с 10 Anti-AI правилами и 4-слойным независимым аудитом субагентом. |
| 2026-08-15 | Archie Bot VPS Service Location and Unpinned Cron Drift Skip Error | cases/archie_bot_vps_service_and_cron_drift_skip.md | Telegram bot Archie (@archiewrightbot) runs as hermes-archie.service on VPS stefan1, not on local Windows PC. Unpinned cron jobs crash with drift_skip when global config changes provider/model. |
| 2026-08-14 | Gemini 3.6 Flash 400 INVALID_ARGUMENT from interrupted turns missing functionResponse | cases/2026-08-13_gemini_role_alternation_400_sanitizer.md | Auto-synthesize dummy functionResponse in _sanitize_gemini_contents when model functionCall is followed by user turn or interrupted. |
| 2026-08-14 | Telegram 409 Conflict due to Windows Startup VBS autostart & local audit auto-spawning local gateways | cases/2026-08-13_dual_polling_409_windows_autostart_and_cloud_audit.md | Servarica VPS is sole 24/7 gateway host; local Windows autostart VBS/LNK scripts removed & audit script forced Cloud-First. |
| 2026-08-12 | Gemini-3.6-Flash Multi-Profile Sync & Sub-Agent Command Approval Loop | cases/2026-08-12_gemini_model_sync_and_subagent_approval_loop.md | Синхронизация Gemini-3.6-flash на всех 6 профилях; зафиксирована turn-scoped работа фолбэков (авто-возврат на Gemini каждый ход) и правило работы ботов в Telegram-группах. |
| 2026-08-11 | Richard HTML Email Signature Restoration & Formatting Rule | cases/richard_email_signature_formatting.md | Использовать утвержденный HTML-шаблон подписи с логотипом для Rich@navo24.com; НЕ добавлять горизонтальную черту (<hr>) перед подписью (запрет самодеятельности от Стефана). |
|------|------|------|---------------|
| 2026-07-28 | Richard 403 / Hypothesis-vs-Fact failure | cases/2026-07-28_richard_403_hypothesis_failure.md | Не путать urllib-403 с битым ключом; Hermes ходит через OpenAI SDK, не urllib. |
| 2026-07-28 | Pinecone vector memory activated | cases/2026-07-28_pinecone_activated.md | embeddings через OpenRouter (free), не Nous; в pinecone_*.py нужен `from pathlib import Path`. |
| 2026-07-28 | Session crash (state.db) + missed self-recovery | cases/2026-07-28_session_crash_self_recovery.md | При падении — сразу зафиксировать+доделать, не ждать Стефана. |
| 2026-07-30 | Callum Vance launch & Telegram formatting fallback | cases/2026-07-30_callum_vance_tg_formatting_fallback.md | tg_send_message с чанкованием по 4000 символов и фолбэком с Markdown на plain text. |
| 2026-07-30 | Alistair bot 403 / raw urllib vs OpenAI SDK | cases/2026-07-30_alistair_403_urllib_sdk.md | Боты должны использовать OpenAI SDK + Fallback Chain, не сырой urllib. |
| 2026-07-30 | Google Workspace & Drive Master Indexer | cases/2026-07-30_gworkspace_master_indexer.md | Drive API выгружает тексты cloud-доков; master_indexer сканирует локальные диски C:\ и G:\. |
| 2026-07-30 | Microsoft 365 domain navo24.com verification | cases/2026-07-30_ms365_domain_navo24_verification.md | Для импорта пользователей в MS365 домен должен быть подтверждён через DNS TXT. |
| 2026-07-31 | Session storage write error & busy input mode | cases/2026-07-31_session_storage_write_error.md | Переключить busy_input_mode на steer; проверить таймауты и state.db при сбоях генерации. |
| 2026-07-31 | Alistair tasktracker & Google OAuth recovery | cases/2026-07-31_alistair_tasktracker_google_oauth.md | Проверить TASKTRACKER_BACKEND, формат ID для LLM и OAuth токены при интеграции ботов с Google Sheets. |
| 2026-08-01 | Individual agent voices & OpenAI STT/TTS | cases/2026-08-01_agent_individual_voices_stt_tts.md | Индивидуальные голоса ботов (onyx, fable, nova, ash, alloy); отправка голосовых сообщений в Telegram требует .ogg Opus через sendVoice из токена соответствующего бота. |
| 2026-08-01 | SeaRates vs TrackingMCP benchmark & Excel reports | cases/2026-08-01_searates_trackingmcp_benchmark_excel.md | Автоматизация 3-дневного сравнения API с выгрузкой многовкладочных Excel-отчетов (openpyxl) и отправкой файлов в Telegram через tg_send_document. |
| 2026-08-01 | Google Workspace & Daily Indexer differential sync | cases/2026-08-01_gworkspace_differential_indexer.md | Дифференциальная фильтрация файлов по mtime / Drive API modifiedTime сокращает время индексации с >60с до <2с. |
| 2026-08-02 | Windows Silent Background Watchdog & VBS | cases/2026-08-02_windows_silent_background_watchdog_vbs.md | Использовать `pythonw.exe`, `CREATE_NO_WINDOW` (0x08000000) и VBScript для автозапуска фоновых процессов на Windows без черных окон. |
| 2026-08-02 | Navo24 Autonomous 24/7 Growth Engine & OODA | cases/2026-08-02_navo_247_growth_engine_ooda.md | Создание структуры `navo_growth/` (STRATEGY, HYPOTHESES_LOG, SYSTEM_PROMPT) и cron-скрипта OODA цикла для автономного роста. |
| 2026-08-02 | Alistair Roster Sync & Model Upgrade | cases/2026-08-02_alistair_roster_and_model_upgrade.md | Апгрейд модели Алистера до `google/gemma-4-31b-it:free` для ликвидации галлюцинаций имён; актуализация ролей (COO Stefan, Evgeny Karavan). |
| 2026-08-02 | Desktop Reorganization & Parallel Whisper Chunks | cases/2026-08-02_desktop_drive_reorganization_whisper_chunks.md | Сортировка Desktop с синхронизацией в Google Drive; нарезка длинных аудио на 3-мин куски перед Whisper API для исключения таймаутов. |
| 2026-08-03 | Richard Marlowe MS Graph Email & HITL Approval | cases/2026-08-03_richard_ms_graph_hitl_email.md | MS Graph OAuth integration для rich@navo24.com; 0 авто-отправок (HITL черновик в Telegram); сохранение In-Reply-To/References/Reply-To. |
| 2026-08-03 | Bot Watchdog Real LLM E2E Verification | cases/2026-08-03_bot_watchdog_real_llm_test.md | Проверка всех 5 ботов через генерацию ответа от реальной LLM модели в bot_watchdog.py, а не просто HTTP getUpdates. |
| 2026-08-03 | Navo24 PPTX Presentation & Design System | cases/2026-08-03_navo24_pptx_presentation_design_system.md | Генерация PPTX из Excel (Для презентации.xlsx) с адаптивной версткой таблицы и фиксом обрезки чисел. |
| 2026-08-03 | MS To-Do Integration via Make.com Webhook | cases/2026-08-03_ms_todo_make_webhook_integration.md | Подключение личного аккаунта MS To-Do (supremo@i.ua) через OAuth middleware вебхук в Make.com. |
| 2026-08-03 | YouTube Watch Later Full List Sorting | cases/2026-08-03_youtube_watch_later_full_list_sorting.md | Снятие искусственного лимита в 10 элементов и пакетная сортировка списка Watch Later в QuickWatch. |
| 2026-08-04 | Richard Telegram Bot Stability & Draft Cleaner | cases/2026-08-04_richard_typing_ticker_and_draft_cleaner.md | Исправление ошибки `_TypingTicker`, внедрение `_clean_draft_body_text()`, авто-CC sales@navo24.com и таймаут-ретраи 429. |
| 2026-08-04 | Oracle Cloud OCI SDK & Always Free Autoregger | cases/2026-08-04_oracle_cloud_oci_sdk_autoregger.md | Настройка `~/.oci/config`, проверка RSA fingerprint и запуск автономного 24/7 сканера Ampere A1 ARM инстансов под pythonw.exe. |
| 2026-08-04 | SQLite WAL Mode Transition & Interrupted Turn Recovery | cases/2026-08-04_sqlite_wal_mode_and_turn_recovery.md | Перевод всех 19 БД SQLite в режим WAL (`busy_timeout=10s`) и внедрение `hermes_turn_recovery.py` с авто-восстановлением ходов. |
| 2026-08-04 | Avalanche Agency Redesign Vite Build & Surge Staging Deployment | cases/2026-08-04_avalanche_surge_staging_vite_deploy.md | Сборка React/Vite приложения, создание `200.html` для роутинга на Surge.sh, авто-детекция языка по IP и RTL поддержка. |
| 2026-08-05 | Richard Sub-Bot Token Isolation & Watchdog Validation | cases/2026-08-05_richard_token_isolation_and_bot_watchdog_preflight.md | Токены субагентов строго изолированы; `bot_watchdog.py` делает preflight проверку `bot_id` перед запуском. |
| 2026-08-05 | Hostinger Multi-Environment Deployment & i18n Mirroring | cases/2026-08-05_hostinger_multi_env_deployment_and_i18n_mirroring.md | Деплой dev/staging на Hostinger (`82.29.199.155:65002`); корень `/` (англ) — единый источник правды; 8 языковых подпапок зеркалируются с `200.html`. |
| 2026-08-06 | Sub-Bots Hermes Profile Migration, Group Mention Policy & System Reorganization | cases/2026-08-06_all_bots_hermes_profiles_and_group_mode.md | Конвертация 5 субагентов в постоянные Hermes-профили; единый репо/провайдеры; настройка режима `@mention` в группах; очистка зомби-процессов и папок. |
| 2026-08-07 | User Account Impersonation Prohibition & DP World Isolation | cases/2026-08-07_user_account_impersonation_and_dpworld_isolation.md | Ни один агент не пишет от аккаунта Стефана; вакансии DP World слать только от Hermes в ЛС. |
| 2026-08-07 | Hermes Agent Update Git Stash & Sub-Bot Group Pairing | cases/2026-08-07_hermes_update_git_stash_and_alistair_pairing.md | Авто-stash локальных файлов перед git pull в desktop апдейте; разрешение ID команды в telegram-approved.json. |
| 2026-08-08 | Standalone Interactive Vercel Kanban Board per Profile | cases/2026-08-08_standalone_profile_vercel_kanban.md | Канбан каждого профиля ИЗОЛИРОВАН и автономен на Vercel (`hermes-stevenson-kanban.vercel.app` / `/api/kanban`); Escape слушатель, детали и комментарии в модалке. |
| 2026-08-08 | Sub-Bot Gateway Auto-Relaunch (Ben) & Live Streaming | cases/2026-08-08_subbot_gateway_relaunch_and_live_streaming.md | При упавшем gateway процессинге релавончить процесс субагента через `hermes.exe --profile <name> gateway run`; включить live output streaming в Telegram. |

## How to use
1. При новой задаче — глянуть index, найти релевантный case.
2. Прочитать только этот файл (через read_file, не весь memory_v2).
3. После решения — дописать новый case + обновить index.
4. Старый `memory` tool — только краткие pointer'ы («см. memory_v2/index.md»), чтобы не упираться в лимит.
