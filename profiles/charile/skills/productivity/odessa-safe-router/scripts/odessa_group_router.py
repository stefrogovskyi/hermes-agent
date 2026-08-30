#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
odessa_group_router.py — Сканер группы 'Не повредит, Одесса' и построитель безопасных маршрутов.
"""

import os
import sys
import re
import json
import argparse
import asyncio
import urllib.parse
from datetime import datetime, timezone, timedelta

# Force UTF-8 encoding
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Constants
GROUP_ID = -1002050105527  # 'Не повредит, Одесса'
API_ID = 20400084
API_HASH = "b2e2d93e1792bc443ae3bd40a9b8979c"

# Candidate session paths
SESSION_PATHS = [
    "/opt/hermes/stefan_userbot.session",
    os.path.expanduser("~/.hermes/stefan_userbot.session"),
    os.path.join(os.environ.get("LOCALAPPDATA", ""), "hermes", "router", "router_telethon_session.session"),
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "router", "router_telethon_session.session"),
    os.path.join(os.path.dirname(__file__), "router_telethon_session.session")
]

def get_session_path():
    for p in SESSION_PATHS:
        # Strip .session suffix for telethon
        base_p = p[:-8] if p.endswith(".session") else p
        if os.path.exists(base_p + ".session") or os.path.exists(p):
            return base_p
    return "/opt/hermes/stefan_userbot"

KEYWORD_PATTERNS = [
    r'##блокпост', r'блокпост', r'\bБП\b', r'\bбп\b', r'\bтцк\b', r'\bмусор\w*',
    r'\bбус\b', r'\bпроверк\w*', r'\bтормозят\b', r'\bпасут\b', r'\bолив\w*',
    r'\bсиние\b', r'\bзеленые\b', r'\bпиксели\b', r'\bледенец\b', r'\bлюстра\b',
    r'\bкаблук\b', r'\bоблава\b', r'\bповестк\w*'
]

async def fetch_group_messages(hours=12, limit=250):
    try:
        from telethon import TelegramClient
    except ImportError:
        return {"error": "Telethon is not installed in the active python environment"}

    sess = get_session_path()
    client = TelegramClient(sess, API_ID, API_HASH)
    await client.connect()

    if not await client.is_user_authorized():
        await client.disconnect()
        return {"error": f"Session at {sess} is not authorized."}

    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    signals = []

    try:
        entity = await client.get_entity(GROUP_ID)
        async for msg in client.iter_messages(entity, limit=limit):
            if msg.date and msg.date < cutoff:
                break
            if not msg.text:
                continue

            raw_text = msg.text.strip()
            # Clean promo links / footers
            clean_text = raw_text.split("❕[Сообщить]")[0].split("Личная [рассылка")[0].strip()
            
            # Check for keyword matches
            is_relevant = any(re.search(pat, clean_text, re.IGNORECASE) for pat in KEYWORD_PATTERNS)
            
            # Extract hashtags as street/location tags
            tags = re.findall(r'#+([A-Za-zА-Яа-я0-9_]+)', clean_text)
            
            dt_str = msg.date.strftime("%H:%M") if msg.date else ""
            dt_full = msg.date.strftime("%Y-%m-%d %H:%M") if msg.date else ""
            
            signals.append({
                "id": msg.id,
                "time": dt_str,
                "datetime": dt_full,
                "text": clean_text,
                "is_alert": is_relevant,
                "tags": tags
            })
    except Exception as e:
        return {"error": f"Failed fetching messages: {str(e)}"}
    finally:
        await client.disconnect()

    return {"success": True, "signals": signals}

def build_google_maps_url(origin: str, destination: str, waypoints: list = None) -> str:
    base = "https://www.google.com/maps/dir/?api=1"
    params = {
        "origin": f"{origin}, Одесса",
        "destination": f"{destination}, Одесса",
        "travelmode": "driving"
    }
    if waypoints:
        params["waypoints"] = "|".join([f"{w}, Одесса" for w in waypoints[:5]])
    query_str = urllib.parse.urlencode(params)
    return f"{base}&{query_str}"

def main():
    parser = argparse.ArgumentParser(description="Odessa Safe Route & Group Scanner")
    parser.add_argument("--scan", action="store_true", help="Scan and list latest live alerts with timestamps")
    parser.add_argument("--hours", type=int, default=12, help="Hours to look back (default: 12)")
    parser.add_argument("--from-loc", dest="from_loc", type=str, help="Starting location (origin)")
    parser.add_argument("--to-loc", dest="to_loc", type=str, help="Destination location")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    res = asyncio.run(fetch_group_messages(hours=args.hours))
    if "error" in res:
        if args.json:
            print(json.dumps(res, ensure_ascii=False))
        else:
            print(f"ERROR: {res['error']}")
        sys.exit(1)
        
    signals = res.get("signals", [])
    alerts = [s for s in signals if s["is_alert"]]
    
    if args.json:
        out = {
            "total_messages": len(signals),
            "total_alerts": len(alerts),
            "alerts": alerts
        }
        if args.from_loc and args.to_loc:
            out["route_url"] = build_google_maps_url(args.from_loc, args.to_loc)
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return

    print(f"=== ОДЕССА: СВОДКА СИГНАЛОВ ИЗ ГРУППЫ 'НЕ ПОВРЕДИТ' ({len(alerts)} активных отметок за последние {args.hours}ч) ===")
    for a in alerts[:25]:
        print(f"• [{a['time']}] {a['text']}")
        
    if args.from_loc and args.to_loc:
        url = build_google_maps_url(args.from_loc, args.to_loc)
        print("\n=== ПОСТРОЕНИЕ МАРШРУТА ===")
        print(f"Откуда: {args.from_loc}")
        print(f"Куда:   {args.to_loc}")
        print(f"Ссылка на Google Maps Навигатор: {url}")

if __name__ == "__main__":
    main()
