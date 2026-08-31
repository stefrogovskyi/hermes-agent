# Email Threading, Signature Placement, and Approval Intercept Guide

## 1. RFC Email Threading Headers
To group an outbound email reply into the exact same thread/conversation in Gmail, Outlook, Apple Mail, and mobile clients:
- **`In-Reply-To`**: Set to the exact `<internetMessageId>` or `Message-ID` of the customer's email.
- **`References`**: Set to `<internetMessageId>`.
- **`Reply-To`**: Always set `Reply-To: Agent Name <agent@domain.com>`. This prevents Gmail/Outlook from filling the user's own email when clicking "Reply".
- **`Subject`**: Prefix with `Re: ` (e.g. `Re: Inquiry about Pricing`).

## 2. HTML Body Ordering & Full History (`body` vs `bodyPreview`)
- **Body Ordering:**
  1. Agent's Reply Text
  2. Corporate HTML Signature (placed IMMEDIATELY below the reply, ABOVE quoted history)
  3. Quoted Customer Email History (`<div class="gmail_quote">--- Исходное сообщение --- ... </div>`)
- **Full History Preservation:** `bodyPreview` from Graph API is only a 255-char teaser. Always extract `msg.get("body", {}).get("content")` (the full HTML body) and pass it as `quoted_html` so the complete accumulated conversation history of all previous turns is preserved across every turn.

## 3. Deterministic Approval Intercept
When the user replies to a draft approval notification in Telegram with keywords like `Отправляй`, `Да`, `Ок`, `Send`:
- Intercept the keyword at the bot polling handler level.
- Read the pending draft JSON from disk (`drafts/latest_draft.json`).
- Immediately call `send_email_direct()` with `in_reply_to` and `quoted_html`.
- Do NOT pass "Отправляй" back through the LLM without draft context — execute deterministically to eliminate 400 Bad Request or "Are you sure?" loops.
