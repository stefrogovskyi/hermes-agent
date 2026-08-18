# Case: SeaRates vs TrackingMCP Benchmark Automation & Multi-Tab Excel Reports

**Date:** 2026-08-01
**Domain:** `business`, `agent_club`

## Symptom / Problem
Stefan required a 3-day automated benchmark comparing SeaRates API vs TrackingMCP across 10 real ocean containers with structured multi-tab Excel exports (`ocean_tracking_comparison_*.xlsx`) sent to Telegram.

## Root Cause
- The benchmarking script lacked `openpyxl` dependency for creating formatted multi-tab Excel workbooks.
- Alistair bot script did not have a dedicated `tg_send_document` helper with `parse_mode=HTML` for sending document files directly to Telegram chats.

## Fix / Implementation
1. **Installed openpyxl**:
   `pip install openpyxl`
2. **Built Benchmark Script (`searates_vs_trackingmcp_benchmarker.py`)**:
   - Queries 10 real container tracking numbers across both SeaRates and TrackingMCP APIs.
   - Generates a multi-tab Excel file with Executive Summary, Event-by-Event Comparison, and Container Level Audit.
3. **Telegram Document Helper (`tg_send_document`)**:
   - Added `tg_send_document(chat_id, file_path, caption)` to `alistair_bot.py` and `searates_vs_trackingmcp_benchmarker.py`.
   - Used `multipart/form-data` POST request with `parse_mode='HTML'` to `https://api.telegram.org/bot<TOKEN>/sendDocument`.

## Reflection / Key Lesson
- When sending `.xlsx` reports to Telegram, ensure `parse_mode` in `sendDocument` matches the caption formatting (HTML or Markdown) to prevent HTTP 400 errors.
- Always verify openpyxl availability before attempting multi-tab Excel workbook generation in automation scripts.
