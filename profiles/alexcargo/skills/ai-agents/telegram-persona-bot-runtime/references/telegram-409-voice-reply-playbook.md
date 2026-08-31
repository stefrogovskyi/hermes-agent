# Telegram persona-bot 409 / voice / reply playbook (session 2026-07-27)

Condensed from a real multi-hour debug of the Liz Harper bot (@lizharperbot,
id 8857115619) on Windows. The other references cover retry-409 and re-exec
zombies; this one covers the mistakes that actually cost time THIS session.

## 1. THE 409 ROOT CAUSE (new this session)
Symptom: bot is the only process, one getUpdates call in code, yet Telegram
returns `HTTP Error 409: Conflict` on every poll. A clean bare poller on the
SAME token (different code) is 409-free.

Root cause: the bot read `TELEGRAM_BOT_TOKEN` from `os.environ` FIRST, falling
back to `.env.local`. The launching environment (Hermes scripts/cron) carried
the HERMES bot token in `os.environ`, so the bot long-polled the WRONG bot and
fought the gateway for it -> eternal 409. The "second copy" Stefan insisted did
not exist truly did not -- the bot was fighting ITSELF against the wrong token.

FIX (hard rule): read the bot token ONLY from the agent's own `.env.local`.
Never `os.environ.get("TELEGRAM_BOT_TOKEN")` unless it is the agent's own
process environment by design. Log `token.split(":")[0]` (bot id) at startup so
a wrong-token hijack is visible immediately.

## 2. GET vs POST getUpdates
A bare GET-with-query-string poller was 409-free; the bot's POST+json variant
got 409 ~21s into every poll. Network paths that replay POST bodies (TLS
inspection / AV) can make Telegram see a 2nd getUpdates. Prefer
`GET https://api.telegram.org/bot<tok>/getUpdates?offset=&timeout=30`.

## 3. COLD RESTART PAUSE (409 keeps coming back)
After killing the bot, Telegram holds the old long-poll connection ~35s. If you
start the new instance immediately it inherits a 409. ALWAYS: kill -> sleep
35-40s -> remove stale lock -> start. This alone fixed "409 returns even after
a clean restart".

## 4. SINGLE-INSTANCE LOCK
Windows-safe PID-lock via `os.open(LOCK_FILE, O_CREAT|O_EXCL|O_WRONLY)`.
Aliveness check MUST use `ctypes.windll.kernel32.OpenProcess` -- `tasklist`
deadlocks under pythonw (no console). Launch via uv `pythonw.exe` directly
(venv python spawns a 2nd long-poll child -> 409).

## 5. VOICE -- match the orchestrator
- IN: Whisper (`whisper-1`) transcribes `message.voice`/`audio` -> text. Logs
  show clean UTF-8; don't trust terminal mojibake, read the log file directly.
- OUT: TTS (`tts-1`, `response_format=opus`) -> `sendVoice`. Key+base_url from
  the bot's OWN `.env.local`.
- SELECTION GOTCHA: "make her like you (Hermes)" => Hermes voice = `echo`.
  Do NOT default to `alloy` (soft female). Confirm exact voice id vs memory.
  OpenAI TTS: female = alloy/nova/shimmer; male = echo/onyx/fable/ash.
  (Hermes=echo, Richard=onyx, Alistair=alloy per house config.)

## 6. reply_to_message / QUOTE (bot "didn't see what I tagged")
If the bot ignores a quoted/reply, it never read `reply_to_message`. Pull the
quoted fragment in priority: `message.quote.text` (dict) ->
`message.text_quote` -> `reply_to_message.text` -> `reply_to_message.caption`
-> photo/voice fallback; inject into the LLM prompt with "answer the quoted
fragment, do NOT say you can't see it". Handle `photo`/`video`/`video_note`
same way (vision via gpt-4o) or media is silently dropped.

## 7. LLM-CALL TIMEOUT IN POLL LOOP
`agent.run_conversation(...)` is synchronous and can hang on a slow free model.
Run it in a daemon thread with `join(timeout=90)`; if alive, return "timed out,
try again". Without this the bot looks dead after the first message.

## 8. PROACTIVITY (orchestrator-side)
When running background tasks / cron for the user: report the RESULT the moment
it completes -- do NOT wait to be asked. Silence after a finished background job
is a failure.
