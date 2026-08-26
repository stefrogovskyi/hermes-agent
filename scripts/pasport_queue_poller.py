#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pasport_queue_poller.py — Фоновый поллер свободных мест в электронной очереди ДП «Документ» (Одесса, ул. Европейская, 27/1).
URL: https://odesa3.pasport.org.ua/solutions/e-queue
"""

import asyncio
import os
import time
import urllib.request
import urllib.parse
from playwright.async_api import async_playwright

URL = "https://odesa3.pasport.org.ua/solutions/e-queue"
HERMES_DIR = os.environ.get("HERMES_HOME", "/opt/hermes")
STATE_FILE = os.path.join(HERMES_DIR, "state", "pasport_queue_state.txt")
TELEGRAM_BOT_TOKEN = "8899116964:AAEmj40q6f9U5fE_H8M4K02z9c6H9g5c" # Hermes default token or bridge
CHAT_ID = "330656040"

# Fetch active Telegram bot token from /opt/hermes/.env
for line in open(os.path.join(HERMES_DIR, ".env")):
    if line.startswith("TELEGRAM_BOT_TOKEN=") and not line.startswith("#"):
        TELEGRAM_BOT_TOKEN = line.split("=", 1)[1].strip()

def send_telegram_alert(msg: str):
    try:
        api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = urllib.parse.urlencode({
            "chat_id": CHAT_ID,
            "text": msg,
            "parse_mode": "HTML",
            "disable_web_page_preview": "false"
        }).encode("utf-8")
        req = urllib.request.Request(api_url, data=payload)
        urllib.request.urlopen(req, timeout=15)
        print("Telegram alert sent successfully!")
    except Exception as e:
        print(f"Error sending TG alert: {e}")

async def check_queue():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        page = await context.new_page()
        
        try:
            await page.goto(URL, wait_until="networkidle", timeout=40000)
            await page.wait_for_timeout(4000)
            
            body_text = await page.evaluate("() => document.body.innerText")
            
            # Key indicator of occupied / available slots
            occupied_phrase = "Наразі всі місця зайняті"
            
            os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
            last_state = ""
            if os.path.exists(STATE_FILE):
                last_state = open(STATE_FILE).read().strip()
                
            if occupied_phrase in body_text:
                # Тихо молчим при занятых местах (watchdog pattern)
                open(STATE_FILE, "w").write("OCCUPIED")
            else:
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 🔥 ВНИМАНИЕ: Появились свободные места в очереди!")
                open(STATE_FILE, "w").write("AVAILABLE")
                
                # Take evidence screenshot
                screenshot_path = f"/opt/hermes/cache/pasport_slot_{int(time.time())}.png"
                await page.screenshot(path=screenshot_path)
                
                alert_text = (
                    "🚨 <b>ПОЯВИЛИСЬ СВОБОДНЫЕ МЕСТА В ЭЛЕКТРОННУЮ ОЧЕРЕДЬ!</b> 🚨\n\n"
                    "🏛 <b>ДП «Документ»: Одесса, ул. Европейская, 27/1</b>\n"
                    f"⏰ Время обнаружения: <code>{time.strftime('%H:%M:%S')}</code>\n\n"
                    f"👉 <a href='{URL}'><b>СРОЧНО ПЕРЕЙТИ К ЗАПИСИ (ЖМИ СЮДА)</b></a>\n\n"
                    "<i>Поллер зафиксировал открытие слотов/окошек. Заходи и занимай талон прямо сейчас!</i>"
                )
                send_telegram_alert(alert_text)
                
        except Exception as e:
            print(f"Error checking queue: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(check_queue())
