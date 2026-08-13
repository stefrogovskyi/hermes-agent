# -*- coding: utf-8 -*-
"""
kanban_daily_brief.py — Утренний 08:00 AM обзор движений карточек, статусов и комментариев Стефана ИСКЛЮЧИТЕЛЬНО на доске Гермеса.
"""

import os, sys, json, urllib.request
from datetime import datetime

AGENT = "hermes"
AGENT_NAME = "🔷 Hermes Stevenson (Orchestrator)"

def fetch_agent_kanban():
    url = f"https://dev.aavalanche.com/kanban_api.php?agent={AGENT}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data
    except Exception:
        return None

def run_kanban_review():
    now_str = datetime.now().strftime("%d.%m.%Y %H:%M")
    data = fetch_agent_kanban()
    
    print(f"<b>📊 ЕЖЕДНЕВНЫЙ УТРЕННИЙ ОБЗОР КАНБАНА ГЕРМЕСА (08:00)</b>")
    print(f"Сводка статусов и комментариев (Срез на {now_str}):\n")
    
    if not data or not data.get("cards"):
        print("⚠️ Нет активных данных по доске Гермеса.")
        return
        
    cards = data.get("cards", [])
    cols = {"todo": [], "in_progress": [], "recurring": [], "completed": []}
    comments_list = []
    
    for c in cards:
        c_col = c.get("column_id", "todo")
        if c_col in cols:
            cols[c_col].append(c)
        if c.get("comments"):
            for cm in c["comments"]:
                comments_list.append((c["title"], cm))
                
    print(f"<b>{AGENT_NAME}</b> (Всего задач: {len(cards)}):")
    print(f"  • 📋 TODO: {len(cols['todo'])} | ⚡ IN PROGRESS: {len(cols['in_progress'])} | 🔄 CRON: {len(cols['recurring'])} | ✅ DONE: {len(cols['completed'])}\n")
    
    if cols["in_progress"]:
        print("⚡ <b>Задачи в работе (IN PROGRESS):</b>")
        for c in cols["in_progress"]:
            moved = f" (🕒 {c['moved_at']})" if c.get("moved_at") else ""
            print(f"  • <code>{c['title']}</code>{moved}")
        print()
            
    if cols["todo"]:
        print("📋 <b>Бэклог (TODO):</b>")
        for c in cols["todo"]:
            print(f"  • <code>{c['title']}</code>")
        print()

    if comments_list:
        print("💬 <b>Комментарии Стефана:</b>")
        for task_title, cm in comments_list:
            author = cm.get("author", "Stefan")
            txt = cm.get("text", "")
            tm = cm.get("timestamp", "")
            print(f"  • <b>{author}</b> к «{task_title}» ({tm}): <i>{txt}</i>")
        print()

if __name__ == "__main__":
    run_kanban_review()
