# Telegram Group Diagnostics & Troubleshooting Reference

## Common Diagnostic Fallacies
1. **Blaming BotFather `/setprivacy`**:
   - **Pitfall**: When a bot fails to respond to its name in a group, claiming that BotFather `/setprivacy` is enabled without verifying log files.
   - **Reality**: In multi-bot setups, group privacy is usually already disabled. The failure is almost always due to:
     - `require_mention: true` in `config.yaml` gating unmentioned text.
     - The bot not having been added to the chat yet (`channel_directory.json` missing the chat entry).
     - Filtering in the platform adapter or missing trigger keywords.

## Diagnostic Steps for Unhandled Group Messages
1. **Check `channel_directory.json`**:
   - Verify whether the chat ID (e.g. `-5305384342`) appears in `profiles/<agent>/channel_directory.json`.
   - If missing, the gateway has not yet registered the bot's presence in that chat.

2. **Inspect `config.yaml`**:
   - Look for `require_mention: true|false`.
   - Look for `group_trigger_keywords` list.
   - Look for `group_allow_from` / `allowed_chats`.

3. **Grep Gateway Logs**:
   - Search `profiles/<agent>/logs/gateway.log` for the chat ID or message text.
   - Look for adapter log lines indicating `Blocked unauthorized user` or `require_mention=true, no mention pattern matched`.
