#!/usr/bin/env python3
"""
Avalanche Content Pipeline — Queue Manager
Manages the article queue for the automated content pipeline.

Usage:
    python3 queue_manager.py add "<url_or_topic>" [--type=rewrite|topic] [--priority=N]
    python3 queue_manager.py list
    python3 queue_manager.py next        # pops + returns the next pending item (marks in_progress)
    python3 queue_manager.py done <id>   # marks item as done, records output path
    python3 queue_manager.py fail <id> "<reason>"
    python3 queue_manager.py reset <id>  # requeue a stuck in_progress item
"""
import json
import sys
import os
import uuid
from datetime import datetime, timezone

QUEUE_DIR = os.environ.get("PIPELINE_QUEUE_DIR", "/opt/hermes/profiles/archie/content_pipeline/queue")
QUEUE_FILE = os.path.join(QUEUE_DIR, "queue.json")


def load_queue():
    if not os.path.exists(QUEUE_FILE):
        return []
    with open(QUEUE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_queue(items):
    os.makedirs(QUEUE_DIR, exist_ok=True)
    tmp = QUEUE_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    os.replace(tmp, QUEUE_FILE)


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def cmd_add(args):
    if not args:
        print("Usage: add <url_or_topic> [--type=rewrite|topic] [--priority=N] [--notes=...]")
        sys.exit(1)
    source = args[0]
    item_type = "rewrite" if source.startswith("http") else "topic"
    priority = 100
    notes = ""
    for a in args[1:]:
        if a.startswith("--type="):
            item_type = a.split("=", 1)[1]
        elif a.startswith("--priority="):
            priority = int(a.split("=", 1)[1])
        elif a.startswith("--notes="):
            notes = a.split("=", 1)[1]

    items = load_queue()
    new_item = {
        "id": uuid.uuid4().hex[:12],
        "source": source,
        "type": item_type,
        "status": "pending",
        "priority": priority,
        "notes": notes,
        "created_at": now_iso(),
        "started_at": None,
        "finished_at": None,
        "output_path": None,
        "error": None,
        "attempts": 0,
    }
    items.append(new_item)
    save_queue(items)
    print(json.dumps(new_item, ensure_ascii=False, indent=2))


def cmd_list(args):
    items = load_queue()
    status_filter = args[0] if args else None
    for it in items:
        if status_filter and it["status"] != status_filter:
            continue
        print(f"[{it['status'].upper():12s}] {it['id']}  {it['type']:8s}  {it['source'][:70]}")


def cmd_next(args):
    items = load_queue()
    pending = [it for it in items if it["status"] == "pending"]
    if not pending:
        print(json.dumps({"empty": True}))
        return
    pending.sort(key=lambda x: (x["priority"], x["created_at"]))
    chosen = pending[0]
    for it in items:
        if it["id"] == chosen["id"]:
            it["status"] = "in_progress"
            it["started_at"] = now_iso()
            it["attempts"] = it.get("attempts", 0) + 1
    save_queue(items)
    print(json.dumps(chosen, ensure_ascii=False, indent=2))


def cmd_done(args):
    if not args:
        print("Usage: done <id> [--output=<path>]")
        sys.exit(1)
    item_id = args[0]
    output_path = None
    for a in args[1:]:
        if a.startswith("--output="):
            output_path = a.split("=", 1)[1]
    items = load_queue()
    found = False
    for it in items:
        if it["id"] == item_id:
            it["status"] = "done"
            it["finished_at"] = now_iso()
            it["output_path"] = output_path
            found = True
    save_queue(items)
    print(json.dumps({"updated": found}))


def cmd_fail(args):
    if len(args) < 1:
        print("Usage: fail <id> [reason]")
        sys.exit(1)
    item_id = args[0]
    reason = args[1] if len(args) > 1 else "unknown"
    items = load_queue()
    found = False
    for it in items:
        if it["id"] == item_id:
            # If under 3 attempts, requeue as pending; else mark permanently failed
            if it.get("attempts", 0) < 3:
                it["status"] = "pending"
            else:
                it["status"] = "failed"
            it["error"] = reason
            found = True
    save_queue(items)
    print(json.dumps({"updated": found}))


def cmd_reset(args):
    if not args:
        print("Usage: reset <id>")
        sys.exit(1)
    item_id = args[0]
    items = load_queue()
    found = False
    for it in items:
        if it["id"] == item_id:
            it["status"] = "pending"
            it["started_at"] = None
            found = True
    save_queue(items)
    print(json.dumps({"updated": found}))


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    cmd = sys.argv[1]
    args = sys.argv[2:]
    dispatch = {
        "add": cmd_add,
        "list": cmd_list,
        "next": cmd_next,
        "done": cmd_done,
        "fail": cmd_fail,
        "reset": cmd_reset,
    }
    fn = dispatch.get(cmd)
    if not fn:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)
    fn(args)


if __name__ == "__main__":
    main()
