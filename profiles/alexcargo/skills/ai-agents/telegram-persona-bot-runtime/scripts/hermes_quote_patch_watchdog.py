#!/usr/bin/env python3
"""hermes_quote_patch_watchdog.py — auto-recover a core-file patch after Hermes updates.

WHY: patches to Hermes CORE files (e.g. plugins/platforms/telegram/adapter.py, which makes
Hermes itself see Telegram message.quote / the quoted fragment) are silently overwritten by
every `hermes update` / desktop auto-update. This watchdog restores the patch automatically.

SAFE:
- Reads only; never touches the file if the marker is present (stdout empty -> silence).
- Re-inserts ONLY the missing block after a known anchor line; never rewrites other content.
- Does NOT restart the gateway (cron lifecycle rules block gateway restart from inside a cron;
  `hermes update` already restarts the gateway, so the owner just relaunches Desktop once).
- If the backup is missing/corrupt, writes to stderr and does nothing destructive.

Run via a `no_agent=True` Hermes cron `every 5m`. Copy this file into
%LOCALAPPDATA%\hermes\scripts\ so the cron finds it by bare name. The backup file
QUOTE_PATCH_BACKUP.txt must sit next to it (same dir) with the patch block delimited by
`=== ТОЧНЫЙ БЛОК ДЛЯ ВСТАВКИ ===` / `=== КОНЕЦ БЛОКА ===` (comment lines starting with `#` are
stripped before insertion).
"""
import os
import re
import sys

HERMES_HOME = os.environ.get("LOCALAPPDATA", os.path.expanduser("~\\AppData\\Local"))
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ADAPTER = os.path.join(HERMES_HOME, "hermes-agent", "plugins", "platforms",
                       "telegram", "adapter.py")
BACKUP = os.path.join(SCRIPT_DIR, "QUOTE_PATCH_BACKUP.txt")
MARKER = "ПОЛЬЗОВАТЕЛЬ ПРОЦИТИРОВАЛ"


def patch_present():
    try:
        return MARKER in open(ADAPTER, encoding="utf-8").read()
    except FileNotFoundError:
        return False


def extract_block_from_backup():
    txt = open(BACKUP, encoding="utf-8").read()
    m = re.search(r"=== ТОЧНЫЙ БЛОК ДЛЯ ВСТАВКИ ===\n(.*?)=== КОНЕЦ БЛОКА ===",
                  txt, re.S)
    if not m:
        return None
    block = m.group(1)
    lines = [ln for ln in block.splitlines() if not ln.startswith("#")]
    return "\n".join(lines).strip("\n") + "\n"


def restore():
    block = extract_block_from_backup()
    if not block:
        sys.stderr.write("BACKUP block not found — abort\n")
        return False
    src = open(ADAPTER, encoding="utf-8").read()
    anchor = 'event.text = self._clean_bot_trigger_text(event.text)'
    if anchor not in src:
        sys.stderr.write("ANCHOR not found in adapter.py — abort (file structure changed?)\n")
        return False
    idx = src.index(anchor)
    new_src = src[:idx + len(anchor)] + "\n" + block + src[idx + len(anchor):]
    open(ADAPTER, "w", encoding="utf-8").write(new_src)
    return patch_present()


if __name__ == "__main__":
    if patch_present():
        sys.exit(0)  # silence — everything ok
    if not os.path.exists(BACKUP):
        sys.stderr.write("PATCH MISSING and no backup — manual fix needed\n")
        sys.exit(1)
    ok = restore()
    if ok:
        print("QUOTE PATCH RESTORED after update — restart Hermes Desktop once to load it")
    else:
        sys.stderr.write("RESTORE FAILED — check adapter.py manually\n")
        sys.exit(1)
