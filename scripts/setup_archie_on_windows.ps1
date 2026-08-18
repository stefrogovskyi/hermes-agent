# Setup Archie Wright profile on Windows Desktop
$hermesDir = "$env:LOCALAPPDATA\hermes\profiles\archie"
$memDir = "$hermesDir\memories"
New-Item -ItemType Directory -Force -Path $memDir | Out-Null

$soul = @"
# 🎭 ТВОЯ ЕДИНСТВЕННАЯ ЗОНА ОТВЕТСТВЕННОСТИ (DOMAIN BOUNDARY)
Ты — субагент Archie Wright (Content Strategist & Chief Copywriter).
Твоя ЧЁТКАЯ зона ответственности: Контент-стратегия, копирайтинг, написание текстов, контент-планы, редактура, статьи, посты и личный Канбан (archie-kanban).
"@

$agents = @"
# SYSTEM ISOLATION & DOMAIN BOUNDARY
You are Archie Wright (Content Strategist & Chief Copywriter).
Default Domain: Контент-стратегия, копирайтинг, написание текстов, контент-планы, редактура, статьи, посты и личный Канбан (archie-kanban).
"@

$config = @"
model:
  default: google/gemini-3.6-flash
  provider: google
system_prompt_append: 'You are Archie Wright, Content Strategist & Chief Copywriter (@archiewrightbot).'
voice: onyx
auto_tts: false
"@

Set-Content -Path "$hermesDir\SOUL.md" -Value $soul -Encoding UTF8
Set-Content -Path "$hermesDir\AGENTS.md" -Value $agents -Encoding UTF8
Set-Content -Path "$hermesDir\config.yaml" -Value $config -Encoding UTF8
Set-Content -Path "$memDir\USER.md" -Value "User: Stefan Rogovskiy (COO Navo)." -Encoding UTF8

Write-Host "✅ Profile 'archie' successfully created in $hermesDir! Restart Hermes Desktop to see Archie." -ForegroundColor Green
