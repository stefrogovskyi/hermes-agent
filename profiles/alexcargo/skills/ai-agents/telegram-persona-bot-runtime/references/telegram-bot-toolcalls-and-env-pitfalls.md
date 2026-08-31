# Telegram Persona Bot Runtime — Key Debugging & Execution Lessons

## 1. Tool Call `content: null` Normalization (HTTP 400 Bad Request)
When calling OpenAI models with tool-calling capabilities (`gpt-4o-mini`, etc.), OpenAI returns message choices where `choice.content` is `None` (null) if tool calls are present.
If this message is appended directly to `messages` and passed back to OpenAI in the next turn of the tool-calling loop, OpenAI throws `HTTP Error 400 Bad Request: Invalid type for messages[N].content: expected a string, given null`.

**Fix:** ALWAYS normalize `choice.content` before appending to `messages`:
```python
msg_to_append = {
    "role": choice.get("role", "assistant"),
    "content": choice.get("content") or ""
}
if choice.get("tool_calls"):
    msg_to_append["tool_calls"] = choice["tool_calls"]
messages.append(msg_to_append)
```

## 2. Background Process Environment Variable Scope (`pythonw.exe`)
Background processes spawned by `bot_watchdog.py` or system startup do NOT inherit terminal environment variables.
If `.env.local` inside the bot directory is missing keys, the background process fails with `HTTP Error 401: Unauthorized` or missing credentials, even while running scripts directly in the terminal works fine.

**Fix:** `_load_env()` in `richard_bot.py` / bot script MUST explicitly load the host's main `.env` file (`C:\Users\Stefan\AppData\Local\hermes\.env` or `~/.env`) BEFORE loading local `.env.local`.

## 3. Microsoft 365 Exchange Mail Integration (Graph API vs Basic Auth IMAP)
In Microsoft 365 Exchange Online, basic authentication for IMAP is blocked tenant-wide by Microsoft Entra ID Security Defaults (`AUTHENTICATE failed`), even if IMAP is enabled in Microsoft 365 Admin Center under User Mail Settings.

**Fix:** Use Microsoft Graph API (`https://graph.microsoft.com/v1.0/users/<email>/mailFolders/inbox/messages`) with OAuth2 `client_credentials` grant and Application permission (`Mail.Read` + Admin Consent) for 100% reliable background email monitoring.
