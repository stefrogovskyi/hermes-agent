' gateway_watcher_launcher.vbs — hidden launch of gateway_watcher.py (no window).
' Task Scheduler / HKCU Run / cron calls THIS vbs (wscript //nologo) so nothing flashes.
Set oShell = CreateObject("WScript.Shell")
cmd = "cmd.exe /c ""C:\Users\Stefan\AppData\Roaming\uv\python\cpython-3.11-windows-x86_64-none\pythonw.exe"" ""C:\Users\Stefan\AppData\Local\hermes\scripts\gateway_watcher.py"""
oShell.Run cmd, 0, False
Set oShell = Nothing
