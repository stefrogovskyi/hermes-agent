# Pinecone Vector Memory — technique & gotchas (verified 2026-07-28)

## What it does
`pinecone_sync.py` (in memory_v2) chunks `cases/`+`principles/` (~800 chars each),
embeds them, and upserts into Pinecone index `hermes-memory` (dim 1536, cosine,
serverless aws us-east-1). `pinecone_query.py` embeds a natural-language question
and returns nearest chunks — semantic search (finds "bot is silent / sends
placeholder" without the words Richard/403). Keyword search (`recall.py`) cannot.

## Embeddings provider — OPENROUTER, not Nous
- OpenRouter `openai/text-embedding-3-small` → FREE, works (dim 1536).
- Nous `text-embedding-3-small` (via Nous portal) → 404 "requires available
  credits" (no paid balance). DO NOT use Nous for embeddings.
- Provider precedence in the scripts: OpenRouter first, Nous fallback.

## Pinecone free tier (Starter, verified)
5 indexes, 2 GB storage, 2M write + 1M read units/month, pauses after 3 weeks
inactivity, us-east-1 only. Plenty for thousands of ~3-5KB cases.

## GOTCHA (cost us a debug cycle)
Standalone scripts that read `.env` via `Path(r"C:\...")` MUST have
`from pathlib import Path` imported at top. Missing it → `NameError` swallowed by
`try/except` → key not loaded → silent fallback to Nous embeddings (404). If
embeddings keep hitting Nous 404, check imports first.

## Activate
1. `PINECONE_API_KEY=...` in `C:/Users/Stefan/AppData/Local/hermes/.env`.
2. `pip install pinecone` (done in hermes venv).
3. `python pinecone_sync.py` (creates index + loads chunks).
4. Query: `python pinecone_query.py <question>`.
Without the key, both scripts no-op gracefully (file search stays active).
