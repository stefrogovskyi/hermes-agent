# Case: 2026-07-28 — Richard 403 / Hypothesis-vs-Fact Failure

## Симптом
Richard (richnavobot) отвечал заглушкой «Richard here — briefly lost the line to the desk» вместо реального ответа. В логе — `HTTP Error 403: Forbidden` по всем моделям (tencent/hy3:free, poolside, stepfun).

## Ложная гипотеза (ЧТО Я СДЕЛАЛ НЕПРАВИЛЬНО)
1. Взял статический urllib-тест (бил ключ из auth.json в `inference-api.nousresearch.com/v1/chat/completions` вручную) → получил 403.
2. **СДЕЛАЛ ВЫВОД «nous-ключ не работает / Hermes на самом деле через OpenRouter»** — не перепроверив факт.
3. Сразу побежал править код: копировал ключи из `.env` Hermes в `.env.local` Ричарда, добавил OpenRouter fallback, менял `_fresh_nous_key()`.
4. Противоречил сам себе: сначала сказал «Hermes работает на hy3:nous», потом «Hermes на OpenRouter».
5. Stefan указал: раз я не доложил о переключении модели (а по правилу должен был) — значит работаю на hy3:nous. Моя догадка была ложной.

## Корень (ФАКТ, проверенный)
- Hermes работает на `tencent/hy3:free` от Nous через **OpenAI SDK** (`_create_openai_client` из `hermes-agent/agent/auxiliary_client.py`), а НЕ через голый urllib.
- Richard бил в Nous **голым urllib** (`_http_json`) → Nous возвращал 403 (SDK шлёт запрос с форматом/заголовками, которые urllib не воспроизводит).
- Статический тест urllib давал 403, но реальный вызов через SDK работал. **Ключ и модель были в порядке — проблема в коде Ричарда (способ отправки), а не в ключе.**
- Доказано фактом: вызов `llm_chat` Ричарда через SDK вернул «I am Hunyuan, a large language model developed by Tencent» на hy3:nous.

## Фикс (применён и проверен)
- `richard_bot.py` `llm_chat` переписан: вместо голого urllib использует `from agent.auxiliary_client import _resolve_nous_pool_runtime_api, _create_openai_client` (тот же механизм, что у Hermes).
- OpenRouter-блок оставлен как страховка, но Ричард на нём не виснет — работает на hy3:nous.
- Ричард теперь идентичен Hermes: `tencent/hy3:free`, `inference-api.nousresearch.com/v1`.

## Рефлексия (зарегистрированный опыт — НЕ ПОТЕРЯНО)
**ЖЁСТКОЕ ПРАВИЛО Стефана:** любую гипотезу сначала ПОДТВЕРЖДАТЬ ФАКТОМ (реальный вызов / лог / ответ), а не выдавать за истину и сразу бежать править код. Ложные гипотезы ломают архитектуру — если системы строятся на ложных допущениях, они постоянно ломаются.
- Правильный паттерн: «я работаю на X → значит X рабочий → проблема в коде, а не в ключе/модели» → проверить ФАКТ (как именно Hermes ходит), потом править.
- НЕ дёргать `getUpdates` ботов вручную — конфликт 409 глушит их очередь (было у Richard/Liz).
- Проверка бота: НЕ просить Стефана «напиши ему». Сам пингую логику бота напрямую в рантайме (вызвать его `llm_chat`/`run_agent` в том же python, как `importlib.util.spec_from_file_location`) и посмотреть ответ+модель.

## Где искать при повторе
- Код Richard: `C:/Users/Stefan/My Drive/Equity/My Biz/Partner companies/Navo/6. Departments/Richard Marlowe/Richard Hermes/richard_bot.py`
- Функция `llm_chat` (строки ~313+) — через OpenAI SDK.
- Hermes runtime client: `C:/Users/Stefan/AppData/Local/hermes/hermes-agent/agent/auxiliary_client.py` (`_resolve_nous_pool_runtime_api`, `_create_openai_client`).
- Если бот молчит и в логе 403 → смотреть, НЕ urllib ли это (нужен SDK).
