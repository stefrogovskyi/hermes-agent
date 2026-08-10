# -*- coding: utf-8 -*-
"""
clean_env_local_and_fix_bot.py — Очистка двойных токенов в .env.local и привязка единственного валидного токена 8846249306:AAE7qkGYc...
"""

import os, urllib.request, json, py_compile

richard_dir = r"C:\Users\Stefan\My Drive\Equity\My Biz\Partner companies\Navo\6. Departments\Richard Marlowe\Richard Hermes"
env_local = os.path.join(richard_dir, ".env.local")
richard_py = os.path.join(richard_dir, "richard_bot.py")

# 1. Test every candidate token in .env.local and keep ONLY the valid one!
valid_token = ""
clean_lines = []

if os.path.exists(env_local):
    lines = open(env_local, encoding="utf-8", errors="ignore").readlines()
    for line in lines:
        if line.strip().startswith("TELEGRAM_BOT_TOKEN="):
            candidate = line.split("=", 1)[1].strip().strip('"').strip("'")
            # Test candidate token
            try:
                url = f"https://api.telegram.org/bot{candidate}/getMe"
                req = urllib.request.Request(url)
                with urllib.request.urlopen(req, timeout=5) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    if data.get("ok"):
                        valid_token = candidate
                        print("🎉 FOUND VALID WORKING TOKEN:", candidate[:20] + "...")
                        clean_lines.append(f"TELEGRAM_BOT_TOKEN={candidate}\n")
                        continue
            except Exception:
                print("Skipping invalid/revoked token line:", line.strip()[:30])
                continue
        clean_lines.append(line)

assert valid_token, "CRITICAL ERROR: No valid working token found!"

# Write back clean .env.local
open(env_local, "w", encoding="utf-8").write("".join(clean_lines))
print("✅ Rewrote clean .env.local without duplicate/stale tokens!")

# 2. Update richard_bot.py to read valid_token
txt = open(richard_py, encoding="utf-8", errors="ignore").read()

clean_token_logic = f'''def _get_clean_bot_token():
    return "{valid_token}"

BOT_TOKEN = _get_clean_bot_token()
'''

import re
txt = re.sub(r'def _get_clean_bot_token\(\):.*?(?=\nimport navo_client|\ndef |\nLOCK_FILE)', clean_token_logic + "\n", txt, flags=re.DOTALL)

open(richard_py, "w", encoding="utf-8").write(txt)
print("✅ Successfully updated richard_bot.py with verified working token!")

py_compile.compile(richard_py, doraise=True)
print("✅ Compiled richard_bot.py cleanly!")
