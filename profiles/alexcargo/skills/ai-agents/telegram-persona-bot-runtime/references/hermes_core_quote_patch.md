# Make Hermes itself see Telegram `message.quote` (quoted/selected fragment)

## Why
Hermes is also a Telegram bot. `plugins/platforms/telegram/adapter.py` already extracts
`message.quote` into `reply_to_text` for the reply-context feature — but that value lands in the
message **metadata**, not in `event.text`. So the assistant model received only the user's question,
never the highlighted fragment. The owner rejected "paste it again" as a workaround: *"you work as
a Telegram bot, you handle all Telegram entities; if Richard got this skill, give it to yourself."*

## Fix (patch `adapter.py`)
File: `%LOCALAPPDATA%\hermes\hermes-agent\plugins\platforms\telegram\adapter.py`
Function: `_handle_text_message` — right AFTER this line:
```python
        event.text = self._clean_bot_trigger_text(event.text)
```
insert:
```python
        # Hermes Stevenson: pull the SELECTED/QUOTED fragment (message.quote) into
        # the text so the assistant sees exactly what the user is replying to.
        _q = getattr(msg, "quote", None)
        _qtext = getattr(_q, "text", None) if _q is not None else None
        if _qtext:
            event.text = (
                "%s\n[ПОЛЬЗОВАТЕЛЬ ПРОЦИТИРОВАЛ ФРАГМЕНТ:\n«%s»\n"
                "— отвечай ПО СУТИ этого фрагмента.]\n" % (event.text, _qtext)
            )
```
Note: `msg` is the local var name for the effective message in that function (`msg =
self._effective_update_message(update)`). If a future refactor renames it, match on
`event.text = self._clean_bot_trigger_text(event.text)` and grab the message object in scope.

## Verify (before declaring done)
1. `python -m py_compile <path to adapter.py>` — must be SYNTAX OK.
2. **Restart the Hermes gateway** (close + reopen the desktop app, or `hermes restart`) so the
   module reloads. The patch does nothing until reload.
3. Ask the owner to quote any phrase from your last message and ask a question. The assistant must
   see the marker `[ПОЛЬЗОВАТЕЛЬ ПРОЦИТИРОВАЛ ФРАГМЕНТ: ...]` and answer on that fragment. If it
   still only sees the question → gateway wasn't reloaded, or the patch didn't land.

## Maintainer caveat (IMPORTANT)
`adapter.py` is **Hermes core**, not a user skill. A Hermes update (`hermes update` / desktop
auto-update) OVERWRITES this patch silently — quoted fragments stop arriving again, with no error.
- Re-apply this patch after every Hermes update.
- Better long-term: upstream a PR so the fix lives in core permanently. The change is small and
  clearly beneficial (the reply-context code already proves `quote` is the desired signal).
- Until the patch is live + gateway reloaded, the only safe fallback is: ask the owner to paste the
  quoted text; never guess or claim to see the quote.
