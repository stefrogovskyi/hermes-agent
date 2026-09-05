#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pull_todo_from_pc.py — 100% фоновая автоматическая синхронизация Microsoft To-Do с десктопа Stefan
Берет live-дамп задач через SSH/Tailscale без открытия каких-либо окон на ПК.
"""

import os
import json
import subprocess
import time

PC_HOST = "Stefan@100.79.157.46"
REMOTE_VBS = r"C:\Users\Stefan\AppData\Local\hermes\scripts\run_todo_silent.vbs"
REMOTE_JSON = r"C:\Users\Stefan\AppData\Local\hermes\todo_live.json"
LOCAL_STATE = "/opt/hermes/state/ms_todo_live_snapshot.json"

def sync_pc_todo():
    print("🔄 [Hermes To-Do Sync] Проверка доступности ПК...")
    
    # 1. Запуск тихого фонового VBS на ПК (WindowStyle=0, без терминала и окон)
    run_cmd = ["ssh", "-o", "ConnectTimeout=6", PC_HOST, f'wscript.exe "{REMOTE_VBS}"']
    try:
        subprocess.run(run_cmd, capture_output=True, timeout=12)
    except Exception as e:
        print(f"⚠️ Ошибка вызова тихого VBS: {e}")

    # 2. Небольшая пауза на запись JSON
    time.sleep(2)

    # 3. Выкачивание обновленного todo_live.json с ПК
    cat_cmd = ["ssh", "-o", "ConnectTimeout=6", PC_HOST, f'type "{REMOTE_JSON}"']
    try:
        res = subprocess.run(cat_cmd, capture_output=True, text=True, timeout=15)
        if res.returncode == 0 and res.stdout.strip():
            raw = res.stdout.strip()
            if raw.startswith("\ufeff"):
                raw = raw[1:]
            data = json.loads(raw)
            if isinstance(data, list) and len(data) > 0:
                with open(LOCAL_STATE, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"✅ [Hermes To-Do Sync] Успешно синхронизировано {len(data)} задач с ПК в {LOCAL_STATE}")
                return True
            else:
                print(f"⚠️ Получен пустой список задач.")
        else:
            print(f"❌ Не удалось прочитать {REMOTE_JSON} с ПК: {res.stderr.strip()[:100]}")
    except Exception as e:
        print(f"❌ Ошибка выкачивания To-Do с ПК: {e}")

    return False

if __name__ == "__main__":
    sync_pc_todo()
