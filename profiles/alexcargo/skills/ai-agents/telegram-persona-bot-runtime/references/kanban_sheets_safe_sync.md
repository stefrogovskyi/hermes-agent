# Kanban (SalesLoop/Gaffer) → Google Sheets safe one-way sync

Reusable building blocks for `tasktracker_client.py` (stdlib only, Google Sheets OAuth
via `%LOCALAPPDATA%\hermes\google_token.json`; kanban via SalesLoop `Authorization: Bearer`).

## Constants
```python
TRACKER_TAB = os.environ.get("TRACKER_TAB", "Tracker")
SALESLOOP_URL = os.environ.get("SALESLOOP_URL", "https://salesloop.fly.dev/v1/tasks/status")
FIELDS = ["id", "task", "owner", "percent", "timeline", "comments"]
```

## Read kanban (Bearer, read-only)
```python
def get_task_status(params=None):
    key = os.environ.get("SALESLOOP_API_KEY", "") or os.environ.get("SALESLOOP_TOKEN", "")
    if not key or key.startswith("stub-"):
        return {"error": "SALESLOOP not set", "backend": "stub"}
    req = urllib.request.Request(SALESLOOP_URL)
    req.add_header("Authorization", "Bearer %s" % key)
    with urllib.request.urlopen(req, timeout=30) as r:
        d = json.loads(r.read().decode())
    return {"ok": d.get("ok"), "generated_at": d.get("generated_at"),
            "count": d.get("count"), "summary": d.get("summary", ""),
            "tasks": d.get("tasks", [])}
```

## Parse the Sheet into main/done blocks (never overwrite owner rows)
```python
def _sheets_structure():
    res = _sheets_api("GET", "/values/" + quote("%s!A1:F1000" % TRACKER_TAB))
    values = res.get("values", [])
    if not values:
        return [], [], 1
    main, done = [], []
    in_done = False
    for i, v in enumerate(values, start=1):
        if i == 1:
            continue  # header
        v = (v + [""] * 6)[:6]
        if not any(x.strip() for x in v):
            if main:
                in_done = True
            continue
        rec = {"_row": i, "_vals": v, "id": v[0].strip(), "task": v[1],
               "owner": v[2], "percent": v[3], "timeline": v[4], "comments": v[5]}
        (done if (in_done or str(v[3]).strip().rstrip("%") == "100") else main).append(rec)
    last_main = main[-1]["_row"] if main else 1
    return main, done, last_main
```

## Owner mapping (Team tab first, hardcoded fallback, unknown → Gaffer)
```python
OWNER_MAP = {
    "stefan": "@stefrogovskiy", "stefan rogovskiy": "@stefrogovskiy", "@stefrogovskiy": "@stefrogovskiy",
    "alexey": "@lxxmng", "aleksey": "@lxxmng", "alex": "@lxxmng", "lxxmng": "@lxxmng", "@lxxmng": "@lxxmng",
    "gaffer": "@thegaffermcp_bot", "thegaffer": "@thegaffermcp_bot", "@thegaffermcp_bot": "@thegaffermcp_bot",
    "richard": "@richnavobot", "@richnavobot": "@richnavobot",
    "alistair": "@qubicpmbot", "@qubicpmbot": "@qubicpmbot",
}
DEFAULT_OWNER = "@thegaffermcp_bot"  # NOTE: Gaffer = @thegaffermcp_bot, NOT @sortitbot
_TEAM_MAP_CACHE = None

def _load_team_map():
    global _TEAM_MAP_CACHE
    if _TEAM_MAP_CACHE is not None:
        return _TEAM_MAP_CACHE
    m = {}
    try:
        res = _sheets_api("GET", "/values/" + quote("Team!A2:D100"))
        for v in res.get("values", []):
            v = (v + [""] * 4)[:4]
            name, nick = v[0].strip(), v[3].strip()
            if nick:
                if name: m[name.lower()] = nick
                m[nick.lower().lstrip("@")] = nick
                m[nick.lower()] = nick
    except Exception:
        pass
    _TEAM_MAP_CACHE = m
    return m

def _owner_to_nick(author_name):
    if not author_name:
        return DEFAULT_OWNER
    key = str(author_name).strip().lower().lstrip("@")
    team = _load_team_map()
    if key in team: return team[key]
    if key in OWNER_MAP: return OWNER_MAP[key]
    for k, v in team.items():
        if k and k in key: return v
    for k, v in OWNER_MAP.items():
        if k and k in key: return v
    return DEFAULT_OWNER
```

