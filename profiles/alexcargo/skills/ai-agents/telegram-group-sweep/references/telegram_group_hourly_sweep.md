# Telegram group hourly sweep — detailed note

Companion to SKILL.md `telegram-group-sweep`. Captured 2026-07-23.

## Why hourly + diff
- Realtime every-message reading burns tokens and is noisy. User wanted: read 1x/hour,
  react only to mentions / useful on-domain content, stay silent otherwise.
- 24 sweeps/day with a persisted `last_update_id` gives full coverage and zero
  re-reads as long as the process stays up.

## The getUpdates contract (exact)
```
GET https://api.telegram.org/bot<TOKEN>/getUpdates
   ?offset=<last_update_id+1>&timeout=0&limit=100
```
- `offset` is 1-based: pass `last_update_id + 1` to skip everything already seen.
- `timeout=0` = long-poll off → returns what's buffered immediately (good for cron).
- Page by `limit=100` until `result` is empty.
- After deciding to accept the batch, set `last_update_id = max(update_id)`.

## Conflict rule, precisely
- Telegram delivers each update to the FIRST client that polls a given token.
- Two processes polling the SAME token → they split/steal each other's updates.
- Two tokens = two independent queues; no interference.
- Therefore: an agent's group sweep must be the SOLE poller of its own token. If
  the same token also feeds a realtime gateway, the sweep starves. Use a separate
  token for group vs DM, OR run only the sweep on that token.

## User correction that produced this skill
First design added a "Hermes Group Watcher" bot on a separate token to read the
group hourly while Richard was left out. User rejected it: "почему мы не можем
настроить самого Ричарда… я не хочу плодить в группе ботов". Correct design:
Richard's own token (`richnavobot`) runs the sweep; orchestrator (Stevenson)
only creates cron + watches digests, never joins the group.

## Script skeleton (stdlib urllib, no pip)
```python
import os, json, urllib.request

def api(token, method, params=None):
    url = f"https://api.telegram.org/bot{token}/{method}"
    req = urllib.request.Request(url,
        data=json.dumps(params or {}).encode(),
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())

def fetch(token, chat_id, last_id):
    out, max_id, offset = [], last_id, last_id + 1
    while True:
        res = api(token, "getUpdates",
                 {"offset": offset, "timeout": 0, "limit": 100}).get("result", [])
        if not res: break
        for u in res:
            uid = u.get("update_id", 0); max_id = max(max_id, uid)
            m = u.get("message") or u.get("edited_message")
            if not m: continue
            if str(m.get("chat", {}).get("id")) != str(chat_id): continue
            if uid <= last_id: continue
            out.append({"id": uid, "from": m.get("from", {}).get("first_name"),
                        "text": (m.get("text") or m.get("caption") or "").strip()})
        offset = max_id + 1
        if len(res) < 100: break
    return out, max_id
```
Subcommands: `fetch` (print JSON), `commit --max-id N`, `send --chat --text`,
`digest --text`. Missing env → `sys.exit(2)`.

## SPOF
- ~24h retention on Telegram side; ~100 queued. Downtime >24h loses old queue.
- Prefer VPS/Modal for the sweep process; Windows Desktop works while alive.
- State file `group_state_<bot>.json` = `{"last_update_id":0,"total_seen":0,"last_run":null}`.
