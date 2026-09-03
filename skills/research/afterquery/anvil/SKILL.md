---
name: afterquery-anvil
description: Use when synthesizing domain-specific reasoning datasets, step-by-step traces, and chain-of-thought data using AfterQuery Anvil.
category: research/afterquery
---

# AfterQuery Anvil (Synthetic Reasoning Data Engine)

Anvil is a research toolkit for creating high-fidelity synthetic reasoning data, step-by-step expert trajectories, and verification chains for training frontier models.

## Key Capabilities
- Automated generation of edge-case scenarios and synthetic operational data.
- Chain-of-thought (CoT) generation and filtering against rigorous quality rubrics.
- Building custom training datasets for specialized vertical domains (e.g. freight forwarding, customs brokerage, contract analysis).

## Repository Location
`/opt/hermes/profiles/alistair/repos/afterquery/anvil`

## Quick Start & Verification
```bash
cd /opt/hermes/profiles/alistair/repos/afterquery/anvil
python3 -c "import os; print('Anvil items:', os.listdir('.'))"
```
