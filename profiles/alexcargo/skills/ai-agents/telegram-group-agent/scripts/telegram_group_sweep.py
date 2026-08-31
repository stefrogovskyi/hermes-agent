#!/usr/bin/env python3
"""
telegram_group_sweep.py — batch Telegram group reader for an AI agent.

One bot token = one consumer of getUpdates. Run on a schedule (e.g. hourly) to
read ONLY new messages (diff via persisted last_update_id), then decide whether
to reply. Does NOT stream realtime.

Subcommands:
  fetch                  -> JSON {"max_id":N,"messages":[...]}
  commit --max-id N      -> persist last_update_id = N (mark as read)
  send --chat C --text T -> reply in a chat as the bot
  digest --text T        -> owner escalation (DM, via bot token)

Env (.env next to script):
  TELEGRAM_BOT_TOKEN   (single bot token)            [required]
  STEFAN_CHAT_ID       (owner chat id for escalations) [optional]
  BOT_USERNAME         (mention handle, e.g. richnavobot) [optional, for detection]
  GROUP_CHAT_ID        (OPTIONAL: restrict to one group; OMIT to read ANY group)
  ON_DOMAIN_KEYWORDS   (optional, comma list of on-domain trigger words)
"""
import os, json, sys, urllib.request
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(HERE, "group_state.json")
ENV_PATH = os.path.join(HERE, ".env")
DEFAULT_ON_DOMAIN = ("logistics,freight,shipping,tracking,rate,shipment,port,"
                     "customs,charter,trackingmcp,schedulesmcp,loadingmcp,freightratesmcp")


def load_env():
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


def api(token, method, params=None, timeout=30):
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = json.dumps(params or {}).encode("utf-8")
    req = urllib.request.Request(url, data=data,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def load_state():
    if os.path.exists(STATE):
        with open(STATE, encoding="utf-8") as f:
            return json.load(f)
    return {"last_update_id": 0, "total_seen": 0, "last_run": None}


def save_state(st):
    with open(STATE, "w", encoding="utf-8") as f:
        json.dump(st, f, ensure_ascii=False, indent=2)


def fetch(token, last_id, restrict_chat=None):
    """Return (messages, max_id). Pages through ALL batches; skips non-message updates."""
    out, max_id, offset = [], last_id, last_id + 1
    while True:
        resp = api(token, "getUpdates", {"offset": offset, "timeout": 0, "limit": 100})
        results = resp.get("result", [])
        if not results:
            break
        for u in results:
            uid = u.get("update_id", 0)
            max_id = max(max_id, uid)
            msg = u.get("message") or u.get("edited_message")
            if not msg:
                continue
            chat = msg.get("chat", {})
            if restrict_chat and str(chat.get("id")) != str(restrict_chat):
                continue
            if uid <= last_id:
                continue
            out.append({
                "update_id": uid,
                "chat_id": chat.get("id"),
                "chat_type": chat.get("type"),
                "from": msg.get("from", {}).get("first_name", "?"),
                "text": (msg.get("text") or msg.get("caption") or "").strip(),
                "date": msg.get("date"),
            })
        offset = max_id + 1
        if len(results) < 100:
            break
    return out, max_id


def main():
    load_env()
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    stefan = os.environ.get("STEFAN_CHAT_ID")
    restrict = os.environ.get("GROUP_CHAT_ID")  # omit => read any chat
    cmd = sys.argv[1] if len(sys.argv) > 1 else "fetch"

    if cmd == "fetch":
        if not token:
            sys.stderr.write("[sweep] missing TELEGRAM_BOT_TOKEN\n")
            sys.exit(2)
        st = load_state()
        msgs, max_id = fetch(token, st["last_update_id"], restrict)
        print(json.dumps({"max_id": max_id, "messages": msgs}, ensure_ascii=False))
        return

    if cmd == "commit":
        max_id = int(sys.argv[sys.argv.index("--max-id") + 1])
        st = load_state()
        st["last_update_id"] = max_id
        st["last_run"] = datetime.now(timezone.utc).isoformat()
        save_state(st)
        print(f"committed last_update_id={max_id}")
        return

    if cmd == "send":
        ci = sys.argv[sys.argv.index("--chat") + 1]
        tx = sys.argv[sys.argv.index("--text") + 1]
        api(token, "sendMessage", {"chat_id": ci, "text": tx})
        print("sent")
        return

    if cmd == "digest":
        if not stefan:
            sys.stderr.write("[sweep] STEFAN_CHAT_ID not set\n")
            sys.exit(3)
        tx = sys.argv[sys.argv.index("--text") + 1]
        api(token, "sendMessage", {"chat_id": stefan, "text": tx})
        print("digested")
        return

    sys.stderr.write(f"unknown cmd {cmd}\n")
    sys.exit(2)


if __name__ == "__main__":
    main()
