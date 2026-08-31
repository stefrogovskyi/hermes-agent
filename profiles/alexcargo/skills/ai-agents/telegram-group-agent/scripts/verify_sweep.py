#!/usr/bin/env python3
"""Ad-hoc verification of telegram_group_sweep.py logic (NO live API, NO token).

Usage:  python verify_sweep.py
Imports the sibling telegram_group_sweep.py, mocks api(), asserts the diff
cursor + multi-chat + send/digest behavior. Delete after running.
"""
import os, sys, tempfile, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
spec = importlib.util.spec_from_file_location("sweep", os.path.join(HERE, "telegram_group_sweep.py"))
sweep = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sweep)

results = []
def check(name, cond, detail=""):
    results.append(bool(cond))
    print(f"[{'PASS' if cond else 'FAIL'}] {name}" + (f" -- {detail}" if detail else ""))

# Isolate from any real .env
sweep.ENV_PATH = os.path.join(tempfile.gettempdir(), "sweep-verify-noenv.env")

def mk_msg(i, cid, text):
    return {"update_id": i,
            "message": {"chat": {"id": cid, "type": "group", "title": "G"},
                        "from": {"first_name": "U"}, "text": text, "date": 1700000000 + i}}

# batch1: 100 updates, every 3rd has NO message key; chat alternates -100/-200
FAKE = [
    [(mk_msg(i, -100 if i % 2 == 0 else -200, "freight") if i % 3 != 0 else {"update_id": i})
     for i in range(1, 101)],
    [mk_msg(i, -100 if i % 2 == 0 else -200, "shipping" if i % 2 == 0 else "politics")
     for i in range(101, 151)],
]
call = {"n": 0}
def fake_api(token, method, params=None, timeout=30):
    assert method == "getUpdates", method
    if call["n"] == 0:
        call["n"] += 1; return {"result": FAKE[0]}
    if call["n"] == 1:
        call["n"] += 1; return {"result": FAKE[1]}
    return {"result": []}
sweep.api = fake_api

# 1) fetch last_id=0: 100 ups - 33 no-message = 67, + 50 = 117
msgs, max_id = sweep.fetch("T", 0)
check("captures only message-bearing updates", len(msgs) == 117, f"got {len(msgs)}")
check("max_id is global max (150)", max_id == 150)
check("reads BOTH chats (no group_id filter)", {m["chat_id"] for m in msgs} == {-100, -200})
check("skips updates without message key", all("text" in m for m in msgs))

# 2) diff: second poll with last_id=150 returns nothing
call["n"] = 0
m2, mx2 = sweep.fetch("T", 150)
check("diff: second poll empty", len(m2) == 0 and mx2 == 150)

# 3) partial diff: last_id=50 -> only id>50
call["n"] = 0
m3, mx3 = sweep.fetch("T", 50)
check("partial diff captures only id>50", all(x["update_id"] > 50 for x in m3))

# 4) commit persists
ts = os.path.join(tempfile.gettempdir(), "sweep-state.json")
sweep.STATE = ts
if os.path.exists(ts):
    os.remove(ts)
sweep.save_state({"last_update_id": 150, "total_seen": 117, "last_run": "x"})
st = sweep.load_state()
check("commit persists last_update_id", st["last_update_id"] == 150)

# 5) missing token -> exit 2
os.environ.pop("TELEGRAM_BOT_TOKEN", None)
sys.argv = ["s", "fetch"]
try:
    sweep.main()
    check("missing token exits non-zero", False, "did not exit")
except SystemExit as e:
    check("missing token exits with code 2", e.code == 2)

# 6) send + digest hit correct targets
sent = {}
def fake2(token, method, params=None, timeout=30):
    sent[method] = params
    return {"ok": True}
sweep.api = fake2
sys.argv = ["s", "send", "--chat", "-100", "--text", "hi"]
sweep.main()
check("send posts to correct chat", sent.get("sendMessage", {}).get("chat_id") == "-100")
sys.argv = ["s", "digest", "--text", "warn"]
sweep.main()
check("digest sends via api", "sendMessage" in sent)

print(f"\nSUMMARY: {sum(results)}/{len(results)} passed")
sys.exit(0 if all(results) else 1)
