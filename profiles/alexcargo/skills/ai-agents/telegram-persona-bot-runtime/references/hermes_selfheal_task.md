# Register the hidden HermesSelfHeal task (Windows) -- no visible window

## 1. Files (copy as-is from this skill's references)
- `references/hermes_selfheal.ps1`  -> `%LOCALAPPDATA%\hermes\scripts\hermes_selfheal.ps1`
- `references/hermes_selfheal_launcher.vbs` -> `%LOCALAPPDATA%\hermes\scripts\hermes_selfheal_launcher.vbs`

## 2. Task XML (hidden + 5-min repeat). Save as `hermes_selfheal_task.xml`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/tasks">
  <Triggers>
    <TimeTrigger>
      <Repetition><Interval>PT5M</Interval><Duration>P3650D</Duration><StopAtDurationEnd>false</StopAtDurationEnd></Repetition>
      <StartBoundary>2026-07-24T00:00:00</StartBoundary>
      <Enabled>true</Enabled>
    </TimeTrigger>
  </Triggers>
  <Principals><Principal id="Author"><UserId>STEFAN\Stefan</UserId><LogonType>Interactive</LogonType><RunLevel>LeastPrivilege</RunLevel></Principal></Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <Hidden>true</Hidden>
    <ExecutionTimeLimit>PT30S</ExecutionTimeLimit>
    <Priority>7</Priority>
  </Settings>
  <Actions Context="Author"><Exec><Command>wscript.exe</Command><Arguments>//nologo "C:\Users\Stefan\AppData\Local\hermes\scripts\hermes_selfheal_launcher.vbs"</Arguments></Exec></Actions>
</Task>
```

## 3. Register
```
schtasks /Create /TN "HermesSelfHeal" /XML "C:\Users\Stefan\AppData\Local\hermes\scripts\hermes_selfheal_task.xml"
```

## 4. If the 5-min repetition didn't apply (PowerShell cmdlet gaps on this host)
`New-ScheduledTaskRepetitionTrigger` does not exist, and `$trigger.Repetition.Interval = ...`
throws 'PropertyNotFound'. Set repetition via the COM object instead:
```powershell
$svc = New-Object -ComObject 'Schedule.Service'; $svc.Connect()
$t = $svc.GetFolder('\').GetTask('HermesSelfHeal')
$t.Definition.Triggers.Item(1).Repetition.Interval = 'PT5M'
$t.Definition.Triggers.Item(1).Repetition.Duration = 'P3650D'
$svc.GetFolder('\').RegisterTaskDefinition('HermesSelfHeal', $t.Definition, 4, $null, $null, 0)
```

## 5. Verify no window
`schtasks /Run /TN "HermesSelfHeal"` -> NO cmd window should appear. Check Event Log
(Application, source HermesSelfHeal) -- it only logs when an actual relaunch happened.

## 6. The alive-detection regex MUST match pythonw + 'gateway run' (LESSON 2026-07-25)
The gateway runs as **`pythonw.exe`** (windowless), NOT `python.exe`. A selfheal
that only does `Get-CimInstance Win32_Process -Filter "Name='python.exe'"` and
matches `-m\s+hermes` will **false-negative on a perfectly healthy gateway** and
try to relaunch Hermes -> conflicts / the Desktop app closing itself. Correct:
```powershell
$procs = Get-CimInstance Win32_Process -Filter "Name='python.exe' or Name='pythonw.exe'"
foreach ($p in $procs) {
    if ($p.CommandLine -match '-m\s+hermes(_cli\.main)?(\s|$)' -or $p.CommandLine -match 'gateway\s+run') { $GATEWAY_ALIVE = $true; break }
}
```
Note `-m hermes_cli.main` (not bare `-m hermes`) — an over-tight `-m\s+hermes(\s|$)`
regex also misses it. Restart the gateway from OUTSIDE its own process
(`hermes gateway restart` is BLOCKED inside the gateway to prevent loops); kill by
matching `gateway run` in the cmdline, then relaunch via
`gateway-service\Hermes_Gateway.vbs` (windowless pythonw). Confirm with
`hermes gateway status` -> "Gateway process running (PID …)".

## 7. "Black console windows keep popping up" is USUALLY explorer.exe (LESSON 2026-07-25)
Recurring black windows titled `C:\Users\Stefan\AppData\Local...` with an empty
black body are **File Explorer windows opened on an empty folder** (dark theme =
solid black), NOT a console and NOT Hermes Desktop DevTools and NOT Claude. Do
not chase DevTools/F12 — that is a different, rarer window.
Root cause on this host: the logon autostart task (`NavoAgentsStartup`) ran a
`.bat` that did `start "" /min "<uv.exe>" run … bot.py` four times; those
`start /min` invocations surface as taskbar/Explorer-flavored windows.
**Fix: retire the .bat.** Point the Task Scheduler action at a windowless VBS that
calls the per-bot watchdogs instead (they launch each bot
`DETACHED_PROCESS | CREATE_NO_WINDOW`, and their pid-lock prevents duplicates):
```vbs
' start_agents_hidden.vbs — 0 windows
Set sh = CreateObject("WScript.Shell")
py = "C:\Users\Stefan\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe"
base = "C:\Users\Stefan\AppData\Local\hermes\scripts\"
sh.Run """"&py&""" """&base&"richard_watchdog.py""", 0, False
' …repeat for alistair/liz/ben…
```
`Set-ScheduledTask -TaskName 'NavoAgentsStartup' -Action (New-ScheduledTaskAction
-Execute 'wscript.exe' -Argument '//nologo "…\start_agents_hidden.vbs"')`.
After switching, kill any duplicate bot procs the old .bat spawned and fix the
lock files (each `<e>.lock` should hold the live worker PID). Two bot PIDs per
entity is NORMAL when the runtime uses run_with_restart (supervisor + worker) —
check ParentProcessId before "deduping".
