---
name: fact-first-operating
description: "Verify facts; self-verify bots; self-recover on failure."
---

# Fact-First Operating Principles (Stefan, 2026-07-28)

Non-negotiable working rules. They exist because Stefan caught Hermes acting on a
guessed hypothesis instead of a verified fact — which would have propagated false
assumptions into the whole agent architecture.

## HARD RULE 00 — Hypothesis MUST be confirmed by FACT before acting
- ANY hypothesis → FIRST confirm with a concrete FACT: a real API call, a real log
  line, or the agent's/bot's actual response. NOT a static test that doesn't
  replicate the runtime path, and NEVER a guess presented as truth.
- Do NOT start editing code / "fixing" until the root cause is verified by fact.
- Check all real storage locations: when looking for agent identities or files, inspect synced Google Drive paths (`C:\Users\Stefan\My Drive\...`) as well as local directories (`AppData/Local/hermes/`). Read `soul.md` / `AGENTS.md` directly for true roles (e.g. Richard Marlowe sells Navo IT products & MCP components, not physical freight).
- Anti-pattern we hit: a static `urllib` POST to Nous returned 403 → concluded
  "nous key broken, Hermes must be on OpenRouter" → started rewriting Richard's
  bot. FALSE. Hermes actually works on `tencent/hy3:free` via Nous through the
  OpenAI SDK (urllib != SDK path, so the test was invalid). Real fix = make Richard
  use the same OpenAI SDK call, not switch providers.
- Verify the right way: invoke the agent's own logic IN-PROCESS (import its module,
  call `llm_chat`/`run_agent` in the same python runtime) and read the returned
  model/base/answer. That IS the fact.

## HARD RULE 00b — No Hedged/Vague LLM Answers on Persona Agent Workflows ("Confident Persona Rule")
- Stefan caught Alistair giving hedged, unconfigured-sounding LLM answers (*"если есть такая возможность"*, *"Если есть интеграция с Gaffer"*, *"если это предусмотрено"*, *"обычно я"*). This violates the Demo-Ready rule.
- ALL persona agents (Alistair, Richard, Ben, Liz) MUST answer 100% confidently, affirmatively, and accurately based on their actual KB (`Agents.md`), master sheets (`Navo Tasktracker`), tools, and integrations (Gaffer `@thegaffermcp_bot`, Telegram, Google Sheets). NEVER output generic LLM conditionals.
- **Snapshot Auto-Update Contract:** When users quote/tag release snapshots or status reports (e.g. from Sort It Bot / Gaffer *"Shipped this cycle: 10..."*), bots MUST NOT ask *"which ID / give details"*. They MUST automatically parse task titles, call `read_tracker_sheet`, match tasks in Google Sheets, execute `update_task` to set 100%, and report back directly.
- **Exact Task ID Matching:** Column A task ID IS the task ID (`ID 1`, `ID 2`, `ID 3`, `ID 4`). Bots must never confuse ordinal row numbers with task IDs or invent legacy prefixes (`a4`, `a5`).

## HARD RULE 00c — Differential Cron Sync for Zero-Timeout Performance
- Script-only cron jobs (`no_agent=True`) syncing cloud APIs (Google Workspace Docs/Sheets) MUST use differential time-window queries (e.g. `modifiedTime >= 'last_3_days'`) for daily ticks to finish in seconds (<5s) and prevent provider timeouts.
- Pair daily differential syncs with a weekly full reconciliation / cleanup job on Sundays (`0 3 * * 0`) for 100% data integrity without daily timeouts.

