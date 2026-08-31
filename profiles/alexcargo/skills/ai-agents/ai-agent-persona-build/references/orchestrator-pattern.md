# Orchestrator pattern (fleet-managing meta-agent)

## When to build this instead of a single persona agent
- User says "orchestrator", "manage my agents/employees", "I'll give you connectors",
  "live even when my computer is off", "talk to me via Telegram/email".
- They want ONE dispatcher that creates, monitors, and aggregates many sub-entities.

## Entity model (one registry, many cards)
- `agent` — autonomous AI agent with a role (sales / support / research / content / ops / finance).
- `virtual_employee` — broader function role; may be a human contractor or an agent.
- `connector` — technical link to an external system (Telegram, Email, Make.com).
- `process` — recurring workflow (onboarding, daily digest, campaign).

## Lifecycle per entity
create → onboard → active → weekly review → pause / archive / delete.
Pause / archive / delete only with user consent.

## Secrets discipline
- NEVER plaintext. Store names only in `agent.config.json` (`auth_env` arrays).
- Real values in host env / secret store.
- The base persona build already frames integrations as env refs — extend the same
  discipline to every connector and channel.

## Always-on
- A `cron` job (daily digest, health check) with `deliver` to the user's priority
  channel is what survives machine reboots. The runtime (Hermes) keeps cron alive.

## Wake-up sequence
config → state → registry → reply in inbound channel, in soul voice.

## Honesty states
- channel `enabled: false` + `channel_health: "disconnected"` until creds arrive.
- `no_data` / `disconnected` / `auth_failed` are valid — never fabricate messages or metrics.

## Validation
- All `*.json` must parse (`json.load`); assert structural invariants (e.g.
  `meta.count == len(entities)`, `guardrails` present, `always_on` flag).
- Generate/validate via `execute_code`; write FINAL files with `write_file`.
