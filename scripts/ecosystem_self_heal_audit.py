# -*- coding: utf-8 -*-
"""
ecosystem_self_heal_audit.py — Ежедневный аудит и самовосстановление всей экосистемы Серварики (04:00 AM).
"""

import os, sys, time, subprocess, json

LOG_FILE = "/opt/hermes/logs/ecosystem_audit.log"
os.makedirs("/opt/hermes/logs", exist_ok=True)

def log(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] [EcosystemSelfHeal] {msg}"
    print(formatted, flush=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(formatted + "\n")

def main():
    log("=== STARTING DAILY ECOSYSTEM SELF-HEAL & AUDIT (04:00 AM) ===")
    
    # 1. Audit & Self-heal systemd services for all 6 profiles
    services = [
        "hermes-default.service",
        "hermes-richard.service",
        "hermes-callum.service",
        "hermes-alistair.service",
        "hermes-ben.service",
        "hermes-liz.service"
    ]
    
    restarted = 0
    for svc in services:
        res = subprocess.run(["systemctl", "is-active", "--quiet", svc])
        if res.returncode != 0:
            log(f"⚠️ Service {svc} is NOT active. Self-healing restart...")
            subprocess.run(["systemctl", "restart", svc])
            restarted += 1
        else:
            log(f"✅ Service {svc}: ACTIVE")
            
    # 2. Verify Token Isolation Guardrails
    profiles = ["richard", "callum", "alistair", "ben", "liz"]
    for p in profiles:
        env_p = f"/opt/hermes/profiles/{p}/.env"
        if os.path.exists(env_p):
            txt = open(env_p, encoding="utf-8", errors="ignore").read()
            if "TELEGRAM_BOT_TOKEN=8682188433" in txt or "TELEGRAM_TOKEN=8682188433" in txt:
                log(f"⚠️ [SECURITY ALERT] Profile {p} contains main Hermes token! Disabling to prevent polling conflict.")
                # Comment out main token
                lines = open(env_p).readlines()
                new_lines = [("# " + l if "8682188433" in l else l) for l in lines]
                open(env_p, "w").write("".join(new_lines))

    # 3. Trigger Git Autosync
    git_sync_script = "/opt/hermes/scripts/git_autosync_hidden.sh"
    if os.path.exists(git_sync_script):
        log("Running Git Autosync...")
        subprocess.run(["/bin/bash", git_sync_script])

    # 4. Check Disk & Memory
    df_res = subprocess.run(["df", "-h", "/opt/hermes"], capture_output=True, text=True)
    log(f"Disk Usage:\n{df_res.stdout.strip()}")

    log(f"=== ECOSYSTEM AUDIT COMPLETED. Restarted services: {restarted} ===")

if __name__ == "__main__":
    main()
