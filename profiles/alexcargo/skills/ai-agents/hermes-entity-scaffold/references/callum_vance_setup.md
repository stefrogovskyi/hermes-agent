# Callum Vance & Proactive Agent Loop Setup (2026-07-30)

## 1. Entity Overview
- **Name:** Callum Vance
- **Role:** Full-Stack Engineer — Navo Sites & Platforms
- **Telegram Bot:** `@callumvancebot` (`8548593141:AAHAHrhnwMl-EynwjmzH3a3YYlWC88xH4JM`)
- **Folder:** `C:\Users\Stefan\My Drive\Equity\My Biz\My companies\Enlight Group\Enlight Board\Callum Vance\Callum Vance Hermes\`
- **Supervised Platforms:** `navo24.com`, `trackingmcp.com`, `schedulesmcp.com`, `loadingmcp.com`, `freightratesmcp.com`

## 2. Access Control Policy
- `CALLUM_ADMIN_IDS = "330656040,1022586369"`
- **Stefan Rogovskiy** (`330656040`): Owner
- **Tech Lead Алексей** (`1022586369`): Authorized Dev/Lead
- **Orchestrator Hermes Stevenson**: Dispatcher
- Guest/team users can ask questions and discuss Navo platforms, but official development orders, code changes, and execution tasks are accepted ONLY from Stefan, Tech Lead Алексей, or Orchestrator.

## 3. Runtime Features
- **Streaming Typing Indicator:** `_TypingTicker` background thread sends `sendChatAction(chat_id, "typing")` every 4s while LLM generation is running.
- **Output Cleaning:** `clean_model_output` strips raw pseudo-XML `<tool_call>...</tool_call>` or `<function=...>` if models output raw string tags.
- **409 Self-Heal:** On `HTTP Error 409: Conflict`, logs duplicate detection and exits cleanly (`sys.exit(0)`), leaving single active long-poll instance.
- **tg_send_message Chunking:** Splitting >4000 char messages with 3 retries and automatic fallback to plain text if Markdown fails.

## 4. Master Indexer & FTS5 Reality Database
- **Script:** `C:\Users\Stefan\AppData\Local\hermes\indexer\master_indexer.py`
- **Database:** `C:\Users\Stefan\AppData\Local\hermes\indexer\index_database.db`
- **Coverage:** 58,633 total files scanned; 15,183 text/DOCX/PDF/code files extracted into SQLite FTS5 index (290,458,107 characters).
- **Knowledge Synthesis:** `C:\Users\Stefan\AppData\Local\hermes\indexer\knowledge_graph.md`.
