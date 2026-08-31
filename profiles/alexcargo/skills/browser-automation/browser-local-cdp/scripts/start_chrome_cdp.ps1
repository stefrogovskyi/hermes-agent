# Launcher for Hermes local-browser CDP session (Windows / PowerShell)
# Run once per machine (or via Task Scheduler at logon) before browser tasks.
$chrome = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
$port  = 9222
$profile = "$env:LOCALAPPDATA\hermes\chrome-cdp-profile"

if (-not (Test-Path $chrome)) { Write-Error "Chrome not found at $chrome"; exit 1 }
# Don't launch a second instance on the same port
if (Test-NetConnection -ComputerName 127.0.0.1 -Port $port -InformationLevel Quiet -WarningAction SilentlyContinue) {
    Write-Host "CDP already listening on :$port — reusing."
    exit 0
}
Start-Process $chrome -ArgumentList "--remote-debugging-port=$port","--user-data-dir=$profile","--no-first-run","--no-default-browser-check" -WindowStyle Minimized
Start-Sleep -Seconds 6
if (Test-NetConnection -ComputerName 127.0.0.1 -Port $port -InformationLevel Quiet -WarningAction SilentlyContinue) {
    Write-Host "OK: Chrome CDP up on http://127.0.0.1:$port"
} else {
    Write-Error "Chrome CDP did not come up on :$port"
}
