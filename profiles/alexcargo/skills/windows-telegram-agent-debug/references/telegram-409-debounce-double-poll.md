# Telegram bot 409: debounce double-poll + key 403 (Richard session)

## Symptom
Richard (and Alistair/Ben) bot alive, single process, but:
- Logs `http attempt N failed: HTTP Error 409: Conflict` every cycle.
- Replies with stub: "Richard here — briefly lost the line to the desk. One moment, try that again?"
- User PMs go unanswered ("тупит", "снова молчит").

## Root cause A — second getUpdates inside debounce (real 409)
Source shell (Richard -> copied to Alistair -> Ben) has:
```python
while True:
    updates = tg_request("getUpdates", token, {"offset": offset, "timeout": 30}, timeout=40)  # MAIN poll
    ...
    if pending:
        time.sleep(3.5)
        extra = tg_request("getUpdates", token, {"offset": offset, "timeout": 3}, timeout=10)  # SECOND poll -> 409
        ...
```
Two concurrent long-polls on one token = 409. Fix: delete the inner
getUpdates block; keep time.sleep(3.5) + FLUSH. Main loop reclaims late
messages on next tick.

## Root cause B — wrong/blocked LLM key (403, not 409)
After fixing 409 the bot still replied with the stub. Log showed:
```
[Richard] model tencent/hy3:free failed: HTTP Error 403: Forbidden; trying next
[Richard] model poolside/laguna-s-2.1:free failed: HTTP Error 403: Forbidden; trying next
[Richard] agent error: HTTP Error 403: Forbidden
```
_fresh_nous_key() prioritised auth.json (providers.nous.access_token),
which was stale/blocked by Nous. Hermes own key (in hermes/.env,
NOUS_API_KEY, len 1777, eyJhbGci...) worked fine.

Fix: write the working Hermes key into the bots .env.local NOUS_API_KEY,
and change _fresh_nous_key() to return os.environ["NOUS_API_KEY"] FIRST
(already loaded from .env.local by _load_env()), falling back to
auth.json only if empty. Note: Hermes and the entity bots run DIFFERENT
models/default providers; the Nous key is shared infra, not a model choice.

## PID-lock phantom duplicate (why the fix did not take)
Launcher prints `already running (pid N) — exit to avoid duplicates` and dies,
while the OLD broken instance keeps polling. Cause: stale PID in <bot>.lock
or a leftover process the launcher did not track.

Kill-all before relaunch (PowerShell -File, NOT WMI -like):
```powershell
Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*richard_bot.py*' } | ForEach-Object {
    "PID=$($_.ProcessId)"; Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue
}
@('C:\Users\Stefan\AppData\Local\hermes\entities\richard.lock') | ForEach-Object { if (Test-Path $_) { Remove-Item $_ -Force } }
```
Then launch exactly one via uv pythonw with `>> richard_run.log 2>&1` so the
log shows `bot started, polling Telegram...`.

## Debug order that worked
1. Get-Process on bot PID + read its log tail (look for 409 vs 403).
2. 409 + single process + getMe ok => inner double-poll (5g). Remove it.
3. 403 on every model => key bad. Source working key from .env.local,
   prioritise env over auth.json.
4. Stub replies persist after code fix => PID-lock phantom (5i). Kill all,
   clear lock, relaunch one.
5. NEVER probe a live bots token with manual getUpdates (5h) — it eats the
   users pending update and 409s the bot.
