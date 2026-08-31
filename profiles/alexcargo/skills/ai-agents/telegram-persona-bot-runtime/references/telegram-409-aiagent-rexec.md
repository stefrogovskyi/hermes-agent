# 409 Conflict on AIAgent-core persona bots (liz_loop.py class)

## Symptom
Bot is silent in Telegram. Log shows repeating `poll err: HTTP Error 409: Conflict`
on every getUpdates, even though only ONE bot process appears in Task Manager.

## Root cause (this session, Stefan / Liz Harper bot)
Two long-poll consumers on the SAME token, both spawned by the launch itself:

1. **AIAgent-core re-exec leaves a zombie parent.** `liz_loop.py` re-execs onto the
   uv base python (`C:\Users\Stefan\AppData\Roaming\uv\python\cpython-3.11-windows-x86_64-none\python.exe`)
   at startup (the hermes `run_agent.AIAgent` core forces a bpython/pythonw re-exec for
   console-free operation). If you launched it via the **venv** python first
   (`...hermes-agent\venv\Scripts\python.exe`), the venv process stays alive as the
   PARENT while the uv-python child does the real long-poll. You now have TWO live
   getUpdates on one token -> 409.
2. **A parallel cron `watchdog` bot** (`Liz Bot Watchdog`, every 10m) also spawned the
   bot (via `liz_watchdog.py` -> uv python). Two independent launchers = two copies.

Note: `deleteWebhook?drop_pending_updates=true` / `getUpdates?offset=-1` does NOT clear a
**long-poll** 409 — Telegram holds the old getUpdates connection for ~60s and the bot
keeps reconnecting every ~20s, so the ghost never expires. Kill ALL copies, wait 60-75s
dead (no process at all), THEN start exactly one.

## Fix
- **Launch via pythonw (uv base) directly**, never via the venv python:
  ```python
  PY = r"C:\Users\Stefan\AppData\Roaming\uv\python\cpython-3.11-windows-x86_64-none\pythonw.exe"
  subprocess.Popen([PY, BOT], cwd=HERE, stdout=lf, stderr=lf,
                   creationflags=0x00000008 | 0x08000000, close_fds=True)
  ```
  Because the process is already on uv-python, the core's re-exec is a no-op -> no zombie
  parent -> exactly one long-poll.
- **Remove/disable the duplicate cron watchdog** for that bot (it double-spawns). Use
  `cronjob action=remove` (or pause) for the `Liz Bot Watchdog` job; rely on a single
  launch, or on the gateway if it manages the entity.
- **Cold restart sequence** (background script, ~100s):
  1. kill every `liz_loop` process (loop until 0, with 2s gaps);
  2. clear `entities/liz.lock`;
  3. `deleteWebhook` + `getUpdates?offset=-1` to drop any ghost;
  4. `time.sleep(75)` so all held connections expire;
  5. launch ONE via pythonw;
  6. verify `Get-CimInstance ... CommandLine -match 'liz_loop'` count == 1 and log shows
     no new 409 after ~20s.

## Detect duplicate spawn quickly (PowerShell, Windows path, not /c/)
```powershell
Get-CimInstance Win32_Process | Where-Object {
  ($_.Name -eq 'python.exe' -or $_.Name -eq 'pythonw.exe') -and $_.CommandLine -match 'liz_loop'
} | ForEach-Object { Write-Host ($_.ProcessId.ToString() + ' ppid=' + $_.ParentProcessId + ' :: ' + $_.CommandLine) }
```
If you see BOTH a venv-python parent AND a uv-python child -> that's the zombie-parent trap.

## MSYS/PowerShell gotchas on this host
- Use Windows paths (`C:\Users\...`), NOT MSYS `/c/Users/...` — `search_files` and many
  tools mangle `/c/` and fail with "No such file".
- Don't inline PowerShell with `$_` in a bash `terminal` call — MSYS substitutes into the
  path. Write a `.ps1` file and run `powershell -NoProfile -ExecutionPolicy Bypass -File x.ps1`.
- `tasklist /FI` works but `Get-CimInstance Win32_Process` is more reliable for cmdline match.
