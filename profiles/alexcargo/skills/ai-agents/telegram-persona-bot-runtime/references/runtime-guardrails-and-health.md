# Runtime Guardrails, Threading & Semantic Health Checks

## 1. Deterministic Approval Interceptor
When a user sends approval triggers (`"отправляй"`, `"да"`, `"ок"`, `"send"`):
- Intercept the trigger **deterministically** at the bot handler level before calling LLM reasoning.
- Load the pending draft JSON from `drafts/draft_latest.json`.
- Execute `send_email_direct()`, mark the draft as `APPROVED_AND_SENT`, and reply to Telegram immediately.

## 2. Hard Unbreakable Guardrail during Draft Generation
When a background poller composes a draft for user confirmation:
- Invoke LLM with `tools=None` (no tool definitions).
- Removing tool definitions physically prevents the LLM from executing auto-send side-effects before user confirmation.

## 3. Full Accumulated RFC Email Threading
- Extract full HTML content `msg.get("body", {}).get("content")` instead of `bodyPreview` (255-char teaser).
- Structure email replies: **Response ➔ Corporate Signature ➔ Quoted History (`--- Исходное сообщение ---`)**.
- Preserve `In-Reply-To` and `References` headers across draft saving and sending.

## 4. Real Semantic LLM Health Checks
- `psutil.pid_exists(pid)` only checks if the Python OS process exists in Task Manager.
- Watchdogs MUST run a **real semantic LLM test** (`run_agent('ping')`) and verify the response is NOT a template/stencil error.
