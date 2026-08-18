# Case: Richard Marlowe MS Graph Email Integration & Human-in-the-Loop Draft Approval

## Summary
- **Date**: 2026-08-03
- **Domain**: agent_club / business
- **Context**: Connecting Richard Marlowe (`rich@navo24.com`) to MS Outlook via MS Graph API for outreach and customer email management.

## Symptom / Challenge
- Previous setup attempted SMTP/IMAP or standard email sending without strict guardrails, risking unintended email dispatch or broken conversation threads.
- Personal email leaks occurred when `Reply-To` headers were misconfigured.

## Solution & Technical Architecture
1. **MS Graph API Authentication**:
   - Azure App registration configured with Tenant ID `dc47c5b1-313f-47eb-ab6f-5f0716f400b5`, Client ID `807fed17-45a8-4c7c-9a28-5997bbd30970`, Client Secret.
   - Token refresh script handles OAuth token renewal (`save_richard_ms_graph.py`).
2. **Strict Human-in-the-Loop (HITL) Guardrail**:
   - **Rule from Stefan**: 0 auto-sends. When an incoming email arrives or an email outreach is triggered, Richard MUST generate a draft, send it to Stefan in Telegram DM, and wait for explicit approval ("Send" / "Approve") before dispatching.
   - Enforced hard guardrail in poller (`fix_richard_draft_hard_guardrail.py`).
3. **Email Threading & Headers**:
   - Poller runs every 15s (`MS Graph poller 15s`).
   - Preserves conversation threading headers (`In-Reply-To` and `References`).
   - Fixed `Reply-To` header to ensure customer replies route back to `rich@navo24.com` rather than Stefan's personal email.
4. **Branded HTML Signature**:
   - Configured official HTML signature with Tahoma font (10pt, #000000) and Navo24 branding.

## Verification & Key Lesson
- Never allow sales/customer-facing agents to auto-send emails without human approval. Send draft to Telegram -> wait for explicit user confirmation -> dispatch via API.
