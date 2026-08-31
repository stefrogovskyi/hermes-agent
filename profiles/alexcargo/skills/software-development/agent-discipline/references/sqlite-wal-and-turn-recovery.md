# SQLite WAL Mode and Turn State Persistence Protocols

## SQLite WAL Mode & Busy Timeout Setup
To prevent `session storage could not be written` and `database is locked` errors during concurrent cron jobs and messaging gateway operations:
1. Ensure all SQLite database files under the user/app data directory run in Write-Ahead Logging (WAL) mode:
   ```python
   import sqlite3
   conn = sqlite3.connect("database.db", timeout=5.0)
   conn.execute("PRAGMA journal_mode=WAL;")
   conn.execute("PRAGMA busy_timeout=10000;") # 10 seconds
   conn.close()
   ```
2. WAL mode allows concurrent readers and writers without blocking or failing session storage writes.

## Turn State Persistence (`session_state.json`)
To guarantee that interrupted turns are always detected and auto-resumed upon gateway restart:
1. On turn start, record state with `IN_FLIGHT` status to `session_state.json`.
2. On turn completion, update status to `COMPLETED`.
3. On gateway startup, check if `session_state.json` contains `IN_FLIGHT`. If found, log entry to `crash_journal.json`, auto-resume the goal task, analyze root cause, and deliver the final result without requiring user prompts.
