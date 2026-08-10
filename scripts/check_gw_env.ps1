$gwpid = 28528
$p = Get-CimInstance Win32_Process -Filter "ProcessId=$gwpid" -ErrorAction SilentlyContinue
if (-not $p) { Write-Host "gateway not running"; exit }
Write-Host "gateway cmdline: " + $p.CommandLine
$paths = @(
    'C:\Users\Stefan\AppData\Local\hermes\.env',
    'C:\Users\Stefan\AppData\Local\hermes\hermes-agent\.env'
)
foreach ($pp in $paths) {
    if (Test-Path $pp) {
        $lines = Get-Content $pp -ErrorAction SilentlyContinue
        $hasLiz = ($lines | Where-Object { $_ -match '8857115619' }).Count
        Write-Host ($pp + " -> liz-token lines: " + $hasLiz)
    } else { Write-Host ($pp + " -> missing") }
}
Write-Host "done"
