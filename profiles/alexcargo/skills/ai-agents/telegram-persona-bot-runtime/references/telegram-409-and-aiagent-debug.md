# Telegram 409 + AIAgent-core debugging (from the Liz Harper build)

Condensed from a multi-hour debug of `liz_agent.py` (AIAgent-core Telegram bot).

## 1. Two 409 Conflict footguns

A Telegram token may have ONLY ONE active long-poll consumer. A 2nd parallel
`getUpdates` → HTTP 409, bot never recovers.

**Footgun A — HTTP helper retries on 409.** A `_http_json` wrapper doing
`for _ in range(3): urlopen(...) except: sleep(2); retry` raises 409 as
`urllib.error.HTTPError` and the RETRY opens a SECOND parallel long-poll →
permanent 409. FIX: on 409, `raise` immediately (no retry). In the poll loop:
catch 409, call `close` once to reset all sessions, continue.
```python
try:
    upd = tg_request("getUpdates", token, {"offset": off, "timeout": 30}, timeout=40)
except Exception as e:
    if "409" in str(e):
        _http_json(f"https://api.telegram.org/bot{token}/close", method="GET", timeout=10)
        log("409 -> closed ghost sessions")
    time.sleep(5)
```
`close` resets every pending long-poll on the token (kills ghosts left by a
killed previous instance). It only works while NOT actively long-polling — the
loop above pauses during close, which is fine.

**First diagnostic when 409 won't die:** call `getMe` with the token your bot
actually loaded and check the `username`/`id`. If it's NOT your bot (e.g. it
resolves to `hermesstevensonbot` when you expected `lizharperbot`), your token
resolution is wrong — you're long-polling on the wrong token and colliding with
that bot's own process. Fix the token source, don't chase ghosts.

**Footgun B — multiple copies running.** Old `pythonw` instances you thought you
killed keep their long-poll alive (~60s). New copy → instant 409. Self-heal:
kill ALL `pythonw` whose commandline ends with your bot script, then `close`,
then start ONE. Verify `count==1` before declaring victory.

## 2. Single-instance guard: Windows named mutex (not PID file)

`os.open(LOCK_FILE, O_CREAT|O_EXCL)` has a TOCTOU race when several copies boot
within ~1s: all read empty/stale lock, all pass "is old pid alive?", all start →
409 again. Use a named mutex (atomic, auto-released on process death):
```python
import ctypes
kernel32 = ctypes.windll.kernel32
mutex = kernel32.CreateMutexW(None, False, "Local\\LizHarperAgentSingleton")
if mutex == 0 or kernel32.GetLastError() == 183:  # ERROR_ALREADY_EXISTS
    sys.exit(0)
_acquire_lock._mutex = mutex   # keep ref so GC doesn't release
```
Use **`Local\`** namespace, NOT `Global\` — `Global\` needs SeCreateGlobalPrivilege
(admin) and fails silently in a non-admin session, falling through to the racy
file lock.

## 3. No black console window (Windows)

Use BASE `pythonw.exe` (NOT venv `python.exe` — uv-launcher spawns conhost).
For process checks/kills prefer `ctypes.CreateToolhelp32Snapshot` over
`powershell.exe`/`tasklist` (those spawn conhost). Watchdog: one `pythonw`
checks mutex/tasklist and relaunches if dead. Autostart via
`HKCU\...\CurrentVersion\Run` → `wscript launcher.vbs` (hidden), no admin.
Scheduled-task registration needs admin (Access denied) — use HKCU Run + cron
self-heal instead.

## 4. AIAgent-core variant (reuse hermes, don't write a new core)

Run `run_agent.AIAgent` in a SEPARATE process (Hermes stays orchestrator):
```python
sys.path.insert(0, HERMES_AGENT_DIR)
from hermes_cli.runtime_provider import resolve_runtime_provider
rt = resolve_runtime_provider(requested="nous")   # reuses host's Nous key
from run_agent import AIAgent
agent = AIAgent(model="tencent/hy3:free", api_key=rt.get("api_key"),
               base_url=rt.get("base_url"), provider="nous",
               requested_provider="nous", enabled_toolsets=["file","memory"],
               quiet_mode=True, ephemeral_system_prompt=LIZ_SYSTEM, session_db=...)
ans = agent.run_conversation(user_text)["final_response"]
```
Gotchas:
- `AIAgent.__init__` takes `api_key/base_url/provider/model/enabled_toolsets/
  ephemeral_system_prompt/requested_provider/session_db/fallback_model` — NOT `runtime=`.
- `run_conversation(user_message)` takes `user_message/system_message/
  conversation_history/...` — NOT `max_turns=` (that's `agent.max_turns` in
  config.yaml, not a call arg).
- Wrap creation+call in try/except so the bot never dies on a bad turn.

## 5. Process-detection false positive (debugging trap)

Grepping `Win32_Process` for your bot name: your OWN powershell/terminal command
contains the script name in its `CommandLine` and matches itself — reporting
"4 watchdogs / 7 agents" that don't exist. Count ONLY
`Name -eq "pythonw.exe" -and CommandLine -like "*your_bot.py*"` for the real count.

## 6. Hermes session-drop rule (operator side)

When operating/debugging these bots via the terminal: any command/check >30s must
NOT use `sleep`/`Start-Sleep` in the MAIN session — the Hermes↔Telegram session
drops ("Orphan recovery / gateway restored"). Use `terminal(background=true,
notify_on_complete=true)` + poll, or `process(action='wait', timeout=...)`.
Keep main-session commands <20s. (The gateway process itself stays alive; it's
the agent's reply channel that blips.)

## 7. Token-resolution footgun: bot sends from the WRONG account

Multi-bot hosts leak the wrong token. Liz's one-shot `liz_say.py` sent status
from `hermesstevensonbot` (Hermes) instead of `lizharperbot` because of TWO bugs:

1. **Path-with-spaces `cd` silently fails** in git-bash/MSYS when the bot dir
   has spaces (`My Drive\Equity\My Biz\...`). `os.getcwd()` then stays at
   `~`/home, so `HERE = dirname(abspath(__file__))` still works (uses `__file__`,
   not cwd) — BUT a script that does `cd && python script.py` and then reads
   `os.path.join(os.getcwd(), ".env.local")` reads the wrong dir.
2. **Token fallback order** listed the shared Hermes `.env` (`TELEGRAM_BOT_TOKEN`)
   right after the bot's own `.env.local`. If the bot's `.env.local` wasn't read
   first, the Hermes token was used → messages went out as Hermes, and (worse)
   the live bot then long-polled on Hermes's token → 409 with Gateway.

FIX (defensive): hardcode the bot's `.env.local` absolute path, and break the
fallback loop on first hit:
```python
LIZ_ENV = r"C:\Users\Stefan\My Drive\Equity\My Biz\My companies\...\Liz Harper\...\liz_agent\.env.local"
tok = None
for f in (LIZ_ENV, os.path.join(HERE, ".env.local"), os.path.join(HERMES_HOME, ".env")):
    if os.path.exists(f):
        for line in open(f, encoding="utf-8"):
            if line.strip().startswith("TELEGRAM_BOT_TOKEN="):
                tok = line.strip().split("=", 1)[1].strip().strip('"'); break
    if tok: break
```
Always confirm with `getMe` (see §1) that the resolved token is YOUR bot.
