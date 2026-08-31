---
name: memory-v2-maintenance
description: 'Maintain Hermes memory_v2: harvest, cases, sync.'
---

# Memory v2 Maintenance (hermes memory_v2)

Hermes long-term memory filesystem at `C:/Users/Stefan/AppData/Local/hermes/memory_v2/`.
It is NOT the 2200-char `memory` tool — that one is only a pointer. memory_v2 holds
full case files (symptom → hypothesis → root cause → fix → reflection), principles, and
domain notes, plus a Pinecone semantic index.

## When to use
- Scheduled cron memory steward (default: 02:00 harvest / 03:00 Pinecone sync).
- After a non-trivial incident is resolved and the session produced durable lessons.
- When you detect a prior session crash, state.db write error, or truncated turn.
- Stefan asks to log a case or remember a rule.

## Layout
- `C:/Users/Stefan/AppData/Local/hermes/memory_v2/`
  - `recall.py` — keyword search helper.
  - `pinecone_query.py` — semantic search helper.
  - `pinecone_sync.py` — re-index chunks to Pinecone.
  - `add_case.py` — scaffold a new case + update `index.md`.
  - `memory_harvest.py` — extract candidates (INSTRUCTION / SUCCESS / METHOD) from a session text.
  - `index.md` — case/domain table.
  - `cases/` — `.md` case files.
  - `principles/` — durable rules.
  - `domains/life_domains.md` — domain-tagged notes.
  - `references/servarica_multiagent_deployment_and_kanban.md` — 24/7 Servarica deployment, Tailscale mesh network, and Vercel Kanban boards.

## VPS Mirroring Rule (PC <-> VPS Sync)
To prevent memory blindness on sub-agents executing on the Servarica VPS (`stefan1`), the `cases/` and `principles/` directories under `memory_v2` must be kept in 1:1 sync with `/opt/hermes/memory_v2/` on VPS. When new cases are added locally, bundle and sync them via scp/tar so sub-agents querying `recall.py` on VPS see 100% of historical cases.

## Harvest workflow (24h extraction → classify → record)

### 1. Extract transcript from state.db (and sub-profiles)
- Root DB: `C:/Users/Stefan/AppData/Local/hermes/state.db`
- Sub-agent profile DBs: `C:/Users/Stefan/AppData/Local/hermes/profiles/<name>/state.db` (`alistair`, `ben`, `callum`, `liz`, `richard`).
- **Column names**: The timestamp column in `messages` is `timestamp` (Unix float epoch in seconds or ISO string; NOT `created_at`). In `sessions`, columns are `started_at` and `ended_at`.
- Direct query for all messages in the last 24h by float epoch timestamp (`timestamp >= cutoff_ts`, where `cutoff_ts = time.time() - 86400`) across all profiles.
  **PERFORMANCE WARNING**: `messages` table in `state.db` (which can grow >400MB) has an index on `(session_id, timestamp)` but NOT on `timestamp` alone. Direct `WHERE timestamp >= ?` on `messages` causes a full table scan and 60s+ timeouts on SQLite. Instead, query `sessions` using indexed `started_at >= ?` first, then batch query `messages` using `session_id IN (...) AND timestamp >= ?`:
  ```sql
  -- Step 1: Get session IDs (uses idx_sessions_started)
  SELECT id FROM sessions WHERE started_at >= ?;

  -- Step 2: Get messages for those sessions (uses idx_messages_session)
  SELECT session_id, role, content, timestamp
  FROM messages
  WHERE session_id IN (...) AND timestamp >= ? AND role IN ('user', 'assistant')
  ORDER BY timestamp ASC;
  ```
