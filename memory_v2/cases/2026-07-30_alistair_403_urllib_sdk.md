# Case: Alistair Bot 403 Forbidden due to raw urllib fallback
Дата: 2026-07-30
Домен: [[agent_club]], [[ai_infra]]

## Симптом
Алистер (`alistair_bot.py`) перестал отвечать в группе и начал выходить с системным заглушечным сообщением: `"Alistair here — lost the line to the desk for a sec. Try again?"`.

## Причина
После изменения файла `alistair_bot.py` функция вызова модели `llm_chat()` откатилась к старому прямому вызову API через `urllib` вместо OpenAI SDK. Запросы блокировались провайдером с ошибкой `403 Forbidden`.

## Решение
1. Восстановлен вызов через OpenAI SDK + Fallback Chain.
2. Проверена и подтверждена автозагрузка `.env.local` при старте бота.
3. Проведено локальное тестирование `run_agent()`.

## Урок / Правило
Боты Agent Club должны вызывать LLM строго через OpenAI SDK с поддержкой Fallback Chain, а не сырой `urllib`. При любых правках ботов обязательно проверять загрузку `.env.local` и работоспособность fallback-цепочки.
