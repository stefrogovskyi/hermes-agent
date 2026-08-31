# Multi-User RBAC & Telegram Security Protocols

When exposing Hermes sub-agents to team members or public Telegram channels while preserving owner isolation:

## 1. Owner & Admin Protection (RBAC)
- **Hard Rule:** Only the designated master owner (`330656040` for Stefan) may have administrative access (`allow_admin_from`) to execute `/new`, change system parameters, or bind the home chat.
- **Home Channel Lock:** Explicitly set `platforms.telegram.home_channel` to the owner's chat ID (`chat_id: "330656040"`) so "Set Home Chat" prompts are never shown to non-owner users.

```yaml
platforms:
  telegram:
    enabled: true
    require_mention: true
    home_channel:
      platform: telegram
      chat_id: "330656040"
    allow_admin_from:
      - "330656040"
    allow_from:
      - "*"
      - "330656040"
    group_allow_from:
      - "*"
```

## 2. YAML vs JSON Array Pitfall in `allow_from`
- **Pitfall:** Serializing `allow_from` as a quoted string of JSON (`'["330656040", "*"]'`) causes the Telegram adapter intake prefilter to fail string parsing, logging `[Telegram] Blocked unauthorized user <ID> in chat <ID>`.
- **Fix:** Always format `allow_from` and `group_allow_from` as native YAML sequence lists.

## 3. GitHub Push Protection & Secret Scanning Unblock
- **Pitfall:** `git push` rejection `GH013: Repository rule violations found ... Push cannot contain secrets` when historical commits in sub-agent memories contain redacted-like tokens or test strings.
- **Fix:** Use GitHub unblock URLs (`/security/secret-scanning/unblock-secret/<ID>`) to allow false positives / revoked keys before re-pushing, and enforce `.gitignore` on all `.env`, `*.session`, and `memory_v2/*.txt` files.

## 4. Fallback Priority Chain Configuration
- Place free 1M-context models (e.g. `stealth/ox-alpha:free` on OpenRouter, `nous`, `nvidia`) at the top of `fallback_providers`.
- Ensure `request_timeout_seconds: 30` and `compression.threshold: 0.15–0.25` are set across all profiles to prevent runaway session token bloat (>600k characters).
