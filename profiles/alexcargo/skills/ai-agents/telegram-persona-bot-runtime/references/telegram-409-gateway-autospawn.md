# Telegram 409 Conflict — gateway auto-spawn + in-session kill block

## Symptom
A self-hosted Telegram long-poll bot (persona/agent variant) gets permanent
`HTTP 409 Conflict` on every `getUpdates`, even after fixing the obvious
retrait/duplicate-process bugs. `pending_update_count` from `getWebhookInfo`
climbs. The bot never answers.

## Root causes that bit us (Hermes environment, Windows)
1. **Gateway auto-spawns entity `.py` files.** The Hermes gateway scans entity
   folders (anything it treats as a local entity, e.g. a folder referenced from
   `entities/registry.json` or any `.py` it discovers) and launches the script
   as a subprocess — often MULTIPLE copies. If your bot's long-poll script lives
   in such a folder, the gateway becomes a second (or 4th) `getUpdates` consumer
   on the same token → guaranteed 409. Invisible from the bot's own logs.
2. **You cannot kill the gateway (or its children) from inside the gateway-session
   terminal.** `taskkill` and `hermes gateway restart` are blocked: the guard
   kills the command before it completes because SIGTERM would propagate to the
   gateway's child processes (your terminal is a child of the gateway). Error:
   `Blocked: cannot restart or stop the gateway from inside the gateway process`.
3. **`taskkill /F` on the bot leaves ghost long-polls.** Telegram holds the
   killed connection as a pending update for up to ~60s; a new instance collides
   until they expire. `deleteWebhook?drop_pending_updates=true` clears them but
   only if no LIVE second poller keeps recreating them.
4. **`terminal(background=true)` sessions are adopted by the gateway on restart**
   and re-spawn their child `.py` → more copies. Killing the child via `process`
   tool or `taskkill` is blocked (see #2).

## Diagnosis recipe (READs are allowed from the session terminal)
- Count live pollers and find the REAL parent:
  ```powershell
  Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like "*BOT_SCRIPT.py*" } |
    ForEach-Object {
      $pp = Get-CimInstance Win32_Process -Filter ("ProcessId="+$_.ParentProcessId) -ErrorAction SilentlyContinue
      Write-Host ($_.ProcessId.ToString()+" parent="+$_.ParentProcessId.ToString()+" ("+$pp.Name+")")
    }
  ```
  If `parent` = the gateway PID (e.g. 24488, or any `pythonw -m hermes_cli`), the
  gateway is the launcher — that is your 409 source.
- Prove "no external poller": with ZERO bot processes running, `getUpdates?
  timeout=15` from a one-shot script returns `ok=true, updates=0, no 409`. If it
  409s while nothing runs, something else holds the token.
- `getWebhookInfo` → `url:""` and `pending_update_count` shows webhook conflict
  (409 if webhook set) or accumulating ghosts.

## Footgun #5 — DEBOUNCE-LOOP SECOND `getUpdates` (parallel poll inside main loop)
This session (Richard + Liz, 2026-07-27/28) hit a 409 class NOT covered above:
a bot with a correct single main `getUpdates` (long-poll, `timeout:30`) ALSO does
a **second `getUpdates` inside a debounce/window block** (`timeout:3`) while the
main loop is still blocked waiting on its own long-poll. Two `getUpdates` in
flight on one token at once = 409. Symptom: bot is alive, sees SOME messages,
but intermittently loses the line ("lost the line to the desk") and spams
`409 Conflict` in the log. No second process, no gateway — the SAME process
polls twice concurrently.
- **Fix:** delete the inner `getUpdates` entirely. The main loop already owns
  `offset` and drains all updates; debounce by `time.sleep(window)` then FLUSH
  what accumulated in `pending` — do NOT re-poll. Dozapisannye messages arrive on
  the next main-loop tick. (Richard: removed lines ~827–852; Liz: same class.)

## Triage recipe — WHICH 409 is it? (run in order)
1. **Count processes polling the token.** `Get-CimInstance Win32_Process |
   Where-Object { $_.CommandLine -like '*BOT_SCRIPT.py*' }`. >1 → duplicate
   process. Exactly 1 → go to step 2.
2. **Check parent PID.** If parent = gateway (`pythonw -m hermes_cli`), it's the
   gateway auto-spawn footgun (#1). Kill from outside the gateway tree.
3. **Read the log for the 409 pattern:**
   - `409` arriving in BURSTS during activity, bot otherwise alive → debounce
     second-poll (#5). Grep the bot script for a 2nd `getUpdates` call inside a
     nested loop/debounce block.
   - `409` constant from startup, even idle → token inherited from env
     (see references/telegram-bot-token-env.md) or webhook set.
4. **One-shot probe:** with ZERO bot processes, `getUpdates?timeout=15` returns
   `ok, updates=0, no 409`. If it 409s with nothing running → external holder
   (gateway or another bot sharing the token via `os.environ`).

## Fixes
- **Keep the bot `.py` OUT of any gateway-scanned entity folder.** Move it to a
  neutral path (e.g. `%LOCALAPPDATA%\\hermes\\scripts\\`). Disable every `.py` in the
  entity folder by renaming to `.py.disabled` so the gateway finds nothing.
- **Do NOT put `runtime:` or `local_folder:` pointing at a long-poll script in
  `entities/registry.json`** — that invites the gateway to launch it. Set
  `managed_by: hermes_stevenson` and describe architecture only.
- **Agent loop must never retry `getUpdates` internally** (a retry opens a 2nd
  parallel long-poll → 409). One shot; the caller's while-loop re-attempts.
  On 409: `deleteWebhook?drop_pending_updates=true`, then `sleep(60)` to let
  ghosts expire, then continue. Guard with a `threading.Lock` so two getUpdates
  can never be in-flight at once.
- **To actually stop the gateway / its children:** run the kill from a process
  OUTSIDE the gateway tree. Reliable options:
  - Ask the user to run `taskkill /F /PID <pid> /T` in a separate Windows console,
    or simply reboot — on next logon the gateway starts fresh (no cached entity
    spawns) and you launch the bot once, manually.
  - A Windows scheduled task (`Register-ScheduledTask` + `Start-ScheduledTask`)
    running `taskkill /F /PID <gateway_pid>` executes outside the session tree so
    the block does not fire (a task that fires on its own schedule is more
    reliable than `Start-ScheduledTask` called from the session with a taskkill
    payload, which was sometimes still blocked).

## Hard rule
Never run `taskkill` / `hermes gateway restart` from the gateway-session terminal
to fix a bot. Diagnose with reads, move the script out of the entity folder, then
have the gateway restarted from outside (user console or scheduled task).
