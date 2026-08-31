# state.db schema notes for memory_v2 extraction

Relevant tables live in:
- Main default profile: `C:/Users/Stefan/AppData/Local/hermes/state.db`
- Sub-agent profiles: `C:/Users/Stefan/AppData/Local/hermes/profiles/<profile_name>/state.db` (e.g. `alistair`, `ben`, `callum`, `liz`, `richard`)

## sessions columns (selected)
- `id` — session key (string, e.g. `cron_...`).
- `source` — `cron`, `telegram`, `tui`, `desktop`, etc.
- `display_name`, `title`
- `started_at`, `ended_at` — ISO timestamp strings or float unix timestamps (no `created_at` exists).
- `message_count`, `tool_call_count`
- `ended_at` is NULL for still-active sessions.

## messages columns (selected)
- `id`, `session_id`
- `role` — `user`, `assistant`, `tool`, `system`
- `content` — raw string payload (often JSON for tool results)
- `tool_name`, `tool_calls`
- `timestamp` — float unix timestamp or ISO string timestamp
- `platform_message_id`
- `finish_reason`

## Common pitfall
1. Queries often fail with `sqlite3.OperationalError: no such column: created_at` because the column is `started_at` / `ended_at` in `sessions` and `timestamp` in `messages`.
2. Timestamps in `messages` may be stored either as float unix timestamps or as ISO 8601 strings depending on session writer context. Test both: `WHERE timestamp >= ? OR timestamp >= ?` passing `cutoff_ts` (float) and `cutoff_iso` (string).
3. Sub-agents run under their own profile directories (`profiles/<name>/state.db`). Query all profiles when harvesting complete 24h context.

## Last-24h cutoff Python snippet
```python
import sqlite3, os, time
from datetime import datetime, timedelta, timezone

cutoff_ts = time.time() - 86400
cutoff_iso = (datetime.now(timezone.utc) - timedelta(hours=24)).isoformat()

profiles = ['', 'alistair', 'ben', 'callum', 'liz', 'richard']
```

## Session selection heuristics
- Include: sessions where `started_at >= cutoff` or `ended_at >= cutoff`.
- Filter: skip `message_count is None or < 2`.
- Filter out `role = 'tool'` to avoid false-positive harvester candidate matches.
