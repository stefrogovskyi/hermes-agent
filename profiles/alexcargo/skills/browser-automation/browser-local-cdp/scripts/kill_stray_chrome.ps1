# kill_stray_chrome.ps1
# Reap ONLY the agent's orphaned Chrome / conhost processes (profile chrome-cdp-profile,
# or any chrome that is NOT the user's real "User Data" profile and NOT the CDP daemon).
# NEVER blanket-kills all chrome.exe -- that would kill the user's real browser (YouTube, etc).
$ErrorActionPreference = 'SilentlyContinue'

# 1) The agent's headless CDP Chrome (by user-data-dir)
$agentChrome = Get-CimInstance Win32_Process -Filter "Name='chrome.exe'" |
  Where-Object { $_.CommandLine -like '*chrome-cdp-profile*' }

# 2) Identify the user's REAL chrome to always spare (default User Data profile, open tabs)
$userPids = @(
  (Get-CimInstance Win32_Process -Filter "Name='chrome.exe' AND CommandLine LIKE '%User Data%'").ProcessId
  (Get-CimInstance Win32_Process -Filter "Name='chrome.exe' AND CommandLine LIKE '%remote-debugging-port=9222%'").ProcessId
) | Where-Object { $_ } | Sort-Object -Unique

# 3) Any chrome whose cmdline is neither the user's profile nor the CDP daemon -> orphan, kill
$allChrome = Get-CimInstance Win32_Process -Filter "Name='chrome.exe'"
$orphanChrome = $allChrome | Where-Object { $_.ProcessId -notin $userPids -and $_.CommandLine -notlike '*User Data*' }

# 4) Orphaned conhost (agent-browser/Chrome daemon consoles). Keep conhost whose parent is a kept chrome.
$orphanCon = Get-CimInstance Win32_Process -Filter "Name='conhost.exe'" |
  Where-Object { $_.ParentProcessId -notin $userPids }

$orphanChrome | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }
$orphanCon | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }

"killed chrome: $($orphanChrome.Count)  conhost: $($orphanCon.Count)  (spared real-chrome pids: $($userPids -join ','))"
