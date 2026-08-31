# False positives in memory_harvest.py

`memory_harvest.py` is a keyword matcher, not an LLM. When fed a raw session
transcript that includes tool outputs, it produces spurious candidates.

## Why it happens
The extractor scans every line for instruction markers and method keywords.
Internal tool dumps contain these same keywords because they show code:
- `read_file` returning script source with `def`, `import`, `return`
- `terminal` outputs containing `if`, `for`, `while`, `class`
- JSON tool results with keys like `content`, `timestamp`, `action`

## Confirmed false-positive patterns (2026-07-29 harvest run)
Raw tool blocks in the cron harvest produced 4 candidates:
- `read_file` returning `memory_harvest.py` source → misclassified as METHOD (memory_systems)
- `read_file` returning `watch_watcher.py` source → misclassified as INSTRUCTION
- `terminal` output showing `richard_scanner.py` source → misclassified as INSTRUCTION

None of these reflected actual user instructions or durable lessons.

## Mitigation
Before piping into `memory_harvest.py`, clean the transcript:
1. Keep only lines from `user` and `assistant` roles.
2. OR: strip entire tool JSON blocks (lines starting/ending with `{` `}` when
   they are tool outputs).
3. OR: extract only `role: content` where role is not `tool`.

A clean transcript produces far fewer false positives and the candidates that
remain are real.

## Rule of thumb
If a candidate's snippet contains code that is not spoken by the user or
assistant, discard it. Re-reading your own case files does not create new facts.
