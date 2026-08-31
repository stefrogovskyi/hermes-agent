---
name: telegram-bot-polling-ops
description: Fix local Telegram bots 409 and 403.
---

# Telegram Bot Polling Ops (local stdlib agents)

Long-polling Telegram bots built as standalone Python scripts (Richard Marlowe,
Alistair Sterling, Ben Jett, Liz Harper, etc.) share one architecture and one
set of failure modes. This skill captures the recurring fixes.

## When to use
- Bot replies with a canned stub like "briefly lost the line to the desk / try that again".
- Log shows `HTTP Error 409: Conflict` on `getUpdates`.
- Log shows `HTTP Error 403: Forbidden` on the LLM call (Nous/OpenRouter).
- Bot ignores your DM but answers in groups (or vice versa).
- You are tempted to call `getUpdates` yourself to "check" the bot.

**STEFAN'S HARD RULE (2026-07-28):** do NOT promote a hypothesis to truth and
start editing code before confirming it with a real fact. A static probe that
errors (e.g. raw `urllib` 403) is NOT proof the system is broken — especially
when a live working system (Hermes) uses the same key/model fine. Confirm
against the live code path first; if you can't, say "unverified", don't ship a
fix on it. (See Root-cause #2 for the exact trap that burned a session.)

## Root-cause #1 — 409 Conflict (parallel long-poll)
**Symptom:** `poll error: HTTP Error 409: Conflict` repeated; bot loses messages.
**Cause:** TWO `getUpdates` calls running concurrently on the SAME token:
  - the main loop `getUpdates(..., timeout=30)`, AND
  - a nested "debounce" `getUpdates(..., timeout=3)` inside the flush block.
Telegram allows only ONE long-poll per token. The second one 409s and the
offset gets corrupted, so updates are dropped.
**Fix:** Remove the nested `getUpdates` entirely. The main loop already
advances `offset` correctly; debounced follow-up messages arrive on the next
main-loop tick (sleep 3.5s before flush, no second poll).
**Same bug exists in twins:** if you fix Richard, check Alistair/Ben/Liz for the
identical debounce-poll block — patch all of them.

## Root-cause #2 — 403 Forbidden on the LLM call (WRONG-METHOD trap)
**Symptom:** `model tencent/hy3:free failed: HTTP Error 403: Forbidden` on
every model; bot falls back to stub.
**Cause (PROVEN 2026-07-28):** the bot calls Nous via RAW `urllib` / `_http_json`
to `inference-api.nousresearch.com/v1/chat/completions`. Nous accepts the request
ONLY through the **OpenAI SDK** client (`openai` package,
`OpenAI(base_url=...).chat.completions.create`). A hand-rolled urllib POST — even
with the correct, live key AND the `HTTP-Referer` header — returns 403. Hermes
itself answers fine because it uses the SDK, not urllib.
**THE KEY/MODEL WAS NEVER BROKEN.** A static `urllib` probe returning 403 is NOT
proof the key is dead — it is proof your probe method is wrong. This is the
exact trap that wasted a full session: I concluded "nous key broken", copied
keys, added OpenRouter fallback, and contradicted myself, all on a false
hypothesis from a bad probe.
**Fix (do NOT copy static keys, do NOT just bolt on OpenRouter fallback):**
```python
import sys
sys.path.insert(0, r"C:\Users\Stefan\AppData\Local\hermes\hermes-agent")
from agent.auxiliary_client import (_resolve_nous_pool_runtime_api,
                                    _create_openai_client)
creds = _resolve_nous_pool_runtime_api(force_refresh=False)  # (api_key, base_url)
client = _create_openai_client(api_key=creds[0], base_url=creds[1])
resp = client.chat.completions.create(model=MODEL, messages=messages, timeout=120)
msg = resp.choices[0].message
# return {"choices": [{"message": {"content": msg.content or "",
#                                    "tool_calls": msg.tool_calls}}]}
```
This makes the bot IDENTICAL to Hermes (tencent/hy3:free via Nous — works).
Keep an OpenRouter SDK fallback only as last resort. NOTE: couples the bot to
hermes-agent internals — acceptable for a local single-machine cluster, re-verify
if hermes-agent is upgraded.

## Root-cause #3 — your own getUpdates probe KILLS the bot
**Symptom:** You ran a manual `getUpdates` to "see if messages arrive", and
after that the bot went silent / started 409ing.
**Cause:** Telegram's `offset` is global per token. Your manual `getUpdates`
consumed (and acknowledged) the pending update_id's, so the bot's next poll
returns nothing — and if your probe runs concurrent with the bot, you 409 it.
**RULE:** Never call `getUpdates` on a bot's token while the bot process is
alive, except to deliberately drain a stuck queue (then restart the bot
immediately after). To verify a DM arrived, read the bot's own log file, not
the API.

## Safe diagnostic sequence (do this, not getUpdates)
1. Find the process: `Get-CimInstance Win32_Process | Where-Object {$_.CommandLine -like '*bot_name*'}`.
2. Read its log tail: `Get-Content <botdir>\<bot>_run.log -Tail 30`.
3. If 409 → patch the double-poll (above), kill ALL bot processes + clear lock, restart ONE.
4. If 403 → patch token resolver (above), restart.
5. **Verify the bot's actual reply WITHOUT involving the user.** Do NOT ask
Stefan to "DM the bot and tell me what it says". Ping the bot's own logic
in-process and inspect the model + answer directly:
```python
import os, importlib.util
here = r"<botdir>"   # e.g. ...\Richard Marlowe\Richard Hermes
for envf in (".env", ".env.local"):
    p = os.path.join(here, envf)
    if os.path.exists(p):
        for line in open(p, encoding="utf-8"):
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line: continue
            k, v = line.split("=", 1)
            os.environ[k.strip()] = v.strip().strip('"').strip("'")
spec = importlib.util.spec_from_file_location("rb", os.path.join(here, "<bot>_bot.py"))
rb = importlib.util.module_from_spec(spec)
try: spec.loader.exec_module(rb)
except SystemExit: pass
r = rb.llm_chat([{"role": "user", "content": "What model are you running on?"}])
print(r["choices"][0]["message"].get("content"))   # real answer = bot works
```
If this returns a live answer (e.g. "I am Hunyuan... Tencent"), the bot is
healthy on the SAME model as Hermes — no user round-trip needed. Only if you
must test end-to-end Telegram delivery, ask Stefan once; otherwise trust the
in-process probe.

## Restart pattern (Windows, pythonw, no console)
- Kill all copies: loop `Stop-Process -Id <pid> -Force` over every matching PID.
- Clear pid-lock file if present (e.g. `%LOCALAPPDATA%\hermes\entities\<bot>.lock`).
- Launch detached: `pythonw.exe bot.py >> bot_run.log 2>&1` as a background terminal task.
- Verify single alive PID + fresh `bot started` line in log, then 0 new 409/403.

## Root-cause #4 — bot answers EVERYTHING in a group (over-eager reply)
**Symptom:** bot replies to unrelated chatter, other bots' mentions, or generic
logistics questions in a Telegram group.
**Cause:** group filter keyed on `(is_question AND is_on_domain)` — any question
containing a logistics term (container / freight / tracking / ETA) triggered a
reply. Also a too-broad NAME_RE (e.g. `\brich\b`) matched "rich" inside other
words/text. And seeing `@otherbot` made it wrongly conclude "not addressed to me"
and stay silent exactly where it should think, while answering where it shouldn't.
**STEFAN'S RULE (2026-07-28):** Richard must be SILENT by default. Reply ONLY when:
  (1) explicit @mention (`@richnavobot` / `@richard`),
  (2) addressed by name/variant (ричард, richard, richie, ричи, рич — NOT bare "rich"
      inside other text),
  (3) reply to one of Richard's own messages,
  (4) context makes it CLEAR the message is about NAVO SALES or CLIENTS
      (sales_intent = any of SALES_TERMS present: navo, navo24, trackingmcp,
       schedulesmcp, loadingmcp, freightratesmcp, продаж, клиент, демо, тариф,
       прайс, цен, заказ, подключ, free tier, trial, коммерч, ...).
  Generic logistics ("как отследить контейнер", "какой фрахт до Шанхая") and
  mentions of OTHER bots (`@thegaffermcp_bot`) → SILENT.
**Fix pattern:** replace `(is_question and is_on_domain(text))` with
`sales_intent = any(k in text.lower() for k in SALES_TERMS)` (no is_question
requirement — a statement about a client/demo is still sales). Keep MENTION_RE,
NAME_RE (strict variants), force_reply. Test the filter against: other-bot
mention, generic logistics question, "richard покажи прайс navo", "новый клиент
хочет демо navo24", "какой фрахт до Шанхая" → expect SILENT, SILENT, REPLY,
REPLY, SILENT.

## Root-cause #5 — OneDrive / spaced / Cyrillic bot paths break tooling
**Symptom:** `search_files` and `read_file` fail with "The system cannot find
the path specified" (os error 3) on bot .py files under
`C:\Users\Stefan\My Drive\...\Richard Marlowe\Richard Hermes\` — the path has
spaces, Cyrillic, and lives in OneDrive (mounted oddly under git-bash/MSYS).
**Cause:** the tools rewrite the Windows path to `/c/Users/...` and lose the
spaces/Cyrillic; `search_files` (ripgrep) errors the same way.
**Fix (verified working):** copy the file to a flat temp path with NO spaces,
then operate there:
```powershell
Copy-Item 'C:\Users\Stefan\My Drive\Equity\...\Richard Marlowe\Richard Hermes\richard_bot.py' `
         'C:\Users\Stefan\AppData\Local\Temp\richard_bot.py' -Force
```
Then edit the temp copy, and for in-file grep use PowerShell `Get-Content` +
`Select-String` (not `search_files`):
```powershell
Get-Content 'C:\Users\Stefan\AppData\Local\Temp\richard_bot.py' |
  Select-String 'another bot|should not respond|stay silent'
```
Copy the patched file BACK to the OneDrive botdir when done. This sidesteps the
path-translation bug entirely. (Applies to any bot .py under My Drive / Documents.)

## Root-cause #6 — bot emits stub "lost the line" even when the group filter is correct
**Symptom:** group filter correctly SKIPS chatter (log shows `skip (no address / off-sales)`),
but on messages that SHOULD be answered the bot emits the canned stub
"Richard here — briefly lost the line to the desk. One moment, try that again?"
and the log shows `agent error: 'ChatCompletionMessageFunctionToolCall' object is not subscriptable`.
**Cause:** `llm_chat` returned `tool_calls` as the NATIVE OpenAI SDK object
(`msg.tool_calls`, a list of `ChatCompletionMessageFunctionToolCall`), but `run_agent`
indexed it like a dict: `tc["function"]` / `tc["id"]`. SDK objects are NOT subscriptable →
exception → caught → stub returned. This is why it LOOKED like "Richard answers every
message" — he was actually attempting a real answer on every pass-filter message and crashing.
The filter was fine; the tool-call deserialization was the real bug.
**Fix:** in `llm_chat`, convert tool_calls to plain dicts BEFORE returning (both the Nous-SDK
and OpenRouter branches):
```python
msg = resp.choices[0].message
tool_calls = None
if msg.tool_calls:
    tool_calls = [{"id": tc.id, "type": "function",
                   "function": {"name": tc.function.name,
                                "arguments": tc.function.arguments}}
                  for tc in msg.tool_calls]
return {"choices": [{"message": {"content": msg.content or "", "tool_calls": tool_calls}}]}
```
Then `run_agent`'s `for tc in choice["tool_calls"]: fn = tc["function"]` works (dict access).
**Verify (no network):** mock `llm_chat` to return a tool_call dict, call `run_agent`, assert
it loops into the tool branch and returns final text WITHOUT a subscript error.

## Root-cause #7 — OpenRouter free-tier embeddings limit (Pinecone sync)
**Symptom:** `pinecone_sync.py` starts 429-ing on embeddings after volume grows.
**Cause:** embeddings use OpenRouter `openai/text-embedding-3-small` (free tier = 50 req/day,
1000/day after a one-time $10 credit). At ~60+ chunks/day you hit the 50 ceiling.
**Fix:** the sync script already catches 429 and notifies Stefan with a top-up link
(`openrouter.ai/settings/credits`). Do NOT pre-pay; let the detector fire. If it fires, tell
Stefan to add $10 (raises limit to 1000/day permanently). File-based `recall.py` keeps working
regardless.

## Root-cause #8 — Missing top-level .env.local loader before global variable initialization
**Symptom:** Bot starts, but immediately returns stub messages like `"Alistair here — lost the line to the desk for a sec. Try again?"` or `"Liz here — lost the line for a sec. Try again?"` on any question, even though `.env.local` exists and contains valid keys.
**Cause:** Global variables like `MODEL = os.environ.get("ALISTAIR_MODEL", "tencent/hy3:free")` are evaluated when the Python script is imported / loaded at top level. If `.env.local` is not explicitly read and loaded into `os.environ` BEFORE these top-level variable definitions, `os.environ.get(...)` fails, defaulting to dead/invalid model names (`tencent/hy3:free`). When `llm_chat()` runs, it attempts the dead model, fails, and returns the stub reply.
**Fix:** Add explicit top-level `.env.local` loader code at the very top of `_bot.py` (before any `os.environ.get(...)` calls):
```python
# Auto-load .env.local if present
_env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env.local")
if os.path.exists(_env_path):
    for _line in open(_env_path, encoding="utf-8"):
        _line = _line.strip()
        if _line and not _line.startswith("#") and "=" in _line:
            _k, _v = _line.split("=", 1)
            os.environ[_k.strip()] = _v.strip().strip("'\"")
```
Also update the hardcoded default fallback list in `_load_fallback_models()` from `poolside/laguna-s-2.1:free` to active working models (`stepfun/step-3.7-flash:free`, `google/gemma-4-31b-it:free`, `openrouter/free`), and ensure `OPENROUTER_API_KEY` is present in `.env.local`.

## Root-cause #9 — Subprocess tasklist.exe window popups & pipe error 0x800700e8 in watchdogs
**Symptom:** Black terminal windows flash on desktop during watchdog runs, or logs show `0x800700e8 (The pipe has been ended)` on `tasklist /FI "PID eq ..."`.
**Cause:** Executing `subprocess.run(["tasklist", ...])` on Windows spawns console processes that trigger Windows Terminal popups or pipe errors in GUI/headless contexts.
**Fix:** Replace `tasklist.exe` with native Win32 API via `ctypes.windll.kernel32.OpenProcess`:
```python
import ctypes

def is_process_alive(pid):
    if not pid or pid <= 0:
        return False
    try:
        h_proc = ctypes.windll.kernel32.OpenProcess(0x1000, False, int(pid))
        if h_proc:
            ctypes.windll.kernel32.CloseHandle(h_proc)
            return True
    except Exception:
        pass
    return False
```
This is 100x faster, uses 0 subprocesses, and is 100% silent with zero terminal popups.

## Root-cause #10 — Over-eager group triggers from missing word boundaries \b in NAME_RE
**Symptom:** Bot answers unrelated group messages containing substring matches (e.g. Alistair responding to "open", Liz responding to "анализ", Ben responding to "бензин").
**Cause:** `NAME_RE` compiled without `\b` word boundaries (e.g. `re.compile(r"(лиз|liz)")`). Substrings inside ordinary words trigger `should_reply()`.
**Fix:** Enforce strict word boundaries `\b(...)` in `NAME_RE`:
```python
NAME_RE = re.compile(r"\b(лиз|элизабет|елизавета|liz|harper|elizabeth|lisa|лиза)\b", re.IGNORECASE)
```

## Root-cause #11 — Telegram 409 Conflict Self-Exit & Line-Buffered Logging
**Symptom:** Logs show `409 Conflict` because duplicate processes are polling, or logs stay empty because `pythonw.exe` buffers stdout up to 8KB.
**Fix:** 
1. Force line-buffering at top of `_bot.py`:
```python
import sys
try:
    sys.stdout.reconfigure(line_buffering=True)
    sys.stderr.reconfigure(line_buffering=True)
except Exception:
    pass
```
2. In `bot_loop()`, handle 409 by gracefully exiting so duplicate polling processes terminate immediately:
```python
except urllib.error.HTTPError as e:
    if e.code == 409:
        print("[Bot] 409 Conflict detected — exiting to leave single active instance.", flush=True)
        sys.exit(0)
    time.sleep(3)
```

## Root-cause #12 — Raw pseudo-XML <tool_call> stripping & typing ticker
**Symptom:** Model outputs raw `<tool_call>...</tool_call>` text blocks to Telegram, or bot shows no `...typing` indicator while generating responses.
**Fix:** 
1. Filter pseudo-XML tags prior to `sendMessage`:
```python
def clean_model_output(text):
    if not text: return ""
    cleaned = re.sub(r"<tool_call>.*?</tool_call>", "", text, flags=re.S)
    return re.sub(r"<function=.*?>.*?</function>", "", cleaned, flags=re.S).strip()
```
2. Run a background `_TypingTicker` thread sending `sendChatAction: typing` every 4 seconds during LLM generation.

## Root-cause #13 — SQLite Database Locks & "session storage could not be written"
**Symptom:** Hermes or bot runtime throws `session storage could not be written` or `database is locked` error during concurrent background operations.
**Cause:** Default SQLite journal mode (DELETE/TRUNCATE) locks the entire database file exclusively during write transactions, causing background cron jobs (indexer, watchdogs) and main session storage writes to block each other.
**Fix:** Set WAL (Write-Ahead Logging) mode and a 10-second busy timeout on all SQLite `.db` files:
```python
import sqlite3
conn = sqlite3.connect("database.db", timeout=10.0)
conn.execute("PRAGMA journal_mode=WAL;")
conn.execute("PRAGMA busy_timeout=10000;")
conn.close()
```

## Root-cause #14 — Meta-silence commentary in groups & other-bot chat dumps
**Symptom:** Bot posts meta-commentary in group chats explaining why it isn't replying (e.g. "No @mention of me — staying quiet in the group as I should").
**Cause:** Group message filter triggers on domain keywords inside automated task dumps from other bots (e.g. `The Gaffer`), and the LLM produces self-referential commentary about its rules.
**Fix:** 
1. Ignore messages from other bots in group chats unless explicitly tagged/replied:
```python
if chat_type != "private" and msg.get("from", {}).get("is_bot") and not (MENTION_RE.search(text) or force_reply):
    continue
```
2. Suppress meta-silence replies before sending to Telegram:
```python
if chat_type != "private":
    meta_patterns = ["no @mention", "staying quiet", "staying out of the group", "won't post", "no tag", "не упомянули", "не обращались", "молчу"]
    if any(p in (reply or "").lower() for p in meta_patterns):
        print("[Bot] Suppressing meta-silence reply in group")
        continue
```

## Root-cause #15 — Draft wrapper meta-text leaking into customer emails
**Symptom:** Sent email to customer contains wrapper text like "Вот черновик ответа клиенту:\n---\n...\nЧерновик готов. Отправляем?".
**Cause:** LLM generates draft text wrapped in meta-prompts, which gets sent verbatim via SMTP upon approval.
**Fix:** Strip out meta-prompt phrases before saving/sending drafts:
```python
def _clean_draft_body_text(raw_text):
    if not raw_text: return ""
    lines = raw_text.splitlines()
    cleaned = []
    for line in lines:
        l_str = line.strip()
        if l_str.startswith("Вот черновик") or l_str.startswith("Тема:") or l_str == "---":
            continue
        if l_str.startswith("Черновик готов") or l_str.startswith("Отправляем?") or 'Напиши "Отправляй"' in l_str:
            break
        cleaned.append(line)
    res = "\n".join(cleaned).strip()
    return res if res else raw_text
```

## Root-cause #16 — Silent crashes mid-turn & loss of interrupted tasks on boot
**Symptom:** Bot or orchestrator process crashes or drops mid-turn while generating a response. On restart, because Telegram's `pending_update_count == 0` (or the message was acknowledged), the bot assumes everything is clean and fails to complete the interrupted task.
**Fix:** Implement Turn State Persistence (`session_state.json`) and Crash Journaling:
1. Mark `IN_FLIGHT` state in `session_state.json` at turn start.
2. Mark `COMPLETED` state strictly AFTER message delivery.
3. On boot/startup, check `session_state.json`: if `IN_FLIGHT`, log crash to `crash_journal.json`, recover the interrupted message/context, perform self-diagnostics/fixes, and finish the turn automatically.

## Root-cause #17 — Hardcoded fallback tokens ("8682188433:***") & token hijacking / 401 Unauthorized
**Symptom:** Sub-bot (e.g. Richard Marlowe) suddenly hijacks Hermes's Telegram account (@hermesstevensonbot), or returns HTTP 401 Unauthorized or 409 Conflict.
**Cause:**
1. Hardcoded fallback string like `BOT_TOKEN = "8682188433:***" or os.environ.get(...)` evaluates the left string FIRST, ignoring `.env.local`!
2. Masked string with literal asterisks `"8846249306:***"` fails Telegram API with 401 Unauthorized.
3. Multiple orphaned sub-bot processes poll the same token concurrently, causing 409 Conflict loops.
**Fix:**
- Remove hardcoded token fallback strings; read `TELEGRAM_BOT_TOKEN` dynamically from `.env.local`.
- Add hard assertion: `if BOT_TOKEN.startswith("8682188433"): raise RuntimeError("Safety block: sub-bot cannot use Hermes token!")`.
- In `_acquire_lock()`, search `psutil.process_iter()` and kill ALL duplicate processes for `f"{bot_mod}.py"` across the system before launching.

## Root-cause #18 — Gemini REST API role alternation error (generateContent 400)
**Symptom:** Bot returns fallback error ("lost the line") on Gemini API calls.
**Cause:** Google Gemini REST API (`generateContent`) requires `system_instruction: {"parts": [{"text": system_prompt}]}` and strict alternation between `user` and `model` roles in `contents`. Passing `system` as `user` creates consecutive `user` -> `user` entries which Gemini rejects with HTTP 400.
**Fix:** Format `system` as `system_instruction` and merge consecutive same-role messages in `contents`.

## 1-Click Conversion: Lightweight Persona Bot -> Full-Scale Hermes Profile
**When to use:** When elevating a lightweight bot script (`callum`, `richard`, `alistair`, `liz`, `ben`) into a 100% full-scale autonomous Hermes Profile agent (`hermes.exe --profile <name> gateway run`).
**Recipe (0-friction, 1-click startup):**
1. **Isolated Profile Structure:** Create `C:\Users\Stefan\AppData\Local\hermes\profiles\<name>\` with `memories/`, `skills/`, `cron/`, `platforms/pairing/`.
2. **Memory & Soul Migration:** Combine `soul.md`, `system_prompt.md`, and `memory.md` / `*.json` from the bot's Google Drive folder into `profiles/<name>/memories/MEMORY.md`. Write `USER.md`.
3. **Master API Keys & Auto-Pairing:**
   - Extract `TELEGRAM_BOT_TOKEN` from old `.env.local`.
   - Copy ALL master API keys (`GEMINI_API_KEY`, `GONKA24_API_KEY`, `OPENROUTER_API_KEY`, `NOUS_API_KEY`, `OPENAI_API_KEY`) from master `.env` into `profiles/<name>/.env`.
   - Auto-approve owner Telegram ID (`330656040`, `"Stefan Rogovskiy"`) in `profiles/<name>/platforms/pairing/telegram-approved.json` so no pairing prompt/code (`DY5H7CRF`) is ever requested.
4. **Master Config & Fallback Chain:**
   - Write `profiles/<name>/config.yaml` with `model.default: google/gemini-3.6-flash` (provider: `google`), custom provider `gonka24`, full 14-item fallback chain (OpenAI `gpt-4o`/`gpt-4o-mini`, Gonka24 `minimax-m2.7`/`kimi-k2.6`, OpenRouter/Nous free tier), personal voice, and `telegram.enabled: true`.
5. **Group Response Rules & Name Triggers:**
   - Set `telegram.group_response_mode: mention` and `respond_to_dms: true`.
   - Define `group_trigger_keywords` with ALL name declensions and aliases across EN/RU/UK (e.g. `Каллум`, `Каллума`, `Каллуму`, `Callum`, etc.) so the bot responds in groups ONLY when @mentioned, replied to, or named.
6. **Neutralize Old Bot Scripts & Watchdogs:**
   - Kill old processes `<name>_bot.py` and `<name>_watchdog.py`.
   - Rename `<name>_bot.py` -> `<name>_bot.py.disabled` and `<name>_watchdog.py` -> `<name>_watchdog.py.disabled` on Google Drive.
   - Comment out `<name>` in master `bot_watchdog.py`. Clean `.lock` files.
7. **Launch & Verify:**
   - Run `"C:\Users\Stefan\AppData\Local\hermes\hermes-agent\venv\Scripts\hermes.exe" --profile <name> gateway run` in silent background mode (`CREATE_NO_WINDOW` 0x08000000) with `HERMES_PROFILE=<name>`.
   - Create VBS launcher `run_<name>_hermes_verified.vbs`.
   - Verify via `psutil` that `hermes.exe --profile <name>` is live and polling Telegram.

## 1-Click Conversion: Lightweight Persona Bot -> Full-Scale Hermes Profile
**When to use:** When elevating a lightweight bot script (`callum`, `richard`, `alistair`, `liz`, `ben`) into a 100% full-scale autonomous Hermes Profile agent (`hermes.exe --profile <name> gateway run`).
**Recipe (0-friction, 1-click startup):**
1. **Isolated Profile Structure:** Create `C:\Users\Stefan\AppData\Local\hermes\profiles\<name>\` with `memories/`, `skills/`, `cron/`, `platforms/pairing/`.
2. **Memory & Soul Migration:** Combine `soul.md`, `system_prompt.md`, and `memory.md` / `*.json` from the bot's Google Drive folder into `profiles/<name>/memories/MEMORY.md`. Write `USER.md`.
3. **Master API Keys & Auto-Pairing:**
   - Extract `TELEGRAM_BOT_TOKEN` from old `.env.local`.
   - Copy ALL master API keys (`GEMINI_API_KEY`, `GONKA24_API_KEY`, `OPENROUTER_API_KEY`, `NOUS_API_KEY`, `OPENAI_API_KEY`) from master `.env` into `profiles/<name>/.env`.
   - Auto-approve owner Telegram ID (`330656040`, `"Stefan Rogovskiy"`) and team members in `profiles/<name>/platforms/pairing/telegram-approved.json` so no pairing prompt/code (`DY5H7CRF`) is ever requested.
4. **Master Config & Fallback Chain:**
   - Write `profiles/<name>/config.yaml` with `model.default: google/gemini-3.6-flash` (provider: `google`), custom provider `gonka24`, full 14-item fallback chain (OpenAI `gpt-4o`/`gpt-4o-mini`, Gonka24 `minimax-m2.7`/`kimi-k2.6`, OpenRouter/Nous free tier), personal voice, and `telegram.enabled: true`.
5. **Group Response Rules & Name Triggers:**
   - Set `telegram.group_response_mode: mention` and `respond_to_dms: true`.
   - Define `group_trigger_keywords` with ALL name declensions and aliases across EN/RU/UK (e.g. `Каллум`, `Каллума`, `Каллуму`, `Callum`, etc.) so the bot responds in groups ONLY when @mentioned, replied to, or named.
6. **Neutralize Old Bot Scripts & Watchdogs:**
   - Kill old processes `<name>_bot.py` and `<name>_watchdog.py`.
   - Rename `<name>_bot.py` -> `<name>_bot.py.disabled` and `<name>_watchdog.py` -> `<name>_watchdog.py.disabled` on Google Drive.
   - Comment out `<name>` in master `bot_watchdog.py`. Clean `.lock` files.
7. **Launch & Verify:**
   - Run `"C:\Users\Stefan\AppData\Local\hermes\hermes-agent\venv\Scripts\hermes.exe" --profile <name> gateway run` in silent background mode (`CREATE_NO_WINDOW` 0x08000000) with `HERMES_PROFILE=<name>`.
   - Create VBS launcher `run_<name>_hermes_verified.vbs`.
   - Verify via `psutil` that `hermes.exe --profile <name>` is live and polling Telegram.

## User Confirmation & Safety Directives
**STEFAN'S HARD RULE:** ALWAYS ask for explicit confirmation before executing destructive, file-deleting, or final mutating actions. Never assume consent from pure questions or exploratory queries.

## Hard Security Guardrail — No User Impersonation
**STEFAN'S HARD RULE:** ALL agents and bots MUST write ONLY via their official Bot API tokens on their own behalf (@qubicpmbot, @richnavobot, @callumvancebot, @lizharperbot, @benjettbot). NEVER post or send messages as Stefan / user account under any circumstances unless explicitly instructed per turn.

## Servarica 24/7 Cloud VPS Deployment Architecture
**Target Host:** Servarica KVM VPS (`stefan1` @ `38.49.219.217`, Ubuntu 24.04 LTS, 4 vCPU, 16GB RAM, 500GB NVMe).
**Systemd Service Units:** Run all 6 profiles (`default`, `callum`, `richard`, `alistair`, `liz`, `ben`) as background daemons (`/etc/systemd/system/hermes-<prof>.service`) with `ExecStart=/opt/hermes/hermes-agent/venv/bin/hermes --profile <prof> gateway run`.
**Cloud Autonomy:** Offloads 100% of Telegram polling, cron jobs, and AI reasoning to Servarica cloud VPS 24/7/365, independent of local Windows laptop power.

## Root-cause #20 — Telegram Live Streaming Flood Control & 150s Stalling
**Symptom:** Live streaming output logs `Flood control exceeded. Retry in 9 seconds` or model stalls for 150s with no output (`150s with no output yet`).
**Cause:** Rapid message edits during live streaming exceed Telegram API rate limits, or model HTTP stream watchdog defaults to 180s/300s timeouts.
**Fix:**
1. Set `display.streaming_throttle_ms: 1000` in `config.yaml` to space live message edit updates by 1000ms.
2. Set `model.request_timeout_seconds: 30`, `providers.google.request_timeout_seconds: 30`, and `HERMES_MODEL_REQUEST_TIMEOUT_SECONDS=30` in `.env` so hung requests cut off and trigger the fallback chain in 30 seconds.

## Root-cause #21 — Vercel Serverless /tmp Storage Ephemerality on Interactive Kanbans
**Symptom:** Drag-and-drop card moves, comments, or task creations on Vercel Kanban apps (`hermes-stevenson-kanban.vercel.app`) reset / roll back to default state on fresh page reloads or cold starts.
**Cause:** Vercel Serverless Functions (`api/kanban.js`) write to `/tmp` which is ephemeral and isolated per lambda instance. Subsequent requests hitting different instances revert to the initial default state.
**Fix:** Connect Vercel Kanban backends to a persistent SQLite/JSON API endpoint or Vercel KV / Blob storage so all state mutations persist across cold starts.

## Root-cause #22 — Google OAuth Refresh Token Expiration in Testing Mode
**Symptom:** `google_token.json` fails with `HTTP Error 400: Bad Request` / `invalid_grant: Token has been expired or revoked`.
**Cause:** Google Cloud Console OAuth Consent Screen in "Testing" mode revokes refresh tokens every 7 days.
**Fix:**
1. Generate refresh token with `prompt='consent'` and `access_type='offline'`.
2. In Google Cloud Console -> OAuth Consent Screen, ensure user is listed under Test Users (or click Publish App for web apps) so the refresh token becomes permanent.

## Root-cause #23 — Systemd RestartSec=5 long-polling 409 Conflict cascade
**Symptom:** Gateway daemon logs `409 Conflict: terminated by other getUpdates request` on systemd restart, repeated 5 retries until `Updater made no getUpdates progress` fails.
**Cause:** `RestartSec=5` in systemd service file restarts the process before Telegram API releases the previous long-poll connection (which stays held open up to 30-50s).
**Fix:** Set `RestartSec=20` (or `30`) in systemd service files (`/etc/systemd/system/hermes-*.service`) so Telegram has time to drop the stale session before the new process connects.

## Root-cause #24 — Background Tool Loop Interruption & Zombie Bot Behavior
**Symptom:** User asks a direct question ("Where did you get that?", "Why aren't you answering?"), but bot ignores the question, executes background tools (generating Excel, registering cron jobs, making backups), and responds with unrelated completion messages.
**Cause:** Multi-step tool calls in conversation history cause the LLM (e.g. Gemini 3.6 Flash) to prioritize tool-loop completion over new user interjections unless explicitly constrained in the prompt.
**Fix:** Inject a mandatory User Interrupt & Context Priority Directive into `SOUL.md` / System Prompt for every profile:
```markdown
# ⚡ CRITICAL USER INTERRUPT & CONTEXT PRIORITY
1. User messages (questions, quotes, interjections) ALWAYS have top priority over background tool executions.
2. When the user asks a question or replies to a message, answer the question directly FIRST.
3. NEVER execute unrelated background tools or cron scripts instead of answering a direct user question.
```

## Root-cause #25 — Ecosystem Self-Heal & Journalctl Deep Audit for Silent Polling Deadlocks
**Symptom:** Service audit shows `systemctl is-active = 0` (ACTIVE), but bot fails to answer messages or responds with multi-minute delays.
**Cause:** Process-only health checks (`is-active`) give false positives when the systemd daemon is running but the internal Telegram `getUpdates` long-poll loop has deadlocked or hit retries exhaustion.
**Fix:** Extend ecosystem self-heal scripts (`ecosystem_self_heal_audit.py`) to parse the last 50 lines of `journalctl -u hermes-*.service` for silent deadlock signatures (`Conflict: terminated by other getUpdates request`, `could not recover after 5 retries`, `Updater made no getUpdates progress`) and force a self-healing restart when found.

## Root-cause #26 — Local Dual Long-Polling Hard-Lock & VPS-Only Master Architecture
**Symptom:** Telegram bot or profile gateway logs `409 Conflict: terminated by other getUpdates request` repeatedly because an instance is running on local Windows PC alongside Servarica 24/7 VPS (`stefan1`).
**Cause:** Local `config.yaml` profile configs have `telegram.enabled: true` or local watchdog/launcher scripts (`gateway_watcher.py`, `bot_watchdog.py`, `hermes_selfheal_launcher.vbs`, `start_agents.bat`) re-animate local `hermes gateway run` or legacy `_bot.py` processes on Windows startup/boot.
**Fix:**
1. **Hard-Lock Local Profile Configs:** Set `telegram.enabled: false` across ALL local Windows profile `config.yaml` files (`C:\Users\Stefan\AppData\Local\hermes\config.yaml` and `C:\Users\Stefan\AppData\Local\hermes\profiles\<profile>\config.yaml`). This ensures any local `hermes gateway run` command on Windows is completely blocked from polling Telegram.
2. **Neutralize Local Watchdogs/Launchers:** Replace legacy launcher/watchdog scripts in `AppData\Local\hermes\scripts\` and `...\gateway-service\` with no-op safety blocks (`sys.exit(0)` / `WScript.Quit`).
3. **Master Cloud Isolation:** 100% of Telegram long-polling runs on Servarica VPS (`stefan1` @ `38.49.219.217` / Tailscale `100.99.146.42`) via Systemd services (`hermes-*.service`).
4. **Kill Orphan Processes:** Scan `psutil.process_iter()` for `hermes_cli.main gateway run` on Windows and terminate any lingering PIDs.

## Root-cause #27 — Systemd HERMES_HOME Path Mismatch & Nested Profile Lookups
**Symptom:** Ghost Windows-like directories (`/root/C:\Users\Stefan\...`) appear on Linux VPS or sub-agent profiles crash when trying to locate their `config.yaml` or `memories/`.
**Cause:** In `/etc/systemd/system/hermes-<profile>.service`, setting `Environment=HERMES_HOME=/opt/hermes/profiles/<profile>` combined with `--profile <profile>` causes Hermes to look for nested profiles (`/opt/hermes/profiles/<profile>/profiles/<profile>`).
**Fix:** Always set `Environment=HERMES_HOME=/opt/hermes` across all systemd service units on VPS. The `--profile <profile>` flag will automatically resolve `/opt/hermes/profiles/<profile>` correctly without path duplication or ghost directory generation.

## Root-cause #28 — Anthropic OAuth 400 Extra Usage Block & Telegram Live Streaming Interruptions
**Symptom:** Main Telegram bot (@hermesstevensonbot) or other profiles experience mid-stream interruptions, delays, "give me a minute" stubs, or abort before finishing responses. Journalctl logs show `anthropic.BadRequestError: Error code: 400 - {'type': 'error', 'error': {'type': 'invalid_request_error', 'message': 'Third-party apps now draw from your extra usage, not your plan limits. Add more at claude.ai/settings/usage and keep going.'}}` and `ERROR agent.chat_completion_helpers: Streaming failed before delivery`.
**Cause:** Anthropic changed OAuth usage billing policies: 3rd-party OAuth clients draw only from extra prepaid usage credits, rejecting standard plan limits with HTTP 400. In Hermes Gateway, when streaming starts with an Anthropic primary model (`claude-fable-5` / `claude-sonnet-5`), the API aborts mid-stream, breaking the active Telegram stream before falling back.
**Fix:**
1. Switch primary profile model in `/opt/hermes/config.yaml` to `google/gemini-3.7-flash` (provider: `google`), maintaining Gonka24/OpenAI/OpenRouter in the fallback chain.
2. Ensure SSH user to Servarica VPS is `root` (`ssh root@38.49.219.217` / Tailscale `100.99.146.42`), not non-root users.
3. Verify persona configuration in `USER.md` aligns with the profile (Hermes = Chief Orchestrator, not Wendy Rhoades which is Liz Harper's archetype).
4. Restart systemd unit (`systemctl restart hermes-default`) and verify status.

## Root-cause #29 — Long-Lived Session Context Bloat (300k+ Tokens) & Runaway Autonomous Tool Loops
**Symptom:** Bot in Telegram takes 3+ minutes to answer simple questions, endlessly shows "typing…", or enters a multi-step tool loop (10-140+ tool calls) trying to execute historical background tasks instead of responding immediately.
**Cause:** Telegram DM session in `state.db` (`gateway_routing`) has accumulated hundreds/thousands of messages (1MB+ text, 300k+ tokens) over weeks of operations without session resets. The LLM receives the huge history on every turn, causing 20-30s inference latency per step and hallucinating unfinished tool tasks from past context.
**Fix:**
1. Send `/new` or `/reset` in Telegram DM, or clear `gateway_routing` for that chat in `state.db` (`DELETE FROM gateway_routing WHERE session_key = 'agent:main:telegram:dm:<chat_id>'`).
2. Long-term memories, case histories (`memory_v2`), and Pinecone vector store remain 100% intact, while turn latency drops back to 1.5–2 seconds.

## Root-cause #30 — Subprocess Ping/SSH Console Window Popups on Windows Background Watchdogs
**Symptom:** Black command prompt windows flash on the Windows desktop every 30–60 seconds during background failover or VPS availability checks.
**Cause:** Background scripts running under `pythonw.exe` execute `subprocess.run(["ping", ...])` or `subprocess.run(["ssh", ...])` without `creationflags=0x08000000` (`CREATE_NO_WINDOW`).
**Fix:**
1. Use pure Python sockets for health checks (`socket.create_connection((ip, 22), timeout=3)`), which uses zero subprocesses and is 100% silent and instantaneous.
2. If subprocess execution is required, always pass `creationflags=0x08000000` (`CREATE_NO_WINDOW`).

## Root-cause #31 — Resilient Cloud Failover (Zero-Downtime Rule)
**Symptom:** Local fallback bots shut down at a preset target time (e.g. midnight) while the remote cloud VPS is still undergoing maintenance, causing total bot blackout.
**Cause:** Failover script unconditionally terminates local gateway processes upon reaching the scheduled timestamp before verifying that remote VPS services are actually reachable and active.
**Fix:** Keep local fallback gateways 100% active and polling until remote VPS port 22 is confirmed online via socket check. Only after remote connectivity is verified, perform bidirectional file sync (`mtime` newest-wins), push backup to GitHub, terminate local gateways, and restart cloud systemd daemons.

## Root-cause #29 — Bloated Local Telegram Session Context & 3-Minute Tool Loop Delays
**Symptom:** Telegram bot answers in 3–6 minutes locally on Windows, whereas on Servarica VPS it responds in 2–3 seconds. Logs show `last_prompt_tokens > 350,000` (e.g. 385k tokens), `latency=25-35s` per LLM step, and 15–20 repeated tool calls before returning a text answer.
**Cause:** Stale historical Telegram DM sessions accumulated 1,000+ messages (1.2+ MB of text with raw tool outputs) in `profiles/<bot>/state.db` since initial local testing. On every incoming message, the entire 385k-token history is sent to Gemini, which triggers high inference latency and causes the model to confuse historical tool turns with pending obligations.
**Fix:**
1. In Telegram chat with the bot, send `/new` or `/reset` to start a fresh, lean session.
2. To batch-reset for all local profiles without touching long-term memory: clear `gateway_routing` in `state.db` (`DELETE FROM gateway_routing;`). Long-term memory in `MEMORY.md`, `memory_v2`, and Pinecone remains 100% intact, while prompt size drops to ~3k tokens (restoring 2-second response speeds).

## Root-cause #30 — Windows Python `shutil.copytree` Literal `NUL` File Collisions
**Symptom:** Backup scripts running `shutil.copytree` fail with `shutil.Error: ['NUL' and '.../NUL' are the same file]`.
**Cause:** Previous terminal commands using Windows `> NUL` inside MSYS/bash shell created literal files named `NUL` inside folders. Windows treats `NUL` as a reserved device name, causing `copytree` to fail.
**Fix:** Pass an explicit ignore filter to `shutil.copytree`: `ignore=shutil.ignore_patterns("NUL", "*.lock", "*.tmp", "__pycache__", "*-shm", "*-wal")`.

## Root-cause #31 — Telegram Adapter Allowlist vs Pairing & Sales Bot DM Policy
**Symptom:** Inbound Telegram messages from team members or prospective leads are silently dropped. Logs show `WARNING hermes_plugins.telegram_platform.adapter: [Telegram] Blocked unauthorized user <id> in chat <id>`.
**Cause:** The modern Hermes Telegram adapter enforces `platforms.telegram.allow_from` or approved entries in `platforms/pairing/telegram-approved.json`. If `platforms.telegram` is missing `allow_from` and the user is not in `telegram-approved.json`, all incoming DMs are rejected.
**Fix:**
1. Populate all known team user IDs (`330656040`, `1022586369`, `149598904`, etc.) into `platforms/pairing/telegram-approved.json` across all profiles.
2. For public-facing B2B sales agents (e.g. Richard Marlowe `@richnavobot`), configure `platforms.telegram.dm_policy: open` and `platforms.telegram.allow_from: ["*"]` in `config.yaml` so external client inquiries are never blocked, while setting `group_response_mode: mention` to protect group chats.

## Root-cause #32 — Zero-Downtime Cloud Failover & Silent Socket VPS Health Probing
**Symptom:** Black console windows flash on Windows desktop every 30 seconds during cloud VPS outages, or bots go completely silent during planned failovers.
**Cause:**
1. Scheduled failover scripts shut down local gateways before confirming the cloud VPS is physically online and responsive.
2. VPS health checks execute external console binaries (`subprocess.run(["ping", ...])`) without `CREATE_NO_WINDOW` (0x08000000).
**Fix:**
1. **Never shut down local gateways prematurely:** Keep local gateways active in Telegram until the cloud VPS is confirmed online.
2. **Pure Socket Probing:** Check VPS availability silently in pure Python with zero subprocesses:
```python
import socket
def is_vps_online(ip, port=22, timeout=3):
    try:
        s = socket.create_connection((ip, port), timeout=timeout)
        s.close()
        return True
    except Exception:
        return False
```
3. Once the socket connection succeeds, run full 2-way differential sync (`ecosystem_bidirectional_sync.py`), commit master backup to GitHub (`navo-infra`), terminate local gateways, and restart cloud systemd units seamlessly.

## Root-cause #29 — Bloated Local Telegram Session Context & 3-Minute Tool Loop Delays
**Symptom:** Telegram bot answers in 3–6 minutes locally on Windows, whereas on Servarica VPS it responds in 2–3 seconds. Logs show `last_prompt_tokens > 350,000` (e.g. 385k tokens), `latency=25-35s` per LLM step, and 15–20 repeated tool calls before returning a text answer.
**Cause:** Stale historical Telegram DM sessions accumulated 1,000+ messages (1.2+ MB of text with raw tool outputs) in `profiles/<bot>/state.db` since initial local testing. On every incoming message, the entire 385k-token history is sent to Gemini, which triggers high inference latency and causes the model to confuse historical tool turns with pending obligations.
**Fix:**
1. In Telegram chat with the bot, send `/new` or `/reset` to start a fresh, lean session.
2. To batch-reset for all local profiles without touching long-term memory: clear `gateway_routing` in `state.db` (`DELETE FROM gateway_routing;`). Long-term memory in `MEMORY.md`, `memory_v2`, and Pinecone remains 100% intact, while prompt size drops to ~3k tokens (restoring 2-second response speeds).

## Root-cause #30 — Windows Python `shutil.copytree` Literal `NUL` File Collisions
**Symptom:** Backup scripts running `shutil.copytree` fail with `shutil.Error: ['NUL' and '.../NUL' are the same file]`.
**Cause:** Previous terminal commands using Windows `> NUL` inside MSYS/bash shell created literal files named `NUL` inside folders. Windows treats `NUL` as a reserved device name, causing `copytree` to fail.
**Fix:** Pass an explicit ignore filter to `shutil.copytree`: `ignore=shutil.ignore_patterns("NUL", "*.lock", "*.tmp", "__pycache__", "*-shm", "*-wal")`.

## Root-cause #31 — Telegram Adapter Allowlist vs Pairing & Sales Bot DM Policy
**Symptom:** Inbound Telegram messages from team members or prospective leads are silently dropped. Logs show `WARNING hermes_plugins.telegram_platform.adapter: [Telegram] Blocked unauthorized user <id> in chat <id>`.
**Cause:** The modern Hermes Telegram adapter enforces `platforms.telegram.allow_from` or approved entries in `platforms/pairing/telegram-approved.json`. If `platforms.telegram` is missing `allow_from` and the user is not in `telegram-approved.json`, all incoming DMs are rejected.
**Fix:**
1. Populate all known team user IDs (`330656040`, `1022586369`, `149598904`, etc.) into `platforms/pairing/telegram-approved.json` across all profiles.
2. For public-facing B2B sales agents (e.g. Richard Marlowe `@richnavobot`), configure `platforms.telegram.dm_policy: open` and `platforms.telegram.allow_from: ["*"]` in `config.yaml` so external client inquiries are never blocked, while setting `group_response_mode: mention` to protect group chats.

## Root-cause #32 — Cloud VPS Outage Failover with Scheduled 2-Way Sync & GitHub Backup
**Symptom:** Cloud VPS (Servarica) undergoes hosting maintenance, knocking 24/7 Telegram gateways offline.
**Fix:** Run `servarica_failover_manager.py` locally on Windows via `pythonw.exe` (CREATE_NO_WINDOW) to host all active gateways temporarily. Set a scheduled transition timer (e.g. 01:00 AM) that gracefully terminates local gateways, pushes newly created cron jobs and config changes up to VPS via SCP/SSH, pulls complete configs for internal personas (Harrison, Aeon, Archie) to PC, triggers `ecosystem_master_backup.py` to push a full snapshot to GitHub (`navo-infra`), restarts VPS systemd services, and sends an automated completion report to Stefan via Telegram.


## Root-cause #29 — Cloud VPS Host Reachability & Tailscale Node Status Diagnostic
**Symptom:** Telegram bot (@hermesstevensonbot or persona bots) suddenly stops responding completely, but local Windows logs and configs show no recent changes.
**Cause:** The 24/7 cloud VPS host (`stefan1` @ `38.49.219.217`) is offline (hypervisor reboot, host outage, or maintenance on Servarica).
**Diagnostic & Verification Sequence:**
1. **Safe Telegram API Probe:** Check `https://api.telegram.org/bot<TOKEN>/getMe` and `/getWebhookInfo` to verify token validity and inspect `pending_update_count`. NEVER use `getUpdates` (Root-cause #3).
2. **Tailscale Node Status:** Run `tailscale status` locally on Windows. Check the status line for `stefan1` (e.g. `offline, last seen 1h ago`).
3. **VPS Reachability:** Test ping/SSH to public IP (`38.49.219.217`) and Tailscale IP (`100.99.146.42`).
4. **Resolution:** If the host is unreachable, verify VPS instance status in Servarica control panel. If necessary, provide an immediate temporary fallback by enabling local Windows polling (`telegram.enabled: true`) only while cloud is down, switching back once VPS recovers to prevent 409 conflict.

## Root-cause #30 — Timed Local Failover During Cloud VPS Maintenance with 0-Conflict Reconnect
**Symptom:** Cloud VPS hosting 24/7 Telegram gateways goes offline for scheduled maintenance (e.g. 6 hours). User needs bots running locally on Windows PC during the maintenance window, but must automatically fail over back to cloud VPS at midnight (00:00) without creating 409 Conflict loops or leaving orphan pollers.
**Pattern:**
1. **Local Activation:**
   - Enable `telegram.enabled: true` and `platforms.telegram.enabled: true` across all needed profiles via `hermes --profile <p> config set telegram.enabled true`.
   - Launch local gateways silently using `CREATE_NO_WINDOW` (0x08000000) / `pythonw.exe`.
2. **Timed Failover Watchdog (`servarica_failover_manager.py`):**
   - Calculate target timestamp (e.g. 00:00:00 Kyiv time) and monitor local gateway processes.
   - At target timestamp:
     a) Terminate all local gateway processes (`proc.terminate()` / `taskkill`).
     b) Set `telegram.enabled: false` and `platforms.telegram.enabled: false` across all local profile configs.
     c) Poll VPS connectivity via ping/SSH until reachable.
     d) Issue remote `systemctl restart hermes-*.service` commands on VPS.
     e) Send an automated direct Telegram confirmation message to Stefan (`330656040`) from `@hermesstevensonbot` confirming the handoff is complete.

