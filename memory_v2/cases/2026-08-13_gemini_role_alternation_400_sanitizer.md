# Case: 2026-08-13_gemini_role_alternation_400_sanitizer

## Симптом
При использовании модели Gemini 3.6 Flash появлялась ошибка HTTP 400:
`INVALID_ARGUMENT: Please ensure that function call turn comes immediately after a user turn or after a function response turn.`
В результате агент сбрасывался на резервную модель и перезапускался.

## Гипотеза / что пошло не так
Предполагали, что провайдер Gemini временно недоступен или неверен API ключ.

## Корень (ФАКТ, проверенный)
При исполнении длинного цикла вызова инструментов (tool call) в случае прерывания процесса, падения соединения или получения нового сообщения от пользователя до отправки `functionResponse`, в истории диалога `state.db` оставался ход модели (`model`) с `functionCall`, за которым не следовал ответ вызова функции (`functionResponse`).
Правила Google Gemini API строго требуют чередования: `model (functionCall)` -> `user (functionResponse)`. Нарушение этого порядка вызывает фатальный `INVALID_ARGUMENT`.

## Фикс (применён и проверен)
1. В функцию `_build_gemini_contents` адаптера `agent/gemini_native_adapter.py` встроен санитайзер `_sanitize_gemini_contents`.
2. Санитайзер сканирует историю сообщений: если за ходом `model` с `functionCall` сразу не следует `functionResponse`, он автоматически синтезирует фиктивный отклик `functionResponse` с заглушкой `[Function execution interrupted or omitted]`, сохраняя правильный порядок ролей.
3. Изменения применены как на VPS Servarica (`/opt/hermes/hermes-agent/agent/gemini_native_adapter.py`), так и на ПК Windows.

## Рефлексия (зарегистрированный опыт)
- Любые обрывы сетевых сессий или инструментальных циклов не должны ломать формат истории сообщений для моделей с жесткой валидацией схемы (Gemini / Anthropic).
- Санитайзеры формата обязаны работать прозрачно в рантайме перед отправкой API-запроса.

## Где искать при повторе
- Adapter code: `agent/gemini_native_adapter.py` (`_sanitize_gemini_contents`)
- Gateway logs: `journalctl -u hermes-default.service -n 100`
