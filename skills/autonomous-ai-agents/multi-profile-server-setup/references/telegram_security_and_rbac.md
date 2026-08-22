# Telegram Security, RBAC & Bot Governance in Multi-Profile Clusters

## 1. Owner & Admin RBAC vs Open Team Consultations
When deploying sub-agent profiles (e.g. `harrison`, `richard`, `callum`) meant to consult team members while preserving owner sovereignty:

```yaml
# config.yaml (Profile level)
owner_id: "330656040" # Master owner ID

platforms:
  telegram:
    enabled: true
    require_mention: true
    # Hardcode home_channel to owner to prevent 'Set Home Chat' hijacking prompts
    home_channel:
      platform: telegram
      chat_id: "330656040"
    # Strict admin access: slash commands (/new, /set, config changes)
    allow_admin_from:
      - "330656040"
    # Open dialogue access: team members can talk/consult without pairing blockers
    allow_from:
      - "*"
      - "330656040"
    group_allow_from:
      - "*"
```

## 2. Preventing 'Set Home Chat' Takeover
- **Issue:** When a non-owner interacts with an unconfigured bot, the UI may prompt 'Set Home Chat'. If clicked by an employee, background alerts and ownership route to that employee.
- **Fix:** Always explicitly define `home_channel.chat_id: "<OWNER_ID>"` in `config.yaml` and instruct the agent's `SOUL.md` that governance and configuration remain exclusive to the owner.

## 3. GitHub Push Protection & Secret Scanning Unblock
- **Issue:** Fine-grained GitHub tokens with full write access will still fail with `403 / GH013: Repository rule violations (Push cannot contain secrets)` if older commits in the git history match secret signatures (Airtable PATs, Vercel tokens, OAuth client secrets).
- **Fix:** Follow the generated secret-unblock URLs on GitHub (`https://github.com/<user>/<repo>/security/secret-scanning/unblock-secret/<ID>`) and allow false positives/test keys before pushing.
