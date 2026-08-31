#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
model_change_gateway_restart.py - restart the Hermes gateway when the model changes.

Keeps Desktop and Telegram on the SAME model: when the owner switches model in the
Desktop app, the running gateway keeps serving the OLD model to Telegram until it
restarts. Hermes cannot self-restart from inside a cron (lifecycle commands blocked),
so this runs as an EXTERNAL no_agent=True cron 'every 2m'.

Each tick:
1. Read the model: block (provider + name) from config.yaml (stdlib, no PyYAML).
2. Compare to the saved fingerprint (state/model_fingerprint.json).
3. If changed -> silently kill 'gateway run' (python/pythonw) and relaunch the
   official gateway-service/Hermes_Gateway.vbs (windowless, CREATE_NO_WINDOW).

Register once:
    cronjob(action=create, no_agent=True, name="Model-change Gateway Autorestart",
            schedule="every 2m", script="model_change_gateway_restart.py")

Prints a line ONLY when it actually restarts (classic silent-watchdog pattern).
"""
import os
import sys
import json
import subprocess

HERMES = os.path.join(os.environ.get("LOCALAPPDATA",
                      os.path.expanduser(r"~\AppData\Local")), "hermes")
CONFIG = os.path.join(HERMES, "config.yaml")
STATE = os.path.join(HERMES, "state", "model_fingerprint.json")
VBS = os.path.join(HERMES, "gateway-service", "Hermes_Gateway.vbs")
NOWIN = 0x08000000  # CREATE_NO_WINDOW


def read_model_fingerprint():
    """provider|name from the model: block of config.yaml, stdlib only."""
    provider = name = ""
    in_model = False
    try:
        with open(CONFIG, encoding="utf-8") as f:
            for line in f:
                if line.startswith("model:"):
                    in_model = True
                    continue
                if in_model:
                    if line[:1] not in (" ", "\t"):  # left the block
                        break
                    s = line.strip()
                    if s.startswith("provider:"):
                        provider = s.split(":", 1)[1].strip()
                    elif s.startswith("name:"):
                        name = s.split(":", 1)[1].strip()
    except Exception:
        pass
    return f"{provider}|{name}"


def load_prev():
    try:
        return json.load(open(STATE, encoding="utf-8")).get("fp", "")
    except Exception:
        return ""


def save(fp):
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    json.dump({"fp": fp}, open(STATE, "w", encoding="utf-8"))


def restart_gateway():
    ps = (
        "Get-CimInstance Win32_Process -Filter \"Name='pythonw.exe' or Name='python.exe'\" | "
        "Where-Object { $_.CommandLine -match 'gateway run' } | "
        "ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }"
    )
    subprocess.run(["powershell", "-NoProfile", "-Command", ps],
                   capture_output=True, timeout=60, creationflags=NOWIN)
    subprocess.Popen(["wscript.exe", VBS], creationflags=NOWIN, close_fds=True)


if __name__ == "__main__":
    fp = read_model_fingerprint()
    prev = load_prev()
    if not prev:
        save(fp)
        sys.exit(0)  # first run: only record
    if fp != prev:
        restart_gateway()
        save(fp)
        print(f"[model-watch] model changed {prev} -> {fp}; gateway restarted silently")
    sys.exit(0)
