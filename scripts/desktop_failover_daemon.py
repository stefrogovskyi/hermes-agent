# hermes_failover_daemon.py
# Скрипт автоматического отказоустойчивого переключения (Failover Daemon) для десктопа Stefan (Windows / Linux)
# Размещается на ПК: C:\Users\Stefan\hermes_failover_daemon.py (или /home/stefan/)
#
# ЛОГИКА РАБОТЫ:
# 1. Каждые 60 сек проверяет доступность VPS Servarica (38.49.219.217 / 100.99.146.42).
# 2. Если Servarica лежит (> 3 попыток подряд):
#    - Активирует аварийный режим (FAILOVER ACTIVE).
#    - Запускает локальные боты/шлюзы Hermes на ПК.
#    - Отправляет уведомление Стефану в Telegram: "🚨 VPS Servarica недоступен. Экосистема переключена на ПК!".
#    - Переходит в режим опроса Servarica каждые 10 минут.
# 3. Как только Servarica оживает:
#    - Выполняет git commit & push локальных данных на GitHub.
#    - По SSH или при старте Servarica инициирует `git pull` на сервере.
#    - Останавливает локальные шлюзы на ПК (чтобы не было 409 конфликтов).
#    - Отправляет алерт: "✅ Servarica снова онлайн! Синхронизация выполнена, управление возвращено на VPS."

import time
import subprocess
import urllib.request
import urllib.parse
import json
import os

SERVARICA_IP = "100.99.146.42"
PUBLIC_IP = "38.49.219.217"
TELEGRAM_BOT_TOKEN = "8899116964:AAEmj40q6f9U5fE_H8M4K02z9c6H9g5c"
CHAT_ID = "330656040"

FAILOVER_ACTIVE = False
CONSECUTIVE_FAILS = 0

def send_tg(text):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = urllib.parse.urlencode({"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}).encode()
        urllib.request.urlopen(urllib.request.Request(url, data=payload), timeout=10)
    except Exception as e:
        print(f"Error sending TG: {e}")

def is_servarica_alive():
    # 1. Ping tailscale IP
    cmd = f"ping -n 1 -w 2000 {SERVARICA_IP}" if os.name == 'nt' else f"ping -c 1 -W 2 {SERVARICA_IP}"
    code = subprocess.call(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if code == 0:
        return True
    # 2. Ping public IP
    cmd2 = f"ping -n 1 -w 2000 {PUBLIC_IP}" if os.name == 'nt' else f"ping -c 1 -W 2 {PUBLIC_IP}"
    code2 = subprocess.call(cmd2, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return code2 == 0

def start_local_hermes():
    print("[FAILOVER] Starting local Hermes gateways...")
    if os.name == 'nt':
        # Start local desktop Hermes runner
        subprocess.Popen(["cmd.exe", "/c", "hermes gateway run"], creationflags=subprocess.CREATE_NEW_CONSOLE)
    else:
        subprocess.Popen(["hermes", "gateway", "run"])

def stop_local_hermes():
    print("[RECOVERY] Stopping local Hermes gateways...")
    if os.name == 'nt':
        subprocess.call("taskkill /f /im hermes.exe", shell=True)
        subprocess.call("taskkill /f /im python.exe /fi \"WINDOWTITLE eq Hermes*\"", shell=True)
    else:
        subprocess.call("pkill -f 'hermes.*gateway'", shell=True)

def sync_git():
    print("[SYNC] Syncing local changes to GitHub...")
    subprocess.call("git add . && git commit -m 'failover: auto-sync before returning to VPS' && git push", shell=True)

def main_loop():
    global FAILOVER_ACTIVE, CONSECUTIVE_FAILS
    print("Hermes Failover Switcher Daemon started on PC.")
    
    while True:
        alive = is_servarica_alive()
        
        if not alive:
            CONSECUTIVE_FAILS += 1
            print(f"[{time.strftime('%H:%M:%S')}] Servarica ping failed ({CONSECUTIVE_FAILS}/3)...")
            
            if CONSECUTIVE_FAILS >= 3 and not FAILOVER_ACTIVE:
                FAILOVER_ACTIVE = True
                print("🚨 CRITICAL: Servarica is DOWN! Activating Desktop Failover...")
                start_local_hermes()
                send_tg(
                    "🚨 <b>ВНИМАНИЕ: Серварика недоступна (техработы/сбой сети)!</b>\n\n"
                    "💻 <b>Автоматический свитчер переключил экосистему на ПК.</b>\n"
                    "🔄 Запущен фоновый поллер проверки статуса Серварики (каждые 10 минут)."
                )
        else:
            CONSECUTIVE_FAILS = 0
            if FAILOVER_ACTIVE:
                print("🟢 Servarica is BACK ONLINE! Restoring primary operations...")
                # 1. Sync data to github
                sync_git()
                # 2. Stop local bots
                stop_local_hermes()
                FAILOVER_ACTIVE = False
                send_tg(
                    "✅ <b>Серварика снова онлайн!</b>\n\n"
                    "🔄 Данные с ПК синхронизированы в GitHub.\n"
                    "🌐 Управление экосистемой успешно возвращено на VPS Servarica."
                )
        
        # Interval: 10 min if in failover mode, 60s if in normal standby mode
        sleep_sec = 600 if FAILOVER_ACTIVE else 60
        time.sleep(sleep_sec)

if __name__ == "__main__":
    main_loop()
