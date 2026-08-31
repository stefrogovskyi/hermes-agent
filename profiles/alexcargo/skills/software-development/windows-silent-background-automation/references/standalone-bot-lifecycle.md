# Standalone Bot Lifecycle & Watchdog Chain (2026-07-30 session)

Concise, copy-pasteable pattern for keeping a standalone Telegram bot agent
(Alistair / Richard / Liz / Ben) alive 24/7 **without flashing windows** or
falling into process-fights. This is the distilled, verified shape from the
2026-07-30 Alistair restart/fix session, linked to the deeper background
theory in the parent skill (§1–§10).

## Files / locations
- Bot dir: `C:\Users\Stefan\My Drive\Equity\My Biz\Partner companies\Navo\6. Departments\<Agent>\Alistair Hermes`
- Watchdog: `<bot_dir>\alistair_watchdog.py`
- Launcher: `<bot_dir>\Alistair_Bot.vbs` (hidden via `wscript //nologo`)
- `.env.local`: lives next to the bot; contains `TELEGRAM_BOT_TOKEN`,
  `GOOGLE_SHEETS_ID`, `NOUS_API_KEY`, `ALISTAIR_MODEL`,
  `OPENROUTER_API_KEY`, etc.
- Lock file: `%LOCALAPPDATA%\hermes\entities\alistair.lock` (written by the
  running bot, READ by the watchdog — **must match**).
- Run log: `<bot_dir>\alistair_run.log`

## 1. Always start via the watchdog (not the bot directly)
```bash
cd "/c/Users/Stefan/AppData/Local/hermes/scripts" && python alistair_watchdog.py
```
The watchdog:
1. Reads the lock-file PID.
2. Checks liveness with `tasklist /FI "PID eq <pid>"` — **never trust the lock
   alone; always verify the process actually exists.**
3. If dead (or no lock), spawns `alistair_bot.py` **detached + no-window**:
   ```python
   flags = 0x00000008 | 0x08000000  # DETACHED_PROCESS | CREATE_NO_WINDOW
   subprocess.Popen([sys.executable, BOT], cwd=HERE,
        stdout=lf, stderr=lf, creationflags=flags, close_fds=True)
   ```
4. Exits silently if already running.

## 2. Two processes per bot is NORMAL
Bots using a `run_with_restart()` supervisor show TWO python processes each
(supervisor parent + worker child). The lock file points at the **worker**.
Do not kill both — killing the parent restarts the child.

## 3. If the bot fails to start / model returns 403
Common cause: model in `.env.local` is dead (e.g. `tencent/hy3:free` → 403).

Fix (non-destructive — don't touch the live process):
1. Edit `ALISTAIR_MODEL` in `.env.local`:
   ```bash
   python -c "
   import re
   f=r'C:\\Users\\Stefan\\...\\Alistair Hermes\\.env.local'
   lines=open(f,encoding='utf-8').readlines()
   out=[l if not l.strip().startswith('ALISTAIR_MODEL=') else 'ALISTAIR_MODEL=poolside/laguna-s-2.1:free\n' for l in lines]
   open(f,'w',encoding='utf-8').writelines(out)
   print('Updated ALISTAIR_MODEL -> poolside/laguna-s-2.1:free')
   "
   ```
2. Restart the bot via the watchdog (step 1 above).

**Verify**: `alistair_run.log` stops emitting
`"model tencent/hy3:free failed: HTTP Error 403"` and the bot reports
`bot started, polling Telegram... stefan_chat=330656040`.

## 4. Verify bot is alive (no shell spawning of tasklist/powershell)
Use `OpenProcess` from a normal python process (NOT pythonw — that can hang):
```python
import ctypes, os
lock = os.path.join(os.environ.get('LOCALAPPDATA', r'C:\Users\Stefan\AppData\Local'),
                    'hermes','entities','alistair.lock')
pid = int(open(lock).read().strip())
h = ctypes.windll.kernel32.OpenProcess(0x0400, False, pid)
print(f'pid={pid} alive={bool(h)}')
if h: ctypes.windll.kernel32.CloseHandle(h)
```
Or, equivalently with tasklist:
```bash
tasklist /FI "PID eq <pid>"
```

## 5. Cron wrapper for no_agent scripts (avoid conhost flash)
Hermes `no_agent` crons that run `.py` files via the uv venv **flash a black
console window** because the uv launcher re-execs the base console interpreter.
Wrap them in a `.sh` that calls BASE python explicitly:
`/c/Users/Stefan/AppData/Roaming/uv/python/cpython-3.11-windows-x86_64-none/python.exe`

Template (copy per job): `scripts/cron_hidden_sh_template.sh`

Then point the cron `script:` at the `.sh` (relative name only).

## 6. Lock-path pitfall (watchdog vs bot)
Symptom: watchdog reports `restarted: FAILED` forever while the bot log says
`already running (pid N)` — the bot is healthy; the **LOCK PATH is wrong**.

The watchdog must read the lock file the bot actually writes. In this env both
agree on `%LOCALAPPDATA%\hermes\entities\alistair.lock`. If you ever split
them, the watchdog's `running()` returns False → it spawns a duplicate →
Telegram `409 Conflict`.

## 7. Restart checklist (Alistair)
1. Fix model in `.env.local` (`ALISTAIR_MODEL=poolside/laguna-s-2.1:free`).
2. `python alistair_watchdog.py` (from `scripts/`).
3. Confirm lock file PID is alive (step 4).
4. Confirm `alistair_run.log` shows `polling Telegram... stefan_chat=330656040`
   and no `HTTP Error 403` lines.

## Reusable scripts (copy to ~/.hermes/scripts/)
- `refresh_nous_key.py` — auto-refresh NOUS_API_KEY in .env from auth.json
  (no gateway restart needed).
- `cron_hidden_sh_template.sh` — .sh wrapper calling BASE python (conhost-free).
- `gateway_watcher.py` — full watchdog with `OpenProcess` liveness
  (parent skill §9b §9e).
