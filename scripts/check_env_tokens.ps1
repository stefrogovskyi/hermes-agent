$p = 'C:\Users\Stefan\AppData\Local\hermes\.env'
if (Test-Path $p) {
    Get-Content $p | Where-Object { $_ -match 'TELEGRAM_BOT_TOKEN' } | ForEach-Object {
        $line = $_
        if ($line -match 'TELEGRAM_BOT_TOKEN=(.+)') {
            $t = $Matches[1].Trim().Trim('"')
            $short = $t.Substring(0, [Math]::Min(12, $t.Length))
            Write-Host ($short + "...  (len=" + $t.Length + ")")
        } else {
            Write-Host ($line.Substring(0, [Math]::Min(30, $line.Length)) + " [commented?]")
        }
    }
} else { Write-Host "NO .env" }
