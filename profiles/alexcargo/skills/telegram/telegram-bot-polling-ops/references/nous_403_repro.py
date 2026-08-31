"""Minimal repro of the Nous 403 class bug for local Telegram bots.
Run from the hermes-agent venv:
  venv/Scripts/python.exe nous_403_repro.py

Shows: (a) a STATIC token from auth.json / .env 403s, (b) a FRESH token from
the live Hermes resolver works. Use this to confirm a 403 is the stale-key
root cause before patching _fresh_nous_key() in a bot.
"""
import json, sys, urllib.request

sys.path.insert(0, r"C:\Users\Stefan\AppData\Local\hermes\hermes-agent")


def _call(key, url, referer="https://hermes-agent.nousresearch.com"):
    import json as _j
    payload = {"model": "tencent/hy3:free", "messages": [{"role": "user", "content": "ping"}]}
    req = urllib.request.Request(url, data=_j.dumps(payload).encode(), method="POST")
    req.add_header("Authorization", "Bearer " + key)
    req.add_header("Content-Type", "application/json")
    req.add_header("HTTP-Referer", referer)
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return "OK -> " + _j.loads(r.read().decode())["choices"][0]["message"]["content"][:30]
    except Exception as e:
        return "FAIL: " + str(e)[:60]


# (a) static token from auth.json
auth = json.load(open(r"C:\Users\Stefan\AppData\Local\hermes\auth.json", encoding="utf-8"))
static_key = auth.get("providers", {}).get("nous", {}).get("access_token", "")
print("STATIC auth.json key:", _call(static_key, "https://inference-api.nousresearch.com/v1/chat/completions"))

# (b) fresh token from live Hermes resolver
from agent.auxiliary_client import _resolve_nous_pool_runtime_api
creds = _resolve_nous_pool_runtime_api(force_refresh=False)
if creds and creds[0]:
    print("RESOLVER key:", _call(creds[0], creds[1].rstrip("/") + "/chat/completions"))
else:
    print("RESOLVER returned None")
