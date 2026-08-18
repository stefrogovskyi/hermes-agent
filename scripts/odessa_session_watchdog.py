#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
odessa_session_watchdog.py — вахтёр Telethon-сессии stefan_userbot.

Логика (watchdog-паттерн: молчит, когда всё хорошо):
  1. Проверяет авторизацию сессии /opt/hermes/stefan_userbot.session
  2. Здорова  -> обновляет холодный бэкап + meta (телефон), печатает НИЧЕГО
  3. Файл битый/пропал -> восстанавливает из бэкапа, перепроверяет
  4. Ревок (unauthorized / AuthKeyDuplicated и т.п.) -> печатает алерт
     с инструкцией по переавторизации (доставляется Стефану в личку)
"""

import os
import sys
import json
import shutil
import sqlite3
import asyncio
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

SESSION_BASE = "/opt/hermes/stefan_userbot"          # без .session
SESSION_FILE = SESSION_BASE + ".session"
BACKUP_DIR = "/opt/hermes/backups"
BACKUP_FILE = os.path.join(BACKUP_DIR, "stefan_userbot.session.bak")
META_FILE = os.path.join(BACKUP_DIR, "stefan_userbot_meta.json")
LOG_FILE = os.path.join(BACKUP_DIR, "session_watchdog.log")

API_ID = 20400084
API_HASH = "b2e2d93e1792bc443ae3bd40a9b8979c"

RELOGIN_HINT = (
    "🔧 Как восстановить (2 минуты):\n"
    "Напиши Гермесу: «переавторизуй сессию одессы» — я запущу интерактивный "
    "вход, Telegram пришлёт тебе код, ты пришлёшь его мне ЧЕРЕЗ ПРОБЕЛЫ "
    "(например «1 2 3 4 5», иначе Telegram аннулирует код), и сессия оживёт."
)


def log(msg: str):
    os.makedirs(BACKUP_DIR, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().isoformat(timespec='seconds')} {msg}\n")


def sqlite_intact(path: str) -> bool:
    """Файл существует и является валидной SQLite-базой telethon."""
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return False
    try:
        con = sqlite3.connect(path)
        row = con.execute("PRAGMA integrity_check").fetchone()
        con.execute("SELECT name FROM sqlite_master LIMIT 1").fetchone()
        con.close()
        return bool(row) and row[0] == "ok"
    except sqlite3.Error:
        return False


def refresh_backup():
    """Снимает консистентную копию сессии через SQLite backup API."""
    os.makedirs(BACKUP_DIR, exist_ok=True)
    src = sqlite3.connect(SESSION_FILE)
    dst = sqlite3.connect(BACKUP_FILE + ".tmp")
    with dst:
        src.backup(dst)
    src.close()
    dst.close()
    os.replace(BACKUP_FILE + ".tmp", BACKUP_FILE)


def restore_from_backup() -> bool:
    if not sqlite_intact(BACKUP_FILE):
        return False
    if os.path.exists(SESSION_FILE):
        shutil.copy2(SESSION_FILE, SESSION_FILE + ".corrupt")
    shutil.copy2(BACKUP_FILE, SESSION_FILE)
    return True


async def check_auth():
    """
    Возвращает кортеж (status, detail):
      status: 'ok' | 'unauthorized' | 'error'
    """
    from telethon import TelegramClient
    from telethon.errors import AuthKeyDuplicatedError, AuthKeyUnregisteredError

    client = TelegramClient(SESSION_BASE, API_ID, API_HASH)
    try:
        await client.connect()
        if not await client.is_user_authorized():
            return "unauthorized", "is_user_authorized() == False (сессия ревокнута)"
        me = await client.get_me()
        # Сохраняем meta для будущей переавторизации
        meta = {
            "phone": getattr(me, "phone", None),
            "user_id": me.id,
            "username": getattr(me, "username", None),
            "last_ok": datetime.now().isoformat(timespec="seconds"),
        }
        os.makedirs(BACKUP_DIR, exist_ok=True)
        with open(META_FILE, "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)
        return "ok", f"authorized as id={me.id}"
    except (AuthKeyDuplicatedError, AuthKeyUnregisteredError) as e:
        return "unauthorized", f"{type(e).__name__}: auth key убит Telegram'ом"
    except Exception as e:
        return "error", f"{type(e).__name__}: {e}"
    finally:
        try:
            await client.disconnect()
        except Exception:
            pass


def main():
    # --- Шаг 1: целостность файла ---
    if not sqlite_intact(SESSION_FILE):
        log("session file missing/corrupt, trying backup restore")
        if restore_from_backup():
            status, detail = asyncio.run(check_auth())
            if status == "ok":
                log(f"restored from backup OK ({detail})")
                print(
                    "🛠 ОДЕССА-РОУТЕР: файл сессии был повреждён/удалён.\n"
                    "✅ Автоматически восстановлен из бэкапа, авторизация "
                    "работает. Вмешательство не требуется."
                )
                refresh_backup()
                return
            log(f"backup restore failed auth: {status} {detail}")
            print(
                "🚨 ОДЕССА-РОУТЕР: сессия повреждена, бэкап восстановлен, "
                f"но авторизация мертва ({detail}).\n\n" + RELOGIN_HINT
            )
            return
        log("no valid backup available")
        print(
            "🚨 ОДЕССА-РОУТЕР: файл сессии повреждён/удалён, валидного "
            "бэкапа нет.\n\n" + RELOGIN_HINT
        )
        return

    # --- Шаг 2: проверка авторизации ---
    status, detail = asyncio.run(check_auth())

    if status == "ok":
        try:
            refresh_backup()
            log(f"healthy, backup refreshed ({detail})")
        except Exception as e:
            log(f"healthy but backup failed: {e}")
            print(f"⚠️ ОДЕССА-РОУТЕР: сессия жива, но не смог обновить бэкап: {e}")
        return  # молчим — всё хорошо

    if status == "unauthorized":
        log(f"UNAUTHORIZED: {detail}")
        print(
            "🚨 ОДЕССА-РОУТЕР: сессия stefan_userbot слетела "
            f"({detail}).\nБэкап тут не поможет — auth key ревокнут на "
            "стороне Telegram (завершение сессии в «Устройствах», смена "
            "пароля 2FA или anti-abuse).\n\n" + RELOGIN_HINT
        )
        return

    # network/прочие ошибки: не спамим алертами, но логируем;
    # если это постоянная проблема, она всплывёт в логе
    log(f"transient error: {detail}")


if __name__ == "__main__":
    main()