- Write clean transcript (formatted as `[<session_id>] (<role>): <content>`) directly to a temp text file (e.g. `session_24h.txt`).
- **CRITICAL**: Filter out `role = 'tool'` messages from the SQL query or python script (`WHERE role IN ('user', 'assistant')`). Including raw `tool` messages feeds previous harvest JSON outputs, file diffs, and tool logs into `memory_harvest.py`, causing hundreds of false positive candidate matches (e.g. 600+ candidates instead of ~20 real ones).
- **Execution Script**:
  ```python
  import sqlite3, time, os

  main_db = 'C:/Users/Stefan/AppData/Local/hermes/state.db'
  profiles_dir = 'C:/Users/Stefan/AppData/Local/hermes/profiles'
  out_path = 'C:/Users/Stefan/AppData/Local/hermes/memory_v2/session_24h.txt'

  cutoff = time.time() - 86400
  dbs = [('default', main_db)]
  if os.path.exists(profiles_dir):
      for p in os.listdir(profiles_dir):
          pdb = os.path.join(profiles_dir, p, 'state.db')
          if os.path.exists(pdb) and pdb != main_db:
              dbs.append((p, pdb))

  all_extracted = []
  for prof_name, db_path in dbs:
      try:
          conn = sqlite3.connect(f'file:{db_path}?mode=ro', uri=True, timeout=10.0)
          cur = conn.cursor()
          cur.execute('SELECT id, title FROM sessions WHERE started_at >= ?', (cutoff,))
          session_map = {sid: title for sid, title in cur.fetchall()}
          
          cur.execute('SELECT DISTINCT session_id FROM messages WHERE timestamp >= ? AND role IN (\'user\', \'assistant\')', (cutoff,))
          for esid in [r[0] for r in cur.fetchall() if r[0] not in session_map]:
              cur.execute('SELECT title FROM sessions WHERE id = ?', (esid,))
              srow = cur.fetchone()
              session_map[esid] = srow[0] if srow else 'Unknown'
              
          session_ids = list(session_map.keys())
          if not session_ids:
              conn.close()
              continue
              
          for i in range(0, len(session_ids), 50):
              batch = session_ids[i:i+50]
              placeholders = ','.join('?' for _ in batch)
              cur.execute(f'''
                  SELECT session_id, role, timestamp, content
                  FROM messages
                  WHERE session_id IN ({placeholders}) AND timestamp >= ? AND role IN ('user', 'assistant')
                  ORDER BY timestamp ASC
              ''', batch + [cutoff])
              for sess_id, role, ts, content in cur.fetchall():
                  all_extracted.append((ts or 0, prof_name, sess_id, session_map.get(sess_id, ''), role, content))
          conn.close()
      except Exception as e:
          print(f'Error reading DB {db_path}: {e}')

  all_extracted.sort(key=lambda x: x[0])
  with open(out_path, 'w', encoding='utf-8') as f:
      current_sess = None
      for ts, prof_name, sess_id, title, role, content in all_extracted:
          if (prof_name, sess_id) != current_sess:
              f.write(f'\n=== PROFILE: {prof_name} | SESSION: {sess_id} ({title}) ===\n')
              current_sess = (prof_name, sess_id)
          dt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts)) if ts else 'N/A'
          f.write(f'[{dt}] [{role}]: {content or ""}\n')
  ```

### 2. Run harvester
```bash
cd "C:/Users/Stefan/AppData/Local/hermes/memory_v2"
"C:/Users/Stefan/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe" memory_harvest.py <transcript_file>
```

### 3. Classify and record candidates
For each candidate (`INSTRUCTION` / `SUCCESS` / `METHOD`) with a domain tag:
- **Verify the suggested domain** — the tagger is heuristic; accept only if correct.
  Valid: `agent_club` / `ai_infra` / `memory_systems` / `business` / `personal` / `new:<name>`.
- **INSTRUCTION / durable rule from Stefan**:
  - New rule → append to `principles/<slug>.md` or `domains/life_domains.md` (e.g. `NO AGENT MAY IMPERSONATE STEFAN`, DP World vacancy isolation to Hermes Stevenson DM, Auto Git Commit & Push without manual pushes, Servarica 24/7 systemd cluster deployment, Per-agent Vercel Kanban boards).
  - Duplicate → update existing file; do not branch.
- **SUCCESS / METHOD**:
  - New case: `C:/Users/Stefan/AppData/Local/hermes/memory_v2/cases/<YYYY-MM-DD_<slug>>.md`
    via `add_case.py <slug> "<desc>" "<lesson>"`.
  - Update existing case: append a dated section directly with `patch` / `write_file`
    because `add_case.py` refuses overwrite.
  - Update `index.md` with the new row in the cases table.
- Cross-link cases to domain notes when they touch pricing, architecture, or bot behavior.

### 4. Re-index
```bash
cd "C:/Users/Stefan/AppData/Local/hermes/memory_v2"
"C:/Users/Stefan/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe" pinecone_sync.py
```

## Critical pitfall: false positives from raw tool transcripts
`memory_harvest.py` is a keyword matcher. Feeding it raw tool output causes false
"INSTRUCTION" / "METHOD" candidates from internal plumbing (script sources, JSON
tool dumps, diagnostic reads). **Mitigation:** clean the transcript first — preserve
only `user` and `assistant` lines, or strip tool JSON blocks. Re-reading existing
memory files does NOT generate new facts.

## Cron caveats
- `execute_code` is blocked in cron mode — use `terminal` to run Python scripts/commands instead (`python -c "..."` or script invocation).
- Cron sessions may **not** support `notify_on_complete` / `watch_patterns`.
  Use `process(action='wait')` or poll manually for background subprocess results.
- Background `terminal(background=true)` processes in cron do not return async
  completion notifications — silently monitor with `process(action='poll')` or
  redirect output to a log file and read it later.

## Error signals in `C:/Users/Stefan/AppData/Local/hermes/logs/errors.log`
Real problems in last-24h — report them:
- `state.db routing save failed: 'NoneType' object has no attribute 'execute'`
- `Persisted transcript lagged live cached history for session ... (disk=N, memory=N+1); preserving live conversation context (possible FTS write corruption)`
- `Stream ended with no finish_reason while a tool call's arguments were still incomplete`
- `Partial stream delivered before error; returning length-truncated stub`
- `Discarding chunk from superseded stream attempt`
- `Tool ... returned error: Background review denied non-whitelisted tool`
- `getaddrinfo failed` on DNS-dependent crons (key refresh, scanner)

If a state.db write error is detected, fix the underlying issue instead of silently discarding.

## Reporting rule
Produce output **only** when there are errors or zero candidates found.
Otherwise stay silent so cron delivery is suppressed.