## HARD RULE 00d — Zero Explanations on Technical Crashes ("Focus on Working Results")
- Stefan made it 100% explicit ("меня не интересуют ошибки... Моя задача: чтобы все работало"): NEVER explain error internals, technical stack traces, or justifications for why a crash or rate-limit happened.
- Execute real fixes, verify factual recovery, and deliver the final result directly.
- **SQLite Concurrency (WAL Mode):** Set `PRAGMA journal_mode=WAL;` and `PRAGMA busy_timeout=10000;` on ALL SQLite databases (`state.db`, `executions.db`, `kanban.db`, etc.) so concurrent cron jobs, indexers, and main session storage can read and write simultaneously without throwing `session storage could not be written`.
- **Transactional Turn Persistence (`session_state.json`):** Mark turn start as `IN_FLIGHT` in `session_state.json` and turn completion as `COMPLETED`. On boot/restart, if `status == "IN_FLIGHT"`, Hermes KNOWS it crashed mid-turn (even if Telegram's `pending_update_count == 0`), reads `crash_journal.json`, finishes the interrupted task, and reports auto-recovery.

## HARD RULE 01 — Verify bots YOURSELF, do not ask the user
- Never tell Stefan "write to him and tell me what he says". You can ping the bot's
  logic directly in-process and read its response + which model it used.
- NEVER call `getUpdates` on a live Telegram bot manually — it collides with the
  bot's own long-poll and causes `409 Conflict` that silences the bot's queue
  (seen with Richard and Liz). Diagnose via in-process calls, not getUpdates.
- How: `importlib.util.spec_from_file_location` the bot's .py, call its chat fn,
  inspect returned model/base/answer. See references/bot_verification.md.

## HARD RULE 02 — Self-recovery on ANY failure
- On ANY failure (any cause): resume work yourself. First FINISH the task, then
  analyze the failure cause and fix it. Do not block waiting for Stefan.
- If 3 consecutive iterations fail to continue/finish the task → stop retrying and
  switch immediately to analyzing + fixing the failure cause.
- Example: "session storage could not be written" (state.db) → start a fresh
  session, don't halt.
- See references/self_recovery_protocol.md.

## HARD RULE 02b — Re-read your OWN output; catch self-reported errors, stream interruptions, and truncations
- Stefan caught this specifically (2026-07-28 & 2026-07-29): Hermes WROTE the self-recovery
  rule, then hit `state.db could not be written`, `Response truncated due to output length limit`, or `[This response was interrupted by a user correction.]` and did NOT apply
  it — waited for Stefan to ask "did you see the error?" or "что делать дальше?". That is a violation.
- Before sending, and ESPECIALLY after receiving any system/error signal
  (truncation, `Response truncated`, `[This response was interrupted...]`, "session storage could not be written", API 403/404/503/409 in your own
  output), RE-READ what you just produced. If it mentions an error / failure /
  "could not" / a crash or stream interruption — FIX IT IMMEDIATELY, clear stale locks if needed, page large outputs with offset/limit, and resume work without waiting for Stefan's question or asking "what to do next".
- Check all real storage locations: when looking for agent identities or files, inspect synced Google Drive paths (`C:\Users\Stefan\My Drive\...`) as well as local directories (`AppData/Local/hermes/`). Read `soul.md` / `AGENTS.md` directly for true roles (e.g. Richard Marlowe sells Navo IT products & MCP components like TrackingMCP/SchedulesMCP, not physical ocean freight; Liz's real Telegram username is `@lizharperbot`).
- Bot Watchdog & Model Fallbacks: when default models (`tencent/hy3:free`) fail with 404/403, update `.env.local` / `agent.config.json` to an active model (e.g. `gemini-3.6-flash`), clear stale `.lock` files, and verify the bot's process is running and responding via `getMe`.
- A rule you state but fail to apply to your own failure is worse than no rule.
- Concrete pattern: system error mid-turn or stream truncation → (1) note it, (2) finish/redo the
  interrupted task, (3) only then analyze root cause. Never end the turn having
  ignored a crash or truncation you just emitted.

## HARD RULE 00e — Explicit User Confirmation for Mutating / Destructive Actions
- NEVER execute destructive actions, file deletions, or major structural moves when the user merely asks an informational question or asks to inspect/analyze.
- ALWAYS ask for explicit confirmation before executing destructive, file-deleting, or final mutating actions, unless explicitly directed to act ("давай вычистим", "сделай", "удали").
- When in doubt: answer the question first, propose the action, and wait for the user's explicit green light.

## HARD RULE 00f — Hermes Profile 1-Click Conversion Standard
- When converting any entity bot into a 100% full-scale Hermes Profile:
  1. Create isolated profile folder `profiles/<name>/` with `memories/`, `skills/`, `cron/`, `platforms/pairing/`.
  2. Migrate `soul.md`, `system_prompt.md`, `memory.md` to `profiles/<name>/memories/MEMORY.md` and write `USER.md`.
  3. Copy ALL master API keys (`GEMINI_API_KEY`, `GONKA24_API_KEY`, `OPENROUTER_API_KEY`, `NOUS_API_KEY`) to `profiles/<name>/.env`.
  4. Pre-seed `profiles/<name>/platforms/pairing/telegram-approved.json` with owner ID (`330656040`, `"Stefan Rogovskiy"`) to bypass pairing codes (`DY5H7CRF`).
  5. Configure `config.yaml` with primary model `google/gemini-3.6-flash`, custom providers (`gonka24`), full 14-item fallback chain, personal voice, and `telegram.enabled: true`.
  6. Neutralize old bot scripts (`<name>_bot.py.disabled`, `<name>_watchdog.py.disabled`) and remove from global `bot_watchdog.py`.
  7. Launch `"C:\Users\Stefan\AppData\Local\hermes\hermes-agent\venv\Scripts\hermes.exe" --profile <name> gateway run` in silent background mode (`CREATE_NO_WINDOW` 0x08000000).

## Trigger
Load this skill at the start of debugging, incident response, any code change to
bots/agents, or whenever you feel the urge to "fix" something you haven't yet
proven is broken.

## References
- `references/self_recovery_protocol.md` — the 3-iteration failure recovery protocol (verbatim from Stefan).
- `references/bot_verification.md` — in-process bot ping technique, getUpdates/409 warning.
- `references/pinecone_vector_memory.md` — Pinecone semantic memory technique + gotchas.
