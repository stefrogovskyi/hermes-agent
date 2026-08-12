# -*- coding: utf-8 -*-
"""
session_sync_watchdog.py — Автоматическое обнаружение и безопасный забор авторизованного .session файла с ПК Стефана по Tailscale.
Запускается на Серварике и опрашивает сетевые ресурсы ПК при его включении.
"""

import os, sys, time, subprocess, shutil

TARGET_SERVARICA_SESSION = "/opt/hermes/stefan_userbot.session"

# Tailscale IPs for Stefan's PCs
PC_IPS = [
    ("Anetta12", "100.119.27.60"),
    ("DESKTOP-MST5PT7", "100.79.157.46")
]

def check_pc_online(ip):
    res = subprocess.run(f"ping -c 1 -W 2 {ip}", shell=True, capture_output=True)
    return res.returncode == 0

def try_fetch_session():
    if os.path.exists(TARGET_SERVARICA_SESSION) and os.path.getsize(TARGET_SERVARICA_SESSION) > 1024:
        print("✅ Session file already exists and is valid on Servarica.")
        return True

    for pc_name, ip in PC_IPS:
        if check_pc_online(ip):
            print(f"📡 PC {pc_name} ({ip}) is ONLINE! Searching for .session file...")
            
            # Common AppData / Hermes paths on Windows PC
            cmd = f"smbclient //100.119.27.60/C$ -N -c 'ls Users\\Stefan\\AppData\\Local\\hermes\\*.session'"
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            print(f"SMB output for {pc_name}:", res.stdout or res.stderr)
            
    return False

if __name__ == "__main__":
    try_fetch_session()