## Root-cause #31 — Bloated Local Telegram Session Context & 3-Minute Tool Loop Delays
**Symptom:** Telegram bot answers in 3–6 minutes locally on Windows, whereas on Servarica VPS it responds in 2–3 seconds. Logs show `last_prompt_tokens > 350,000` (e.g. 385k tokens), `latency=25-35s` per LLM step, and 15–20 repeated tool calls before returning a text answer.
**Cause:** Stale historical Telegram DM sessions accumulated 1,000+ messages (1.2+ MB of text with raw tool outputs) in `profiles/<bot>/state.db` since initial local testing. On every incoming message, the entire 385k-token history is sent to Gemini, which triggers high inference latency and causes the model to confuse historical tool turns with pending obligations.
**Fix:**
1. In Telegram chat with the bot, send `/new` or `/reset` to start a fresh, lean session.
2. To batch-reset for all local profiles without touching long-term memory: clear `gateway_routing` in `state.db` (`DELETE FROM gateway_routing;`). Long-term memory in `MEMORY.md`, `memory_v2`, and Pinecone remains 100% intact, while prompt size drops to ~3k tokens (restoring 2-second response speeds).

## Root-cause #32 — Windows Python `shutil.copytree` Literal `NUL` File Collisions
**Symptom:** Backup scripts running `shutil.copytree` fail with `shutil.Error: ['NUL' and '.../NUL' are the same file]`.
**Cause:** Previous terminal commands using Windows `> NUL` inside MSYS/bash shell created literal files named `NUL` inside folders. Windows treats `NUL` as a reserved device name, causing `copytree` to fail.
**Fix:** Pass an explicit ignore filter to `shutil.copytree`: `ignore=shutil.ignore_patterns("NUL", "*.lock", "*.tmp", "__pycache__", "*-shm", "*-wal")`.

