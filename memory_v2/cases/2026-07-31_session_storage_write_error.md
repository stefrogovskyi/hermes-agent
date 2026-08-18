# Session Storage Write Error & Busy Input Mode Recovery (2026-07-31)

## Symptom
During an active session, Hermes encountered the system error:
`⚠️ No reply: the turn was stopped because session storage could not be written (the transcript would have been lost on restart). Check disk space / permissions for the state DB, then send another message.`
Additionally, mid-turn user edits or typed messages triggered `[This response was interrupted by a user correction.]` loops.

## Hypothesis
1. Disk space or permissions issue on `state.db`.
2. Session storage lock conflict when user inputs are delivered while generation is in progress with `display.busy_input_mode: interrupt`.

## Fact / Verification
1. Disk check (`df -h`) confirmed 283 GB available on `C:\`. Filesystem permissions on `AppData/Local/hermes/state.db` were normal (rw-r--r--).
2. Inspection of `config.yaml` showed `display.busy_input_mode: interrupt` and provider timeout at 60s, causing generation aborts on mid-turn user messages.

## Root Cause
`display.busy_input_mode: interrupt` caused mid-turn user input to cancel generation turns, leading to interrupted turns and state write locks.

## Fix
1. Updated Hermes config: `hermes config set display.busy_input_mode steer` (appends mid-turn messages as steering context instead of interrupting).
2. Increased request timeout: `hermes config set providers.nous.request_timeout_seconds 120`.
3. Updated memory rules and model pin in `config.yaml` to ensure fallback stability.

## Reflection / Rule
- Always check disk space first, but if disk space is sufficient, inspect `busy_input_mode` and lock state.
- Mode `steer` prevents aborted state writes during mid-turn messaging.
