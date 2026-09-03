---
name: afterquery-ide-bench
description: Use when benchmarking and evaluating autonomous software engineering agents on real development environments using AfterQuery IDE-Bench.
category: research/afterquery
---

# AfterQuery IDE-Bench (Agentic Software Engineering Evaluation)

IDE-Bench measures the real-world coding capability of LLMs and subagents inside realistic IDE setups (editing files, executing tests, debugging terminal output).

## Key Capabilities
- Benchmarks agent code generation, multi-file editing, and syntax integrity.
- Evaluates subagent autonomous performance (e.g. Callum coding tasks).
- Measures regression risk before applying large patches to cluster code.

## Repository Location
`/opt/hermes/profiles/alistair/repos/afterquery/IDE-Bench`

## Quick Start & Verification
```bash
cd /opt/hermes/profiles/alistair/repos/afterquery/IDE-Bench
python3 -c "import os; print('IDE-Bench items:', os.listdir('.'))"
```
