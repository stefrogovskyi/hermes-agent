#!/usr/bin/env python3
"""
pinecone_sync.py — индексирует memory_v2 (cases + principles) в Pinecone.
Не мешает: если PINECONE_API_KEY не задан — тихо выходит.
Создаёт index "hermes-memory" (dim 1536, cosine) при первом запуске.
Эмбеддинги — через OpenRouter (text-embedding-3-small, free), fallback на Nous.

Использование:
  python pinecone_sync.py            # полная синхронизация
  python pinecone_sync.py --check    # только проверка готовности
"""
import os, sys, glob, time
from pathlib import Path

MEMORY_V2 = os.path.dirname(os.path.abspath(__file__))
INDEX_NAME = "hermes-memory"

def collect():
    files = []
    for pat in ("cases/*.md", "principles/*.md"):
        files.extend(glob.glob(os.path.join(MEMORY_V2, pat)))
    out = []
    for fp in files:
        try:
            text = open(fp, encoding="utf-8").read()
        except Exception:
            continue
        # делим на чанки ~800 символов для лучшего поиска
        chunk = 800
        for i in range(0, len(text), chunk):
            out.append((fp, i // chunk, text[i:i+chunk]))
    return out

def get_embedder():
    """Вернуть функцию embed(text)->list[float] или None.
    Прямой OpenAI API Key — приоритет (text-embedding-3-small).
    OpenRouter / Nous — фолбэки."""
    oak = os.environ.get("OPENAI_API_KEY")
    if not oak:
        for p in (Path("/opt/hermes/.env"), Path(r"C:\Users\Stefan\AppData\Local\hermes\.env")):
            try:
                if p.exists():
                    for line in p.read_text(encoding="utf-8").splitlines():
                        if line.strip().startswith("OPENAI_API_KEY="):
                            oak = line.split("=", 1)[1].strip().strip("\r").strip('"')
                            break
            except Exception:
                pass
            if oak:
                break

    if oak:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=oak)
            def embed_direct_oai(t):
                r = client.embeddings.create(model="text-embedding-3-small", input=t)
                return r.data[0].embedding
            return embed_direct_oai
        except Exception as e:
            print("[pinecone_sync] Direct OpenAI embed fail: %s" % e)

    # явно подгрузить OPENROUTER_API_KEY из .env Hermes, если нет в env
    ork = os.environ.get("OPENROUTER_API_KEY")
    if ork:
        ork = ork.strip().strip("\r").strip('"')
    if not ork:
        for p in (Path("/opt/hermes/.env"), Path(r"C:\Users\Stefan\AppData\Local\hermes\.env")):
            try:
                if p.exists():
                    for line in p.read_text(encoding="utf-8").splitlines():
                        if line.strip().startswith("OPENROUTER_API_KEY="):
                            ork = line.split("=",1)[1].strip().strip("\r").strip('"')
                            break
            except Exception:
                pass
            if ork:
                break
    if ork:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=ork, base_url="https://openrouter.ai/api/v1")
            def embed_oai(t):
                try:
                    r = client.embeddings.create(model="openai/text-embedding-3-small", input=t)
                    return r.data[0].embedding
                except Exception as e:
                    # детектор исчерпания лимита OpenRouter (429)
                    if "429" in str(e) or "Rate limit" in str(e) or "rate_limit" in str(e):
                        msg = ("[pinecone_sync] ⚠️ OpenRouter free-tier лимит embeddings исчерпан (429). "
                               "Нужно закинуть $10 на openrouter.ai/settings/credits — это поднимет лимит "
                               "с 50 до 1000 запросов/день навсегда. Пока Pinecone-синк приостановлен; "
                               "файловый поиск recall.py продолжает работать.")
                        print(msg)
                        # пытаемся уведомить Стефана в Telegram (если gateway доступен)
                        try:
                            import urllib.request, urllib.parse
                            tok = None
                            for env_p in (Path("/opt/hermes/.env"), Path(r"C:\Users\Stefan\AppData\Local\hermes\.env")):
                                if env_p.exists():
                                    for line in env_p.read_text(encoding="utf-8").splitlines():
                                        if line.strip().startswith("TELEGRAM_BOT_TOKEN="):
                                            tok = line.split("=",1)[1].strip().strip("\r").strip('"')
                                            break
                                if tok:
                                    break
                            if tok:
                                uid = "330656040"
                                urllib.request.urlopen(
                                    f"https://api.telegram.org/bot{tok}/sendMessage?chat_id={uid}&text="
                                    + urllib.parse.quote(msg), timeout=10)
                        except Exception:
                            pass
                        raise
                    raise
            return embed_oai
        except Exception as e:
            print("[pinecone_sync] OpenRouter embed fail: %s" % e)
    # фолбэк: Hermes Nous (может требовать кредитов)
    try:
        for hp in ("/opt/hermes/hermes-agent", r"C:\Users\Stefan\AppData\Local\hermes\hermes-agent"):
            if os.path.exists(hp):
                sys.path.insert(0, hp)
                break
        from agent.auxiliary_client import _resolve_nous_pool_runtime_api, _create_openai_client
        creds = _resolve_nous_pool_runtime_api(force_refresh=False)
        if creds and creds[0]:
            client = _create_openai_client(api_key=creds[0], base_url=creds[1])
            def embed_nous(t):
                r = client.embeddings.create(model="text-embedding-3-small", input=t)
                return r.data[0].embedding
            return embed_nous
    except Exception as e:
        print("[pinecone_sync] Nous embed fail: %s" % e)
    return None