## Batched safe sync (insert-after-main, match-by-id, never clobber)
```python
def sync_to_sheets(params=None):
    data = get_task_status()
    if "error" in data:
        return data
    tasks = data.get("tasks", [])
    main, done, last_main = _sheets_structure()
    existing = {r["id"]: r for r in main + done if r["id"]}
    added = updated = skipped = 0
    next_n = 1
    for r in main:
        try: next_n = max(next_n, int(r["id"]) + 1)
        except ValueError: pass
    new_rows, update_calls, insert_at = [], [], last_main + 1
    for t in tasks:
        tid = str(t.get("id", "")).strip()
        if not tid:
            tid = str(next_n); next_n += 1
        title = (t.get("title") or "").strip()
        short, full = title, ""
        if len(title) > 90:
            short, full = title[:87].rstrip() + "...", title
        owner = _owner_to_nick(t.get("author_name"))
        pct, timeline = "10%", _default_timeline()
        today = datetime.date.today().strftime("%d.%m.%Y")
        cnew = "📥 %s Gaffer: %s | %s | %s" % (
            today, (t.get("status") or "").upper(), t.get("category", ""), t.get("feasibility") or "")
        if full:
            cnew += "\n" + full
        if tid in existing:
            rec = existing[tid]
            nv = [rec["id"], short or rec["task"], owner or rec["owner"],
                  rec["percent"] or pct, rec["timeline"] or timeline, rec["comments"]]
            if cnew not in rec["comments"]:
                nv[5] = (rec["comments"] + "\n" + cnew).strip()
            if short and short != rec["task"]:
                nv[1] = short
            if nv != rec["_vals"]:
                update_calls.append((rec["_row"], nv)); updated += 1
            else:
                skipped += 1
        else:
            new_rows.append([tid, short, owner, pct, timeline, cnew]); added += 1
    if new_rows:
        _sheets_insert_rows(insert_at, len(new_rows))           # ONE batch insertDimension
        _sheets_api("POST", "/values/" + quote("%s!A:F" % TRACKER_TAB) + ":append",
                    body={"values": new_rows},
                    params={"valueInputOption": "USER_ENTERED", "insertDataOption": "INSERT_ROWS"})
    if update_calls:
        reqs = []
        for ridx, vals in update_calls:
            reqs.append({"updateCells": {
                "range": {"sheetId": _sheet_id(), "startRowIndex": ridx - 1, "endRowIndex": ridx,
                          "startColumnIndex": 0, "endColumnIndex": 6},
                "rows": [{"values": [{"userEnteredValue": {"stringValue": str(v)}} for v in vals]}],
                "fields": "userEnteredValue"}})
        _sheets_api("POST", ":batchUpdate", body={"requests": reqs})   # ONE batch update
    _ensure_done_block()   # force the two-block structure
    return {"ok": True, "added": added, "updated": updated, "skipped": skipped,
            "backend": "sheets<-salesloop", "summary": data.get("summary", "")}
```

`_sheets_insert_rows(start, n)` = `batchUpdate` `insertDimension` (sheetId from `_sheet_id()`);
`_sheets_green_row(ridx)` = `repeatCell` backgroundColor `{0.85,0.93,0.85}`; `_sheets_move_row_to_done`
deletes the source row then inserts at the done-block top + greens it. All hit `:batchUpdate`.

## 100% lifecycle — move to done (green) and back to main

The owner's rule: a task at 100% is light-green-filled and lives in the done block (below the
blank separator). A task that drops below 100% returns to the top of the main block and loses
its green. `sync_to_sheets` should call `_ensure_done_block()` at the end so the structure always
resolves to exactly two blocks.

