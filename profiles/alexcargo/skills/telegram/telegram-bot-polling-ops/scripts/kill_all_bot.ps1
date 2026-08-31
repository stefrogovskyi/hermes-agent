# Kill every process whose command line matches a bot script name, then clear
# the pid-lock file. Usage: .\kill_all_bot.ps1 -Name "richard_bot"
param(
    [string]$Name = "richard_bot"
)
Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like "*$Name*" } | ForEach-Object {
    "PID=$($_.ProcessId) START=$($_.CreationDate)"
    Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue
    "  -> killed"
}
$lockPaths = @(
    "C:\Users\Stefan\AppData\Local\hermes\entities\$Name.lock",
    "C:\Users\Stefan\AppData\Local\hermes\$Name.lock"
)
foreach ($lp in $lockPaths) {
    if (Test-Path $lp) { Remove-Item $lp -Force; "LOCK REMOVED: $lp" }
}
Write-Host "DONE"
