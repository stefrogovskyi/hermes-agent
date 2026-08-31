# Liz 409 — external second consumer (2026-07-27 session)

## Symptom
`liz_loop.py` (single process, PID verified unique) loops `HTTP Error 409: Conflict`
forever. Gateway does NOT hold the Liz token (checked `.env`, `gateway_state.json`,
gateway cmdline — no `8857115619`). No other local python process contains the
Liz token. Even after **5 full minutes of total silence** (bot killed, no restart),
the 409 returns within ~22s of the next launch.

## Root cause
Telegram allows exactly ONE long-poll per token. A 409 that survives a 5-minute
local silence with exactly one local poller means **a SECOND long-poll consumer
exists OUTSIDE this machine** — e.g. an old Hermes/agent deploy in the cloud,
another Windows session, or the token pasted into another bot/app. `deleteWebhook`
+ `sleep(60)` and `getUpdates?offset=-1` only clear ghosts that originated on THIS
host; they cannot evict a poller running elsewhere.

## Definitive fix — revoke the token in @BotFather
A new bot token invalidates EVERY existing long-poll session everywhere, including
the external one.
1. In Telegram, message @BotFather -> `/revoke` (or select the bot -> Revoke token).
2. Copy the new `XXXXXXXX:YYYY` token.
3. Write it into the bot's `.env.local` (`Liz Harper Hermes/.env.local` ->
   `TELEGRAM_BOT_TOKEN=...`). Do NOT log/echo the token.
4. Kill all local bot processes, wait ~10s, launch exactly one instance (see pattern
   below). 409 should be gone on first poll.

## Working PowerShell patterns (Windows / MSYS gotchas)
MSYS bash mangles `$_` / `$()` inside `powershell -Command "..."` and `search_files`
fails on `/c/Users/...` paths. **Always write a `.ps1` file and run it:**
`powershell -NoProfile -ExecutionPolicy Bypass -File C:\path\to\x.ps1`

Kill all instances of a bot by cmdline substring:
```powershell
for ($i=0;$i -lt 8;$i++){
  Get-CimInstance Win32_Process | Where-Object { ($_.Name -eq 'python.exe' -or $_.Name -eq 'pythonw.exe') -and $_.CommandLine -match 'liz_loop' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
  Start-Sleep -Seconds 2
}
$lock="C:\Users\Stefan\AppData\Local\hermes\entities\liz.lock"
if (Test-Path $lock){ Remove-Item $lock -Force }
```

Find parent of a re-exec'd bot (to detect double-poller):
```powershell
Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match 'liz_loop' } | ForEach-Object {
  $pp=Get-CimInstance Win32_Process -Filter ("ProcessId="+$_.ParentProcessId)
  Write-Host ($_.ProcessId.ToString()+' ppid='+$_.ParentProcessId+' parent='+$pp.Name)
}
```

Force-drop Telegram ghost sessions (run from the bot host; helps local ghosts only):
```powershell
$tok = (Get-Content 'C:\...\Liz Harper Hermes\.env.local' | Where-Object { $_ -match 'TELEGRAM_BOT_TOKEN=' } | Select-Object -First 1) -replace '.*=' -replace '"'
Invoke-RestMethod "https://api.telegram.org/bot$tok/deleteWebhook?drop_pending_updates=true"
Invoke-RestMethod "https://api.telegram.org/bot$tok/getUpdates?offset=-1&timeout=1"
```

## Pitfall — launch via uv pythonw, NOT venv python
`liz_loop.py` uses the Hermes AIAgent core, which re-execs the process onto the
uv python (`C:\Users\Stefan\AppData\Roaming\uv\python\...\pythonw.exe`) for a
console-free run. If you launch it via the **venv** python, you get TWO long-polls:
the venv parent + the uv-python child -> permanent 409. Launch directly:
`C:\Users\Stefan\AppData\Roaming\uv\python\cpython-3.11-windows-x86_64-none\pythonw.exe liz_loop.py`
(with `DETACHED_PROCESS | CREATE_NO_WINDOW` flags, stdout/stderr -> log file).

## Pitfall — cron watchdog spawns duplicates
A `cronjob` "Liz Bot Watchdog" (every 10m) that launches the bot will, combined with
any manual launch, produce two pollers -> 409. If 409 appears right after you start
the bot, check `cronjob list` for a watchdog on that bot and pause/remove it.
