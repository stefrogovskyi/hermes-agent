# -*- coding: utf-8 -*-
"""
tg_userbot_auth.py — Одноэтапный скрипт отправки и подтверждения кода Telethon.
"""

import asyncio, json, os, sys
from telethon import TelegramClient

api_id = 31246421
api_hash = "e96f7e4b8785d721deb761c55e2c8252"
phone = "+380636222272"
session_path = "/opt/hermes/stefan_userbot.session"
state_path = "/opt/hermes/state/tg_login_state.json"

async def send_code():
    client = TelegramClient(session_path, api_id, api_hash)
    await client.connect()
    res = await client.send_code_request(phone)
    state = {
        "phone": phone,
        "phone_code_hash": res.phone_code_hash,
        "api_id": api_id,
        "api_hash": api_hash
    }
    os.makedirs("/opt/hermes/state", exist_ok=True)
    open(state_path, "w").write(json.dumps(state))
    print(f"CODE_SENT: {res.phone_code_hash}")
    await client.disconnect()

async def submit_code(code):
    if not os.path.exists(state_path):
        print("ERROR: No state file found")
        return
    state = json.load(open(state_path))
    client = TelegramClient(session_path, api_id, api_hash)
    await client.connect()
    try:
        user = await client.sign_in(phone=state["phone"], code=code, phone_code_hash=state["phone_code_hash"])
        print(f"AUTH_SUCCESS: Signed in as {user.first_name} (@{user.username or user.id})")
    except Exception as e:
        print(f"AUTH_ERROR: {e}")
    finally:
        await client.disconnect()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "submit":
        asyncio.run(submit_code(sys.argv[2]))
    else:
        asyncio.run(send_code())
