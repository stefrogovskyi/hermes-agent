#!/usr/bin/env python3
"""refresh_nous_keys.py — belt-and-suspenders against Nous JWT expiry.

WHY: the host's nous JWT (~/AppData/Local/hermes/auth.json -> providers.nous.access_token)
EXPIRES (short-lived, ~hours). Bots read it FRESH at runtime via _fresh_nous_token()/_fresh_nous_key(),
but if that runtime read ever fails, a stale static copy in each bot's .env.local would 401.
This script copies the CURRENT token from auth.json into NOUS_API_KEY of every bot's .env.local,
so the env fallback is never itself stale. Run via a no_agent Hermes cron every 30m.

It is SILENT on success and returns non-zero on error (so the cron alerts).
Secrets stay local — .env.local is gitignored in every repo.

USAGE: cronjob(create, no_agent=True, script="refresh_nous_keys.py", schedule="every 30m")
"""
import json
import os

AUTH = os.path.expanduser(r"~\\AppData\\Local\\hermes\\auth.json")

# Edit this list when you add a bot. Each entry is the bot's .env.local path.
TARGETS = [
    r"C:\Users\Stefan\My Drive\Equity\My Biz\Partner companies\Navo\6. Departments\Richard Marlowe\Richard Hermes\.env.local",
    r"C:\Users\Stefan\My Drive\Equity\My Biz\Partner companies\Navo\6. Departments\Alister Sterling\Alistair Hermes\.env.local",
]


def fresh_token():
    try:
        d = json.load(open(AUTH, encoding="utf-8"))
        return d.get("providers", {}).get("nous", {}).get("access_token", "")
    except Exception as e:
        print("ERR read auth.json: %s" % e)
        return ""


def write_target(path, token):
    if not os.path.exists(path):
        print("SKIP (no file): %s" % path)
        return
    lines = open(path, encoding="utf-8").read().splitlines()
    out, replaced = [], False
    for ln in lines:
        if ln.startswith("NOUS_API_KEY="):
            out.append("NOUS_API_KEY=%s" % token)
            replaced = True
        else:
            out.append(ln)
    if not replaced:
        out.append("NOUS_API_KEY=%s" % token)
    open(path, "w", encoding="utf-8").write("\n".join(out) + "\n")
    print("UPDATED %s" % os.path.basename(os.path.dirname(path)))


def main():
    tok = fresh_token()
    if not tok or tok.startswith("stub-"):
        print("NO fresh token — nothing to do")
        return
    for t in TARGETS:
        write_target(t, tok)
    print("done, token len %d" % len(tok))


if __name__ == "__main__":
    main()
