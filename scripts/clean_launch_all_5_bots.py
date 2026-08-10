# -*- coding: utf-8 -*-
"""
clean_launch_all_5_bots.py — Безупречный запуск ровно 1 чистого процесса для каждого из 5 ботов.
"""

import psutil, subprocess, sys, time, os

bots_cfg = [
    (r"C:\Users\Stefan\My Drive\Equity\My Biz\Partner companies\Navo\6. Departments\Richard Marlowe\Richard Hermes", "richard_bot.py", "richard.lock"),
    (r"C:\Users\Stefan\My Drive\Equity\My Biz\Partner companies\Navo\6. Departments\Alister Sterling\Alistair Hermes", "alistair_bot.py", "alistair.lock"),
    (r"C:\Users\Stefan\My Drive\Equity\My Biz\My companies\Enlight Group\Enlight Board\Callum Vance\Callum Vance Hermes", "callum_vance_bot.py", "callum.lock"),
    (r"C:\Users\Stefan\My Drive\Equity\My Biz\My companies\Enlight Group\Enlight Board\Liz Harper\Liz Harper Hermes", "liz_harper_bot.py", "liz.lock"),
    (r"C:\Users\Stefan\My Drive\Equity\My Biz\My companies\Enlight Group\Avalanche Agency\Team\Ben Jett\Ben Jett Hermes", "ben_jett_bot.py", "ben.lock")
]

print("=== 1. ЗАВЕРШЕНИЕ ВСЕХ СТАРЫХ ПРОЦЕССОВ БОТОВ ===")
script_names = [b[1] for b in bots_cfg]

for p in psutil.process_iter(["pid", "name", "cmdline"]):
    try:
        cmd = " ".join(p.info["cmdline"] or [])
        if any(s in cmd for s in script_names) and "watchdog" not in cmd and "clean_launch" not in cmd:
            print(f"Killing PID {p.info['pid']}: {cmd[:60]}...")
            p.kill()
    except Exception:
        pass

time.sleep(1)

# Удаляем старые лок-файлы
for bdir, bfile, block in bots_cfg:
    for lp in [os.path.join(bdir, block), os.path.join(r"C:\Users\Stefan\AppData\Local\hermes\entities", block)]:
        if os.path.exists(lp):
            try: os.remove(lp)
            except: pass

print("\n=== 2. ЗАПУСК РОВНО ПО 1 ЧИСТОМУ ПРОЦЕССУ ДЛЯ КАЖДОГО БОТА ===")
pythonw_exe = sys.executable.replace("python.exe", "pythonw.exe")

for bdir, bfile, block in bots_cfg:
    proc = subprocess.Popen([pythonw_exe, bfile], cwd=bdir, creationflags=0x08000000)
    print(f"🚀 Запущен {bfile} с PID {proc.pid}")

time.sleep(3)

print("\n=== 3. ПРОВЕРКА АКТИВНЫХ ПРОЦЕССОВ В ОС ===")
for bdir, bfile, block in bots_cfg:
    active = []
    for p in psutil.process_iter(["pid", "name", "cmdline"]):
        try:
            cmd = " ".join(p.info["cmdline"] or [])
            if (cmd.endswith(bfile) or f" {bfile}" in cmd) and "watchdog" not in cmd:
                active.append(p.info["pid"])
        except Exception:
            pass
    print(f"  • {bfile}: {len(active)} активных процессов (PIDs: {active})")