```python
def _row_in_done(rec):
    main, done, _ = _sheets_structure()
    return any(d["_row"] == rec["_row"] for d in done)

def _sheets_update(p):
    # find the row by ID across BOTH blocks (fresh structure — never trust a stale _row)
    main, done, _ = _sheets_structure()
    row = next((r for r in main + done if str(r["id"]).strip() == str(p.get("id")).strip()), None)
    if not row:
        return {"error": "task %s not found" % p.get("id"), "backend": "sheets"}
    merged = dict(row)
    for f in FIELDS[1:]:
        if f in p:
            merged[f] = p[f]
    pct_raw = str(merged.get("percent", "")).strip().rstrip("%")
    is_done = (pct_raw == "100")
    if "percent" not in p:
        is_done = (str(row["percent"]).strip().rstrip("%") == "100")
    # F: append a dated line, never delete prior content
    if p.get("comments"):
        today = datetime.date.today().strftime("%d.%m.%Y")
        merged["comments"] = (row["comments"] + "\n%s: %s" % (today, p["comments"])).strip() \
            if row["comments"] else "%s: %s" % (today, p["comments"])
    pct = merged.get("percent", "")
    if pct not in (None, "") and not str(pct).endswith("%"):
        pct = str(pct) + "%"
    in_done = _row_in_done(row)
    if is_done and not in_done:
        rec = {"id": row["id"], "_row": row["_row"], "task": merged.get("task", ""),
               "owner": merged.get("owner", ""), "percent": "100%",
               "timeline": merged.get("timeline", ""), "comments": merged.get("comments", "")}
        _sheets_move_row_to_done(rec, [])
        return {"ok": True, "updated": merged, "moved_to_done": True, "backend": "sheets"}
    if (not is_done) and in_done:
        # BUG-FIX: pass the MERGED record (with the new percent), NOT the stale `row`.
        # Passing `row` re-inserts the OLD percent (e.g. 100%) so the task stays in done.
        rec = {"id": row["id"], "_row": row["_row"], "task": merged.get("task", ""),
               "owner": merged.get("owner", ""), "percent": merged.get("percent", ""),
               "timeline": merged.get("timeline", ""), "comments": merged.get("comments", "")}
        _sheets_move_row_to_main(rec)
        return {"ok": True, "updated": merged, "moved_to_main": True, "backend": "sheets"}
    values = [[str(row["id"]), merged.get("task", ""), merged.get("owner", ""),
               pct, merged.get("timeline", ""), merged.get("comments", "")]]
    _sheets_api("PUT", "/values/" + quote("%s!A%d:F%d" % (TRACKER_TAB, row["_row"], row["_row"])),
                body={"values": values}, params={"valueInputOption": "USER_ENTERED"})
    return {"ok": True, "updated": merged, "backend": "sheets"}

def _ensure_done_block():
    """After any sync, force the two-block structure: every 100% row moves to done,
    every non-100% row in done returns to main."""
    main, done, _ = _sheets_structure()
    for r in list(main):
        if str(r["percent"]).strip().rstrip("%") == "100":
            _sheets_move_row_to_done(r, [])
            main, done, _ = _sheets_structure()   # structure shifted — re-read
    for r in list(done):
        if str(r["percent"]).strip().rstrip("%") != "100":
            _sheets_move_row_to_main(r)
            main, done, _ = _sheets_structure()
```

`_sheets_move_row_to_done(rec, _)`: delete source row → re-read structure → insert ONE blank at
`last_main + 1` → write values → `_sheets_green_row`.
`_sheets_move_row_to_main(rec)`: delete source row → re-read structure → if the cell right after
`main` is non-empty (done block with no separator), insert a blank separator first → insert at
`last_main + 1` → write values (no green). Both re-read `_sheets_structure()` AFTER the delete
because row indices shift.

## Pitfalls (all hit live this session)
1. **Never `PUT ...!A2:F1000`** — it overwrites the owner's hand rows. Insert after main, match by id.
2. **Batch or timeout:** 47 single-row writes = 60s+ → terminal/cron times out mid-sync → partial data.
3. **B truncated >90 chars → full text into F**, never drop it.
4. **D untouched on update, F appended (never cleared).**
5. **Gaffer nick = `@thegaffermcp_bot`** (not `@sortitbot`). Unknown author → `@thegaffermcp_bot`.
6. **SalesLoop wants `Authorization: Bearer`, not `X-API-Key`** — wrong header = 401.
7. **Read-only API:** no PATCH/POST — "two-way sync" is impossible; mirror kanban→sheet only.
8. **Verify:** after sync, assert owner's row 2 is unchanged and kanban rows sit after it.
9. **100%→main bug (cost a rework):** in `_sheets_update`, the return-to-main branch must pass the
   MERGED record to `_sheets_move_row_to_main`, NOT the stale `row`. Passing `row` carries the old
   `percent` (100%) so the re-inserted row is still 100% and lands back in done. Symptom: after
   `update id=X percent=55`, the task stays in the done block (`in_done=True`). Fix shown above.
10. **Find rows by ID via `_sheets_structure()`, not a stale `_row` from an earlier read.** After a
    move/delete the structure shifts; re-read it inside the handler before acting.
11. **`_sheets_add` must insert after the main block too** (use `last_main + 1`), not `:append` to
    the sheet end — otherwise the new task lands AFTER the done block and breaks the two-block rule.
    Apply the same field mapping as `sync_to_sheets` (B truncate→F, owner→Team nick, D=10% default,
    E=+7d default).
