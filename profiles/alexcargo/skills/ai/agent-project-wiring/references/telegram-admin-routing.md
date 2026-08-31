# Telegram bot: admin vs client routing by chat_id (stdlib-only)

## Pattern (used in richard_bot.py)
Two system prompts, selected at request time by whether the sender's `chat_id`
is in an admin allowlist env var (`RICHARD_ADMIN_IDS`, comma-separated).

```python
RICHARD_SYSTEM = "You are Richard Marlowe, Navo sales agent... (client/sales mode)"
RICHARD_ADMIN_SYSTEM = ("You are the OPERATIONS CONSOLE for Richard Marlowe, "
    "talking to Stefan, the project admin. NOT client mode. Help build/audit "
    "Richard; be concise and technical; if a non-admin reaches this console, refuse.")

def bot_loop():
    admin_ids = [x.strip() for x in os.environ.get("RICHARD_ADMIN_IDS","").split(",") if x.strip()]
    ...
    is_admin = str(chat_id) in admin_ids
    system = RICHARD_ADMIN_SYSTEM if is_admin else RICHARD_SYSTEM
    reply = run_agent(text, system=system)
```

## Why it matters
- Deep file/code edits still happen in the Hermes desktop chat (orchestrator
  has the tools); the Telegram bot only surfaces status + accepts notes in admin mode.
- This split lets ONE bot serve both "talk to Richard the salesman" (clients)
  and "talk to the build console" (Stefan) without two bots.

## Env vars the bot needs
TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID (optional lock to one chat),
RICHARD_ADMIN_IDS, NOUS_API_KEY (LLM), NAVO_API_KEY (product API).

## Gotcha
- Detect admin by the REAL constant substring (e.g. `RICHARD_ADMIN_SYSTEM[:25]`),
  not a hand-typed string — a typo in the test mock silently mis-routes.
- Telegram long-polling via urllib: `getUpdates` with `timeout=30`, bump offset
  by `update_id + 1`, skip non-message updates.