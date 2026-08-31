# 409 footgun #3 — debounce double-getUpdates + the manual-probe trap (2026-07-28)

## Footgun: debounce double-getUpdates
A bot whose MAIN loop already runs `getUpdates(timeout=30)` must NOT also call
`getUpdates(timeout=3)` inside a debounce window (the "catch dozapisannye messages"
block). Two concurrent long-polls on one token -> 409 Conflict -> bot silently
drops the line ("not replying in PM").

FIX: delete the inner getUpdates. The main loop already drains updates with the
correct offset; dozapisy arrive on the next tick (sleep 3.5s, then FLUSH). Verified fix
in Richard/Alistair/Ben: richard_bot.py (was ~828), alistair_bot.py (~650),
ben_jett_bot.py (~652) - remove the `try: extra = tg_request("getUpdates", ...)` block,
keep time.sleep(3.5) + FLUSH.

Log signature: repeated `http attempt N failed: HTTP Error 409: Conflict` /
`poll error: HTTP Error 409: Conflict` while process alive and CPU low.

## DIAGNOSTIC RULE - never call getUpdates manually on a live bot
During debugging, do NOT run your own getUpdates (even offset=-1) against the bot's
token to "check the queue". It (1) consumes the update the bot should process, and
(2) collides with the bot's own poll -> 409. Real case 2026-07-28: Richard looked
"not replying in PM" because the assistant's own diagnostic getUpdates ate Stefan's
message. Check liveness by reading the bot's log file, or send a test msg and watch the
log. To prove delivery without disturbing the bot, use getMe - never getUpdates.

After any manual getUpdates probe, restart the bot so it re-syncs from current server
offset (lost messages won't return, but new ones flow).
