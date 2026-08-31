# Rate-limit recovery pattern (SMTP + MS Graph + API)

## Context
Discovered 2026-08-04 during a Richard Marlowe email integration session.
The bot uses SMTP (via `richard_email.py`) to send emails and MS Graph API
for inbox polling. Both can raise transient 429 / connection-timeout errors.

## Pattern: 3-attempt retry with backoff
```python
for attempt in range(3):
    try:
        server.sendmail(EMAIL_ADDRESS, recipients, msg.as_string())
        smtp_ok = True
        break
    except Exception as e:
        smtp_err = e
        log(f"🔁 Попытка SMTP {attempt+1}/3 не удалась: {e}")
        time.sleep(1)
```

## Key lessons
- HTTP 429 / connection timeouts are transient — a 1-second sleep + retry almost always succeeds.
- Always wrap `sendmail()` in a retry loop in SMTP-based senders, not just at the HTTP layer.
- Log each retry attempt with attempt number and error string so transient failures are visible in logs.
- After 3 failed attempts, surface the *original* error (raise the last seen exception), not a hallucinated success message.
- For HTTP-level APIs, the same pattern applies: retry on 429 with `Retry-After` header or fixed 1–2s backoff.