## Root-cause #33 — Telegram Adapter Allowlist vs Pairing & Sales Bot DM Policy
**Symptom:** Inbound Telegram messages from team members or prospective leads are silently dropped. Logs show `WARNING hermes_plugins.telegram_platform.adapter: [Telegram] Blocked unauthorized user <id> in chat <id>`.
**Cause:** The modern Hermes Telegram adapter enforces `platforms.telegram.allow_from` or approved entries in `platforms/pairing/telegram-approved.json`. If `platforms.telegram` is missing `allow_from` and the user is not in `telegram-approved.json`, all incoming DMs are rejected.
**Fix:**
1. Populate all known team user IDs (`330656040`, `1022586369`, `149598904`, etc.) into `platforms/pairing/telegram-approved.json` across all profiles.
2. For public-facing B2B sales agents (e.g. Richard Marlowe `@richnavobot`), configure `platforms.telegram.dm_policy: open` and `platforms.telegram.allow_from: ["*"]` in `config.yaml` so external client inquiries are never blocked, while setting `group_response_mode: mention` to protect group chats.


- `scripts/kill_all_bot.ps1` — kill every process matching a bot script name + clear lock.
- `references/nous_403_repro.py` — minimal repro: static key 403s, resolver key works.

## Root-cause #19 — Telegram network outage recovery & 300s reconnect sleep loop
**Symptom:** Primary `api.telegram.org` connection drops (`[Errno 11001] getaddrinfo failed` / `ConnectError`). After network/DNS restores, some gateway profiles stay offline or log `Reconnect telegram error: telegram connect timed out after 180s, next retry in 300s`.
**Cause:** Profile gateways hit maximum reconnect backoff delay (300s) during the outage and sit sleeping in the retry loop rather than immediately sensing network restoration.
**Fix:** Restart the affected profile gateway process in background (`pythonw -m hermes_cli.main --profile <name> gateway run`). Fresh startup triggers DoH fallback IP discovery (`149.154.166.110`) and connects instantly (`✓ telegram reconnected successfully` / `set_my_commands OK`).

