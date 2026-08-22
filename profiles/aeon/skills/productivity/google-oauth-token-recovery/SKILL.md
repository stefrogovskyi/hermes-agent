---
name: google-oauth-token-recovery
description: "Recover revoked/expired Google OAuth tokens; re-auth flow."
version: 1.0.0
author: Hermes (session-derived)
license: MIT
category: productivity
tags:
  - google
  - oauth
  - token
  - drive
  - contacts
metadata:
  hermes:
    tags: [google, oauth, token, drive, contacts]
    related_skills: [google-workspace]
---

# Google OAuth Token Recovery

## When to Use

`TOKEN_REVOKED` / `invalid_grant` from any Google integration, the user says they changed the OAuth app (e.g. "made the token permanent"), or a `403 accessNotConfigured` appears after re-auth. Complements the bundled `google-workspace` skill's setup flow with hard-won lifecycle facts.

## Key facts (verified live 2026-08)

1. **Testing → Production switch kills old tokens.** Refresh tokens issued while the OAuth app was in *Testing* expire in 7 days AND are invalidated when the app moves to *Production*. Moving to Production does NOT revive anything — one final re-authorization is required, after which the refresh token is genuinely permanent.
2. **PKCE code_verifier must be persisted.** If `--auth-url` and `--auth-code` run in separate processes (always true for chat-driven flows), save `flow.code_verifier` to disk at URL-generation time and restore it before `fetch_token`, or the exchange dies with `invalid_grant: Missing code verifier` and the one-time code is burned — forcing the user to click through consent again. Working implementation: `/opt/hermes/scripts/google_reauth.py` (Stefan's VPS).
3. **Scope union on re-auth.** When re-authorizing, request the union of every scope any consumer uses (Workspace scopes + `youtube` + `youtube.force-ssl` on Stefan's stack — the evening YouTube cron shares this token). Otherwise a "successful" re-auth silently breaks a neighboring integration.
4. **`HERMES_HOME` matters.** Token lives at `$HERMES_HOME/google_token.json` (`/opt/hermes/` on the VPS, NOT `~/.hermes/`). A "file not found" during checks usually means the env var wasn't exported, not a missing token.
5. **Enabled scopes ≠ enabled APIs.** After re-auth, each Google API must also be enabled in the Cloud project. `403 accessNotConfigured` names the exact enable-URL — send those links to the user; no new token needed afterwards, retry works within a minute.

## Verification sequence after any re-auth

```bash
export HERMES_HOME=/opt/hermes
python3 $HERMES_HOME/skills/productivity/google-workspace/scripts/setup.py --check   # expect AUTHENTICATED
# then one real call per service the user cares about (drive search, gmail search,
# calendar list, contacts list) — report a per-service ✅/⚠️ table, not just "check passed".
```

## Contacts search pitfall

`contacts list` (People API `connections`) caps around 1000 results — a surname search over the list output misses people. Use `people:searchContacts` instead: send one empty-query request first (cache warmup, required by the API), sleep ~1s, then query each spelling variant (Cyrillic + Latin: «Коваленко» and "Kovalenko") and dedupe by `resourceName`.
