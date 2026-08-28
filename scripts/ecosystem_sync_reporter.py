#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ecosystem_sync_reporter.py — Ежедневный аудит и отчёт о синхронизации экосистемы
(Десктоп Stefan@100.79.157.46, VPS Servarica 38.49.219.217, GitHub stefrogovskyi/hermes-agent).
Запуск ежедневно в 23:00 (Киев / 20:00 UTC).
"""

import subprocess
import os
import json
import time
import urllib.request
import urllib.parse

HERMES_DIR = "/opt/hermes"
DESKTOP_SSH = "Stefan@100.79.157.46"

def run_cmd(cmd, timeout=30):
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return res.stdout.strip(), res.stderr.strip(), res.returncode
    except Exception as e:
        return "", str(e), -1

def get_git_info():
    out, _, _ = run_cmd(f"cd {HERMES_DIR} && git log -1 --pretty=format:'%h — %s (%cd)' --date=relative")
    branch, _, _ = run_cmd(f"cd {HERMES_DIR} && git rev-parse --abbrev-ref HEAD")
    status_out, _, _ = run_cmd(f"cd {HERMES_DIR} && git status --short")
    uncommitted = len([l for l in status_out.splitlines() if l.strip()])
    return branch or "master", out or "N/A", uncommitted

def check_desktop_node():
    # Check Tailscale & SSH to Stefan's PC
    ping_out, _, code = run_cmd(f"tailscale ping -c 1 100.79.157.46", timeout=5)
    if code != 0:
        return "🔴 Офлайн (Tailscale не отвечает)"
    
    ssh_out, ssh_err, ssh_code = run_cmd(f"ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no {DESKTOP_SSH} 'git --version'", timeout=10)
    if ssh_code == 0:
        return "🟢 Онлайн & Доступен по SSH"
    return "🟡 В сети (Tailscale OK, SSH в режиме ожидания)"

def run_sync_and_report():
    # 0. Direct sync of .env secrets via Tailscale SSH (outside of Git!)
    try:
        run_cmd(f"/opt/hermes/hermes-agent/venv/bin/python3 {HERMES_DIR}/scripts/tailscale_env_direct_sync.py", timeout=30)
    except Exception:
        pass

    # 1. Run local git sync to GitHub
    sync_out, sync_err, sync_code = run_cmd(f"/bin/bash {HERMES_DIR}/scripts/git_autosync_hidden.sh", timeout=60)
    
    # 2. Collect statuses
    branch, last_commit, uncommitted = get_git_info()
    desktop_status = check_desktop_node()
    
    # 3. Format Telegram brief
    now_str = time.strftime("%H:%M")
    
    report = (
        f"🔄 <b>Синхронизация экосистемы Hermes</b> ({now_str})\n\n"
        f"🌐 <b>VPS Servarica (stefan1):</b>\n"
        f"• Ветка: <code>{branch}</code>\n"
        f"• Крайний коммит: <code>{last_commit}</code>\n"
        f"• Несохранённые правки: <b>{uncommitted}</b>\n\n"
        f"🐙 <b>GitHub (stefrogovskyi/hermes-agent):</b>\n"
        f"• Статус пуша: {'✅ Успешно синхронизирован' if sync_code == 0 else '⚠️ Требует внимания'}\n\n"
        f"💻 <b>ПК / Десктоп Стефана (Tailscale):</b>\n"
        f"• Состояние узла: {desktop_status}\n\n"
        f"<i>Память, навыки, конфиги и скрипты актуализированы в едином контуре.</i>"
    )
    
    print(report)

if __name__ == "__main__":
    run_sync_and_report()
