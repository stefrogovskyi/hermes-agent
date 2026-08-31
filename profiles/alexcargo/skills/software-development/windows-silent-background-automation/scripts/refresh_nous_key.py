#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
refresh_nous_key.py — keep NOUS_API_KEY fresh in ~/.hermes/.env so the Hermes
gateway never crashes on an expired token (the real root cause of "Telegram bot
went silent"). Copies the current access_token from auth.json (Hermes itself
refreshes auth.json via its refresh_token) into .env, preserving other lines.

Run from a no_agent cron every 30 min (use the BASE python from cron_hidden_sh_template.sh
to avoid a conhost window). Do NOT restart the gateway from this script — just refresh .env.
"""
import json
import os

HERMES_HOME = os.environ.get("HERMES_HOME") or os.path.expanduser(
    r"~\AppData\Local\hermes"
)
AUTH = os.path.join(HERMES_HOME, "auth.json")
ENV = os.path.join(HERMES_HOME, ".env")


def main():
    if not os.path.isfile(AUTH):
        print("[refresh_nous_key] auth.json not found, skip")
        return 1
    try:
        d = json.load(open(AUTH, encoding="utf-8"))
    except Exception as e:
        print(f"[refresh_nous_key] auth.json parse error: {e}")
        return 1

    token = (d.get("providers", {}).get("nous", {}).get("access_token") or "").strip()
    if not token:
        print("[refresh_nous_key] no access_token in auth.json, skip")
        return 1

    lines = open(ENV, encoding="utf-8").read().splitlines() if os.path.isfile(ENV) else []
    key = "NOUS_API_KEY="
    out = [key + token if ln.startswith(key) else ln for ln in lines]
    if not any(ln.startswith(key) for ln in out):
        out.append(key + token)
    open(ENV, "w", encoding="utf-8").write("\n".join(out) + "\n")

    print(f"[refresh_nous_key] NOUS_API_KEY updated (len={len(token)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
