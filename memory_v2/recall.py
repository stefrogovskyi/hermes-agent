#!/usr/bin/env python3
"""
recall.py — быстрый поиск по долгосрочной памяти Hermes (memory_v2).
Без внешних сервисов: использует ripgrep-подобный поиск через subprocess grep
(или встроенный re-скан файлов). Возвращает релевантные куски кейсов/принципов.

Использование:
  python recall.py <ключевое слово> [еще слова...]
  python recall.py richard 403
  python recall.py гипотеза факт
"""
import sys, os, re, glob

MEMORY_V2 = os.path.dirname(os.path.abspath(__file__))

def collect_files():
    files = []
    for pat in ("cases/*.md", "principles/*.md", "index.md"):
        files.extend(glob.glob(os.path.join(MEMORY_V2, pat)))
    return files

def search(query_terms, files, max_hits=8, ctx=2):
    terms = [t.lower() for t in query_terms if t]
    if not terms:
        return []
    results = []
    for fp in files:
        try:
            text = open(fp, encoding="utf-8").read()
        except Exception:
            continue
        lines = text.splitlines()
        lower = [l.lower() for l in lines]
        for i, ln in enumerate(lower):
            if any(t in ln for t in terms):
                start = max(0, i - ctx)
                end = min(len(lines), i + ctx + 1)
                snippet = "\n".join(lines[start:end])
                results.append((fp, i + 1, snippet))
                if len(results) >= max_hits:
                    return results
    return results

def main_with_terms(terms):
    """Точка входа для импорта из других скриптов (напр. pinecone_query)."""
    files = collect_files()
    hits = search(terms, files)
    if not hits:
        print("[recall] ничего не найдено по:", " ".join(terms))
        return
    print(f"[recall] найдено {len(hits)} совпадений:\n")
    for fp, line_no, snippet in hits:
        rel = os.path.relpath(fp, MEMORY_V2)
        print(f"=== {rel} (строка {line_no}) ===")
        print(snippet)
        print()

def main():
    if len(sys.argv) < 2:
        print("Usage: python recall.py <keyword> [more keywords]")
        return
    main_with_terms(sys.argv[1:])

if __name__ == "__main__":
    main()
