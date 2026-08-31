# hermes_selfheal.ps1 — EXTERNAL self-healing for the Hermes orchestrator (gateway).
# Runs via Windows Task Scheduler every 5 min, INDEPENDENTLY of Hermes (so it still
# fires even if Hermes is fully dead).
#
# CORRECTED behaviour (after two bugs bit us live):
#   1. NEVER kills a healthy open Desktop. If the GUI (Hermes.exe) is already up — even
#      with a briefly-dead gateway — exit 0 silently. Only relaunch when BOTH the gateway
#      (python -m hermes) AND the GUI (Hermes.exe) are gone.
#   2. Relaunch HIDDEN (-WindowStyle Hidden), never Minimized — Minimized still paints a
#      visible console window that the user keeps closing, which re-triggers the heal loop.
#   3. LAUNCHED VIA wscript launcher (references/hermes_selfheal_launcher.vbs), NOT directly
#      as a powershell.exe Action — a direct powershell Action makes Task Scheduler spawn a
#      visible cmd host window every run (owner saw it pop every 5 min). The vbs is windowless.
#
# Register via references/hermes_selfheal_task.md (Task XML + COM repetition fix).

$ErrorActionPreference = "SilentlyContinue"

# 1. Gateway (python -m hermes) alive -> quiet exit.
$GATEWAY_ALIVE = $false
try {
    $procs = Get-CimInstance Win32_Process -Filter "Name='python.exe'"
    foreach ($p in $procs) {
        if ($p.CommandLine -match '-m\s+hermes(\s|$)') {
            $GATEWAY_ALIVE = $true
            break
        }
    }
} catch {}
if ($GATEWAY_ALIVE) { exit 0 }

# 2. Hermes.exe GUI already running -> DO NOT touch the user's open Desktop.
$hermesRunning = $false
try {
    if (Get-CimInstance Win32_Process -Filter "Name='Hermes.exe'") {
        $hermesRunning = $true
    }
} catch {}
if ($hermesRunning) { exit 0 }

# 3. Fully down: relaunch Hermes.exe HIDDEN (no visible window), from its own dir.
$EXE_DIR = "C:\Users\Stefan\AppData\Local\hermes\hermes-agent\apps\desktop\release\win-unpacked"
$HERMES_EXE = Join-Path $EXE_DIR "Hermes.exe"
if (Test-Path $HERMES_EXE) {
    Set-Location $EXE_DIR
    Start-Process -FilePath $HERMES_EXE -WindowStyle Hidden
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $msg = "Hermes was fully down at $ts - relaunched hidden (no visible window)."
    Write-EventLog -LogName Application -Source "HermesSelfHeal" -EntryType Information -EventId 1001 -Message $msg -ErrorActionSilentlyContinue
}
exit 0
