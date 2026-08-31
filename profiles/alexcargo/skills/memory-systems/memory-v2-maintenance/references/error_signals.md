# Error signals in last-24h logs (from 2026-07-29 harvest)

Real failures found in `C:/Users/Stefan/AppData/Local/hermes/logs/errors.log`:

## state.db routing failures
```
state.db routing save failed: 'NoneType' object has no attribute 'execute'
```
- Impact: session routing not persisted.
- Likely cause: active writer is None during save; concurrent state mutation.
- Action: restart gateway / retry routing save; do not silently drop.

## FTS write corruption
```
Persisted transcript lagged live cached history for session <id> (disk=N, memory=N+1); preserving live conversation context (possible FTS write corruption)
```
- Impact: disk transcript falls behind live cache by 1 message.
- Action: preserve live context; check disk IO and FTS compaction; restart gateway if repeated.

## Partial stream drops (mid-tool-call)
```
Stream ended with no finish_reason while a tool call's arguments were still incomplete
Partial stream delivered before error; returning length-truncated stub
Discarding chunk from superseded stream attempt
```
- Impact: tool calls truncated; session may loop or retry.
- Action: API/provider capacity issue; retry backoff built-in. Repeated drops = upstream 503 or client concurrency bug.

## Background review privilege loss
```
Tool <name> returned error: Background review denied non-whitelisted tool
```
- Impact: agent loses write / read / patch privileges mid-session.
- Action: session is in background-review mode; manual fix via foreground session.

## DNS / getaddrinfo failures
```
getaddrinfo failed
```
- Impact: crons that refresh keys or hit remote endpoints fail.
- Action: retry later; verify DNS / network; intermittent.
