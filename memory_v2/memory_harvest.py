#!/usr/bin/env python3
"""
memory_harvest.py — извлечение полезного из сессии в memory_v2.
Не пишет файлы сам (это делает агент — Hermes), а ВЫВОДИТ кандидатов:
инструкции Стефана, зафиксированные методики, успешные кейсы + предложенную категорию домена.

Использование:
  python memory_harvest.py <path_to_session_text.txt>
  python memory_harvest.py -   (читает stdin)

Вывод: список кандидатов с тегом домена (agent_club / ai_infra / memory_systems /
business / personal / new:<name>). Агент решает, создать case или дописать в domains/.
"""
import sys, re

DOMAINS = {
    "agent_club": ["бот", "richard", "лиз", "liz", "alistair", "ben", "агент", "409", "403", "getUpdates", "ттс", "голос", "ping", "боту"],
    "ai_infra": ["nous", "openrouter", "gemini", "hy3", "модел", "провайдер", "embed", "sdk", "urllib", "api key", "ключ"],
    "memory_systems": ["памят", "memory", "pinecone", "recall", "кейс", "индекс", "семантич", "вектор"],
    "business": ["searates", "navo", "avalanch", "логист", "фрахт", "груз", "silpo", "заказ", "бизнес"],
    "personal": ["стефан", "русск", "проактив", "сам", "обуч", "рефлекс", "правило", "запомни", "всегда", "никогда"],
}

INSTRUCTION_MARKERS = [
    "запомни", "правило", "всегда", "никогда", "не делай", "не надо", "делай",
    "обязан", "требу", "запрещ", "никогда не", "сначала", "провер", "факт",
]

def classify(text):
    t = text.lower()
    scores = {d: sum(1 for k in kws if k in t) for d, kws in DOMAINS.items()}
    best = max(scores, key=scores.get)
    if scores[best] == 0:
        return "new:uncategorized"
    return best

def extract_candidates(text):
    lines = text.splitlines()
    cands = []
    for i, ln in enumerate(lines):
        low = ln.lower()
        # инструкция Стефана (маркеры)
        if any(m in low for m in INSTRUCTION_MARKERS):
            cands.append(("INSTRUCTION", ln.strip(), classify(ln)))
        # успешный кейс / завершённая задача
        elif re.search(r"(готово|сделан|работает|проверен|запущен|исправлен|доделал|активирован)", low) and len(ln) > 30:
            cands.append(("SUCCESS", ln.strip(), classify(ln)))
        # методика (как делать)
        elif re.search(r"(через|использ|вызвать|напрямую|в рантайме|скрипт|функци)", low) and len(ln) > 40:
            cands.append(("METHOD", ln.strip(), classify(ln)))
    return cands

def main():
    if len(sys.argv) > 1 and sys.argv[1] != "-":
        text = open(sys.argv[1], encoding="utf-8").read()
    else:
        text = sys.stdin.read()
    cands = extract_candidates(text)
    if not cands:
        print("[harvest] кандидатов не найдено")
        return
    print(f"[harvest] найдено {len(cands)} кандидатов:\n")
    for kind, snippet, dom in cands[:25]:
        print(f"[{kind}] ({dom})\n  {snippet[:160]}\n")
    # сводка по доменам
    from collections import Counter
    cnt = Counter(d for _, _, d in cands)
    print("=== Распределение по доменам ===")
    for d, n in cnt.most_common():
        print(f"  {d}: {n}")

if __name__ == "__main__":
    main()
