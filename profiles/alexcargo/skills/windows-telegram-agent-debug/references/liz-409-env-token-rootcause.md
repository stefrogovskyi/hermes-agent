# Liz 409 — final root cause (2026-07-27): env-inherited WRONG token

## The bug
`liz_loop.py` main():
```python
token = os.environ.get("TELEGRAM_BOT_TOKEN", "")   # <-- BUG: Hermes env carries HERMES token
if not token:
    # ... fallback to LIZ_DIR/.env.local, then HERMES_HOME/.env
```
Launched from the Hermes environment (scripts/cron/terminal), the process inherited the
HERMES bot token. Liz long-polled the Hermes bot, fighting the gateway → 409 forever.

## Why every earlier hypothesis failed
- Single-instance lock, watchdog removal, 5-min silences, GET vs POST, deleteWebhook,
  `getUpdates?offset=-1`, gateway kill — ALL irrelevant: the conflict was with the
  gateway on the OTHER token.
- Signature: dead Liz → her own token probes clean (180s, 0 conflicts);
  live Liz → 409 ~21s into every poll; exactly 1 process, 1 socket to Telegram.

## The bisect that found it
1. Instrumented `tg_get_updates` to log thread — proved ONE call site.
2. `netstat`-style `Get-NetTCPConnection -OwningProcess` — ONE socket to 443.
3. Bare minimal poller (same uv pythonw, same GET loop, token read straight from
   `.env.local`) ran 150s clean while full bot 409'd → diffed the two → token source.

## The fix (applied)
```python
# NEVER read TELEGRAM_BOT_TOKEN from os.environ
token = ""
for f in (os.path.join(LIZ_DIR, ".env.local"), os.path.join(HERE, ".env.local")):
    ...
log("token source ok, bot id=%s" % token.split(":")[0])   # self-check at startup
```
Also removed HERMES_HOME/.env fallback (that file holds the Hermes token).

## Error-handler that is proven clean
On any poll error: `time.sleep(10)` + retry. No deleteWebhook, no offset=-1.
Ghost long-polls expire on their own in ~35s.

## Verified working state
- Bot: **@lizharperbot** (id 8857115619) — note: NOT "lizharpbot".
- `token source ok, bot id=8857115619` then silence; `agent created for chat 330656040`
  on first real message. 4+ min zero 409.

## Also fixed this session
- Proactive digest thread removed (Stefan forbade unsolicited digests).
- "Liz Bot Watchdog" cronjob removed (double-launcher).
- getUpdates switched to GET with query string (harmless; not the root cause).
