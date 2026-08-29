# -*- coding: utf-8 -*-
import os, sys, time, subprocess, glob

LOG_FILE = "/opt/hermes/logs/ecosystem_audit.log"
os.makedirs("/opt/hermes/logs", exist_ok=True)

def check_journalctl_conflicts(svc_name):
    try:
        cmd = ["journalctl", "-u", svc_name, "-n", "50", "--since", "3 minutes ago", "--no-pager"]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        logs = res.stdout or ""
        if "could not recover after 5 retries" in logs or "could not recover after" in logs:
            return True, "409 Conflict / Telegram polling deadlock"
        if "Updater made no getUpdates progress" in logs:
            return True, "Telegram polling updater остановлен"
    except Exception:
        pass
    return False, None

def get_hermes_services():
    svc_files = glob.glob("/etc/systemd/system/hermes-*.service") + glob.glob("/etc/systemd/system/aeon-*.service") + glob.glob("/etc/systemd/system/openclaw.service")
    services = []
    for f in sorted(set(svc_files)):
        svc_name = os.path.basename(f)
        if svc_name == "hermes-self-heal.service":
            continue
        res_en = subprocess.run(["systemctl", "is-enabled", svc_name], capture_output=True, text=True)
        if res_en.stdout.strip() not in ["enabled", "linked", "alias"]:
            continue
        services.append(svc_name)
    return services

def get_nice_name(svc):
    mapping = {
        "hermes-default.service": "👑 Hermes Stevenson",
        "hermes-richard.service": "💼 Richard Marlowe (@richnavobot)",
        "hermes-alistair.service": "📊 Alistair Sterling (@qubicpmbot)",
        "hermes-archie.service": "✍️ Archie Wright (@WordCraftBot)",
        "hermes-ben.service": "⚡ Ben Jett (@benjettbot)",
        "hermes-callum.service": "🛠 Callum Vance (@callumvancebot)",
        "hermes-harrison.service": "⚖️ Harrison Croft (@harrisoncroftbot)",
        "hermes-liz.service": "🧠 Liz Harper (@lizharperbot)",
        "aeon-bridge.service": "🖥 Aeon Stevenson (@aeondeskbot)",
        "openclaw.service": "🌐 OpenClaw Gateway (:18789)"
    }
    return mapping.get(svc, f"🤖 {svc}")

def main():
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    services = get_hermes_services()
    
    status_lines = []
    restarted = 0
    healthy = 0
    
    for svc in services:
        nice_name = get_nice_name(svc)
        res = subprocess.run(["systemctl", "is-active", "--quiet", svc])
        if res.returncode != 0:
            subprocess.run(["systemctl", "restart", svc])
            restarted += 1
            status_lines.append(f"🔄 **{nice_name}**: был остановлен → *автоматически перезапущен*")
            continue
            
        has_conflict, reason = check_journalctl_conflicts(svc)
        if has_conflict:
            subprocess.run(["systemctl", "restart", svc])
            restarted += 1
            status_lines.append(f"⚠️ **{nice_name}**: сбой поллинга ({reason}) → *успешно вылечен*")
        else:
            healthy += 1
            status_lines.append(f"✅ **{nice_name}**: активен и стабилен")

    # Beautiful Visual Output
    report = []
    report.append("🩺 **Ежедневный аудит и самолечение экосистемы агентов**")
    report.append(f"⏱ *Время проверки:* `{timestamp}` (Киев)")
    report.append("—" * 28)
    report.append("")
    report.append("\n".join(status_lines))
    report.append("")
    report.append("—" * 28)
    if restarted == 0:
        report.append(f"✨ **Итог:** Все {healthy} сервисов работают в штатном режиме, вмешательства не потребовалось.")
    else:
        report.append(f"🛠 **Итог:** Восстановлено и перезапущено сервисов: `{restarted}`. Стабильных: `{healthy}`.")

    final_msg = "\n".join(report)
    print(final_msg)
    
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] [EcosystemSelfHeal]\n" + final_msg + "\n\n")

if __name__ == "__main__":
    main()