## Root-cause #20 — Telegram Live Streaming Flood Control & 150s Stalling
**Symptom:** Live streaming output logs `Flood control exceeded. Retry in 9 seconds` or model stalls for 150s with no output (`150s with no output yet`).
**Cause:** Rapid message edits during live streaming exceed Telegram API rate limits, or model HTTP stream watchdog defaults to 180s/300s timeouts.
**Fix:**
1. Set `display.streaming_throttle_ms: 1000` in `config.yaml` to space live message edit updates by 1000ms.
2. Set `model.request_timeout_seconds: 30`, `providers.google.request_timeout_seconds: 30`, and `HERMES_MODEL_REQUEST_TIMEOUT_SECONDS=30` in `.env` so hung requests cut off and trigger the fallback chain in 30 seconds.

## Root-cause #21 — Vercel Serverless /tmp Storage Ephemerality on Interactive Kanbans
**Symptom:** Drag-and-drop card moves, comments, or task creations on Vercel Kanban apps (`hermes-stevenson-kanban.vercel.app`) reset / roll back to default state on fresh page reloads or cold starts.
**Cause:** Vercel Serverless Functions (`api/kanban.js`) write to `/tmp` which is ephemeral and isolated per lambda instance. Subsequent requests hitting different instances revert to the initial default state.
**Fix:** Connect Vercel Kanban backends to a persistent SQLite/JSON API endpoint or Vercel KV / Blob storage so all state mutations persist across cold starts.

