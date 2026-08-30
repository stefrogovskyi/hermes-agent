# Multi-Profile RBAC & Security Guardrails Reference

## 1. Telegram Owner & Access Isolation (RBAC)

When creating sub-agents with public access for company employees, prevent accidental "Set Home Chat" overrides or administrative takeover by strictly separating `owner_id`, `home_channel`, `allow_admin_from`, and `allow_from`.

```yaml
# 1. Primary Owner ID
owner_id: "330656040"

platforms:
  telegram:
    enabled: true
    require_mention: true
    # Home channel bound strictly to Owner
    home_channel:
      platform: telegram
      chat_id: "330656040"
    # Admin commands (/new, /set, system reconfig) restricted to Owner
    allow_admin_from:
      - "330656040"
    # General queries open to team
    allow_from:
      - "*"
      - "330656040"
    group_allow_from:
      - "*"
```

## 2. Model Streaming Interruption & Auto-Compression Safeguards

- **Gemini 503 Spike Mitigation:** Always maintain a high-context 1st-tier fallback (such as `stealth/ox-alpha` with 1M context or `nous/laguna-s-2.1:free`) ahead of paid endpoints.
- **Context Bloat Reduction:** When sub-agents run heavy outreach/logging loops, configure `compression.threshold: 0.15` and `compression.target_ratio: 0.15` to automatically compact 500k+ token sessions before stream drops occur.

## 3. Serverless Framework Integration (Aeon vs Hermes)

- **Architecture Distinction:**
  - **Hermes:** Persistent stateful server daemon, real-time WebSocket / Long-Polling (~1-2s response), interactive human-agent collaboration.
  - **Aeon:** Serverless GitHub Actions workflow harness, zero approval loops, self-healing cron runners, batch background tasks (~1-3m execution cycles).
- **Instant Response Bridge Pattern:** For serverless frameworks like Aeon, deploy an `aeon-bridge.service` on the VPS to instantly reply to command menus (`/status`, `/skills`, `/harness`) within 50ms while dispatching heavy autonomous runs to GitHub Actions.
