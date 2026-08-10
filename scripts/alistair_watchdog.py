#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
alistair_watchdog.py — держит Telegram-бота Алистера живым 24/7.
Проверяет pid-лок; если процесс мёртв/отсутствует — запускает бота заново.
Тихий: печатает строку только когда что-то сделал (перезапуск) — для cron no_agent.
"""
import os
import sys
import time
import subprocess

HERE = r"C:\Users\Stefan\My Drive\Equity\My Biz\Partner companies\Navo\6. Departments\Alister Sterling\Alistair Hermes"
# Лок в локальном каталоге (совпадает с alistair_bot.py — НЕ в OneDrive-папке).
_LOCK_DIR = os.path.join(os.environ.get("LOCALAPPDATA",
                         os.path.expanduser(r"~\AppData\Local")), "hermes", "entities")
LOCK = os.path.join(_LOCK_DIR, "alistair.lock")
BOT = os.path.join(HERE, "alistair_bot.py")
LOG = os.path.join(HERE, "alistair_run.log")


def pid_alive(pid):
    try:
        # 0x08000000 = CREATE_NO_WINDOW (prevents black console flashes on Windows)
        out = subprocess.run(["tasklist", "/FI", "PID eq %d" % pid],
                             capture_output=True, text=True, timeout=15,
                             creationflags=0x08000000).stdout
        return str(pid) in out
    except Exception:
        return False


def running():
    if not os.path.exists(LOCK):
        return False
    try:
        pid = int(open(LOCK, encoding="utf-8").read().strip())
    except Exception:
        return False
    return pid_alive(pid)


def start():
    # запускаем detached, без окна; лог дописываем
    flags = 0x00000008 | 0x08000000  # DETACHED_PROCESS | CREATE_NO_WINDOW
    with open(LOG, "a", encoding="utf-8") as lf:
        subprocess.Popen([sys.executable, BOT], cwd=HERE,
                         stdout=lf, stderr=lf, creationflags=flags, close_fds=True)


if __name__ == "__main__":
    if running():
        sys.exit(0)  # всё ок — тихо выходим (cron ничего не пришлёт)
    start()
    time.sleep(6)
    ok = running()
    print("[watchdog %s] Alistair bot was down -> restarted: %s"
          % (time.strftime("%Y-%m-%d %H:%M"), "OK" if ok else "FAILED"))
    sys.exit(0 if ok else 1)
