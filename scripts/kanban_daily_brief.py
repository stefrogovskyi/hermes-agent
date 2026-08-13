# -*- coding: utf-8 -*-
"""
kanban_daily_brief.py — Утренний 08:00 AM обзор движений карточек, статусов и комментариев Стефана на всех 6 Канбан-бордах Vercel.
"""

import os, sys, json, urllib.request
from datetime import datetime

AGENTS = ["hermes", "ben", "richard", "callum", "alistair", "liz"]
AGENT_NAMES = {
    "hermes": "🔷 Hermes Stevenson (Orchestrator)",
    "ben": "🟠 Ben Jett (Growth Marketing)",
    "richard": "💼 Richard Marlowe (B2B Sales)",
    "callum": "💻 Callum Vance (Tech Lead)",
    "alistair": "🟣 Alistair Sterling (Operations)",
    "liz": "🌸 Liz Harper (HR & Internal Comms)"
}

def fetch_agent_kanban(agent):
    url = f"https://dev.aavalanche.com/kanban_api.php?agent={agent}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data
    except Exception as e:
        return None

def run_kanban_review():
    now_str = datetime.now().strftime("%d.%m.%Y %H:%M")
    print(f"<b>📊 ЕЖЕДНЕВНЫЙ УТРЕННИЙ ОБЗОР КАНБАНОВ (08:00)</b>")
    print(f"Сводка статусов и комментариев на 6 досках Vercel (Срез на {now_str}):\n")
    
    total_cards = 0
    total_comments = 0
    
    for agent in AGENTS:
        display_name = AGENT_NAMES.get(agent, agent.upper())
        data = fetch_agent_kanban(agent)
        
        if not data or not data.get("cards"):
            print(f"<b>{display_name}</b>: ⚠️ Нет активных данных\n")
            continue
            
        cards = data.get("cards", [])
        total_cards += len(cards)
        
        cols = {"todo": [], "in_progress": [], "recurring": [], "completed": []}
        agent_comments = []
        
        for c in cards:
            c_col = c.get("column_id", "todo")
            if c_col in cols:
                cols[c_col].append(c)
            if c.get("comments"):
                for cm in c["comments"]:
                    agent_comments.append((c["title"], cm))
                    total_comments += 1
                    
        print(f"<b>{display_name}</b> (Всего карточек: {len(cards)}):")
        print(f"  • 📋 TODO: {len(cols['todo'])} | ⚡ IN PROGRESS: {len(cols['in_progress'])} | 🔄 CRON: {len(cols['recurring'])} | ✅ DONE: {len(cols['completed'])}")
        
        # Show in_progress items
        if cols["in_progress"]:
            for c in cols["in_progress"][:3]:
                moved = f" (🕒 {c['moved_at']})" if c.get("moved_at") else ""
                print(f"    ➔ ⚡ <code>{c['title']}</code>{moved}")
                
        # Show recent comments if any
        if agent_comments:
            for task_title, cm in agent_comments[-2:]:
                author = cm.get("author", "Stefan")
                txt = cm.get("text", "")
                tm = cm.get("timestamp", "")
                print(f"    💬 <b>{author}</b> к «{task_title}» ({tm}): <i>{txt}</i>")
                
        print()

if __name__ == "__main__":
    run_kanban_review()