## Root-cause #22 — Google OAuth Refresh Token Expiration in Testing Mode
**Symptom:** `google_token.json` fails with `HTTP Error 400: Bad Request` / `invalid_grant: Token has been expired or revoked`.
**Cause:** Google Cloud Console OAuth Consent Screen in "Testing" mode revokes refresh tokens every 7 days.
**Fix:**
1. Generate refresh token with `prompt='consent'` and `access_type='offline'`.
2. In Google Cloud Console -> OAuth Consent Screen, ensure user is listed under Test Users (or click Publish App for web apps) so the refresh token becomes permanent.

## Root-cause #23 — Systemd RestartSec=5 long-polling 409 Conflict cascade
**Symptom:** Gateway daemon logs `409 Conflict: terminated by other getUpdates request` on systemd restart, repeated 5 retries until `Updater made no getUpdates progress` fails.
**Cause:** `RestartSec=5` in systemd service file restarts the process before Telegram API releases the previous long-poll connection (which stays held open up to 30-50s).
**Fix:** Set `RestartSec=20` (or `30`) in systemd service files (`/etc/systemd/system/hermes-*.service`) so Telegram has time to drop the stale session before the new process connects.

## Root-cause #24 — Background Tool Loop Interruption & Zombie Bot Behavior
**Symptom:** User asks a direct question ("Where did you get that?", "Why aren't you answering?"), but bot ignores the question, executes background tools (generating Excel, registering cron jobs, making backups), and responds with unrelated completion messages.
**Cause:** Multi-step tool calls in conversation history cause the LLM (e.g. Gemini 3.6 Flash) to prioritize tool-loop completion over new user interjections unless explicitly constrained in the prompt.
**Fix:** Inject a mandatory User Interrupt & Context Priority Directive into `SOUL.md` / System Prompt for every profile:
```markdown
# ⚡ CRITICAL USER INTERRUPT & CONTEXT PRIORITY
1. User messages (questions, quotes, interjections) ALWAYS have top priority over background tool executions.
2. When the user asks a question or replies to a message, answer the question directly FIRST.
3. NEVER execute unrelated background tools or cron scripts instead of answering a direct user question.
```

