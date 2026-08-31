# Message batching (debounce) — one coherent reply per chat

## Why
The owner's bar: when a user sends SEVERAL messages in a row, the bot must assemble them
into ONE connected reply, not answer each separately (which looks fragmented and ignores
cross-message context). Symptom that triggered this: owner sent two messages back-to-back
in a group; the bot replied to each independently — "he doesn't hold context."

## Pattern (verified live, both Richard + Alistair this session)
1. Declare `pending = {}` right before the `while True:` poll loop.
2. Inside the per-update loop, STOP calling `run_agent` / sending. Instead append each
   eligible message to `pending[chat_id]` (a list of dicts carrying `full_text`,
   `memory_key`, `group_id`/chat id, `voice_in`, `voice_req`, and `system` for Richard's
   `run_agent(system=...)` variant). Keep fast-command branches (`/help`, `/sync`) as-is —
   they still reply immediately.
3. AFTER the `for upd in updates...` loop (still inside the try), do the debounce + flush:
   - If `pending` is non-empty, `time.sleep(3.5)` to let the user finish typing more.
   - One short follow-up poll: `tg_request("getUpdates", token, {"offset": offset,
     "timeout": 3}, timeout=10)` — fold any extra same-chat messages into `pending`.
   - FLUSH: for each `chat_id`, if 1 message → send as-is; if >1 → join with `\n---\n`
     and prepend a directive "Пользователь прислал N сообщений подряд. Ответь ОДНИМ
     связным ответом, учитывая ВСЮ переписку ниже как единый контекст:". Call `run_agent`
     ONCE, then send (voice if any item requested voice).
   - `pending.clear()`.

## Key points / pitfalls
- The debounce window (3.5s) is a tradeoff: too short → misses the 2nd message; too long →
  user waits. 3.5s fit this owner's typing rhythm; tune if they complain of lag.
- `voice_in`/`voice_req` must be computed BEFORE appending (in Richard's case they were
  originally computed after `run_agent`; move them up so the dict has them).
- The extra poll uses `timeout: 3` (short) — it only exists to catch the tail of a burst,
  not to replace the main 30s long-poll.
- Keep the SAME `memory_key` as the first item (per-user/group memory still applies).
- Fast commands (`/sync`, `/help`) MUST stay outside batching (immediate reply) or the bot
  feels frozen after a slash command.

## Richard variant (run_agent takes system=)
```python
pending = {}
while True:
    try:
        updates = tg_request("getUpdates", token, {"offset": offset, "timeout": 30}, timeout=40)
        for upd in updates.get("result", []):
            offset = upd["update_id"] + 1
            msg = upd.get("message")
            if not msg: continue
            chat = msg["chat"]; chat_id = chat["id"]
            chat_type = chat.get("type", "private")
            # ... media/quote/filter pipeline as before ...
            # after skip-checks pass:
            full_text = (media_hint + text + reply_ctx) if (media_hint or reply_ctx) else text
            _voice_in = bool(msg.get("voice") or msg.get("audio"))
            _voice_req = bool(VOICE_REQ_RE.search(text))
            pending.setdefault(chat_id, []).append({
                "full_text": full_text, "memory_key": memory_key,
                "group_id": group_id, "system": system,
                "voice_in": _voice_in, "voice_req": _voice_req, "tag": tag,
            })
        # ===== DEBOUNCE + FLUSH =====
        if pending:
            time.sleep(3.5)
            try:
                extra = tg_request("getUpdates", token, {"offset": offset, "timeout": 3}, timeout=10)
                for _upd in extra.get("result", []):
                    offset = _upd["update_id"] + 1
                    _m = _upd.get("message")
                    if not _m: continue
                    _cid = _m["chat"]["id"]
                    _t = (_m.get("text") or "").strip()
                    if not _t: continue
                    pending.setdefault(_cid, []).append({
                        "full_text": _t,
                        "memory_key": _key_for(_m["chat"].get("type","private"), _cid, _m.get("from",{}).get("id")),
                        "group_id": _cid if _m["chat"].get("type")!="private" else None,
                        "system": RICHARD_SYSTEM,
                        "voice_in": bool(_m.get("voice") or _m.get("audio")),
                        "voice_req": bool(VOICE_REQ_RE.search(_t)), "tag": "[debounce]",
                    })
            except Exception as e:
                print("[Richard] debounce poll err: %s" % e)
            for _cid, _items in pending.items():
                _texts = [it["full_text"] for it in _items]
                if len(_texts) == 1:
                    _batch = _texts[0]
                else:
                    _batch = ("[Пользователь прислал %d сообщений подряд. Ответь ОДНИМ "
                              "связным ответом, учитывая ВСЮ переписку ниже как единый "
                              "контекст:]\n" % len(_texts)) + ("\n---\n".join(_texts))
                _it = _items[0]
                try:
                    reply = run_agent(_batch, system=_it["system"], token=token,
                                      chat_id=_cid, memory_key=_it["memory_key"],
                                      group_id=_it["group_id"])
                except Exception as e:
                    print("[Richard] agent error: %s" % e)
                    reply = ("Richard here — briefly lost the line to the desk. "
                             "One moment, try that again?")
                if (_it["voice_in"] or _it["voice_req"]) and openai_key():
                    tg_send_voice(token, _cid, reply or "(no response)")
                else:
                    tg_send_message(token, _cid, reply or "(no response)")
            pending.clear()
    except Exception as e:
        print("[Richard] poll error: %s" % e); time.sleep(5)
```

## Alistair variant (run_agent has no system=)
Same structure; the flush call is `run_agent(_batch, token=token, chat_id=_cid,
memory_key=_it["memory_key"])` and the dict omits `"system"`. Fast branches `/help`
and `/sync` stay immediate (they `continue` before reaching the append).
