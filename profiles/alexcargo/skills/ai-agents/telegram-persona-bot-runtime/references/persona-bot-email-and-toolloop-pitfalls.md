# Persona Bot Production Pitfalls & Fixes (Telegram, Email, Tool Calling)

This reference documents verified production pitfalls and exact fixes discovered during self-hosted persona bot operations (e.g. Richard Marlowe / Alistair).

---

## 1. OpenAI Tool Calling `null` Content Normalization (400 Bad Request)

### Symptom
When an OpenAI model (`gpt-4o-mini`) generates `tool_calls`, `choice.content` is `None` (JSON `null`). When appending `choice` back to `messages` for subsequent turns in the tool loop, sending `"content": null` throws:
`HTTP Error 400 Bad Request: Invalid type for 'messages[1].content': expected a string, given null.`

### Root Cause & Fix
The choice dictionary must be normalized before being appended to `messages`.

```python
choice = resp["choices"][0]["message"]

# NORMALIZE CONTENT
msg_to_append = {
    "role": choice.get("role", "assistant"),
    "content": choice.get("content") or ""
}
if choice.get("tool_calls"):
    msg_to_append["tool_calls"] = choice["tool_calls"]

messages.append(msg_to_append)
```

**CRITICAL:** This normalization MUST be applied both on the initial tool call AND inside the `while choice.get("tool_calls")` loop!

---

## 2. Missing `_TypingTicker` Definition (NameError)

### Symptom
When tested directly without `token`/`chat_id`, typing ticker is skipped. But when invoked from Telegram bot loop with `token` & `chat_id`, missing `_TypingTicker` throws:
`NameError: name '_TypingTicker' is not defined`
dropping into `except Exception` and returning fallback stub text (`"Richard here — briefly lost the line..."`).

### Fix
Ensure `_TypingTicker` class is defined ABOVE `run_agent()`!

---

## 3. Background Process Environment Variable Mismatch

### Symptom
`run_agent()` works fine when tested via `terminal` because terminal inherits host shell env vars (e.g. `OPENAI_API_KEY`), BUT fails silently when executed as a background process (`pythonw.exe` / `bot_watchdog.py`) because `.env.local` was missing the API keys.

### Fix
`_load_env()` in persona bot code MUST load host Hermes `.env` (`C:\Users\Stefan\AppData\Local\hermes\.env`) FIRST before loading local `.env.local`.

---

## 4. Fast-Path Command Interception (Human-in-the-Loop Approval)

### Symptom
When a user replies "Отправляй" or "Да" in Telegram to approve a draft, passing "Отправляй" alone to the LLM without passing the stored draft context causes the LLM to hallucinate or ask "What shall I send?".

### Fix
Fast-path intercept approval triggers ("Отправляй", "Да", "Ок", "Send") at the bot loop level BEFORE calling LLM.
- Check if a pending draft exists in `drafts/latest_draft.json`.
- Immediately execute `send_email_direct()`.
- Notify the user in Telegram: `🚀 ПИСЬМО УСПЕШНО ОТПРАВЛЕНО КЛИЕНТУ!`.

---

## 5. MS Graph Email Polling & `isRead` Filter Gotcha

### Symptom
Filtering inbox messages on `$filter=isRead eq false` misses incoming emails if the user opens Outlook Web App in their browser (which automatically marks unread emails as `isRead = true`).

### Fix
Fetch recent inbox messages by date (`$orderby=receivedDateTime desc&$top=10`), ignoring `isRead`, and track processed message IDs in a `seen_msg_ids` set / file to guarantee zero missed emails.

---

## 6. Email Threading & Quoted History Placement

### Symptom
Using `m.get("bodyPreview")` (a 255-char snippet) truncates accumulated thread history. And placing the corporate signature AFTER `quoted_html` puts the signature at the bottom of the entire email chain instead of right below the sender's reply text.

### Fix
- Extract full HTML body `msg.get("body", {}).get("content")` instead of `bodyPreview`.
- Place corporate HTML signature IMMEDIATELY below agent's reply text and ABOVE `quoted_html`.
- Set `In-Reply-To` and `References` headers with `Re:` in subject to preserve conversation threading.
