' hermes_selfheal_launcher.vbs -- windowless launch of the self-heal ps1.
' Task Scheduler points its Action at THIS (wscript.exe //nologo ...vbs), not at
' powershell.exe directly, so no black cmd host window flashes every 5 minutes.
Set oShell = CreateObject("WScript.Shell")
cmd = "powershell.exe -NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -NonInteractive -File ""C:\Users\Stefan\AppData\Local\hermes\scripts\hermes_selfheal.ps1"""
oShell.Run cmd, 0, False
Set oShell = Nothing
