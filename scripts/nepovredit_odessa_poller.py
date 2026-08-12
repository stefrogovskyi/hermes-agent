# -*- coding: utf-8 -*-
"""
nepovredit_odessa_poller.py — Автоматический мониторинг сигналов и точек из приватного канала «Не повредит, Одесса».
Работает через авторизованную сессию Юзербота Стефана (@stefrogovskiy) 24/7 с точными метками времени (ЧЧ:ММ).
"""

import asyncio, os, sys, json, re, html
from datetime import datetime
from telethon import TelegramClient

HERMES_DIR = "/opt/hermes"
SESSION_PATH = os.path.join(HERMES_DIR, "stefan_userbot.session")
CACHE_FILE = os.path.join(HERMES_DIR, "state", "odessa_seen_msgs.json")
os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)

API_ID = 31246421
API_HASH = "e96f7e4b8785d721deb761c55e2c8252"
TARGET_CHANNEL_ID = -1002050105527  # Не повредит, Одесса

def load_seen_ids():
    if os.path.exists(CACHE_FILE):
        try:
            return set(json.load(open(CACHE_FILE, encoding='utf-8')).get('seen_ids', []))
        except Exception:
            pass
    return set()

def save_seen_ids(seen_ids):
    data = {
        'seen_ids': list(seen_ids)[-500:],  # keep last 500
        'last_check': datetime.now().isoformat()
    }
    open(CACHE_FILE, 'w', encoding='utf-8').write(json.dumps(data, ensure_ascii=False, indent=2))

def clean_text(raw_text):
    if not raw_text: return ""
    # Strip promotional boilerplate footers
    txt = raw_text.split("❕[Сообщить]")[0].split("❕Сообщить❕")[0]
    txt = re.sub(r"##", "", txt)
    txt = txt.strip()
    return txt

async def poll_odessa_channel(limit=10, show_all=False):
    seen_ids = load_seen_ids()
    is_first_run = len(seen_ids) == 0
    
    client = TelegramClient(SESSION_PATH, API_ID, API_HASH)
    await client.connect()
    
    if not await client.is_user_authorized():
        print("❌ ERROR: Userbot session not authorized.")
        await client.disconnect()
        return

    try:
        channel = await client.get_entity(TARGET_CHANNEL_ID)
    except Exception as e:
        print(f"❌ Could not get entity for channel ID {TARGET_CHANNEL_ID}: {e}")
        await client.disconnect()
        return

    msgs = await client.get_messages(channel, limit=limit)
    await client.disconnect()

    if not msgs:
        print("В канале нет новых сообщений.")
        return

    new_items = []
    current_seen = set(seen_ids)

    for m in msgs:
        msg_id = m.id
        current_seen.add(msg_id)
        
        txt = clean_text(m.text)
        if not txt: continue
        
        pub_time = m.date.strftime("%H:%M") if m.date else "N/A"
        pub_date = m.date.strftime("%d.%m.%Y") if m.date else "N/A"
        
        item = {
            "id": msg_id,
            "time": pub_time,
            "date": pub_date,
            "text": txt
        }
        
        if show_all or is_first_run or msg_id not in seen_ids:
            new_items.append(item)

    save_seen_ids(current_seen)

    print(f"### 📍 СИГНАЛЫ И ТОЧКИ — «НЕ ПОВРЕДИТ, ОДЕССА» (Срез на {datetime.now().strftime('%d.%m.%Y %H:%M')})\n")
    print(f"📡 **Проверена лента канала.** Отобрано сообщений с точным временем публикации:\n")

    if not new_items:
        print("Новых сигналов с момента последней проверки не поступало.")
        return

    for item in new_items:
        print(f"⏰ <b>[{item['time']}]</b> ({item['date']})")
        print(f"  📍 {html.escape(item['text'])}\n")

if __name__ == "__main__":
    show_all_flag = "--all" in sys.argv or "-a" in sys.argv
    asyncio.run(poll_odessa_channel(limit=15, show_all=show_all_flag))
