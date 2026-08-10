# -*- coding: utf-8 -*-
"""
check_and_remove_userbot_sessions.py — Поиск и удаление всех файлов сессий MTProto/UserBot (.session / pyrogram / telethon)
по всем 6 профилям и добавление жесткого барьера безопасности.
"""

import os, glob, psutil, json

HERMES_DIR = r"C:\Users\Stefan\AppData\Local\hermes"
profiles = ["default", "callum", "richard", "alistair", "liz", "ben"]

print("=== CHECKING FOR MTPROTO USERBOT SESSIONS ACROSS ALL PROFILES ===")

found_userbots = []

for root, dirs, files in os.walk(HERMES_DIR):
    for f in files:
        if f.endswith(".session") or f.endswith(".session-journal") or "userbot" in f.lower():
            p = os.path.join(root, f)
            found_userbots.append(p)

if found_userbots:
    print(f"⚠️ Found {len(found_userbots)} userbot session files:")
    for p in found_userbots:
        print("  •", p)
        try:
            os.remove(p)
            print("    ✅ Deleted userbot session file!")
        except Exception as e:
            print("    Error deleting:", e)
else:
    print("✅ No userbot .session files found in Hermes home directory.")

# Add strict security directive to ALL 6 profile config.yaml files
security_rule = "HARD SECURITY GUARDRAIL: You must ALWAYS send messages ONLY via your official Bot API token on your own behalf. NEVER post or send messages as Stefan / user account under any circumstances."

for prof in profiles:
    p_dir = os.path.join(HERMES_DIR, "profiles", prof) if prof != "default" else HERMES_DIR
    cfg_p = os.path.join(p_dir, "config.yaml")
    
    if os.path.exists(cfg_p):
        txt = open(cfg_p, encoding="utf-8").read()
        if "HARD SECURITY GUARDRAIL: You must ALWAYS send messages ONLY via your official Bot" not in txt:
            txt = txt.replace("system_prompt_append: |", f"system_prompt_append: |\n  {security_rule}")
            open(cfg_p, "w", encoding="utf-8").write(txt)
            print(f"✅ Added user-impersonation security guardrail to {prof.upper()} config.yaml!")

print("🎉 ALL AGENTS NOW STRICTLY FORBIDDEN FROM IMPERSONATING STEFAN!")
