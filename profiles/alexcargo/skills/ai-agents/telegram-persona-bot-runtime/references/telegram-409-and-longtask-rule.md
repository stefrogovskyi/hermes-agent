# Telegram bot 409 + long-task session-drop rules (2026-07-26, Liz upgrade)

## 1. THIRD 409 cause — retry-on-HTTPError re-issues `getUpdates`

Symptom: bot logs `HTTP Error 409: Conflict` every ~30-40s forever, even with a
single process and a valid single-instance lock. Root cause found the hard way:

A generic HTTP helper like
```python
for _ in range(3):
    try:
        return urlopen(req, timeout=...)
    except Exception as e:
        log(e); time.sleep(2)
```
catches the `HTTPError` that Telegram raises on 409 and **retries** — which opens a
SECOND parallel `getUpdates` long-poll on the same token. Telegram now sees two
concurrent long-polls -> 409 -> retry -> second poll -> 409 ... infinite loop. The
single-instance lock (PID file) does NOT help, because the duplicate is spawned
by the same process, sequentially, inside the retry loop.

Fix (apply in the HTTP helper, not just the caller):
```python
except urllib.error.HTTPError as e:
    if e.code == 409:
        raise                      # do NOT retry -- caller does telegram close()
    if e.code == 429:
        time.sleep(2 ** (attempt + 1)); continue   # back off, then retry
    ...
```
On 409 the caller should call `bot<token>/close` (resets all server-side long-poll
sessions) and continue the loop -- NOT retry the request inline.

Also: `close` does not always clear a ghost from a *killed* previous instance quickly;
if 409 persists with one process, the earlier copies' long-polls may still be held by
Telegram for up to ~60s. Wait it out or call `close` at startup.

## 2. Silent token swap on spaces-in-path (bot sends as the WRONG account)

Symptom: a one-shot `sendMessage` "works" but arrives from `@hermesstevensonbot`
instead of `@lizharpbot` (or vice-versa). Root cause:
```python
os.chdir("C:/Users/Stefan/My Drive/Equity/My Biz/.../Liz Harper/...")  # spaces!
tok = read_first(".env.local") or read_fallback("C:/.../hermes/.env")
```
`cd` with unquoted spaces in git-bash/MSYS can silently fail, so `os.getcwd()` is the
home dir, `.env.local` is not found, and the FALLBACK (Hermes `.env`) token is used.
The bot then polls/sends under the wrong token -> 409 vs the real owner, or messages
from the wrong identity.

Fix: resolve the token config from an **absolute path** baked into the script
(`HERE = os.path.dirname(os.path.abspath(__file__))`), never from `os.getcwd()`.
In one-off test scripts, hardcode the absolute `.env.local` path too. Verify with
`getMe` before sending.

## 3. Long foreground commands drop the Hermes<->Telegram session ("Orphan recovery")

User rule (Stefan, 2026-07-26): any command/check >~30-60s MUST NOT use `sleep` /
`Start-Sleep` in the MAIN terminal session -- the session appears to "drop" and shows
"Orphan recovery / shlyuz vosstanovlen". The gateway process itself stays alive; it is
the assistant's long-held main-session command that the transport times out.

Rule for this skill's run/maintain work:
- Use `terminal(background=true, notify_on_complete=true)` + poll, or
  `process(action='wait', timeout=...)` for anything long.
- Keep main-session commands short (<20s). A 40-60s `sleep` before a log check is the
  classic trigger -- split it: launch in background, then a short separate check.
- Do NOT confuse this with the gateway actually crashing -- verify `gateway run`
  process is alive before assuming a crash.

## 4. Single-instance watchdog pattern that survived (Liz)

- Watchdog = separate `pythonw` process, single-instance via its own lock file.
- Every ~20s: if `liz.lock` absent or its PID dead -> spawn exactly ONE
  `pythonw liz_agent.py` with `creationflags=0x00000008 | 0x08000000`
  (DETACHED + CREATE_NO_WINDOW) so no console window spawns.
- Autostart: `HKCU\Software\Microsoft\Windows\CurrentVersion\Run` ->
  `pythonw "<abs path>\liz_agent_watchdog.py"` (no admin needed).
- The agent itself also holds `liz.lock` (atomic `O_CREAT|O_EXCL`); the watchdog checks
  it rather than scanning process command lines (scanning `Where-Object {$_ -like
  '*liz_agent*'}` ALSO matches your own powershell command text -> false "4 copies").
