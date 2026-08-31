---
name: agent-discipline
description: Fact-first debugging and autonomous crash recovery.
---

# Agent Discipline

Core operating contract for autonomous sessions.

## 0 — Confirm hypotheses with FACT before action (principle 00)
Any time you form a hypothesis about why something broke or how something works:
1. **Stop before editing code/config.**
2. Verify with a real call, log, traceroute, or actual response — not by analogy or a hand-built test that does not match the real runtime path.
3. Only then apply a fix.
4. If you cannot get a fact in one shot, say so explicitly instead of inferring.

Pitfall: do not use a hand-rolled `urllib` test to prove a key is broken when the real runtime uses an SDK that may add headers/formatting. Run the same code path the runtime uses.

## 1 — Self-recover on ANY failure, no waiting for user (principle 01)
When a tool returns an error, the platform reports a storage failure (`session storage could not be written`), an interruption occurs (`[This response was interrupted...]`), or you see an exception in your own output:
1. **Log the failure internally** (memory/case file / `crash_journal.json`).
2. **Auto-resume the interrupted task immediately** — restore the goal context from `session_state.json` (where pre-turn state is marked `IN_FLIGHT`), log the interrupt cause, and continue from the exact checkpoint without asking the user "what next" or explaining error internals. The user expects 100% autonomous self-healing: do NOT present raw error messages to the user or ask them to report bugs.
3. **Prevent SQLite locks & storage failures:** Convert SQLite database files to Write-Ahead Logging (`PRAGMA journal_mode=WAL;`) and set a 10-second busy timeout (`PRAGMA busy_timeout=10000;`) to prevent `database is locked` / storage write failures during concurrent cron and gateway operations.
4. **Analyze the root cause after** the task is restored.
5. If the same task fails 3 consecutive times across retries, stop retrying and switch to root-cause analysis.
6. Never wait for the user to ask “are you done?” after you reported an error — report the resolution instead.

Pitfall: if a state-DB or session storage write fails, check WAL mode and busy_timeout settings, start fresh, and regenerate the artifact rather than retrying the same write.

Pitfall (Foreground self-restart loop): Never run `systemctl restart <own-service>` synchronously inside a tool execution turn. Restarting the agent's own service kills the active process mid-turn with SIGTERM (`exit_code: -15`), leaving an interrupted session state (`Operation interrupted`) in the DB that causes restart-loops upon gateway recovery. If a gateway process must restart itself, schedule the restart via a detached background process (e.g. `nohup bash -c "sleep 2 && systemctl restart <service>" >/dev/null 2>&1 &`) so the active turn finishes sending its response to the user before the gateway drops.

## 2 — Re-read your own messages/outputs (principle 02)
After you generate a response or after a system error, re-scan your own output for:
- Self-reported errors or crashes
- “I cannot do X”
- “stub”, “not implemented”, “not connected”
- Platform error notices (state.db, truncation, 429/403)

If found, act immediately — do not wait for the user to quote it back to you.

## 3 — Ask once, then act; do not loop
If you do not know something critical:
1. Ask the user **once** with a tight, scoped question.
2. On the next turn, act autonomously.
3. Do not re-ask the same question in subsequent turns.

## 4 — Confirmation gate before destructive/mutating actions (principle 04)
When the user asks an informational question (e.g., "what text did I highlight?", "what files are here?"), answer ONLY the question.
1. **DO NOT execute destructive, file-deleting, or final mutating actions** based on a question alone.
2. Always ask for explicit user confirmation before deleting files, terminating processes, or applying unconfirmed changes.
3. "Don't rush ahead — answer what was asked first."

## 5 — Truthful state reporting
Never say “fixed”, “working”, or “done” without a current, positive fact check in the same task. A previous green test does not prove current health after code or config changes.

## How to use
This skill governs debugging, crash recovery, bot operation, and any task where the user said “stop guessing, verify first” or similar. When invoked:
- Read `references/interrupt-autoresume-and-google-drive-entity-inspection.md` for specific interrupt auto-resume and Google Drive entity path inspection protocols.
- Read only the relevant case under `memory_v2/cases/` if known.
- Apply principles 00–02 in order.
- After resolution, write a case (or append to an existing one) so future sessions inherit the lesson.
