#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
whatsapp_inbound_triage.py — Richard Marlowe (Navo24)
Monitors incoming WhatsApp messages, generates AI drafts,
and prepares notifications for Stefan in Telegram.
"""

import os
import sys
import json
import time
import requests
from datetime import datetime, timezone

EVENTS_FILE = "/opt/hermes/profiles/richard/services/whatsapp-gateway/inbound_events.jsonl"
PROCESSED_FILE = "/opt/hermes/profiles/richard/services/whatsapp-gateway/processed_events.json"

def load_processed():
    if os.path.exists(PROCESSED_FILE):
        try:
            with open(PROCESSED_FILE, "r") as f:
                return set(json.load(f))
        except Exception:
            return set()
    return set()

def save_processed(processed_ids):
    with open(PROCESSED_FILE, "w") as f:
        json.dump(list(processed_ids), f, indent=2)

def generate_draft_response(client_name, message_text):
    """
    Drafts an elite, left-aligned B2B reply from Richard Marlowe (Connections Manager / Navo24).
    """
    text_lower = message_text.lower()
    
    if any(w in text_lower for w in ["rate", "price", "quote", "ставка", "цена", "стоимость"]):
        reply = (
            f"Hello {client_name},\n\n"
            "Thank you for reaching out to Navo24. We provide real-time container freight rates ex-Asia "
            "with full market benchmark transparency. Are you looking for spot container rates, "
            "or would you like to integrate our live FreightRates API into your system?\n\n"
            "You can also explore our free tier (5 active containers & 100 API calls) at navo24.com.\n\n"
            "Best regards,\n"
            "Richard Marlowe\n"
            "Connections Manager | Navo24\n"
            "+44 7360 065904 | rich@navo24.com"
        )
    elif any(w in text_lower for w in ["track", "где груз", "трекинг", "статус", "контейнер", "container", "eta"]):
        reply = (
            f"Hello {client_name},\n\n"
            "Thanks for your message. Navo24 tracks containers across 234 global ocean carriers with direct DCSA events, "
            "observed ETAs, and port congestion data. What container numbers or carrier lines are you currently monitoring?\n\n"
            "I would be glad to set up a test account or run a live tracking demonstration for you.\n\n"
            "Best regards,\n"
            "Richard Marlowe\n"
            "Connections Manager | Navo24\n"
            "+44 7360 065904 | rich@navo24.com"
        )
    else:
        reply = (
            f"Hello {client_name},\n\n"
            "Thank you for getting in touch with Navo24. We specialize in ocean freight intelligence "
            "(Tracking across 234 carriers, Schedules across 255 ports, Live Rates, and 3D Load optimization).\n\n"
            "How can we best assist your operations today?\n\n"
            "Best regards,\n"
            "Richard Marlowe\n"
            "Connections Manager | Navo24\n"
            "+44 7360 065904 | rich@navo24.com"
        )
    return reply

def check_new_inbound():
    if not os.path.exists(EVENTS_FILE):
        return []
        
    processed_ids = load_processed()
    new_events = []
    
    with open(EVENTS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
                event_id = f"{event.get('sender')}_{event.get('timestamp')}"
                if event_id not in processed_ids:
                    event["id"] = event_id
                    new_events.append(event)
                    processed_ids.add(event_id)
            except Exception:
                continue
                
    save_processed(processed_ids)
    return new_events

def format_telegram_alert(event):
    name = event.get("name", "Клиент")
    phone = event.get("sender")
    msg = event.get("message")
    draft = generate_draft_response(name, msg)
    
    alert = (
        f"🟢 **НОВОЕ ВХОДЯЩЕЕ В WHATSAPP (+44 7360 065904)**\n\n"
        f"👤 **Клиент:** {name} (`+{phone}`)\n"
        f"💬 **Сообщение клиента:**\n"
        f"«{msg}»\n\n"
        f"✍️ **Подготовленный черновик ответа (Richard Marlowe):**\n"
        f"```\n{draft}\n```\n\n"
        f"👉 *Напиши «Да» или «Отправляй» для мгновенной отправки, либо напиши свой вариант текста.*"
    )
    return alert, draft

if __name__ == "__main__":
    events = check_new_inbound()
    if events:
        for ev in events:
            alert, draft = format_telegram_alert(ev)
            print(alert)

