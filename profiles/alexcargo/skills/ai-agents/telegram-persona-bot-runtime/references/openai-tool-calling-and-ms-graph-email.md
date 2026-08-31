# OpenAI Tool Calling & MS Graph Email Integration Guide for Telegram Persona Bots

## 1. OpenAI Tool Calling `content: null` HTTP 400 Bad Request Fix

When using OpenAI models (`gpt-4o-mini`, `gpt-4o`) with function calling (`tools=[...]`), OpenAI returns `choice["message"]["content"] = None` on tool-calling turns.

If the assistant message object with `"content": None` is appended directly back into `messages` for subsequent tool-execution turns, OpenAI API rejects the payload with:
`HTTP Error 400 Bad Request: Invalid type for messages[N].content: expected a string, given null`

### Fix:
Always normalize `choice["content"]` from `None` to `""` before appending to `messages`:

```python
choice = resp["choices"][0]["message"]
msg_to_append = {
    "role": choice.get("role", "assistant"),
    "content": choice.get("content") or ""
}
if choice.get("tool_calls"):
    msg_to_append["tool_calls"] = choice["tool_calls"]

messages.append(msg_to_append)
```

## 2. History Window Clamping

Clamp memory history retrieval in bot polling loops to `history_get(memory_key)[-10:]`.
Allowing memory arrays to grow unbounded causes stale test chatter to dilute prompt context, causing the agent to repeat old rejections or get stuck in past conversational loops.

## 3. Microsoft 365 Email Integration & Azure App Registration

In Microsoft 365 Exchange Online, basic authentication for IMAP is disabled tenant-wide by Security Defaults.
To read mailbox messages via Graph API (`https://graph.microsoft.com/v1.0/users/{email}/mailFolders/inbox/messages`) using `client_credentials` grant flow:

1. Create Azure App Registration in Azure Portal (`portal.azure.com`).
2. Add **`Application permissions`** (`Mail.Read` / `Mail.ReadWrite`) under Microsoft Graph (DO NOT use Delegated permissions, which return `403 Forbidden / Authorization_RequestDenied`).
3. Click **`Grant admin consent for <Org>`** (1-click as Admin).
4. Use `Directory (tenant) ID`, `Application (client) ID`, and `Client Secret Value` (the `Value` column, NOT the `Secret ID` column).

## 4. Outlook Corporate Signature Rule

When agents compose or reply to emails via Outlook/Office 365, avoid generating custom hardcoded text signatures (e.g. `Agent Name / Title`).
End body text with a simple closing (`Best regards, Richard`), allowing Outlook's native pre-configured signature to attach cleanly.
