# Windows 11 Input & Terminal Troubleshooting: Touchpad Gesture Freeze & Invisible Overlay

This reference documents the root causes, diagnostic workflows, and proven fixes for two related Windows 11 desktop UX anomalies that occur when background agents interact with Windows scheduled tasks and console apps.

---

## 1. "Invisible Glass" Overlay & Touchpad Tap/Right-Click Freeze

### Symptoms
- Single left click or drag via physical touchpad press works, but:
  - **Double-tap** (tap to open/click) fails completely or feels unresponsive.
  - **Two-finger tap** (simulated Right-Click) is ignored across application windows (browser, editor, explorer).
  - Swiping or clicking feels like clicking on an "invisible transparent glass sheet" over application windows.
- Pressing `Win+D` (Show Desktop) temporarily restored behavior or partially reset focus.
- **Definitive Fix Gesture**: Performing a **4-finger horizontal swipe** to a neighboring Virtual Desktop and swiping back immediately resets the gesture state machine and restores all tap/gesture functionality.

### Root Causes
1. **Windows 11 Gesture Hook State-Machine Lock (`DWM` / `InputHost`)**:
   - In Windows 11 Precision Touchpad architecture, the high-level multi-finger gesture pipeline (3/4 fingers: virtual desktop switches, Alt-Tab) and the low-level micro-tap pipeline (1/2 fingers: tap-to-click, two-finger right click) are handled by separate stages.
   - When background processes spawn interactive console windows, steal transient focus, or get terminated abruptly while grabbing input handles, the high-level gesture recognizer hangs in an intermediate "waiting for gesture completion" state.
   - While hung, it blocks low-level tap events from passing through to foreground application windows.
   - **Why 4-finger swipe fixes it**: Swiping across virtual desktops forces the input pipeline to fire a full gesture lifecycle completion event, resetting the internal gesture engine state.
2. **PrecisionTouchPad Registry Corruption (DWORD `4294967295` / `0xFFFFFFFF`)**:
   - When registry values under `HKCU:\Software\Microsoft\Windows\CurrentVersion\PrecisionTouchPad` get corrupted or set to `-1` (`4294967295`), the driver falls back to requiring physical hardware switch clicks rather than capacitive taps.
   - Missing `RightClick` key (`null`) defaults to physical bottom-right corner click only, disabling two-finger tap for context menus.
   - `AAPThreshold` (Accidental Palm Press sensitivity) corrupted to `0` misclassifies rapid double-taps as palm rests.

### Proven Fix & Recovery Script (PowerShell)

```powershell
# 1. Restore canonical clean DWORD settings for Windows 11 Precision Touchpad
$path = "HKCU:\Software\Microsoft\Windows\CurrentVersion\PrecisionTouchPad"
if (-not (Test-Path $path)) { New-Item -Path $path -Force | Out-Null }

Set-ItemProperty -Path $path -Name "TapsEnabled" -Value 1 -Type DWord
Set-ItemProperty -Path $path -Name "TapAndDrag" -Value 1 -Type DWord
Set-ItemProperty -Path $path -Name "TwoFingerTapEnabled" -Value 1 -Type DWord
Set-ItemProperty -Path $path -Name "RightClick" -Value 1 -Type DWord          # 1 = Two-finger tap for right click
Set-ItemProperty -Path $path -Name "AAPThreshold" -Value 2 -Type DWord        # 2 = Medium Sensitivity (Balanced)
Set-ItemProperty -Path $path -Name "PanEnabled" -Value 1 -Type DWord
Set-ItemProperty -Path $path -Name "ZoomEnabled" -Value 1 -Type DWord

# 2. Broadcast WM_SETTINGCHANGE (0x001A) to input subsystem
Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
public class User32 {
    [DllImport("user32.dll", SetLastError = true, CharSet = CharSet.Auto)]
    public static extern IntPtr SendMessageTimeout(IntPtr hWnd, uint Msg, UIntPtr wParam, string lParam, uint fuFlags, uint uTimeout, out UIntPtr lpdwResult);
}
"@
$result = [UIntPtr]::Zero
[User32]::SendMessageTimeout([IntPtr]0xffff, 0x001A, [UIntPtr]::Zero, "PrecisionTouchPad", 2, 1000, [ref]$result) | Out-Null

# 3. User Action Reminder:
# If input state-machine is hung in memory, perform a quick 4-finger horizontal swipe across Virtual Desktops to force-reset the gesture engine.
```

---

## 2. Preventing Background Windows Terminal Flashes & Sticking Windows

### Root Cause
In Windows 11, when **Windows Terminal** (`wt.exe` / `WindowsTerminal.exe`) is set as the default terminal application, launching background maintenance tasks (e.g. `powershell.exe -WindowStyle Hidden`) from Task Scheduler still causes Windows Terminal to briefly spawn a visible terminal tab (`ctrl+alt+1`, `C:\WINDOWS\system32\...`) that can steal focus or get stuck on the screen.

### Strict Prevention Pattern
Never register scheduled tasks or background daemons to call `powershell.exe` directly. Always launch via an invisible `wscript.exe` wrapper:

```vbs
' C:\Users\<User>\AppData\Local\hermes\scripts\run_silent.vbs
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -File ""C:\path\to\script.ps1""", 0, False
```

Register with Scheduled Task:
```powershell
$action = New-ScheduledTaskAction -Execute "wscript.exe" -Argument '"C:\path\to\run_silent.vbs"'
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -Hidden -Priority 7
Register-ScheduledTask -TaskName "TaskName" -Action $action -Trigger $trigger -Settings $settings -Force
```
