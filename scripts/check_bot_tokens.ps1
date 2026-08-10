$files = @(
  'C:\Users\Stefan\My Drive\Equity\My Biz\Partner companies\Navo\6. Departments\Alister Sterling\Alistair Hermes\.env.local',
  'C:\Users\Stefan\My Drive\Equity\My Biz\My companies\Enlight Group\Avalanche Agency\Team\Ben Jett\Ben Jett Hermes\.env.local',
  'C:\Users\Stefan\My Drive\Equity\My Biz\Partner companies\Navo\6. Departments\Richard Marlowe\Richard Hermes\.env.local'
)
foreach ($f in $files) {
  if (Test-Path $f) {
    $tok = (Get-Content $f | Where-Object { $_ -match 'TELEGRAM_BOT_TOKEN=' } | Select-Object -First 1)
    if ($tok -match '=(\d+):') { Write-Host ($f.Split('\')[-2] + ' -> bot id ' + $Matches[1]) }
    else { Write-Host ($f + ' -> no token line') }
  } else { Write-Host ($f + ' -> MISSING') }
}
Write-Host '--- searching liz token id 8857115619 across all drive bot folders ---'
$roots = @('C:\Users\Stefan\My Drive\Equity\My Biz')
foreach ($r in $roots) {
  Get-ChildItem $r -Recurse -Filter '.env.local' -ErrorAction SilentlyContinue | ForEach-Object {
    $hit = Select-String -Path $_.FullName -Pattern '8857115619' -ErrorAction SilentlyContinue
    if ($hit) { Write-Host ('LIZ TOKEN FOUND IN: ' + $_.FullName) }
  }
}
Write-Host 'done'
