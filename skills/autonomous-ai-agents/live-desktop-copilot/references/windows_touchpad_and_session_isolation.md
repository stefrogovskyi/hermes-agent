# Windows Desktop Touchpad Freeze & Headless Remote Remediation

## Symptoms
1. **"Invisible Glass" Effect**: Mouse clicks work, but trackpad taps (single/double tap) and precision gestures (two-finger scroll, four-finger desktop switch) stop responding.
2. **Missing Taskbar / Desktop**: Can happen if an administrator or agent terminates `explorer.exe` remotely.

## Technical Diagnosis
- **Session Isolation (Session 0 vs Session 1)**: Windows separates background services and SSH daemons into Session 0, while the logged-in interactive user sits in Session 1.
- **`TextInputHost.exe` Overlay**: This process manages the Windows Touch Keyboard and Input Experience. Under high memory pressure (>=95% RAM), it frequently crashes or leaves an invisible full-screen transparent modal window that captures touchpad touch events before they reach underlying applications.
- **Why killing `explorer.exe` over SSH breaks the Taskbar**: Launching `explorer.exe` or `start explorer.exe` from an SSH console attempts to create the shell inside Session 0 rather than Session 1. Windows actively blocks shell creation in Session 0, leaving the user with an empty screen.

## Verified Remediation Playbook

### 1. Remove the Invisible Touchpad Interceptor Safely
Run directly from SSH:
```cmd
taskkill /f /im TextInputHost.exe 2>nul
taskkill /f /im TabTip.exe 2>nul
taskkill /f /im ShellHost.exe 2>nul
taskkill /f /im conhost.exe 2>nul
```
*Note*: `TextInputHost.exe` will automatically restart in a clean, non-frozen state when the user clicks or types next, restoring touch and gesture input.

### 2. If Taskbar Disappeared (Recovering Explorer in Session 1)
Instruct the user:
1. Press `Ctrl + Shift + Esc` (opens Task Manager natively in Session 1).
2. Click **File -> Run new task** (`Файл -> Запустить новую задачу`).
3. Type `explorer` and press Enter.
*Alternative*: Press `Win + R`, type `explorer`, and press Enter.

### 3. Triage Memory Bloat via Remote CLI
Do not use raw PowerShell scripts over SSH if they contain unescaped quotation marks or `$_` pipeline tokens. Use `tasklist /fo csv`:
```cmd
tasklist /fo csv
```
Identify runaway process trees (e.g. Chrome tabs, Electron apps) and recommend closing unused tabs to keep memory below 85%.
