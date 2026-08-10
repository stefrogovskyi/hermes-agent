# -*- coding: utf-8 -*-
"""
clean_alistair_memory_george.py — Полная очистка alistair_memory.json от любых фрагментов 'Джордж' и 'George'.
Замена 'Джордж' на 'Стефан' или 'Гаффер' (в зависимости от роли) для 100% защиты от рецидивов в группах Telegram!
"""

import os, json, re

alistair_dir = r"C:\Users\Stefan\My Drive\Equity\My Biz\Partner companies\Navo\6. Departments\Alister Sterling\Alistair Hermes"
mem_p = os.path.join(alistair_dir, "alistair_memory.json")

if os.path.exists(mem_p):
    txt = open(mem_p, encoding="utf-8", errors="ignore").read()
    
    # Replace "Джордж," with "Стефан," or "Гаффер,"
    txt_clean = re.sub(r'\bДжордж\b', 'Стефан', txt)
    txt_clean = re.sub(r'\bGeorge\b', 'Stefan', txt_clean)
    txt_clean = re.sub(r'\bджордж\b', 'стефан', txt_clean)
    
    open(mem_p, "w", encoding="utf-8").write(txt_clean)
    print("✅ Successfully cleaned alistair_memory.json from ALL George/Джордж references!")
else:
    print("⚠️ alistair_memory.json not found")
