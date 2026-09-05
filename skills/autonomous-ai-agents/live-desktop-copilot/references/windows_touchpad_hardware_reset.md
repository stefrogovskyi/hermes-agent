# Windows Precision Touchpad Hardware Reset & Touch Tap Recovery Protocol

## Problem Description
User experiences a "sheet of glass" on the Windows desktop:
- Physical bottom-corner mechanical clicks work.
- Light finger taps (single tap to click, double tap), two-finger tap, and multi-finger gestures (four-finger swipe) do NOT register.
- Even closing applications or checking RAM usage does not resolve the issue.

## Architecture Understanding
1. Physical clicks go through the generic `HID-compliant mouse` endpoint.
2. Taps, gestures, and multi-touch positions go through the OEM Precision Touchpad hardware controller (e.g. `ASUS Precision Touchpad [HID\ASUE140D&COL02...]` interfaced over `I2C HID [ACPI\ASUE140D\6]`).
3. If the I2C interrupt controller or Precision Touchpad driver hangs, click events still fire mechanically, but gesture/tap tracking is dropped.
4. Concurrently, invisible system windows (`TextInputHost.exe`, `TabTip.exe`, `Cua.AgentCursorOverlay`) can overlay the desktop and swallow touch events.

## Recovery Script (Run via Remote SSH / PowerShell)

```powershell
# 1. Terminate potential invisible touch overlays
Get-Process -Name "TextInputHost", "TabTip", "ShellHost" -ErrorAction SilentlyContinue | Stop-Process -Force

# 2. Re-initialize the Precision Touchpad hardware device via PnP
$tp = Get-PnpDevice -FriendlyName "*Precision Touchpad*" -ErrorAction SilentlyContinue
if ($tp) {
    Write-Output "Cycling Precision Touchpad device: $($tp.InstanceId)"
    Disable-PnpDevice -InstanceId $tp.InstanceId -Confirm:$false
    Start-Sleep -Seconds 1
    Enable-PnpDevice -InstanceId $tp.InstanceId -Confirm:$false
}

# 3. Ensure registry gestures are explicitly enabled
$regPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\PrecisionTouchPad"
Set-ItemProperty -Path $regPath -Name "TapsEnabled" -Value 1
Set-ItemProperty -Path $regPath -Name "TwoFingerTapEnabled" -Value 1
Set-ItemProperty -Path $regPath -Name "TapAndDrag" -Value 1
Set-ItemProperty -Path $regPath -Name "FourFingerSlideEnabled" -Value 0xffff

# 4. Notify all top-level windows of the setting change via Win32 API
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class PrecisionSettingNotifier {
    [DllImport("user32.dll", SetLastError = true, CharSet = CharSet.Auto)]
    public static extern IntPtr SendMessageTimeout(
        IntPtr hWnd,
        uint Msg,
        UIntPtr wParam,
        string lParam,
        uint fuFlags,
        uint uTimeout,
        out UIntPtr lpdwResult
    );
}
"@

$result = [UIntPtr]::Zero
[PrecisionSettingNotifier]::SendMessageTimeout(
    [IntPtr]0xffff,
    0x001A, # WM_SETTINGCHANGE
    [UIntPtr]::Zero,
    "PrecisionTouchPad",
    2,      # SMTO_ABORTIFHUNG
    1000,
    [ref]$result
)

Write-Output "Touchpad hardware driver cycled and Win32 gesture settings reloaded."
```
