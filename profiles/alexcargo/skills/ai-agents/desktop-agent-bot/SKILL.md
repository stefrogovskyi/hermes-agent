---
name: desktop-agent-bot
description: >-
  Run a stdlib-only Python agent / Telegram bot locally on the user's Windows
  Desktop (the Hermes host) WITHOUT cloud deployment and WITHOUT over-engineering.
  Covers the KISS runtime (one python process), reusing Hermes' own LLM provider
  so the sub-agent needs no separate API key, single-source-of-truth system prompt,
  and the per-token single-consumer rule. Use when building/running Richard Marlowe,
  or any local agent bot the user wants alive on their machine.
---

# Desktop Agent Bot (local Python agent/Telegram bot on the Hermes host)

Pattern for running an AI agent as a **local** long-polling Python bot on the
user's Windows Desktop — where Hermes itself runs. Captured from the
Richard-Marlowe setup (2026-07-23).

## When to use
- User wants an agent (sales/support/ops) live as a Telegram bot on their machine.
- User says "make it like you" / "сделай как себе" → the bot must use the SAME
  LLM provider as Hermes, not demand a separate OpenRouter/API key.
- Avoid for: cloud-hosted agents (use Modal/VPS), or pure cron sweeps (see
  `telegram-group-sweep`).

## RUNTIME — keep it stupid simple (user-corrected, hard lesson)
A desktop bot = **ONE background python process**. That is all.
```bash
cd "<bot folder>" && python bot.py
```
Launch it with `terminal(background=true)`, not `nohup`/`setsid` (the harness
refuses shell-level backgrounding and can't track it).

**DO NOT build any of these** (all wasted 40 min in the Richard session):
- ✗ PowerShell `while($true)` daemon (`keep_richard.ps1`) — crashed, and a second
  copy spawned a SECOND update-consumer → Telegram **409 Conflict** with the manual bot.
- ✗ `Richard_Bot.vbs` Startup shortcut wrapping a daemon — fragile.
- ✗ Task Scheduler XML task (`schtasks /Create /XML`) — needs **admin** ("Access is
  denied" from this shell) and is brittle (UTF-16 encoding + `Date` format errors).

**Only** add reboot-survival (Startup-folder VBS launching `python bot.py` hidden,
OR a Task Scheduler task) if the user EXPLICITLY needs the bot alive after a laptop
reboot. Even then: no supervision loop — `python bot.py` long-poll is enough.

## LLM PROVIDER — reuse Hermes' own `nous` credentials (no separate key)
The user has NO OpenRouter key and was confused why the bot needed one ("чтобы ты
работал, я же не давал никакой ключ"). The fix: point the bot at Hermes' own
provider, read live from `auth.json`.

- `C:\Users\Stefan\AppData\Local\hermes\auth.json`
  → `providers.nous.access_token` (Bearer token, ~1777 chars)
  → `providers.nous.inference_base_url` (e.g. `https://inference-api.nousresearch.com/v1`)
- Bot endpoint: `{inference_base_url}/chat/completions`, `Authorization: Bearer {access_token}`.
- Write the token into the bot's `.env.local` as `NOUS_API_KEY` (NOT `stub-…`) — local
  file only, never print the value, never commit. This makes the bot "live" exactly
  like Hermes, no stub fallback.
- See `references/nous-credential-reuse.md` for the exact read-recipe.

## SYSTEM PROMPT — single source of truth
- The bot MUST read its persona from `system_prompt.md` (project folder), NOT a
  hardcoded string. The Richard bug: the bot had a hardcoded `RICHARD_SYSTEM` and
  silently ignored all persona edits (British humour, "don't spam") made in the md.
- `load_system_prompt()` at startup: open `system_prompt.md`, strip `#`/`>` lines,
  pass to the LLM `system` field.

## TELEGRAM — single consumer per token (shared rule)
One token's `getUpdates` → exactly ONE consumer. So:
- A realtime long-polling bot OR an hourly sweep — never both on the same token.
- User wanted **instant** answers ("отвечать тут же, не ждать hourly sweep") → chose
  REALTIME; the hourly-sweep cron was **paused** to avoid the 409. Encode this
  decision: realtime wins when the agent must converse; sweep is for batch readers.
- Privacy: BotFather `/setprivacy` → Turn off, then **remove & re-add** bot to group
  (Telegram caches privacy at join time). Without this the bot sees only @mentions.
- In groups: reply only on `@mention` or on-domain content; never on every message;
  never spam. Off-topic addressed to it: 1–2 short sentences, occasionally.

## VERIFY before declaring done
1. `python -m py_compile bot.py` — but MSYS mangles absolute paths with spaces:
   `cd` into the folder and compile the relative name.
2. `RICHARD_SELFTEST="..." python bot.py` — exercises the LLM path offline-ish.
3. Exactly ONE python process for the bot: `2 PIDs = 1 venv chain` (python →
   python uv). More than one *chain* = duplicate = 409 risk.
4. `getMe` via Bot API returns the bot username → token valid, no leak.
5. Live test: send a PM to the bot; confirm it answers (tail the bot log).

## Pitfalls (from the session)
- **Hardcoded prompt** → persona edits silently ignored. Load from md.
- **Separate OpenRouter key** → user has none; reuse `auth.json` nous token.
- **Daemon / Task Scheduler** → crashes or 409. One `python bot.py`.
- **MSYS path with spaces** → `py_compile /c/Users/.../bot.py` fails; use `cd` + relative.
- **Two consumers on one token** → 409. One bot, one mode (realtime XOR sweep).
- **Hedged/vague LLM responses ("если есть интеграция/возможность")** → User hate signal. In system prompt, explicitly prohibit hedged phrases ("если есть возможность", "если предусмотрено"). Bot must state its actual live tools and workflows with 100% confidence.
- **Snapshot auto-update rule** → When user quotes/tags release reports (Sort It Bot, Gaffer), bot must parse task titles, auto-match against tracker sheet, and update percent to 100% without asking "what's the task ID?".
- **No deletion/hiding on 100% completion** → Completed 100% tasks move to bottom "ВЫПОЛНЕННЫЕ ЗАДАЧИ" block with light-green background fill (#d9ead3). Rows are NEVER deleted or hidden from the Google Sheet.
- **Flawed PID-only Health Checks** → Checking `psutil.pid_exists(pid)` alone is a false-positive trap! A bot process can be alive in OS Task Manager while returning template/stencil errors to the user due to dead model endpoints or expired API keys. Watchdogs MUST run a **Real Semantic LLM Test (`run_agent('ping')`)** to verify actual generation output. If a stencil error is returned, auto-heal keys and restart silently via `pythonw.exe`.
- **Group Bot Message Filtering & Meta-Commentary Suppression** → In Telegram group chats, persona bots MUST filter out messages from other bots (`msg.get("from", {}).get("is_bot")`) unless explicitly tagged or replied to. Furthermore, if a bot's LLM generates meta-commentary about silence (*"staying quiet"*, *"no @mention"*, *"not tagged"*, *"не упомянули"*, *"молчу"*), the reply MUST be suppressed and NOT published to the group chat to avoid spamming.
- **Auto-Sending During Draft Generation (Guardrail Failure)** → When generating email drafts for user approval, LLM calls MUST run **WITHOUT TOOLS** (`tools=None`). Otherwise, the LLM will execute `send_email` tool calls *during draft generation*, sending the email to the customer BEFORE asking the user for confirmation!
- **`bodyPreview` Truncation Trap** → MS Graph API `bodyPreview` truncates email bodies to 255 chars and strips history. Always extract full HTML body (`msg.get("body", {}).get("content")`) to preserve full conversation history across turns. Order: **1. Reply Text ➔ 2. Signature ➔ 3. Quoted History (`--- Исходное сообщение ---`)**.
- **Startup Email Truncation / Drop** → Do NOT mark existing inbox messages as "already seen" on startup. Use a persistent disk file (`processed_email_ids.json`) to track processed message IDs, and record an ID ONLY AFTER the notification has been delivered to the user in Telegram.

## CONVERTING A PERSONA BOT INTO A FULL-SCALE HERMES PROFILE
When the user asks to "elevate", "convert", or "make bot X a full Hermes agent on par with you":
1. **Create Profile Directory:** `C:\Users\Stefan\AppData\Local\hermes\profiles\<name>\` with `memories/`, `skills/`, `cron/`.
2. **Migrate Persona & Memory:** Copy `soul.md` + `memory.md` from Google Drive into `profiles/<name>/memories/MEMORY.md`. Write `memories/USER.md`.
3. **Configure Master Model & Fallbacks:** Set `google/gemini-3.6-flash` (provider `google`), `gonka24` custom provider, and copy the full 14-item `fallback_providers` chain into `profiles/<name>/config.yaml`.
4. **Disable Old Bot & Watchdog:** Kill `pythonw.exe <bot>_bot.py`. Rename `<bot>_watchdog.py` to `<bot>_watchdog.py.disabled` and remove `<name>` from `bot_configs` in `scripts/bot_watchdog.py`. Clear lock files in `entities/<name>.lock`.
5. **Launch Hermes Profile Gateway:** Run `"C:\Users\Stefan\AppData\Local\hermes\hermes-agent\venv\Scripts\hermes.exe" --profile <name> gateway run` in background via VBS or `subprocess.Popen(..., creationflags=0x08000000)` with `HERMES_PROFILE=<name>`.

## Support files
- `references/nous-credential-reuse.md` — exact recipe to read Hermes' `auth.json`
  `nous` token + inference URL and wire it into a sub-agent bot with no separate key.
- `references/searates-and-tasktracker-patterns.md` — SeaRates API endpoints, 100% completion light-green fill protocol (no deletion/hiding), snapshot auto-matching, and anti-hedging rules.

## Overlap note (for the curator)
This skill overlaps with `ai-agents/telegram-group-sweep` (same per-token
single-consumer rule, same "minimal bot footprint" preference). They are
complementary, not duplicates: `telegram-group-sweep` covers the *hourly
diff/batch-read* pattern and its decision tree; this skill covers the *local
realtime desktop runtime* + provider-reuse + KISS. If consolidating, fold the
runtime/credential/KISS lessons here into a shared "local agent bot" umbrella and
keep `telegram-group-sweep` for the scheduled-read decision tree.