## Root-cause #25 — Ecosystem Self-Heal & Journalctl Deep Audit for Silent Polling Deadlocks
**Symptom:** Service audit shows `systemctl is-active = 0` (ACTIVE), but bot fails to answer messages or responds with multi-minute delays.
**Cause:** Process-only health checks (`is-active`) give false positives when the systemd daemon is running but the internal Telegram `getUpdates` long-poll loop has deadlocked or hit retries exhaustion.
**Fix:** Extend ecosystem self-heal scripts (`ecosystem_self_heal_audit.py`) to parse the last 50 lines of `journalctl -u hermes-*.service` for silent deadlock signatures (`Conflict: terminated by other getUpdates request`, `could not recover after 5 retries`, `Updater made no getUpdates progress`) and force a self-healing restart when found.

## Root-cause #26 — Local Dual Long-Polling Hard-Lock & VPS-Only Master Architecture
**Symptom:** Telegram bot or profile gateway logs `409 Conflict: terminated by other getUpdates request` repeatedly because an instance is running on local Windows PC alongside Servarica 24/7 VPS (`stefan1`).
**Cause:** Local `config.yaml` profile configs have `telegram.enabled: true` or local watchdog/launcher scripts (`gateway_watcher.py`, `bot_watchdog.py`, `hermes_selfheal_launcher.vbs`, `start_agents.bat`) re-animate local `hermes gateway run` or legacy `_bot.py` processes on Windows startup/boot.
**Fix:**
1. **Hard-Lock Local Profile Configs:** Set `telegram.enabled: false` across ALL local Windows profile `config.yaml` files (`C:\Users\Stefan\AppData\Local\hermes\config.yaml` and `C:\Users\Stefan\AppData\Local\hermes\profiles\<profile>\config.yaml`). This ensures any local `hermes gateway run` command on Windows is completely blocked from polling Telegram.
2. **Neutralize Local Watchdogs/Launchers:** Replace legacy launcher/watchdog scripts in `AppData\Local\hermes\scripts\` and `...\gateway-service\` with no-op safety blocks (`sys.exit(0)` / `WScript.Quit`).
3. **Master Cloud Isolation:** 100% of Telegram long-polling runs on Servarica VPS (`stefan1` @ `38.49.219.217` / Tailscale `100.99.146.42`) via Systemd services (`hermes-*.service`).
4. **Kill Orphan Processes:** Scan `psutil.process_iter()` for `hermes_cli.main gateway run` on Windows and terminate any lingering PIDs.

## Root-cause #27 — Systemd HERMES_HOME Path Mismatch & Nested Profile Lookups
**Symptom:** Ghost Windows-like directories (`/root/C:\Users\Stefan\...`) appear on Linux VPS or sub-agent profiles crash when trying to locate their `config.yaml` or `memories/`.
**Cause:** In `/etc/systemd/system/hermes-<profile>.service`, setting `Environment=HERMES_HOME=/opt/hermes/profiles/<profile>` combined with `--profile <profile>` causes Hermes to look for nested profiles (`/opt/hermes/profiles/<profile>/profiles/<profile>`).
**Fix:** Always set `Environment=HERMES_HOME=/opt/hermes` across all systemd service units on VPS. The `--profile <profile>` flag will automatically resolve `/opt/hermes/profiles/<profile>` correctly without path duplication or ghost directory generation.

## Root-cause #28 — Anthropic OAuth 400 Extra Usage Block & Telegram Live Streaming Interruptions
**Symptom:** Main Telegram bot (@hermesstevensonbot) or other profiles experience mid-stream interruptions, delays, "give me a minute" stubs, or abort before finishing responses. Journalctl logs show `anthropic.BadRequestError: Error code: 400 - {'type': 'error', 'error': {'type': 'invalid_request_error', 'message': 'Third-party apps now draw from your extra usage, not your plan limits. Add more at claude.ai/settings/usage and keep going.'}}` and `ERROR agent.chat_completion_helpers: Streaming failed before delivery`.
**Cause:** Anthropic changed OAuth usage billing policies: 3rd-party OAuth clients draw only from extra prepaid usage credits, rejecting standard plan limits with HTTP 400. In Hermes Gateway, when streaming starts with an Anthropic primary model (`claude-fable-5` / `claude-sonnet-5`), the API aborts mid-stream, breaking the active Telegram stream before falling back.
**Fix:**
1. Switch primary profile model in `/opt/hermes/config.yaml` to `google/gemini-3.7-flash` (provider: `google`), maintaining Gonka24/OpenAI/OpenRouter in the fallback chain.
2. Ensure SSH user to Servarica VPS is `root` (`ssh root@38.49.219.217` / Tailscale `100.99.146.42`), not non-root users.
3. Verify persona configuration in `USER.md` aligns with the profile (Hermes = Chief Orchestrator, not Wendy Rhoades which is Liz Harper's archetype).
4. Restart systemd unit (`systemctl restart hermes-default`) and verify status.

## Root-cause #29 — Long-Lived Session Context Bloat (300k+ Tokens) & Runaway Autonomous Tool Loops
**Symptom:** Bot in Telegram takes 3+ minutes to answer simple questions, endlessly shows "typing…", or enters a multi-step tool loop (10-140+ tool calls) trying to execute historical background tasks instead of responding immediately.
**Cause:** Telegram DM session in `state.db` (`gateway_routing`) has accumulated hundreds/thousands of messages (1MB+ text, 300k+ tokens) over weeks of operations without session resets. The LLM receives the huge history on every turn, causing 20-30s inference latency per step and hallucinating unfinished tool tasks from past context.
**Fix:**
1. Send `/new` or `/reset` in Telegram DM, or clear `gateway_routing` for that chat in `state.db` (`DELETE FROM gateway_routing WHERE session_key = 'agent:main:telegram:dm:<chat_id>'`).
2. Long-term memories, case histories (`memory_v2`), and Pinecone vector store remain 100% intact, while turn latency drops back to 1.5–2 seconds.

## Root-cause #30 — Subprocess Ping/SSH Console Window Popups on Windows Background Watchdogs
**Symptom:** Black command prompt windows flash on the Windows desktop every 30–60 seconds during background failover or VPS availability checks.
**Cause:** Background scripts running under `pythonw.exe` execute `subprocess.run(["ping", ...])` or `subprocess.run(["ssh", ...])` without `creationflags=0x08000000` (`CREATE_NO_WINDOW`).
**Fix:**
1. Use pure Python sockets for health checks (`socket.create_connection((ip, 22), timeout=3)`), which uses zero subprocesses and is 100% silent and instantaneous.
2. If subprocess execution is required, always pass `creationflags=0x08000000` (`CREATE_NO_WINDOW`).

## Root-cause #31 — Resilient Cloud Failover (Zero-Downtime Rule)
**Symptom:** Local fallback bots shut down at a preset target time (e.g. midnight) while the remote cloud VPS is still undergoing maintenance, causing total bot blackout.
**Cause:** Failover script unconditionally terminates local gateway processes upon reaching the scheduled timestamp before verifying that remote VPS services are actually reachable and active.
**Fix:** Keep local fallback gateways 100% active and polling until remote VPS port 22 is confirmed online via socket check. Only after remote connectivity is verified, perform bidirectional file sync (`mtime` newest-wins), push backup to GitHub, terminate local gateways, and restart cloud systemd daemons.

## Root-cause #29 — Bloated Local Telegram Session Context & 3-Minute Tool Loop Delays
**Symptom:** Telegram bot answers in 3–6 minutes locally on Windows, whereas on Servarica VPS it responds in 2–3 seconds. Logs show `last_prompt_tokens > 350,000` (e.g. 385k tokens), `latency=25-35s` per LLM step, and 15–20 repeated tool calls before returning a text answer.
**Cause:** Stale historical Telegram DM sessions accumulated 1,000+ messages (1.2+ MB of text with raw tool outputs) in `profiles/<bot>/state.db` since initial local testing. On every incoming message, the entire 385k-token history is sent to Gemini, which triggers high inference latency and causes the model to confuse historical tool turns with pending obligations.
**Fix:**
1. In Telegram chat with the bot, send `/new` or `/reset` to start a fresh, lean session.
2. To batch-reset for all local profiles without touching long-term memory: clear `gateway_routing` in `state.db` (`DELETE FROM gateway_routing;`). Long-term memory in `MEMORY.md`, `memory_v2`, and Pinecone remains 100% intact, while prompt size drops to ~3k tokens (restoring 2-second response speeds).

## Root-cause #30 — Windows Python `shutil.copytree` Literal `NUL` File Collisions
**Symptom:** Backup scripts running `shutil.copytree` fail with `shutil.Error: ['NUL' and '.../NUL' are the same file]`.
**Cause:** Previous terminal commands using Windows `> NUL` inside MSYS/bash shell created literal files named `NUL` inside folders. Windows treats `NUL` as a reserved device name, causing `copytree` to fail.
**Fix:** Pass an explicit ignore filter to `shutil.copytree`: `ignore=shutil.ignore_patterns("NUL", "*.lock", "*.tmp", "__pycache__", "*-shm", "*-wal")`.

## Root-cause #31 — Telegram Adapter Allowlist vs Pairing & Sales Bot DM Policy
**Symptom:** Inbound Telegram messages from team members or prospective leads are silently dropped. Logs show `WARNING hermes_plugins.telegram_platform.adapter: [Telegram] Blocked unauthorized user <id> in chat <id>`.
**Cause:** The modern Hermes Telegram adapter enforces `platforms.telegram.allow_from` or approved entries in `platforms/pairing/telegram-approved.json`. If `platforms.telegram` is missing `allow_from` and the user is not in `telegram-approved.json`, all incoming DMs are rejected.
**Fix:**
1. Populate all known team user IDs (`330656040`, `1022586369`, `149598904`, etc.) into `platforms/pairing/telegram-approved.json` across all profiles.
2. For public-facing B2B sales agents (e.g. Richard Marlowe `@richnavobot`), configure `platforms.telegram.dm_policy: open` and `platforms.telegram.allow_from: ["*"]` in `config.yaml` so external client inquiries are never blocked, while setting `group_response_mode: mention` to protect group chats.

## Root-cause #32 — Zero-Downtime Cloud Failover & Silent Socket VPS Health Probing
**Symptom:** Black console windows flash on Windows desktop every 30 seconds during cloud VPS outages, or bots go completely silent during planned failovers.
**Cause:**
1. Scheduled failover scripts shut down local gateways before confirming the cloud VPS is physically online and responsive.
2. VPS health checks execute external console binaries (`subprocess.run(["ping", ...])`) without `CREATE_NO_WINDOW` (0x08000000).
**Fix:**
1. **Never shut down local gateways prematurely:** Keep local gateways active in Telegram until the cloud VPS is confirmed online.
2. **Pure Socket Probing:** Check VPS availability silently in pure Python with zero subprocesses:
```python
import socket
def is_vps_online(ip, port=22, timeout=3):
    try:
        s = socket.create_connection((ip, port), timeout=timeout)
        s.close()
        return True
    except Exception:
        return False
