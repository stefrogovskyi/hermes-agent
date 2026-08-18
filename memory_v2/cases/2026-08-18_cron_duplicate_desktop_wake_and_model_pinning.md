# Case: Cron Duplication on Desktop Wake-up & Explicit Model Pinning for Background Cron Jobs

**Date**: 2026-08-18
**Category**: agent_club / ai_infra

## Context & Problem
1. **Duplicate Cron Execution**: The evening YouTube playlist review cron job was firing twice or at unexpected times (e.g. 07:30 AM).
2. **Global Model Drift Crash**: Changing default LLM model globally (e.g., from Claude Sonnet to Gemini Flash or vice versa) caused background cron jobs without explicit model declarations to either fail, hit default fallbacks, or misbehave.

## Root Cause Analysis
1. **Desktop Cron Wake-Up**: Servarica VPS (`stefan1`) is the primary 24/7 cron runner. However, a desktop instance (`desktop-mst5pt7`) had local cron background service active. When the PC woke up from sleep/hibernate, it caught up on missed runs and triggered duplicate messages (e.g. at `07:30:56+03:00`).
2. **Unpinned Cron Jobs**: Cron jobs created without an explicit `model:` field in `config.yaml` or job payload default to whatever provider/model is active globally. When global active model is changed, unpinned jobs inherit the new default, leading to prompt/formatting mismatches or model drift.

## Solution & Standard
1. **Cron Hosting Isolation**: Keep all 24/7 cron scheduling strictly on VPS (`stefan1`). Desktop background cron services must remain disabled or set to `enabled: false`.
2. **Explicit LLM Model Pinning**: Every cron job that uses an LLM (such as `Career Scanner`, `YouTube Evening Review`, `ODDA Growth Engine`) MUST explicitly declare its target provider and model in its job definition (e.g. `model: gemini / google/gemini-3.6-flash`).
3. **Timezone Uniformity**: Align cron schedule declarations in UTC on VPS (e.g. 20:00 UTC = 23:00 MSK/Kyiv).

## Verification
- Verified Career Scanner pinned to `gemini / google/gemini-3.6-flash`.
- Verified desktop cron autostart disabled. Single delivery path confirmed on VPS live adapter.
