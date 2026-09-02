#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
openclaw_auto_updater.py — Тихий авто-апдейтер OpenClaw 2.0 (проверка git upstream, билд и перезапуск службы).
"""

import os, subprocess, time, json, shutil

APP_DIR = "/opt/openclaw/app"
LOG_FILE = "/opt/hermes/logs/openclaw_updater.log"
SERVICE_NAME = "openclaw.service"

os.makedirs("/opt/hermes/logs", exist_ok=True)

def log(msg):
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def check_and_update():
    if not os.path.exists(APP_DIR):
        log(f"Directory {APP_DIR} does not exist.")
        return

    # 1. Fetch remote updates
    try:
        log("Checking for OpenClaw upstream updates...")
        res_fetch = subprocess.run(["git", "-C", APP_DIR, "fetch", "origin"], capture_output=True, text=True, timeout=60)
        if res_fetch.returncode != 0:
            log(f"Git fetch error: {res_fetch.stderr.strip()}")
            return

        # 2. Check revs
        local_rev = subprocess.run(["git", "-C", APP_DIR, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
        remote_rev = subprocess.run(["git", "-C", APP_DIR, "rev-parse", "@{u}"], capture_output=True, text=True).stdout.strip()

        if local_rev == remote_rev:
            log(f"OpenClaw 2.0 is up to date (Commit: {local_rev[:8]}). No rebuild needed.")
            return

        log(f"New update found! Local: {local_rev[:8]} -> Remote: {remote_rev[:8]}. Pulling...")
        res_pull = subprocess.run(["git", "-C", APP_DIR, "pull", "--ff-only"], capture_output=True, text=True, timeout=60)
        if res_pull.returncode != 0:
            log(f"Git pull failed: {res_pull.stderr.strip()}")
            return

        log("Installing dependencies (pnpm install)...")
        res_install = subprocess.run(["pnpm", "--dir", APP_DIR, "install"], capture_output=True, text=True, timeout=180)
        if res_install.returncode != 0:
            log(f"Dependencies install failed: {res_install.stderr.strip()[:200]}")
            return

        # Remove stale dist artifact locks if present
        lock_dir = os.path.join(APP_DIR, ".artifacts", "dist-artifacts.lock")
        if os.path.exists(lock_dir):
            shutil.rmtree(lock_dir, ignore_errors=True)

        log("Building OpenClaw 2.0 (npm run build)...")
        res_build = subprocess.run(["npm", "--prefix", APP_DIR, "run", "build"], capture_output=True, text=True, timeout=900)
        if res_build.returncode != 0:
            log(f"Build failed: {res_build.stderr[:200]}")
            return

        log("Restarting openclaw.service...")
        res_restart = subprocess.run(["systemctl", "restart", SERVICE_NAME], capture_output=True, text=True, timeout=30)
        if res_restart.returncode == 0:
            log(f"✅ OpenClaw 2.0 successfully updated and restarted to commit {remote_rev[:8]}!")
        else:
            log(f"Service restart failed: {res_restart.stderr.strip()}")

    except subprocess.TimeoutExpired:
        log("Timeout during OpenClaw update process.")
    except Exception as e:
        log(f"Unexpected error: {e}")

if __name__ == "__main__":
    check_and_update()
