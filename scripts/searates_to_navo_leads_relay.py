# -*- coding: utf-8 -*-
"""
searates_to_navo_leads_relay.py — 24/7 Telethon Relay: Requests • SeaRates & Msg • SeaRates -> Navo Leads (-1004425230295)
"""

import asyncio
import json
import os
import sys
import datetime
from telethon import TelegramClient, events

# Configuration
API_ID = 31246421
API_HASH = "e96f7e4b8785d721deb761c55e2c8252"
SESSION_PATH = "/opt/hermes/stefan_userbot.session"

SOURCE_REQUESTS_ID = -1001074173093  # Requests • SeaRates
SOURCE_MSG_ID = -1001564462737       # Msg • SeaRates
TARGET_LEADS_ID = -1004425230295      # Navo Leads (formerly sr leads)

STATE_FILE = "/opt/hermes/state/searates_relay_state.json"
LOG_FILE = "/opt/hermes/searates_relay.log"

def log(msg):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{now}] {msg}"
    print(formatted, flush=True)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(formatted + "\n")
    except Exception:
        pass

def load_seen_ids():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return set(json.load(f))
        except Exception as e:
            log(f"Error loading state file: {e}")
    return set()

def save_seen_ids(seen_ids):
    os.makedirs("/opt/hermes/state", exist_ok=True)
    try:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(list(seen_ids), f)
    except Exception as e:
        log(f"Error saving state file: {e}")

async def run_catchup(client, seen_ids):
    log("=== STARTING CATCH-UP SCAN FOR SEARATES CHANNELS ===")
    
    try:
        target = await client.get_entity(TARGET_LEADS_ID)
    except Exception as e:
        log(f"Error resolving target channel Navo Leads: {e}")
        return

    for sid in [SOURCE_REQUESTS_ID, SOURCE_MSG_ID]:
        try:
            source = await client.get_entity(sid)
            source_title = getattr(source, "title", str(sid))
            log(f"Scanning source channel: {source_title} ({sid})")
            
            # Fetch recent 50 messages
            async for msg in client.iter_messages(source, limit=50):
                unique_key = f"{sid}_{msg.id}"
                if unique_key in seen_ids:
                    continue
                
                # Forward/copy message
                try:
                    await client.forward_messages(target, msg)
                    seen_ids.add(unique_key)
                    log(f" -> CATCH-UP FORWARDED msg {msg.id} from {source_title} to Navo Leads")
                    await asyncio.sleep(1)
                except Exception as e:
                    log(f" -> ERROR forwarding catch-up msg {msg.id} from {source_title}: {e}")
                    
        except Exception as e:
            log(f"Error scanning source {sid}: {e}")
            
    save_seen_ids(seen_ids)
    log("=== CATCH-UP SCAN COMPLETED ===")

async def main():
    log("=== STARTING TELEGRAM SEARATES RELAY DAEMON ===")
    seen_ids = load_seen_ids()
    
    client = TelegramClient(SESSION_PATH, API_ID, API_HASH)
    await client.connect()
    
    if not await client.is_user_authorized():
        log("CRITICAL ERROR: Userbot session is NOT authorized!")
        return

    me = await client.get_me()
    log(f"Authorized as {me.first_name} (@{me.username or me.id})")
    
    # 1. Run initial Catch-Up
    await run_catchup(client, seen_ids)
    
    # 2. Register Live Event Handler
    @client.on(events.NewMessage(chats=[SOURCE_REQUESTS_ID, SOURCE_MSG_ID]))
    async def handler(event):
        try:
            msg = event.message
            chat_id = event.chat_id
            unique_key = f"{chat_id}_{msg.id}"
            
            if unique_key in seen_ids:
                return
                
            source_title = "Requests • SeaRates" if chat_id == SOURCE_REQUESTS_ID else "Msg • SeaRates"
            log(f"LIVE NEW MESSAGE in {source_title} (ID: {msg.id})")
            
            target = await client.get_entity(TARGET_LEADS_ID)
            await client.forward_messages(target, msg)
            
            seen_ids.add(unique_key)
            save_seen_ids(seen_ids)
            log(f" -> LIVE FORWARDED msg {msg.id} to Navo Leads successfully!")
        except Exception as e:
            log(f" -> ERROR in live message handler: {e}")

    log("=== RELAY DAEMON IS LIVE & LISTENING FOR NEW MESSAGES ===")
    await client.run_until_disconnected()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log("Relay stopped by user.")
    except Exception as e:
        log(f"Fatal error in relay daemon: {e}")
