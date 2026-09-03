---
name: afterquery-mle-reasoning
description: Use when building autonomous bug localization, error hypothesis testing, and self-healing pipelines for scrapers and APIs using AfterQuery MLE Reasoning.
category: research/afterquery
---

# AfterQuery MLE Reasoning Environment

The MLE Reasoning Environment is designed to benchmark and train autonomous agents on real machine learning and software engineering debugging tasks.

## Key Capabilities
- Hypothesis generation and targeted test execution.
- Automated bug localization across multi-file repositories.
- Self-healing scraper architecture: when carrier sites change markup, run the reasoning loop to pinpoint and patch broken CSS/XPath selectors.

## Repository Location
`/opt/hermes/profiles/alistair/repos/afterquery/mle-reasoning-environment`

## Quick Start & Verification
```bash
cd /opt/hermes/profiles/alistair/repos/afterquery/mle-reasoning-environment
python3 -c "import os; print('MLE modules:', os.listdir('.'))"
```

## Practical Application for Cluster
- Autonomous repair of daily tracking scripts when carrier endpoints (Maersk, MSC, CMA CGM) return 403/429 or changed DOM structures.
