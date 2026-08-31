# Telegram Persona Bot Runtime — Hardened Production Fixes

## 1. Host `.env` Loading Priority
Background daemon processes (`pythonw.exe` spawned via `bot_watchdog.py`) do NOT inherit terminal shell env vars. The bot MUST explicitly load `C:\Users\Stefan\AppData\Local\hermes\.env` BEFORE loading its local `.env.local` at startup:
```python
def _load_env():
    host_env = r"C:\Users\Stefan\AppData\Local\hermes\.env"
    if os.path.exists(host_env):
        with open(host_env, encoding="utf-8", errors="ignore") as fh:
            for line in fh:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    k, v = k.strip(), v.strip().strip('"').strip("'")
                    if k:
                        os.environ[k] = v
    # Then load local .env.local
```

## 2. OpenAI Tool Call `content: null` Normalization (Prevents HTTP 400 Crashes)
When OpenAI `gpt-4o-mini` returns a tool call choice with `"content": None`, appending `choice` directly back to `messages` for subsequent tool loop iterations causes OpenAI to reject the payload with `HTTP Error 400: Invalid type for messages[N].content: expected a string, given null`.
**Fix:** Always normalize `choice["content"]` to `""` before appending to `messages`:
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

## 3. Deterministic Human-in-the-Loop Approval Interceptor
When a user replies "Отправляй", "Да", "Ок", "Send" in Telegram to approve a pending email draft, do NOT rely on LLM reasoning to guess the draft context from disk. Intercept approval triggers at the bot polling level before calling the LLM:
```python
def _check_and_execute_draft_approval(user_text, chat_id, token):
    text_clean = user_text.lower().strip()
    triggers = ["отправляй", "отправь", "да", "ок", "ok", "send"]
    if not any(text_clean == t or text_clean.startswith(t + " ") for t in triggers):
        return False
    # Load latest pending JSON draft from drafts_dir, execute send_email_direct(), delete draft, notify Telegram!
    return True
```

## 4. MS Graph Email Threading & Full Accumulated History
- **Do NOT filter strictly by `isRead eq false`:** Outlook Web App auto-marks incoming emails as read within 1s. Filter by `$orderby=receivedDateTime desc` and track processed IDs in memory/disk.
- **Do NOT use `bodyPreview`:** `bodyPreview` is a 255-char plain text teaser that strips all thread history. Use `msg.get("body", {}).get("content")` to retain the complete 8,000+ char accumulated conversation thread.
- **Place HTML Signature ABOVE Quoted History:** Format replies as `body_html + official_signature_html + quoted_history_html` so the corporate signature sits immediately under the agent's new text and above the quoted thread.
