# Principle 02: Windows Silent Background Automation

## Rule
On Windows hosts, all background agents, watchdogs, and long-running daemons MUST execute silently without spawning visible Command Prompt (`cmd.exe`) or Terminal windows.

## Enforcement Mechanism
1. **Executable**: Use `pythonw.exe` (windowless Python interpreter) instead of `python.exe`.
2. **Process Creation Flags**: Pass `creationflags=0x08000000` (`CREATE_NO_WINDOW`) or `SW_HIDE` (`0`) to `subprocess.Popen`.
3. **Startup Auto-Run**: Wrap background triggers in VBScript (`.vbs`) using `WScript.Shell.Run command, 0, False` (the `0` parameter hides the window completely).

## Pitfall
Using standard `python.exe` or executing `.bat`/`cmd` scripts directly causes black console windows to flash on screen every time a scheduled task or watchdog poll executes, interrupting user activity and risking accidental window closure by the user.
