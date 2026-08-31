# Email Draft Guardrails & Semantic LLM Health Checks

Captured from the 2026-08-03 session.

## 1. Hard Human-In-The-Loop Approval Guardrail
When an AI sales/support agent (like Richard Marlowe) drafts email replies for human approval:
- **PROBLEM:** If the LLM call during draft generation includes email-sending tools, the model may execute `send_email` *during draft generation*, sending the message to the customer BEFORE asking the human for permission!
- **SOLUTION:** Call the LLM for draft generation **WITHOUT TOOLS** (`tools=None`). The LLM literally lacks the capability to execute tool calls, forcing it to return text only.
- **DETERMINISTIC APPROVAL:** Intercept human approval commands (`"Отправляй"`, `"Да"`, `"Ок"`) at the bot handler level. Upon detecting approval, load the saved draft JSON and execute `remail.send_email_direct()` deterministically.

## 2. Full Conversation Threading & Signature Placement
- **`bodyPreview` vs `body`:** Microsoft Graph API `bodyPreview` is a 255-character plain text teaser that strips history. Always fetch `msg.get("body", {}).get("content")` to preserve full multi-turn conversation history.
- **Block Order:**
  1. Reply Text (New message)
  2. Corporate HTML Signature (`https://bit.ly/4hLg86T`, `Tahoma 10pt`, `#0000FF` blue links)
  3. Quoted History (`--- Исходное сообщение ---` containing full previous emails)
- **RFC Threading Headers:** Always set `In-Reply-To` and `References` headers and prefix the subject with `Re:`.

## 3. Real Semantic LLM Health Checks (No False Positives)
- **PROBLEM:** Testing bots via `psutil.pid_exists(pid)` is a false-positive trap. An OS process can be alive while returning template/stencil errors (e.g. *"LLM key not connected"*) due to dead model endpoints (`403 Forbidden`).
- **SOLUTION:** Watchdogs must execute a **Real Semantic LLM Test** (`run_agent("ping test")`) that inspects actual text generation output.
- **RECOVERY:** If the output contains stencil error strings or times out (>15s), the watchdog automatically heals API keys in `.env.local` and restarts the bot silently via `pythonw.exe`.
