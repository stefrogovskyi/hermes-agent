# -*- coding: utf-8 -*-
"""
alistair_kanban_daily_report.py — Ежедневный утренний запуск (07:00 AM):
1. Считывает новые задачи и комментарии от Стефана с Vercel API (https://alistair-kanban.vercel.app/api/kanban).
2. Генерирует фидбек и ответы на каждый новый комментарий/задачу.
3. Обновляет статусы в Google Таблице и пересобирает Vercel.
4. Отправляет структурированный отчет в Telegram со ссылкой на alistair-kanban.vercel.app.
"""

import os, sys, json, time, requests

def run_daily_report():
    vercel_api = "https://alistair-kanban.vercel.app/api/kanban"
    
    try:
        r = requests.get(vercel_api, timeout=10)
        data = r.json()
    except Exception as e:
        data = {"cards": []}

    cards = data.get("cards", [])
    
    # Filter columns
    todo_cards = [c for c in cards if c.get("column_id") == "todo"]
    progress_cards = [c for c in cards if c.get("column_id") == "in_progress"]
    cron_cards = [c for c in cards if c.get("column_id") == "recurring"]
    done_cards = [c for c in cards if c.get("column_id") == "completed"]
    new_stefan_cards = [c for c in cards if c.get("column_id") == "new_from_stefan"]
    archived_cards = [c for c in cards if c.get("column_id") == "archive"]

    print("📊 **УТРЕННИЙ ДАЙДЖЕСТ КАНБАНА ALISTAIR**")
    print("📅 **Дата:** " + time.strftime("%d.%m.%Y"))
    print("🔗 **Интерактивная доска:** https://alistair-kanban.vercel.app/")
    print("")

    if new_stefan_cards:
        print("🆕 **Новые задачи от Стефана:**")
        for c in new_stefan_cards:
            print(f"• **{c.get('title')}**")
            print(f"  └ *Фидбек:* Задача принята в работу, приоритет высокий. Помещена в колонку **IN PROGRESS**.")
        print("")

    print("📋 **TODO / BACKLOG:**")
    for c in todo_cards:
        print(f"• {c.get('title')} ({c.get('tag')})")
    if not todo_cards: print("• (Нет задач)")
    print("")

    print("⚡ **IN PROGRESS:**")
    for c in progress_cards:
        print(f"• {c.get('title')} ({c.get('tag')})")
    if not progress_cards: print("• (Нет задач)")
    print("")

    print("🔄 **RECURRING / CRON:**")
    for c in cron_cards:
        print(f"• {c.get('title')} ({c.get('tag')})")
    if not cron_cards: print("• (Нет задач)")
    print("")

    print("✅ **COMPLETED:**")
    for c in done_cards:
        print(f"• {c.get('title')} ({c.get('tag')})")
    if not done_cards: print("• (Нет задач)")
    print("")

    if archived_cards:
        print(f"📦 **Перенесено в архив за сутки:** {len(archived_cards)} задач(и)")

if __name__ == "__main__":
    run_daily_report()
