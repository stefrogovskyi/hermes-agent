---
name: memory-recall
description: Use when starting a non-trivial task, debugging, or investigating an incident — search Hermes long-term memory (memory_v2) for relevant past cases and principles before acting. Trigger on keywords like 'remember', 'last time', 'we had this before', 'check memory', or any complex/recurring problem.
---

# Memory Recall (memory_v2)

Hermes has a long-term memory filesystem at `C:/Users/Stefan/AppData/Local/hermes/memory_v2/`.
It is NOT the 2200-char `memory` tool — that one is only a pointer. memory_v2 holds
full case files (symptom → hypothesis → root cause → fix → reflection) and principles.

## When to use
- Starting a complex task, debugging, or investigating an incident.
- Before forming a hypothesis about WHY something broke — check if we've seen it.
- Stefan mentions "last time", "we had this", "remember the rule about...".

## How to search (FACT-FIRST, never guess)
1. Run the recall helper:
   `python C:/Users/Stefan/AppData/Local/hermes/memory_v2/recall.py <keywords>`
   (uses the hermes venv: `C:/Users/Stefan/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe`)
2. Or read `C:/Users/Stefan/AppData/Local/hermes/memory_v2/index.md` for the case table.
3. Read ONLY the relevant case file(s) — do NOT load all memory.

## If semantic search is needed (concept match, not keyword)
Run `python C:/Users/Stefan/AppData/Local/hermes/memory_v2/pinecone_query.py <query>`
(requires PINECONE_API_KEY in env; falls back to recall.py if not set).

## Hard rule (from principle 00_hypothesis_fact)
CONFIRM any hypothesis with a FACT (real call / log / output) BEFORE editing code.
Do not guess the root cause and start fixing unverified.

## After resolving
Add a case: `python memory_v2/add_case.py <slug> "<desc>" "<lesson>"`
Or append to an existing case file under `cases/`.
