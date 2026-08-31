# Telegram bot 409 — self-spawn + parallel watchdog double-instance (Liz Harper case, 2026-07-27)

## Symptom
Bot is silent in Telegram. Log shows an endless loop of:
```
poll err: HTTP Error 409: Conflict
409 -> dropped pending updates / ghost sessions
```
The bot holds the token but a SECOND long-poll on the same token exists → Telegram
rejects the second with 409, and (because the bot's 409-handler sleeps 60s and
retries) it stays silent.

## Root cause (TWO sources of a twin long-poll, NOT two different bot scripts)
1. **Self-spawn.** Launching `liz_loop.py` via a venv-`python` parent produced a
   CHILD process that ran the same `liz_loop.py` via the `uv`-launcher python.
   Diagnostic proof: the child's `PPID` equals the parent bot PID, and the child
   command line is the same `liz_loop.py` under a different interpreter
   (`...Roaming\uv\python\cpython-3.11-windows...\python.exe`).
2. **Parallel cron watchdog.** A "Bot Watchdog" cron job (`liz_watchdog.py`, every
   10 min) ALSO launches a `liz_loop.py` on the same token. Even after you
   `cronjob action=pause` that job, one already-queued run can still spawn a twin
   before the pause takes effect.

## Windows diagnostic (run as a .ps1 — MSYS mangles `$_` in inline PowerShell)
```powershell
Get-CimInstance Win32_Process | Where-Object { ($_.Name -eq 'python.exe' -or $_.Name -eq 'pythonw.exe') -and $_.CommandLine -match 'liz_loop' } | ForEach-Object {
    Write-Host ($_.ProcessId.ToString() + ' PPID=' + $_.ParentProcessId.ToString() + ' :: ' + $_.CommandLine)
}
```
If you see TWO `liz_loop` rows and one `PPID` == the other's PID → self-spawn.
If you see rows from BOTH a venv path and the `uv` path with different PIDs and
unrelated PPIDs → a watchdog/launcher spawned the twin.

## Fix sequence
1. Kill ALL `liz_loop` PIDs (kill via PID; never match on the bare profile path
   `Google\Chrome\User Data` — that kills the user's visible Chrome, not the bot).
2. Remove the stale lock: `entities/liz.lock` (always clear it after a kill so the
   single instance can re-acquire cleanly).
3. `cronjob action=pause` the "Bot Watchdog" job AND verify no `liz_watchdog`
   process is alive (re-run the diagnostic).
4. Launch EXACTLY ONE instance (venv `python` + `CREATE_NO_WINDOW` flags
   `0x00000008 | 0x08000000`; log redirected to a file). Wait ~70s, re-run the
   diagnostic. If a second PID reappears with PPID == your bot PID, the bot is
   self-spawning — remove the re-exec (or launch via the `uv` launcher directly so
   no child fork happens).
5. Confirm: exactly one PID, no 409 in the log, and the bot answers a test message.

## User preference — NO unsolicited digests
Stefan rejected proactive/hourly "digest" messages from Liz
("регулярные сводки мне не нужны"). If a persona bot has a `proactive_loop` /
hourly digest thread, disable it (comment out the
`threading.Thread(target=proactive_loop, ...)` launch AND the function body).
Persona bots answer only when addressed — they must not push scheduled summaries
on their own initiative. (A weekly order-prep digest sent by the Hermes MAIN agent
via a user-requested cron is separate and allowed — that is not the bot's own
initiative.)
