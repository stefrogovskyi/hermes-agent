#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ben_watchdog.py — держит Telegram-бота Бена Джетта живым 24/7.
"""
import os
import sys
import time
import subprocess

HERE = r"C:\Users\Stefan\My Drive\Equity\My Biz\My companies\Enlight Group\Avalanche Agency\Team\Ben Jett\Ben Jett Hermes"
_LOCK_DIR = os.path.join(os.environ.get("LOCALAPPDATA",
                         os.path.expanduser(r"~\AppData\Local")), "hermes", "entities")
LOCK = os.path.join(_LOCK_DIR, "ben.lock")
BOT = os.path.join(HERE, "ben_jett_bot.py")
LOG = os.path.join(HERE, "ben_run.log")


def pid_alive(pid):
    try:
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
    py_exe = r"C:\Users\Stefan\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe"
    with open(LOG, "a", encoding="utf-8") as lf:
        subprocess.Popen([py_exe, BOT], cwd=HERE,
                         stdout=lf, stderr=lf, creationflags=flags, close_fds=True)


if __name__ == "__main__":
    if running():
        sys.exit(0)
    start()
    time.sleep(6)
    ok = running()
    print("[watchdog %s] Ben bot was down -> restarted: %s"
          % (time.strftime("%Y-%m-%d %H:%M"), "OK" if ok else "FAILED"))
    sys.exit(0 if ok else 1)
