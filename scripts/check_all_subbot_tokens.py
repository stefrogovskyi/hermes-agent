# -*- coding: utf-8 -*-
import os, urllib.request, json

env_paths = [
    ("Hermes", r"C:\Users\Stefan\AppData\Local\hermes\.env"),
    ("Richard", r"C:\Users\Stefan\My Drive\Equity\My Biz\Partner companies\Navo\6. Departments\Richard Marlowe\Richard Hermes\.env.local"),
    ("Alistair", r"C:\Users\Stefan\My Drive\Equity\My Biz\Partner companies\Navo\6. Departments\Alister Sterling\Alistair Hermes\.env.local"),
    ("Callum", r"C:\Users\Stefan\My Drive\Equity\My Biz\My companies\Enlight Group\Enlight Board\Callum Vance\Callum Vance Hermes\.env.local"),
    ("Liz", r"C:\Users\Stefan\My Drive\Equity\My Biz\My companies\Enlight Group\Enlight Board\Liz Harper\Liz Harper Hermes\.env.local")
]

for name, p in env_paths:
    if os.path.exists(p):
        tok = ""
        for line in open(p, encoding='utf-8', errors='ignore'):
            if line.strip().startswith('TELEGRAM_BOT_TOKEN='):
                tok = line.split('=', 1)[1].strip().strip('"').strip("'")
        if tok:
            url = f"https://api.telegram.org/bot{tok}/getMe"
            try:
                req = urllib.request.Request(url)
                with urllib.request.urlopen(req, timeout=5) as resp:
                    data = json.loads(resp.read().decode('utf-8'))
                    res = data.get('result', {})
                    print(f"✅ {name}: {res.get('first_name')} (@{res.get('username')}) | Token: {tok[:15]}...")
            except Exception as e:
                print(f"❌ {name}: HTTP Error {e} | Token: {tok[:15]}...")
        else:
            print(f"⚠️ {name}: TELEGRAM_BOT_TOKEN missing in {p}")
    else:
        print(f"⚠️ {name}: File missing: {p}")