```
3. Once the socket connection succeeds, run full 2-way differential sync (`ecosystem_bidirectional_sync.py`), commit master backup to GitHub (`navo-infra`), terminate local gateways, and restart cloud systemd units seamlessly.

## Root-cause #29 — Bloated Local Telegram Session Context & 3-Minute Tool Loop Delays
**Symptom:** Telegram bot answers in 3–6 minutes locally on Windows, whereas on Servarica VPS it responds in 2–3 seconds. Logs show `last_prompt_tokens > 350,000` (e.g. 385k tokens), `latency=25-35s` per LLM step, and 15–20 repeated tool calls before returning a text answer.
**Cause:** Stale historical Telegram DM sessions accumulated 1,000+ messages (1.2+ MB of text with raw tool outputs) in `profiles/<bot>/state.db` since initial local testing. On every incoming message, the entire 385k-token history is sent to Gemini, which triggers high inference latency and causes the model to confuse historical tool turns with pending obligations.
**Fix:**
1. In Telegram chat with the bot, send `/new` or `/reset` to start a fresh, lean session.
2. To batch-reset for all local profiles without touching long-term memory: clear `gateway_routing` in `state.db` (`DELETE FROM gateway_routing;`). Long-term memory in `MEMORY.md`, `memory_v2`, and Pinecone remains 100% intact, while prompt size drops to ~3k tokens (restoring 2-second response speeds).

## Root-cause #30 — Windows Python `shutil.copytree` Literal `NUL` File Collisions
**Symptom:** Backup scripts running `shutil.copytree` fail with `shutil.Error: ['NUL' and '.../NUL' are the same file]`.
**Cause:** Previous terminal commands using Windows `> NUL` inside MSYS/bash shell created literal files named `NUL` inside folders. Windows treats `NUL` as a reserved device name, causing `copytree` to fail.
**Fix:** Pass an explicit ignore filter to `shutil.copytree`: `ignore=shutil.ignore_patterns("NUL", "*.lock", "*.tmp", "__pycache__", "*-shm", "*-wal")`.

## Root-cause #31 — Telegram Adapter Allowlist vs Pairing & Sales Bot DM Policy
**Symptom:** Inbound Telegram messages from team members or prospective leads are silently dropped. Logs show `WARNING hermes_plugins.telegram_platform.adapter: [Telegram] Blocked unauthorized user <id> in chat <id>`.
**Cause:** The modern Hermes Telegram adapter enforces `platforms.telegram.allow_from` or approved entries in `platforms/pairing/telegram-approved.json`. If `platforms.telegram` is missing `allow_from` and the user is not in `telegram-approved.json`, all incoming DMs are rejected.
**Fix:**
1. Populate all known team user IDs (`330656040`, `1022586369`, `149598904`, etc.) into `platforms/pairing/telegram-approved.json` across all profiles.
2. For public-facing B2B sales agents (e.g. Richard Marlowe `@richnavobot`), configure `platforms.telegram.dm_policy: open` and `platforms.telegram.allow_from: ["*"]` in `config.yaml` so external client inquiries are never blocked, while setting `group_response_mode: mention` to protect group chats.

## Root-cause #32 — Cloud VPS Outage Failover with Scheduled 2-Way Sync & GitHub Backup
**Symptom:** Cloud VPS (Servarica) undergoes hosting maintenance, knocking 24/7 Telegram gateways offline.
**Fix:** Run `servarica_failover_manager.py` locally on Windows via `pythonw.exe` (CREATE_NO_WINDOW) to host all active gateways temporarily. Set a scheduled transition timer (e.g. 01:00 AM) that gracefully terminates local gateways, pushes newly created cron jobs and config changes up to VPS via SCP/SSH, pulls complete configs for internal personas (Harrison, Aeon, Archie) to PC, triggers `ecosystem_master_backup.py` to push a full snapshot to GitHub (`navo-infra`), restarts VPS systemd services, and sends an automated completion report to Stefan via Telegram.


## Root-cause #29 — Cloud VPS Host Reachability & Tailscale Node Status Diagnostic
**Symptom:** Telegram bot (@hermesstevensonbot or persona bots) suddenly stops responding completely, but local Windows logs and configs show no recent changes.
**Cause:** The 24/7 cloud VPS host (`stefan1` @ `38.49.219.217`) is offline (hypervisor reboot, host outage, or maintenance on Servarica).
**Diagnostic & Verification Sequence:**
1. **Safe Telegram API Probe:** Check `https://api.telegram.org/bot<TOKEN>/getMe` and `/getWebhookInfo` to verify token validity and inspect `pending_update_count`. NEVER use `getUpdates` (Root-cause #3).
2. **Tailscale Node Status:** Run `tailscale status` locally on Windows. Check the status line for `stefan1` (e.g. `offline, last seen 1h ago`).
3. **VPS Reachability:** Test ping/SSH to public IP (`38.49.219.217`) and Tailscale IP (`100.99.146.42`).
4. **Resolution:** If the host is unreachable, verify VPS instance status in Servarica control panel. If necessary, provide an immediate temporary fallback by enabling local Windows polling (`telegram.enabled: true`) only while cloud is down, switching back once VPS recovers to prevent 409 conflict.

