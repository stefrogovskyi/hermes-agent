# Case: 2026-07-28 — Pinecone vector memory activated

## Симптом
Нужна семантическая память поверх memory_v2 (файлы + grep не ловят «похожий инцидент» без точных слов).

## Решение (ФАКТ, проверено end-to-end)
- `pinecone_sync.py` — создаёт index `hermes-memory` (dim 1536, cosine, aws us-east-1),
  режет cases/principles на чанки ~800 символов, векторизует через OpenRouter
  `openai/text-embedding-3-small` (free), грузит в Pinecone.
- `pinecone_query.py` — семантический поиск. Если Pinecone/embed недоступны — fallback на recall.py.
- **Ключ Pinecone:** `PINECONE_API_KEY` в `hermes/.env`. План Starter (free): 5 indexes, 2GB, 2M write/1M read units/mo.
- **Embeddings:** OpenRouter (free), НЕ Nous (Nous embeddings требуют кредитов → 404).

## Баг, который нашли и исправили
- `pinecone_sync.py` / `pinecone_query.py` НЕ импортировали `from pathlib import Path`
  → чтение `.env` падало молча (NameError в try/except) → `ork` пустой → embeddings шли
  на Nous (404). Фикс: добавить `from pathlib import Path`.
- Размерность: `text-embedding-3-small` = 1536 (не 1024). Index создан с 1536.

## Как пользоваться
- Индексировать новые кейсы: `python pinecone_sync.py` (в папке memory_v2).
- Семантический поиск: `python pinecone_query.py <вопрос на русском>`.
- Skill `memory-recall` дёргает recall.py; для семантики — pinecone_query.py.

## Антихрупкость
- Файловая память (recall.py) работает ВСЕГДА (без внешних сервисов).
- Pinecone — надстройка, не мешает: без ключа система на файлах.
- Obsidian (опционально): открыть memory_v2/ как Vault → визуальный граф связей.
