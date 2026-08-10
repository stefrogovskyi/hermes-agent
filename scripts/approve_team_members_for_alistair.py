# -*- coding: utf-8 -*-
"""
approve_team_members_for_alistair.py — Внесение всех участников группы Navo Tech geeks (Стефан, Женя Karavan, Алексей/Роберт, Sort It Bot)
в список разрешенных пользователей (telegram-approved.json) во все профили, чтобы Алистер реагировал на упоминания команды!
"""

import os, json, time, psutil, subprocess

HERMES_DIR = r"C:\Users\Stefan\AppData\Local\hermes"
profiles = ["default", "callum", "richard", "alistair", "liz", "ben"]

approved_team = {
    "330656040": {"user_name": "Stefan Rogovskiy", "approved_at": time.time()},
    "1022586369": {"user_name": "Robert / Alexey", "approved_at": time.time()},
    "363779334": {"user_name": "Eugene Karavan", "approved_at": time.time()},
    "8806090295": {"user_name": "Sort It Bot", "approved_at": time.time()}
}

print("=== AUTHORIZING TEAM MEMBERS IN TELEGRAM PAIRING ACROSS ALL PROFILES ===")

for prof in profiles:
    p_dir = os.path.join(HERMES_DIR, "profiles", prof) if prof != "default" else HERMES_DIR
    pair_dir = os.path.join(p_dir, "platforms", "pairing")
    os.makedirs(pair_dir, exist_ok=True)
    
    app_f = os.path.join(pair_dir, "telegram-approved.json")
    
    # Merge existing approved users if present
    existing = {}
    if os.path.exists(app_f):
        try:
            existing = json.load(open(app_f, encoding="utf-8"))
        except Exception:
            existing = {}
            
    existing.update(approved_team)
    
    open(app_f, "w", encoding="utf-8").write(json.dumps(existing, indent=2, ensure_ascii=False))
    print(f"✅ Approved Eugene Karavan, Robert, Stefan & Sort It Bot in {prof.upper()} telegram-approved.json!")

# Restart Alistair Gateway
hermes_exe = r"C:\Users\Stefan\AppData\Local\hermes\hermes-agent\venv\Scripts\hermes.exe"

for p in psutil.process_iter(['pid', 'name', 'cmdline']):
    try:
        cmd = ' '.join(p.info['cmdline'] or [])
        if 'hermes.exe' in cmd and 'alistair' in cmd:
            print(f"🛑 Restarting Alistair Gateway PID {p.info['pid']} to apply team approvals...")
            psutil.Process(p.info['pid']).kill()
    except Exception:
        pass

time.sleep(2)

env = os.environ.copy()
env["HERMES_PROFILE"] = "alistair"

proc = subprocess.Popen([hermes_exe, "--profile", "alistair", "gateway", "run"], env=env, creationflags=0x08000000)
print(f"🚀 RESTARTED ALISTAIR GATEWAY WITH FULL TEAM APPROVALS! (PID {proc.pid})")

time.sleep(3)

print("🎉 ALISTAIR IS NOW FULLY AUTHORIZED TO RESPOND TO TEAM MEMBERS IN GROUPS!")
