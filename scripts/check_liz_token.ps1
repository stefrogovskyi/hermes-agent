$paths = @(
    'C:\Users\Stefan\AppData\Local\hermes\scripts\.env.local',
    'C:\Users\Stefan\AppData\Local\hermes\.env',
    'C:\Users\Stefan\My Drive\Equity\My Biz\My companies\Enlight Group\Enlight Board\Liz Harper\Liz Harper Hermes\.env.local'
)
foreach ($p in $paths) {
    if (Test-Path $p) {
        $lines = Get-Content $p -ErrorAction SilentlyContinue | Where-Object { $_ -match 'TELEGRAM_BOT_TOKEN' }
        Write-Host ("=== " + $p + " ===")
        foreach ($l in $lines) { Write-Host ($l.Substring(0, [Math]::Min(35, $l.Length)) + "...") }
    }
}
