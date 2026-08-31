# Relaunch the user's VISIBLE Chrome (same profile) with a CDP debug port,
# so Hermes browser tools can attach to their already-logged-in session.
# After running this: `python -m hermes_cli.main config set browser.cdp_url http://127.0.0.1:9223`
#
# WARN THE USER FIRST: this closes their current Chrome. Tabs restore via
# --restore-last-session; cookies/auth persist because the profile is unchanged.
#
# Adjust $Port and $Profile as needed. Do NOT kill Chrome instances that use a
# DIFFERENT profile (e.g. a separate Hermes CDP profile) — match on the profile path.

$Port    = 9223
$Profile = "$env:LOCALAPPDATA\Google\Chrome\User Data"
$ChromeExe = "C:\Program Files\Google\Chrome\Application\chrome.exe"
if (-not (Test-Path $ChromeExe)) {
    $ChromeExe = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
}

# Kill only the visible-profile Chrome (match cmdline on this profile path).
Get-CimInstance Win32_Process -Filter "Name='chrome.exe'" |
    Where-Object { $_.CommandLine -match [regex]::Escape($Profile) -and $_.CommandLine -notmatch 'remote-debugging' } |
    ForEach-Object {
        Write-Host "kill visible chrome $($_.ProcessId)"
        Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue
    }

Start-Sleep -Seconds 2

Start-Process $ChromeExe -ArgumentList @(
    "--remote-debugging-port=$Port",
    "--user-data-dir=`"$Profile`"",
    "--restore-last-session"
)
Write-Host "relaunched Chrome with CDP on $Port"

# Verify the port is listening:
#   Get-NetTCPConnection -LocalPort 9223
#   curl http://127.0.0.1:9223/json/version
