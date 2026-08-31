# Google OAuth PKCE Decoupled Exchange & Telegram Streaming Rate Limits

## 1. Google OAuth PKCE Decoupled Exchange Pitfall
- **Symptom:** Exchanging an authorization code in a subsequent turn returns:
  `HTTP Error 400: Bad Request - {"error": "invalid_grant", "error_description": "Missing code verifier."}`
- **Root Cause:** `google_auth_oauthlib.flow.InstalledAppFlow` defaults to PKCE with a randomly generated `code_challenge`. When the user is given the URL in Turn 1 and pastes the redirect URL in Turn 2, the original Python memory state is lost. Posting to `https://oauth2.googleapis.com/token` without the corresponding `code_verifier` fails.
- **Solution:**
  1. Generate explicit `code_verifier` (e.g. `secrets.token_urlsafe(64)`).
  2. Compute `code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode()).digest()).decode().replace('=', '')`.
  3. Save `code_verifier` to disk (e.g. `oauth_verifier.txt` or `google_oauth_pending.json`).
  4. In the exchange turn, read `code_verifier` from disk and include in the token POST payload (`code_verifier: ...`).

## 2. Google Contacts Scope Requirements
- Standard Workspace tokens (`gmail.readonly`, `drive`, `youtube`) do NOT cover Google Contacts / Address Book.
- To access Google Contacts via Google People API (`https://people.googleapis.com/v1/people/me/connections`), the OAuth consent request MUST explicitly include:
  - `https://www.googleapis.com/auth/contacts.readonly` (or `https://www.googleapis.com/auth/contacts`).

## 3. Telegram Live Streaming Flood Control & 1000ms Throttling
- **Symptom:** Streaming agents log `Flood control exceeded. Retry in 9 seconds` during active token output generation.
- **Root Cause:** Rapid `editMessageText` calls on live streams exceed Telegram's rate limit (~1 edit per second).
- **Solution:** Configure `display.streaming_throttle_ms: 1000` in `config.yaml` across all profiles so message edits are spaced by at least 1,000ms.

## 4. Multi-Agent Group Mention Filter & Inflected Aliases
- In group chats, prevent bot cross-talk and chatter by configuring:
  ```yaml
  platforms:
    telegram:
      group_response_mode: mention
      aliases: ["name", "склонение1", "склонение2", "@botname"]
  ```
- Bots respond ONLY when directly @mentioned, reply-quoted, or explicitly named in any grammatical case/language.
