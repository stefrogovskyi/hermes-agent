# -*- coding: utf-8 -*-
"""
bind_richard_to_real_working_token.py — Автоматическое подтягивание живого рабочего токена из .env.local в richard_bot.py.
"""

import os, re, urllib.request, json, py_compile

richard_dir = r"C:\Users\Stefan\My Drive\Equity\My Biz\Partner companies\Navo\6. Departments\Richard Marlowe\Richard Hermes"
env_local = os.path.join(richard_dir, ".env.local")
richard_py = os.path.join(richard_dir, "richard_bot.py")

# 1. Read real token from .env.local
real_token = ""
if os.path.exists(env_local):
    for line in open(env_local, encoding="utf-8", errors="ignore"):
        if line.strip().startswith("TELEGRAM_BOT_TOKEN="):
            t = line.split("=", 1)[1].strip().strip('"').strip("'")
            if t:
                # Test token with getMe
                try:
                    url = f"https://api.telegram.org/bot{t}/getMe"
                    with urllib.request.urlopen(url, timeout=5) as resp:
                        data = json.loads(resp.read().decode("utf-8"))
                        if data.get("ok"):
                            real_token = t
                            print("✅ REAL VALID TOKEN FOUND IN .env.local:", real_token[:15] + "...")
                except Exception as e:
                    print("Token test error:", e)

assert real_token, "CRITICAL ERROR: No valid working token found in .env.local!"

# 2. Update richard_bot.py with clean token reader
txt = open(richard_py, encoding="utf-8", errors="ignore").read()

clean_token_logic = f'''def _get_clean_bot_token():
    env_local = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env.local")
    if os.path.exists(env_local):
        for line in open(env_local, encoding="utf-8", errors="ignore"):
            if line.strip().startswith("TELEGRAM_BOT_TOKEN="):
                t = line.split("=", 1)[1].strip().strip('"').strip("'")
                if t:
                    return t
    return "{real_token}"

BOT_TOKEN = _get_clean_bot_token()
'''

txt = re.sub(r'def _get_clean_bot_token\(\):.*?(?=\nimport navo_client|\ndef |\nLOCK_FILE)', clean_token_logic + "\n", txt, flags=re.DOTALL)

open(richard_py, "w", encoding="utf-8").write(txt)
print("✅ Successfully updated richard_bot.py with real working token!")

py_compile.compile(richard_py, doraise=True)
print("✅ Compiled richard_bot.py cleanly without syntax errors!")
