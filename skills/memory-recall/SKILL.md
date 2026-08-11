---
name: memory-recall
description: "Semantic and vector memory recall via memory_v2, Pinecone, and local cases/principles store."
version: 2.0.0
author: Hermes Agent
license: MIT
---

# Memory Recall Skill (Memory V2)

This skill enables deep memory recall, harvesting, and Pinecone vector synchronization across all sessions.

## Structure
- `/opt/hermes/memory_v2/principles/` — Core rules, directives, and preferences from Stefan.
- `/opt/hermes/memory_v2/cases/` — Proven workflows, solutions, and historical cases.
- `/opt/hermes/memory_v2/domains/` — Domain-specific knowledge (Life, Sales, Engineering, Ops).
- `/opt/hermes/memory_v2/pinecone_sync.py` — Vector embeddings sync into Pinecone.
- `/opt/hermes/memory_v2/memory_harvest.py` — Session transcript harvester.
