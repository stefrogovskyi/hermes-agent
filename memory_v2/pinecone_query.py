#!/usr/bin/env python3
"""
pinecone_query.py — семантический поиск по memory_v2 через Pinecone.
Если PINECONE_API_KEY не задан ИЛИ нет эмбеддинга — падает на recall.py (keyword).

Использование:
  python pinecone_query.py <запрос на естественном языке>
  python pinecone_query.py почему бот молчит и шлёт заглушку
"""
import os, sys
from pathlib import Path

MEMORY_V2 = os.path.dirname(os.path.abspath(__file__))

def keyword_fallback(query):
    print("[pinecone_query] Pinecone недоступен — keyword-поиск:")
    sys.path.insert(0, MEMORY_V2)
    import recall
    recall.main_with_terms(query.split())

def main():
    if len(sys.argv) < 2:
        print("Usage: python pinecone_query.py <query>")
        return
    query = " ".join(sys.argv[1:])
    key = os.environ.get("PINECONE_API_KEY")
    if not key:
        try:
            for line in Path(r"C:\Users\Stefan\AppData\Local\hermes\.env").read_text(encoding="utf-8").splitlines():
                if line.strip().startswith("PINECONE_API_KEY="):
                    key = line.split("=",1)[1].strip().strip('"')
                    os.environ["PINECONE_API_KEY"] = key
        except Exception:
            pass
    if not key:
        keyword_fallback(query)
        return
    # гарантированно загрузить OPENROUTER_API_KEY в env (для embeddings)
    if not os.environ.get("OPENROUTER_API_KEY"):
        try:
            for line in Path(r"C:\Users\Stefan\AppData\Local\hermes\.env").read_text(encoding="utf-8").splitlines():
                if line.strip().startswith("OPENROUTER_API_KEY="):
                    os.environ["OPENROUTER_API_KEY"] = line.split("=",1)[1].strip().strip('"')
        except Exception:
            pass
    try:
        from pinecone import Pinecone
    except ImportError:
        keyword_fallback(query)
        return

    # 1. Попробовать прямо через OPENAI_API_KEY
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

    embed = None
    if oak:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=oak)
            embed = lambda t: client.embeddings.create(model="text-embedding-3-small", input=t).data[0].embedding
        except Exception as e:
            print("[pinecone_query] OpenAI embed fail:", e)

    if not embed:
        oa = os.environ.get("OPENROUTER_API_KEY")
        if oa:
            try:
                from openai import OpenAI
                client = OpenAI(api_key=oa, base_url="https://openrouter.ai/api/v1")
                embed = lambda t: client.embeddings.create(model="openai/text-embedding-3-small", input=t).data[0].embedding
            except Exception:
                pass
    if not embed:
        try:
            sys.path.insert(0, r"C:\Users\Stefan\AppData\Local\hermes\hermes-agent")
            from agent.auxiliary_client import _resolve_nous_pool_runtime_api, _create_openai_client
            creds = _resolve_nous_pool_runtime_api(force_refresh=False)
            if creds and creds[0]:
                c = _create_openai_client(api_key=creds[0], base_url=creds[1])
                embed = lambda t: c.embeddings.create(model="text-embedding-3-small", input=t).data[0].embedding
        except Exception:
            pass
    if not embed:
        keyword_fallback(query)
        return

    pc = Pinecone(api_key=key)
    index = pc.Index("hermes-memory")
    vec = embed(query)
    res = index.query(vector=vec, top_k=5, include_metadata=True)
    print(f"[pinecone_query] семантический поиск по '{query}':\n")
    matches = res.matches if hasattr(res, "matches") else res.get("matches", [])
    for m in matches:
        meta = m.metadata if hasattr(m, "metadata") else m.get("metadata", {})
        score = m.score if hasattr(m, "score") else m.get("score", 0.0)
        file_name = meta.get("file") if isinstance(meta, dict) else getattr(meta, "file", "unknown")
        text_val = meta.get("text", "") if isinstance(meta, dict) else getattr(meta, "text", "")
        print(f"=== {file_name} (score {score:.2f}) ===")
        print(text_val[:400])
        print()

if __name__ == "__main__":
    main()
