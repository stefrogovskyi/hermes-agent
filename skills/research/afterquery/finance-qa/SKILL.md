---
name: afterquery-finance-qa
description: Use when building, evaluating, or auditing financial reasoning, margin optimization, and multi-step rate calculations using AfterQuery FinanceQA.
category: research/afterquery
---

# AfterQuery FinanceQA (Financial Reasoning & Tariff Math)

FinanceQA is a specialized dataset and evaluation harness focused on complex financial analysis, multi-table cross-referencing, and numerical reasoning for AI models.

## Key Capabilities
- Benchmarking LLM precision on balance sheets, P&L statements, and multi-tiered cost structures.
- Preventing rounding errors and unit mismatches ($ vs € vs ₴) in automated financial outputs.
- Testing complex freight quotation models (Bunker Adjustment Factor + Ocean Freight + Inland Haulage + Demurrage calculation).

## Repository Location
`/opt/hermes/profiles/alistair/repos/afterquery/FinanceQA`

## Quick Start & Verification
```bash
cd /opt/hermes/profiles/alistair/repos/afterquery/FinanceQA
python3 -c "import os; print('FinanceQA files:', os.listdir('.'))"
```

## Practical Application
Use this benchmark to test whether newly added LLM models (e.g. Gemini 3.8 Flash vs Claude 3.7 vs DeepSeek) can accurately calculate complex freight rates and logistics demurrage without numerical hallucination.
