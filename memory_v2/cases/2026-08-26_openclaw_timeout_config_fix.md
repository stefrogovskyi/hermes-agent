# OpenClaw Timeout Config Fix & Service Restart

**Дата:** 2026-08-26
**Домен:** `agent_club` / `ops_infrastructure`

## Контекст и симптомы
При обращениях к OpenClaw (`@clawstevensonbot`, порт 18789) от Стефана возникала ошибка таймаута:
`Request timed out before a response was generated. Please try again, or increase agents.defaults.timeoutSeconds in your config.`

## Диагностика и исправление
1. **Проблема:** В конфигурации OpenClaw по умолчанию таймаут ожидания ответа генерации был занижен (10 секунд), из-за чего комплексные генеративные запросы с инструментами сбрасывались до завершения работы моделей.
2. **Исправление:**
   - Изменен параметр `timeoutSeconds` в конфигурационном файле OpenClaw (`agents.defaults.timeoutSeconds`).
   - Сервис `openclaw.service` корректно перезапущен через systemd и подтвержден статус **Active / Running**.
   - Проведено сквозное E2E тестирование сообщений через Telegram бот OpenClaw — задержка ликвидирована.

## Ключевой урок
При таймаутах генерации в Gateway-ботах системно изменять `timeoutSeconds` в конфиге соответствующего агента и проверять лог `journalctl -u <service>` на предмет обрыва длинных LLM-ответов.
