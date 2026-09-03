---
name: afterquery-harbor
description: Use when building agent verification loops, ground-truth evaluations, and anti-hallucination verifier factories via AfterQuery Harbor.
category: research/afterquery
---

# AfterQuery Harbor (Agent Evaluation & Verifier Factory)

Harbor is an industrial evaluation and verification framework for coding and autonomous agents (Claude Code, OpenHands, Codex CLI). It provides deterministic environment sandboxes and verifier pipelines.

## Key Capabilities
- **Verifier Factory:** Attach automated assertion suites to agent task completions.
- **Anti-Hallucination Guard:** Requires objective tool outputs (HTTP 200, regex check, math assertion) before an agent can claim task completion.
- Sandboxed environment orchestration (Docker, modal, local).

## Repository Location
`/opt/hermes/profiles/alistair/repos/afterquery/harbor`

## Quick Start & Verification
```bash
cd /opt/hermes/profiles/alistair/repos/afterquery/harbor
# Check verifiers and runners
python3 -c "import os; print('Harbor structure:', [d for d in os.listdir('.') if os.path.isdir(d)])"
```

## Practical Application
Use Harbor's verification design for Navo:
1. Wrap container tracking status queries in an assertion verifier (ensuring container number matches ISO 6346 before returning data).
2. Validate freight quote calculations against contractual baseline tariffs.