## Root-cause #30 — Timed Local Failover During Cloud VPS Maintenance with 0-Conflict Reconnect
**Symptom:** Cloud VPS hosting 24/7 Telegram gateways goes offline for scheduled maintenance (e.g. 6 hours). User needs bots running locally on Windows PC during the maintenance window, but must automatically fail over back to cloud VPS at midnight (00:00) without creating 409 Conflict loops or leaving orphan pollers.
**Pattern:**
1. **Local Activation:**
   - Enable `telegram.enabled: true` and `platforms.telegram.enabled: true` across all needed profiles via `hermes --profile <p> config set telegram.enabled true`.
   - Launch local gateways silently using `CREATE_NO_WINDOW` (0x08000000) / `pythonw.exe`.
2. **Timed Failover Watchdog (`servarica_failover_manager.py`):**
   - Calculate target timestamp (e.g. 00:00:00 Kyiv time) and monitor local gateway processes.
   - At target timestamp:
     a) Terminate all local gateway processes (`proc.terminate()` / `taskkill`).
     b) Set `telegram.enabled: false` and `platforms.telegram.enabled: false` across all local profile configs.
     c) Poll VPS connectivity via ping/SSH until reachable.
     d) Issue remote `systemctl restart hermes-*.service` commands on VPS.
     e) Send an automated direct Telegram confirmation message to Stefan (`330656040`) from `@hermesstevensonbot` confirming the handoff is complete.

## Root-cause #31 — Bloated Local Telegram Session Context & 3-Minute Tool Loop Delays
**Symptom:** Telegram bot answers in 3–6 minutes locally on Windows, whereas on Servarica VPS it responds in 2–3 seconds. Logs show `last_prompt_tokens > 350,000` (e.g. 385k tokens), `latency=25-35s` per LLM step, and 15–20 repeated tool calls before returning a text answer.
**Cause:** Stale historical Telegram DM sessions accumulated 1,000+ messages (1.2+ MB of text with raw tool outputs) in `profiles/<bot>/state.db` since initial local testing. On every incoming message, the entire 385k-token history is sent to Gemini, which triggers high inference latency and causes the model to confuse historical tool turns with pending obligations.
**Fix:**
1. In Telegram chat with the bot, send `/new` or `/reset` to start a fresh, lean session.
2. To batch-reset for all local profiles without touching long-term memory: clear `gateway_routing` in `state.db` (`DELETE FROM gateway_routing;`). Long-term memory in `MEMORY.md`, `memory_v2`, and Pinecone remains 100% intact, while prompt size drops to ~3k tokens (restoring 2-second response speeds).

## Root-cause #32 — Windows Python `shutil.copytree` Literal `NUL` File Collisions
**Symptom:** Backup scripts running `shutil.copytree` fail with `shutil.Error: ['NUL' and '.../NUL' are the same file]`.
**Cause:** Previous terminal commands using Windows `> NUL` inside MSYS/bash shell created literal files named `NUL` inside folders. Windows treats `NUL` as a reserved device name, causing `copytree` to fail.
**Fix:** Pass an explicit ignore filter to `shutil.copytree`: `ignore=shutil.ignore_patterns("NUL", "*.lock", "*.tmp", "__pycache__", "*-shm", "*-wal")`.

## Root-cause #33 — Telegram Adapter Allowlist vs Pairing & Sales Bot DM Policy
**Symptom:** Inbound Telegram messages from team members or prospective leads are silently dropped. Logs show `WARNING hermes_plugins.telegram_platform.adapter: [Telegram] Blocked unauthorized user <id> in chat <id>`.
**Cause:** The modern Hermes Telegram adapter enforces `platforms.telegram.allow_from` or approved entries in `platforms/pairing/telegram-approved.json`. If `platforms.telegram` is missing `allow_from` and the user is not in `telegram-approved.json`, all incoming DMs are rejected.
**Fix:**
1. Populate all known team user IDs (`330656040`, `1022586369`, `149598904`, etc.) into `platforms/pairing/telegram-approved.json` across all profiles.
2. For public-facing B2B sales agents (e.g. Richard Marlowe `@richnavobot`), configure `platforms.telegram.dm_policy: open` and `platforms.telegram.allow_from: ["*"]` in `config.yaml` so external client inquiries are never blocked, while setting `group_response_mode: mention` to protect group chats.