def main():
    key = os.environ.get("PINECONE_API_KEY")
    if key:
        key = key.strip().strip("\r").strip('"')
    if not key:
        # попытаться загрузить из .env Hermes
        for p in (Path("/opt/hermes/.env"), Path(r"C:\Users\Stefan\AppData\Local\hermes\.env")):
            try:
                if p.exists():
                    for line in p.read_text(encoding="utf-8").splitlines():
                        if line.strip().startswith("PINECONE_API_KEY="):
                            key = line.split("=",1)[1].strip().strip("\r").strip('"')
                            os.environ["PINECONE_API_KEY"] = key
                            break
            except Exception:
                pass
            if key:
                break
    if not key:
        print("[pinecone_sync] PINECONE_API_KEY не задан — пропуск. Файловый поиск recall.py активен.")
        return
    # гарантированно загрузить OPENROUTER_API_KEY в env (для embeddings)
    if not os.environ.get("OPENROUTER_API_KEY"):
        for p in (Path("/opt/hermes/.env"), Path(r"C:\Users\Stefan\AppData\Local\hermes\.env")):
            try:
                if p.exists():
                    for line in p.read_text(encoding="utf-8").splitlines():
                        if line.strip().startswith("OPENROUTER_API_KEY="):
                            ork = line.split("=",1)[1].strip().strip("\r").strip('"')
                            os.environ["OPENROUTER_API_KEY"] = ork
                            break
            except Exception:
                pass
            if os.environ.get("OPENROUTER_API_KEY"):
                break

    try:
        from pinecone import Pinecone
    except ImportError:
        print("[pinecone_sync] pinecone SDK не установлен — pip install pinecone. Пропуск.")
        return

    embed = get_embedder()
    if not embed:
        print("[pinecone_sync] нет провайдера эмбеддингов — пропуск. Добавь OPENAI_API_KEY или настрой Nous embeddings.")
        return

    pc = Pinecone(api_key=key)
    if INDEX_NAME not in [i.name for i in pc.list_indexes()]:
        pc.create_index(name=INDEX_NAME, dimension=1536, metric="cosine",
                        spec={"serverless": {"cloud": "aws", "region": "us-east-1"}})
        time.sleep(5)
    index = pc.Index(INDEX_NAME)

    chunks = collect()
    print(f"[pinecone_sync] индексирую {len(chunks)} чанков...")
    batch = []
    for fp, ci, text in chunks:
        vec = embed(text)
        rel = os.path.relpath(fp, MEMORY_V2).replace("\\", "/")
        batch.append({"id": f"{rel}#{ci}", "values": vec,
                      "metadata": {"file": rel, "chunk": ci, "text": text[:500]}})
        if len(batch) >= 50:
            index.upsert(vectors=batch)
            batch = []
    if batch:
        index.upsert(vectors=batch)
    print(f"[pinecone_sync] готово: {len(chunks)} чанков в index '{INDEX_NAME}'")

if __name__ == "__main__":
    main()
