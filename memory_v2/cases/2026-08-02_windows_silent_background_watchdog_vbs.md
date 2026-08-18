# Case: Windows Silent Background Automation & Startup VBS Watchdog

**Date**: 2026-08-02  
**Domain**: `agent_club` / `ai_infra`  
**Cross-ref**: `principles/02_windows_silent_automation.md`

## Symptom
Closing terminal windows on Windows inadvertently killed background bot processes (Richard, Liz, Ben), leaving stale lock PIDs. Furthermore, running scheduled watchdogs flaked black Command Prompt windows on screen.

## Hypothesis & Root Cause
Background python processes launched via standard `python.exe` attached to console windows. Closing the console terminated the child processes.

## Fix
1. Updated `bot_watchdog.py` to use `pythonw.exe` with `creationflags=0x08000000` (`CREATE_NO_WINDOW`).
2. Created a silent startup wrapper `silent_bot_watchdog.vbs` under `AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\` using `WScript.Shell.Run ..., 0, False`.
3. Executed watchdog auto-heal, successfully recovering all 5 agents (Alistair, Richard, Callum, Liz, Ben) without any visible UI impact.

## Reflection
All Windows background automation must strictly adhere to the `pythonw.exe` + `CREATE_NO_WINDOW` (`0x08000000`) + VBScript `0` pattern to remain 100% silent and resilient against console closures.
