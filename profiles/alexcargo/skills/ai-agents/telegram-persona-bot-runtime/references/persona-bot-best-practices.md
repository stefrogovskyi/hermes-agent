# Telegram Persona Bot Operational Best Practices

This guide documents proven patterns and gotchas for Telegram persona bots (Alistair, Richard, Callum, Liz).

## 1. Group Name Triggering & Russian Declensions
Always match all grammatical cases/declensions for bot names in Russian:
```python
NAME_RE = re.compile(
    r"\b(алистер[а-я]*|alistair[a-z]*|allister|alister|алику)\b",
    re.I
)
```

## 2. Auto-Update Snapshot & Release Report Handling
When a user quotes or tags a release report/snapshot (e.g. from Sort It Bot or Gaffer) containing shipped/completed tasks and says "обнови в трекере":
1. **Never ask "which task IDs?"** — task names are already present in the quoted report.
2. Call `read_tracker_sheet` to fetch all live tasks from Google Sheets.
3. Fuzzy-match task titles from the report against tasks in the sheet.
4. Call `update_task` for each matching task and set `percent: 100%`.
5. Return a concise report listing updated tasks with IDs and titles.

## 3. Google Sheets Task Completion Rules
When a task reaches 100% completion:
- **Move to Done Block:** Move the row to the bottom "ВЫПОЛНЕННЫЕ ЗАДАЧИ" block in the Google Sheet (`Tracker` tab).
- **Light-Green Fill:** Apply a light-green background fill (`#d9ead3`) to the entire row.
- **NEVER DELETE OR HIDE:** Never call `deleteDimension` or hide rows — completed tasks must remain visible in the sheet for history and auditing.

## 4. Confident Demo-Ready Persona Voice
When asked about capabilities or internal workflows:
- **Zero Hedging:** Never use vague/hedged phrases ("если есть возможность", "если предусмотрено", "обычно я").
- **100% Assertive:** State exact real integrations confidently (Google Sheets `Navo Tasktracker`, Gaffer `@thegaffermcp_bot`, Telegram, SeaRates, Navo24 MCP).

## 5. Single Document Attachment
When producing reports or audits:
- **Do not split into multiple text messages.**
- Send **one consolidated summary message** with the generated `.html` / `.xlsx` file attached directly as a Telegram document (`sendDocument`).
