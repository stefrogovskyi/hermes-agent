# Case: Archie Bot VPS Service Location and Unpinned Cron Drift Skip Error

## Дата
2026-08-15

## Симптом
1. Пользователь спросил, почему модель Anthropic/Claude не переключается для телеграм-бота Арчи Райта (`@archiewrightbot`) после изменений в локальном профиле `profiles/archie`.
2. В логах `errors.log` наблюдались сбои крон-задач (например, `dpworld-jobs-daily`) с ошибкой `RuntimeError: [drift_skip] Skipped to prevent unintended spend: global inference config drifted since this job was created (provider 'gemini' -> 'anthropic'; model 'google/gemini-3.6-flash' -> 'claude-sonnet-5'), and this job is unpinned.`.

## Гипотеза / что пошло не так
1. Ложное предположение: запуск `hermes` или правка `profiles/archie/config.yaml` на локальном ПК управляет ботом Арчи в реальном времени.
2. Неутентифицированные/распиненные крон-задачи продолжают работать на глобальных дефолтах при смене дефолтного провайдера/модели.

## Корень (ФАКТ, проверенный)
1. **Местонахождение сервиса Арчи**: Боевой Telegram-бот `@archiewrightbot` реально работает на удалённом VPS `stefan1` (Servarica) как systemd-сервис `hermes-archie.service`. Изменения локального файла `profiles/archie/config.yaml` на Windows ПК не влияют на сервис на VPS до тех пор, пока конфигурация не обновлена на самом VPS.
2. **Claude Code OAuth vs OpenRouter**: OAuth-токены Claude Code (`~/.claude/.credentials.json`) привязаны к локальной сессии устройства. На VPS для стабильного доступа к моделям Anthropic используется `OPENROUTER_API_KEY` (`anthropic/claude-sonnet-5`).
3. **Cron Drift Skip**: В Hermes v0.20+ запуск unpinned крон-задач блокируется с `[drift_skip]`, если глобальный провайдер/модель в `config.yaml` изменились с момента создания задачи (`gemini` -> `anthropic`).

## Фикс (применён и проверен)
1. Для актуализации Арчи обновлены конфигурации профилей и проверен статус `hermes-archie.service` на VPS `stefan1`.
2. Для предотвращения `drift_skip` крон-задач необходимо явно закреплять (pin) провайдера и модель в параметрах крон-задачи (`cronjob action=update job_id=<id> provider=gemini model=gemini-3.6-flash`).

## Рефлексия (зарегистрированный опыт)
1. Изменения провайдеров/моделей для телеграм-ботов субагентов должны синхронизироваться на VPS `stefan1`, где работают их systemd-сервисы.
2. Для всех критических cron-задач всегда указывать явный `provider` и `model` при создании/обновлении, чтобы избежать сбоев `[drift_skip]` при экспериментах с дефолтной моделью Hermes.

## Где искать при повторе
- VPS `stefan1`: `/etc/systemd/system/hermes-archie.service`, `/opt/hermes/profiles/archie/`
- Крон-расписание: `C:/Users/Stefan/AppData/Local/hermes/cron/scheduler.py`, `C:/Users/Stefan/AppData/Local/hermes/logs/errors.log`
