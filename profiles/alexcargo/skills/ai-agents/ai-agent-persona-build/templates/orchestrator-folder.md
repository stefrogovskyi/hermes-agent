# Orchestrator folder scaffold (copy-ready)

Tree to create under the agent's home folder:
```
Hermes Stevenson/
├── soul.md                  # from base persona build
├── Agents.md                # from base persona build
├── tools.md                 # from base persona build (add connector contracts)
├── system_prompt.md         # from base persona build (condense + fleet duties)
├── agent.config.json        # channels/integrations/cron/guardrails (env-only secrets)
├── README.md
├── entities/
│   ├── registry.json
│   └── TEMPLATE.md
├── processes/
│   ├── index.json
│   └── TEMPLATE.md
├── memory/
│   └── state.json
├── connectors/
│   └── README.md
└── channels/
    └── README.md
```

### entities/registry.json
```json
{
  "entities": [
    {
      "id": "hermes_stevenson",
      "type": "orchestrator",
      "name": "Hermes Stevenson",
      "role": "orchestrator",
      "status": "active",
      "owner": "stefan",
      "channels": ["desktop", "telegram", "email"],
      "created": "YYYY-MM-DD",
      "note": "Главный оркестратор."
    }
  ],
  "meta": { "count": 1, "active": 1, "paused": 0, "archived": 0, "last_updated": "YYYY-MM-DD" }
}
```

### processes/index.json
```json
{
  "processes": [
    {
      "id": "daily_digest",
      "name": "Ежедневная сводка",
      "trigger": "cron 0 9 * * *",
      "status": "idle",
      "owner_entity": "hermes_stevenson",
      "description": "Собрать активные процессы, эскалации needs_decision и метрики агентов, отправить владельцу.",
      "escalates_to": "stefan"
    }
  ],
  "meta": { "count": 1, "active": 0, "idle": 1 }
}
```

### memory/state.json
```json
{
  "state": "initialized",
  "last_wake": "YYYY-MM-DD",
  "active_tasks": [],
  "escalations": [],
  "needs_decision": [],
  "channel_health": { "telegram": "disconnected", "email": "disconnected", "desktop": "active" },
  "log": [ { "ts": "YYYY-MM-DD", "event": "orchestrator_created", "detail": "initialized in home folder." } ]
}
```

### agent.config.json (channel/integration skeleton)
```json
{
  "orchestrator": { "name": "Hermes Stevenson", "role": "Chief Orchestrator", "owner": "stefan", "always_on": true, "preferred_channel": "telegram" },
  "channels": [
    { "id": "telegram", "type": "messenger", "enabled": false, "auth_env": ["TELEGRAM_BOT_TOKEN"] },
    { "id": "email", "type": "email", "enabled": false, "auth_env": ["EMAIL_IMAP_HOST","EMAIL_IMAP_USER","EMAIL_IMAP_PASS","EMAIL_SMTP_HOST","EMAIL_SMTP_USER","EMAIL_SMTP_PASS"] },
    { "id": "desktop", "type": "local_app", "enabled": true, "auth_env": [] }
  ],
  "integrations": [
    { "id": "make", "type": "automation", "enabled": false, "auth_env": ["MAKE_API_TOKEN","MAKE_WEBHOOK_URL"] },
    { "id": "hermes_runtime", "type": "runtime", "enabled": true, "auth_env": [] }
  ],
  "cron": [ { "id": "daily_digest", "schedule": "0 9 * * *", "enabled": false, "deliver": "telegram", "prompt": "Сводка активных агентов и эскалаций." } ],
  "guardrails": [ "no_financial_transactions_without_confirmation", "no_public_posts_without_approval", "never_fabricate_data", "no_hire_fire_delete_without_consent", "secrets_only_as_env_refs", "always_escalate_critical" ],
  "pending_connectors": ["Telegram bot-token", "Email IMAP/SMTP", "Make.com API token + webhook"]
}
```

`entities/TEMPLATE.md`, `processes/TEMPLATE.md`, `connectors/README.md`, `channels/README.md`
are free-text stubs — copy the structure from `references/orchestrator-pattern.md`.
