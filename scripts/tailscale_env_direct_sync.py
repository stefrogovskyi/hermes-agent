#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tailscale_env_direct_sync.py — Прямая защищённая синхронизация .env файлов между ПК и Servarica
Работает поверх Tailscale SSH (без передачи секретов в Git!).
"""

import subprocess
import os

DESKTOP_SSH = "Stefan@100.79.157.46"
HERMES_DIR = "/opt/hermes"
PROFILES = ["richard", "default", "callum", "harrison", "alistair", "archie", "liz", "ben"]

def sync_envs_from_desktop():
    print("Checking Tailscale connection to Desktop...")
    res = subprocess.run(f"tailscale ping -c 1 100.79.157.46", shell=True, capture_output=True, text=True)
    if res.returncode != 0:
        print("Desktop is offline, skipping direct .env sync.")
        return

    # Direct scp / cat of .env files from Desktop
    for prof in PROFILES:
        desktop_env_path = f"C:/Users/Stefan/AppData/Local/hermes/profiles/{prof}/.env" if prof != "default" else "C:/Users/Stefan/AppData/Local/hermes/.env"
        local_env_path = f"/opt/hermes/profiles/{prof}/.env" if prof != "default" else "/opt/hermes/.env"
        
        cmd = f"ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no {DESKTOP_SSH} 'type \"{desktop_env_path}\"'"
        proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if proc.returncode == 0 and len(proc.stdout.strip()) > 50:
            os.makedirs(os.path.dirname(local_env_path), exist_ok=True)
            with open(local_env_path, "w", encoding="utf-8") as f:
                f.write(proc.stdout)
            print(f"✅ Successfully synced .env for profile [{prof}] directly from PC!")

if __name__ == "__main__":
    sync_envs_from_desktop()
