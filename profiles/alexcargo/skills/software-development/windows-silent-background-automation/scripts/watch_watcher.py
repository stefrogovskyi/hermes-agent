#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""watch_watcher.py - self-heal for gateway_watcher.py.

Run from a Hermes no_agent cron (every 5 min). If the gateway_watcher lock pid
is dead, relaunch the watcher hidden via BASE pythonw. Does NOT touch the
gateway itself.
"""
import os
import subprocess
import ctypes

HERMES_HOME = os.environ.get("HERMES_HOME") or os.path.expanduser(
    r"~\\AppData\\Local\\hermes"
)
WATCHER = os.path.join(HERMES_HOME, "scripts", "gateway_watcher.py")
PY_EXE = r"C:\Users\Stefan\AppData\Roaming\uv\python\cpython-3.11-windows-x86_64-none\pythonw.exe"


def _pid_alive(pid):
    h = ctypes.windll.kernel32.OpenProcess(0x0400, False, pid)
    if h:
        ctypes.windll.kernel32.CloseHandle(h)
        return True
    return False


def watcher_alive():
    lock = os.path.join(HERMES_HOME, "scripts", "gateway_watcher.lock")
    if os.path.exists(lock):
        try:
            pid = int(open(lock, encoding="utf-8").read().strip() or "0")
            if pid and _pid_alive(pid):
                return True
        except Exception:
            pass
    return False


def main():
    if watcher_alive():
        return 0
    try:
        flags = 0x00000008 | 0x08000000
        subprocess.Popen(
            [PY_EXE, WATCHER], cwd=HERMES_HOME,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            creationflags=flags, close_fds=True,
        )
        return 0
    except Exception:
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
