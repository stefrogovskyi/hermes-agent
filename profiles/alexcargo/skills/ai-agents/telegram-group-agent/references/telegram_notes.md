# Telegram Group Agent — Notes & Gotchas

## Running Python on this Windows host
- `python3` resolves to a Microsoft Store stub → error "Python was not found; run
  without arguments to install from the Microsoft Store". Do NOT use `python3`.
- Use the Hermes venv python directly:
  `C:\Users\Stefan\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe`
  (forward slashes or quoted backslashes both work in bash/git-bash).
- Installing packages: `uv pip install --python <path>` failed to recognize the
  venv path. Use `python.exe -m pip install <pkg>` instead (pip is in the venv).
- For `py_compile` / running a script with a space in the path, pass the path in
  double quotes and use forward slashes: `"C:/Users/.../telegram_group_sweep.py"`.

## getUpdates cursor details
- `update_id` is a monotonically increasing integer, GLOBAL per bot (spans all
  chats the bot is in). One cursor (`last_update_id`) therefore covers every chat.
- `offset` is "first update_id to return" — so pass `last_update_id + 1`.
- Always page: a single `getUpdates` returns up to `limit` (100) results. Loop
  until an empty result or a batch smaller than 100, else you drop messages.
- `timeout=0` = short poll (returns immediately). Good for batch cron runs.
- Updates with no `message`/`edited_message` key (callback queries, inline
  queries, channel posts) must be skipped — they have no chat text.

## Privacy mode (BotFather)
- Default bot privacy = bot only sees messages that @mention it or are replies.
- For full-group context: BotFather → `/setprivacy` → **Turn off**.
- Privacy is per-bot, not per-chat.

## Token scope
- A token is per-bot. Two bots = two tokens = two independent update queues, no
  conflict. The same token used by two consumers (e.g. a realtime gateway AND a
  poller) collides — only one sees the updates.
- Confirm a token works: `GET https://api.telegram.org/bot<TOKEN>/getMe` →
  returns `{"ok":true,"result":{"id":...,"username":"richnavobot",...}}`.
