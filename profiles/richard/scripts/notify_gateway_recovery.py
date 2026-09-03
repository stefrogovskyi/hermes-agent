#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
notify_gateway_recovery.py — Richard Marlowe Gateway Recovery Notifier
Sends a direct Telegram notification to Stefan (330656040) whenever the Gateway service restarts / recovers,
including the active LLM model loaded in config.yaml.
"""

import os
import sys
import yaml
import requests
from datetime import datetime, timezone
from dotenv import load_dotenv

# Load env variables from richard profile
load_dotenv("/opt/hermes/profiles/richard/.env")
load_dotenv("/opt/hermes/.env")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TARGET_CHAT_ID = "330656040" # Stefan Rogovskiy
CONFIG_PATH = "/opt/hermes/profiles/richard/config.yaml"

def get_active_model():
    try:
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                cfg = yaml.safe_load(f)
                model_cfg = cfg.get("model", {})
                if isinstance(model_cfg, dict):
                    return model_cfg.get("default", "google/gemini-3.7-flash")
                elif isinstance(model_cfg, str):
                    return model_cfg
    except Exception as e:
        print(f"Error reading model from config: {e}")
    return "google/gemini-3.7-flash"

def send_recovery_alert():
    if not TELEGRAM_TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN not found.")
        return
        
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    active_model = get_active_model()
    
    text = (
        f"🟢 **Richard Marlowe Gateway: Успешное восстановление**\n\n"
        f"Шлюз **Richard (@richnavobot)** успешно перезапущен и восстановил соединение.\n"
        f"• **Активная модель:** `{active_model}`\n"
        f"• **Время:** `{now_str}`\n"
        f"• **Статус:** Gateway Online & Operational\n"
        f"• **Подсистемы:** B2B Outreach Engine, Inbound Email Sync, Cross-CRM, Cron Scheduler — активны."
    )
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TARGET_CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    
    try:
        r = requests.post(url, json=payload, timeout=10)
        if r.status_code == 200:
            print(f"Recovery notification (Model: {active_model}) sent successfully to Stefan!")
        else:
            print(f"Telegram API response: {r.status_code} {r.text}")
    except Exception as e:
        print(f"Failed to send recovery notification: {e}")

if __name__ == "__main__":
    send_recovery_alert()
