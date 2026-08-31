# -*- coding: utf-8 -*-
"""
webhook_409_probe.py — diagnose & fix the silent "bot won't reply / 409 Conflict" failure.

ROOT CAUSE: a leftover webhook (usually from an old Make.com / Zapier / n8n scenario) is still
attached to the bot. Telegram delivers updates to EITHER a webhook OR getUpdates — never both.
With a webhook live, your local long-polling bot gets `HTTP 409 Conflict` and sees nothing.

Usage:
    python webhook_409_probe.py            # just print webhook status
    python webhook_409_probe.py --delete   # also delete the webhook, then re-print

Needs TELEGRAM_BOT_TOKEN (set it, or it reads .env.local in the cwd).
"""
import os, sys, json, urllib.request

def _load_env_local():
    for envf in (".env", ".env.local"):
        if os.path.exists(envf):
            for line in open(envf, encoding="utf-8"):
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k, v = k.strip(), v.strip().strip('"').strip("'")
                if k and k not in os.environ:
                    os.environ[k] = v

def _get(tok, method):
    url = "https://api.telegram.org/bot%s/%s" % (tok, method)
    return json.loads(urllib.request.urlopen(url, timeout=20).read())

if __name__ == "__main__":
    _load_env_local()
    tok = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not tok:
        print("ERROR: TELEGRAM_BOT_TOKEN not set", file=sys.stderr)
        sys.exit(2)
    me = _get(tok, "getMe").get("result", {})
    print("bot username:", me.get("username"), "id:", me.get("id"))
    info = _get(tok, "getWebhookInfo")["result"]
    print("webhook url:", repr(info.get("url")) or "(none — good for local polling)")
    if info.get("url"):
        print(">> webhook is LIVE -> local long-polling bot will get 409 Conflict and stay silent.")
        if "--delete" in sys.argv:
            r = _get(tok, "deleteWebhook?drop_pending_updates=true")
            print("deleteWebhook:", r)
            after = _get(tok, "getWebhookInfo")["result"]
            print("webhook url after:", repr(after.get("url")) or "(none)")
            print(">> restart the local bot now; the 409 should stop.")
        else:
            print(">> re-run with --delete to remove the webhook and let local polling work.")
