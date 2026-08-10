# -*- coding: utf-8 -*-
"""
clean_richard_history_memory.py — Очистка устаревшей истории тестов из richard_memory.json для чистой работы Ричарда.
"""

import os, json

richard_dir = r"C:\Users\Stefan\My Drive\Equity\My Biz\Partner companies\Navo\6. Departments\Richard Marlowe\Richard Hermes"
mem_p = os.path.join(richard_dir, "richard_memory.json")

if os.path.exists(mem_p):
    data = json.loads(open(mem_p, encoding="utf-8", errors="ignore").read())
    
    # Reset Stefan's direct history key u:330656040
    data["u:330656040"] = []
    
    # Save back
    open(mem_p, "w", encoding="utf-8").write(json.dumps(data, indent=2, ensure_ascii=False))
    print("✅ Successfully cleared old test history for Stefan's key u:330656040!")

# Also patch richard_bot.py history_get() to clamp to last 10 messages max
bot_p = os.path.join(richard_dir, "richard_bot.py")
txt = open(bot_p, encoding="utf-8", errors="ignore").read()

old_hist = "return data.get(key, [])"
new_hist = "return data.get(key, [])[-10:]"

if old_hist in txt:
    txt = txt.replace(old_hist, new_hist)
    open(bot_p, "w", encoding="utf-8").write(txt)
    print("✅ Clamped history_get() in richard_bot.py to last 10 messages!")
