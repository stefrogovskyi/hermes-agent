# Case: 2026-08-13_dual_polling_409_windows_autostart_and_cloud_audit

## Симптом
Telegram-агенты (@hermesstevensonbot, @richnavobot, @alistair_bot, @callumvancebot, @lizharperbot, @ben_bot) обрывали генерацию ответов, дублировали сообщения в чатах или возвращали ошибку Telegram API:
`HTTP 409 Conflict: terminated by other getUpdates request`.

## Гипотеза / что пошло не так
Первоначально предположили, что сбой вызван зависанием процессов на VPS Servarica. Однако перезапуск systemd сервисов на VPS не решал проблему окончательно — через несколько минут ошибки 409 появлялись вновь.

## Корень (ФАКТ, проверенный)
1. В папке `AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup` на ПК оставалось 8 устаревших VBS-скриптов и .lnk ярлыков (`Hermes_Gateway.vbs`, `Alistair_Bot.vbs`, `silent_bot_watchdog.vbs` и др.). При каждом старте/перезагрузке Windows они поднимали локальные фоновые процессы `pythonw.exe`, делавшие `getUpdates` к Telegram API с теми же токенами, что и облачные сервисы на Servarica VPS.
2. Скрипт аудита `ecosystem_self_heal_audit.py` на ПК обладал "локальной слепотой": не подключался к VPS по SSH, видел отсутствие локальных процессов на Windows и ошибочно делал вывод "боты упали!", после чего принудительно запускал дублирующие локальные шлюзы на ПК.

## Фикс (применён и проверен)
1. Из автозапуска Windows (`Startup`) полностью удалены все 8 VBS/LNK скриптов.
2. В `C:\Users\Stefan\AppData\Local\hermes\scripts\` нейтрализовано 35+ вочдог-скриптов заглушками безопасности (`sys.exit(0)` / `[SAFETY BLOCK]`).
3. Скрипт `ecosystem_self_heal_audit.py` полностью переписан на Cloud-First архитектуру: через SSH инспектирует `journalctl` на Servarica VPS, проверяет 0 конфликтов 409, а при обнаружении случайного локального шлюза на ПК мгновенно завершает его (`kill`).
4. На Servarica VPS перезапущены все 6 `systemd` сервисов (`hermes-default`, `hermes-richard`, `hermes-alistair`, `hermes-ben`, `hermes-callum`, `hermes-liz`).
5. Настроен системный таймер на VPS для независимой инспекции каждые 60 секунд.

## Рефлексия (зарегистрированный опыт)
- Единственным 24/7 узлом исполнения Telegram-шлюзов является Servarica VPS (`stefan1`).
- На ПК запрещён любой автоматический запуск шлюзов ботов Telegram.
- Локальный аудит обязан быть Cloud-First и проверять реальное состояние облачных демонов.

## Где искать при повторе
- VPS services: `systemctl status hermes-*.service` на Servarica (`38.49.219.217` / `100.99.146.42`)
- Audit script: `C:\Users\Stefan\AppData\Local\hermes\scripts\ecosystem_self_heal_audit.py`
- Windows Startup folder: `C:\Users\Stefan\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`
