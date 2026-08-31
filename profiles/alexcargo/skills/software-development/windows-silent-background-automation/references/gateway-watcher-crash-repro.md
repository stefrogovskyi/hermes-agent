# Gateway Watcher Crash Repro (2026-07-29)

## Observed behavior
`watch_watcher.py` (cron self-heal) runs every ~6 min, sees a dead PID in
`gateway_watcher.lock`, restarts the watcher, but the new watcher also dies
within seconds.

`gateway_watcher.log` repeats:
```
[HH:MM:SS] watcher started
[HH:MM:SS] START gateway (no gateway run process)
[HH:MM:SS] gateway start command issued
```
No follow-up health-check loops. Lock file advances to a new PID each tick,
but each PID is dead by the next tick.

## Evidence gathered
- `tasklist /FI "PID eq <lock>"` → "No tasks running"
- `OpenProcess(0x0400, False, <lock>)` → `0` (handle invalid)
- `gateway_state.json` shows `gateway_state: running`, `telegram: connected`,
  `pid: 44408` — the real gateway is fine.
- `gateway_pids()` (PEB cmdline scan) returns `[]` even though the gateway
  is running (pid 44408 via `gateway_state.json`).
- `subprocess.Popen([PY_EXE, WATCHER], ...)` returns a PID that is not present
  in tasklist within seconds — the watcher script crashes immediately after
  launch.

## Key diagnosis
Pid-lock + "Popen returned pid" ≠ "process stayed alive".
For windowless pythonw, a startup exception kills the script without stderr.

`NtQueryInformationProcess`-based cmdline reading (PEB walk) is fragile:
  - access violation if target exits between snapshot and query
  - WoW64 / permission issues can cause silent empty-string returns
  - broad `except Exception: return ""` masks the failure

## Fix path applied
1. Verified base `pythonw.exe` path exists.
2. Confirmed new pythonw procs not appearing → crashed immediately.
3. Did NOT touch the live gateway (pid 44408, telegram connected).
4. Result reported to user as a failure of the watcher chain, not a gateway issue.

## Reusable probe script (Windows, ctypes, no shell)
```python
import ctypes, os
pid = int(open(os.path.expanduser(r"~\\AppData\\Local\\hermes\\scripts\\gateway_watcher.lock")).read())
h = ctypes.windll.kernel32.OpenProcess(0x0400, False, pid)
print(f"pid={pid} alive={bool(h)}")
if h:
    ctypes.windll.kernel32.CloseHandle(h)
```

## Reusable probe: check if Popen'd process survived
Run as normal python (not pythonw) so you can see exceptions:
```python
import subprocess, sys, time
p = subprocess.Popen([r"C:\Users\Stefan\AppData\Roaming\uv\python\cpython-3.11-windows-x86_64-none\pythonw.exe",
                      r"C:\Users\Stefan\AppData\Local\hermes\scripts\watch_watcher.py"],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("returned", p.pid)
time.sleep(2)
# now check same pid via tasklist or psutil
```
If the pid vanishes, the script crashed at import or top-level code.
