# Windows 10/11 Silent Background Task Execution & UTF-8 BOM Handling

## 1. Zero-Disruption Rule for Windows Automation (No Black Console Popups)

On modern Windows 10/11 machines where Windows Terminal or conhost is default, invoking commands via Task Scheduler or background scripts as `powershell.exe -WindowStyle Hidden` can still briefly flash a black console or steal keyboard focus from the active foreground app.

### The Proven VBScript Wrapper Pattern
To run PowerShell or CLI commands completely invisible (`WindowStyle = 0`):
```vbscript
' run_silent.vbs
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -File ""C:\Path\To\script.ps1""", 0, False
```
- The `0` parameter forces `SW_HIDE` at the Win32 window creation level.
- The `False` parameter ensures non-blocking asynchronous handoff.
- Invoke via: `wscript.exe C:\Path\To\run_silent.vbs`.

## 2. PowerShell UTF-8 BOM Trap in Python Pipeline

When Windows PowerShell writes files using `Set-Content -Encoding UTF8` or `Out-File -Encoding UTF8`, it prepends the 3-byte Byte Order Mark (`0xEF, 0xBB, 0xBF` / `\ufeff`).

### The Bug:
Standard Python `json.loads(text)` fails with:
`json.decoder.JSONDecodeError: Unexpected UTF-8 BOM (decode using utf-8-sig): line 1 column 1 (char 0)`

### The Fix:
Always decode with `utf-8-sig` or strip leading BOM:
```python
raw = stdout.strip()
if raw.startswith("\ufeff"):
    raw = raw[1:]
data = json.loads(raw)
```
Or for file reads:
```python
with open(path, "r", encoding="utf-8-sig") as f:
    data = json.load(f)
```
