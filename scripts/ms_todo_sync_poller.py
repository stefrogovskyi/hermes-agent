#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ms_todo_sync_poller.py — Синхронизация задач Microsoft To-Do (supremo@i.ua) с Hermes Ecosystem
"""

import os
import json
import urllib.request
from datetime import datetime

HERMES_DIR = "/opt/hermes"
CACHE_FILE = f"{HERMES_DIR}/cache/ms_todo_tasks.json"

def get_webhook_url():
    env_file = f"{HERMES_DIR}/.env"
    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                if line.startswith("MAKE_TODO_WEBHOOK_URL="):
                    return line.split("=", 1)[1].strip()
    return os.environ.get("MAKE_TODO_WEBHOOK_URL", "")

def sync_ms_todo():
    url = get_webhook_url()
    if not url:
        print("❌ Ошибка: MAKE_TODO_WEBHOOK_URL не найден в .env")
        return False

    print(f"🔄 Запуск синхронизации Microsoft To-Do (supremo@i.ua)...")
    payload = {
        "action": "fetch_tasks",
        "user_email": "supremo@i.ua",
        "timestamp": datetime.utcnow().isoformat(),
        "target": "hermes-agent"
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "User-Agent": "Hermes-Agent/2.0"}
    )

    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
            status = resp.status
            body = resp.read().decode("utf-8")
            print(f"✅ Webhook принят Make.com (HTTP {status}): {body}")
            
            # Save synchronization event
            os.makedirs(f"{HERMES_DIR}/cache", exist_ok=True)
            sync_meta = {
                "last_sync_utc": datetime.utcnow().isoformat(),
                "status": "success",
                "account": "supremo@i.ua",
                "response": body
            }
            with open(CACHE_FILE, "w", encoding="utf-8") as f:
                json.dump(sync_meta, f, indent=2, ensure_ascii=False)
            return True
    except Exception as e:
        print(f"❌ Ошибка отправки вебхука в Make.com: {e}")
        return False

if __name__ == "__main__":
    sync_ms_todo()
