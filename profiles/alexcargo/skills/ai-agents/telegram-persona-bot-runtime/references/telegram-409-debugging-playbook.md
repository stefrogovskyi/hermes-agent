# Telegram Bot 409 & Runtime Debugging Playbook (field notes)

Durable techniques from a multi-hour 409 + capability-debug on the Liz Harper bot
(@lizharperbot) and siblings (Richard/Alistair/Ben). Class-level — reuse on ANY
self-hosted long-poll Telegram agent.

## A. WHY "409 Conflict" appears when you KNOW there is only one copy

The user will often insist "there is no second copy anywhere." Believe them — and
PROVE it dynamically instead of guessing. The real cause is almost never a second
process; it is one of:

1. **Token inherited from `os.environ` (THE #1 cause).**
   `token = os.environ.get("TELEGRAM_BOT_TOKEN", "")` then fallback to file.
   If the bot is launched from the orchestrator/Hermes's environment, that env var
   carries the ORCHESTRATOR's token. The bot then long-polls the WRONG bot and fights
   the gateway → eternal 409. The token's own owner "never ran a second copy" — yet the
   conflict is real because the bot polls a different bot's token.
   **FIX:** read the token ONLY from the agent's own `.env.local`. Never from env.
   Log `token.split(":")[0]` at startup so a wrong token is visible instantly.

2. **`deleteWebhook` / `getUpdates?offset=-1` inside the 409 handler.**
   These open a SECOND getUpdates while the first (still held by Telegram ~35s) is
   alive → perpetuates 409. A bare GET long-poll with NO handler, just `time.sleep(10)`
   + retry, is proven clean.

3. **POST+json getUpdates vs GET query-string.** In one environment a POST variant
   got 409 ~21s into every poll while an identical GET probe stayed clean for 180s
   (something on the network path replayed POST bodies). Not universal — but if 409 is
   stubborn, switch getUpdates to GET query-string.

## B. DYNAMIC PROOF SEQUENCE (run this before assuming a second copy)

1. Kill the bot. Wait 35–40s (Telegram holds a dead long-poll ~35s).
2. From a throwaway script, long-poll the token's getUpdates YOURSELF for 180s.
   - `ok_polls=N conflicts=0` ⇒ token is CLEAN ⇒ the conflict is INSIDE the bot's
     runtime (token/env/token-source bug), NOT an external copy.
   - any `409` ⇒ a real second consumer exists (some other bot/cloud holding the token).
3. Run a BARE poller (same pythonw, same token, same GET, but WITHOUT the bot's
   lock/deleteWebhook/imports). Clean ⇒ the bug is in the bot's own code differences.

This sequence ended a 6-hour "second copy" hunt in one pass.

## C. SINGLE-INSTANCE GUARD (Windows, no console hang)

- PID-lock via `os.open(LOCK_FILE, os.O_CREAT|os.O_EXCL|os.O_WRONLY)`; second instance
  exits silently.
- Check old-PID liveness with **ctypes `kernel32.OpenProcess`** — NEVER `tasklist`
  (deadlocks under pythonw, no console).
- Launch with the **base `pythonw`** (uv), NOT a venv python (venv-launcher re-execs a
  child `uv-python` ⇒ two pollers ⇒ 409). `CREATE_NO_WINDOW` + log to file.
- Restart recipe: kill → sleep 40 → start. Never start a new instance while the old
  long-poll may still be held by Telegram.

## D. CAPABILITY UPGRADE CHECKLIST (make a bot "behave like the orchestrator")

When a bot "can't see text / quotes / voice / photos":

1. **`reply_to_message` / quote is NOT parsed by default.** Add it explicitly:
   pull `msg["quote"]["text"]` (dict), then `msg["text_quote"]`, then
   `reply_to_message["text"]`/`["caption"]`; inject as a context block
   "[USER QUOTED … «fragment» — answer THAT]". Without this, replying-to-a-message
   looks empty to the bot.
2. **Voice**: Whisper `audio/transcriptions` on `voice`/`audio` file_id (download via
   `getFile`→`file_path`→`https://api.telegram.org/file/bot{tok}/{path}`). Reply with
   voice via TTS `audio/speech` → `sendVoice` multipart.
3. **Photo/Video**: vision (`gpt-4o` chat/completions, base64 image_url) → text.
4. **`ephemeral_system_prompt` / system prompt variable MUST be defined** before
   `AIAgent(...)` is constructed — a missing var ⇒ NameError ⇒ agent never initializes
   ⇒ bot "answers weird / ignores you". Load personality from `system_prompt.md`.
5. **LLM call timeout**: `run_conversation` can hang forever on a slow free model
   (hy3:free via Nous). Wrap in a `threading.Thread` + `join(timeout=90)`; on timeout
   return a friendly "try again" and `log()` the error. Otherwise the poll loop blocks
   and the bot "stops answering" after a few messages.

## E. BEHAVIOR RULES WORTH BAKING INTO THE SYSTEM PROMPT

- **NO META RULE (HARD):** never discuss own config/triggers/reply policy
  ("nobody tagged me", "I only answer when mentioned", "staying out of the group").
  If a message isn't for the bot → zero output (code already stays silent). If it
  answers → substance only, like a human colleague.
- **VOICE RULE:** state the bot DOES reply with voice when voice arrives; never claim
  "I am text-only."
- **Proactive features OFF by default.** Unsolicited digests/spam annoy the owner.
  Escalations (people/legal/financial risk) go to the owner immediately, unasked.

## F. DIAGNOSTIC SCRIPTS (reusable, stdlib)

- Kill + count processes matching `liz_loop`: `Get-CimInstance Win32_Process` filter
  on `CommandLine -match 'liz_loop'` (PowerShell, not `ps`/`tasklist`).
- `getMe` to confirm the bot username the token actually resolves to (catches the
  `@lizharpbot` vs `@lizharperbot` mismatch — docs drift from reality).
- `getWebhookInfo` → empty `url` confirms 409 isn't webhook-driven.
