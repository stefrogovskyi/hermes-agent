# -*- coding: utf-8 -*-
import os, sys, time, subprocess, json, sqlite3, glob

LOG_FILE = "/opt/hermes/logs/ecosystem_audit.log"
os.makedirs("/opt/hermes/logs", exist_ok=True)

def log(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] [EcosystemSelfHeal] {msg}"
    print(formatted, flush=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(formatted + "\n")

def check_journalctl_conflicts(svc_name):
    try:
        cmd = ["journalctl", "-u", svc_name, "-n", "50", "--since", "3 minutes ago", "--no-pager"]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        logs = res.stdout or ""
        if "could not recover after 5 retries" in logs or "could not recover after" in logs:
            return True, "409 Conflict or Telegram polling deadlock detected"
        if "Updater made no getUpdates progress" in logs:
            return True, "Telegram polling updater stopped"
    except Exception:
        pass
    return False, None

def get_hermes_services():
    svc_files = glob.glob("/etc/systemd/system/hermes-*.service")
    services = []
    for f in sorted(svc_files):
        svc_name = os.path.basename(f)
        if svc_name != "hermes-self-heal.service":
            services.append(svc_name)
    if "openclaw.service" in [os.path.basename(p) for p in glob.glob("/etc/systemd/system/*.service")]:
        services.append("openclaw.service")
    return services

def main():
    log("=== STARTING ADVANCED ECOSYSTEM SELF-HEAL AND AUDIT ===")
    services = get_hermes_services()
    log(f"Monitoring {len(services)} services: {services}")
    restarted = 0
    for svc in services:
        res = subprocess.run(["systemctl", "is-active", "--quiet", svc])
        if res.returncode != 0:
            log(f"[WARNING_not_active] Service {svc} is NOT active. Restarting...")
            subprocess.run(["systemctl", "restart", svc])
            restarted += 1
            continue
        has_conflict, reason = check_journalctl_conflicts(svc)
        if has_conflict:
            log(f"[SILENT_POLLING_FAILURE] in {svc} - {reason}! Executing forced self-heal restart...")
            subprocess.run(["systemctl", "restart", svc])
            restarted += 1
        else:
            log(f"[OK_active] Service {svc}: ACTIVE AND HEALTHY")
    log(f"=== ECOSYSTEM AUDIT COMPLETED. Restarted/Healed services: {restarted} ===")

if __name__ == "__main__":
    main()
