# Anthropic (Claude Code Pro) OAuth Token — Master Reference

## СТАТУС: Долгоживущий токен установлен 15.08.2026

Пользователь предоставил долгоживущий OAuth access token (валидность ~1 год,
подтверждён прямым запросом к api.anthropic.com — авторизация прошла,
единственная ошибка была rate_limit, не authentication).

**Установлен: 15.08.2026, истекает: ~15.08.2027**

## Где физически лежит токен (везде один и тот же файл)

```
Windows PC (Hermes Desktop):  C:\Users\Stefan\.claude\.credentials.json
VPS (Servarica, stefan1):     /root/.claude/.credentials.json
```

Формат:
```json
{
  "claudeAiOauth": {
    "accessToken": "sk-ant-oat01-...",
    "refreshToken": "sk-ant-ort01-...",
    "expiresAt": <epoch_ms, ~1 год от даты установки>,
    "scopes": [...]
  }
}
```

Hermes (agent/anthropic_adapter.py::read_claude_code_credentials) всегда
сначала проверяет этот файл при провайдере `anthropic`. Никакой отдельной
установки в `.env` или `config.yaml` не требуется — все компоненты (Archie в
Telegram, Hermes Desktop, avalanche-content-pipeline скилл, cron-джобы)
читают этот единый файл автоматически.

## Кто использует этот токен

- **Hermes Desktop** (Windows) — читает `C:\Users\Stefan\.claude\.credentials.json`
- **Archie Wright Telegram-бот** (VPS, `hermes-archie.service`) — читает
  `/root/.claude/.credentials.json`
- **avalanche-content-pipeline** cron-джоб (VPS, профиль archie) — тот же
  файл, тот же провайдер `anthropic`

Остальные 5 профилей на VPS (default, alistair, ben, callum, liz, richard)
используют `provider: google` — этот токен их не касается.

## Проверка валидности в любой момент

```bash
# Windows
python3 -c "
import json, datetime
d = json.load(open('C:/Users/Stefan/.claude/.credentials.json'))
exp = d['claudeAiOauth']['expiresAt']
dt = datetime.datetime.fromtimestamp(exp/1000, tz=datetime.timezone.utc)
print('expiresAt:', dt, '| valid:', dt > datetime.datetime.now(datetime.timezone.utc))
"

# VPS
ssh -i ~/.ssh/id_rsa root@38.49.219.217 "/opt/hermes/hermes-agent/venv/bin/python3 -c \"
import json, datetime
d = json.load(open('/root/.claude/.credentials.json'))
exp = d['claudeAiOauth']['expiresAt']
dt = datetime.datetime.fromtimestamp(exp/1000, tz=datetime.timezone.utc)
print('expiresAt:', dt, '| valid:', dt > datetime.datetime.now(datetime.timezone.utc))
\""
```

Прямая проверка через реальный запрос к Anthropic (401 = протух/невалиден,
429 = валиден, просто rate limit, любой другой код = разбираться отдельно):
```bash
curl -s -w "\nHTTP_STATUS:%{http_code}\n" \
  -X POST https://api.anthropic.com/v1/messages \
  -H "Authorization: Bearer <accessToken>" \
  -H "anthropic-beta: oauth-2025-04-20" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{"model":"claude-sonnet-4-5","max_tokens":10,"messages":[{"role":"user","content":"hi"}]}'
```

## Автоматическое напоминание перед истечением

Настроен cron-джоб (см. Hermes cron list), который проверит валидность
токена заблаговременно (за ~2 недели до истечения) и напомнит пользователю
обновить его, чтобы не допустить повторного пропадания доступа к Anthropic.

## Если токен всё же перестанет работать раньше срока

1. Проверить оба файла (Windows/VPS) на предмет валидности через скрипты выше.
2. Если один протух, а другой валиден — скопировать валидную версию:
   ```
   scp -i ~/.ssh/id_rsa "C:/Users/Stefan/.claude/.credentials.json" root@38.49.219.217:/root/.claude/.credentials.json
   ssh -i ~/.ssh/id_rsa root@38.49.219.217 "chmod 600 /root/.claude/.credentials.json && systemctl restart hermes-archie.service"
   ```
3. Если оба протухли — запросить у пользователя новый долгоживущий токен и
   повторить процедуру установки, описанную в этом файле.

Последнее обновление: 15.08.2026, долгоживущий токен установлен и
подтверждён рабочим на Windows и VPS.
