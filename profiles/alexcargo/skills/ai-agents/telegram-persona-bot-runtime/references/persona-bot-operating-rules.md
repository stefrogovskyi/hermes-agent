# Persona Bot Response Rules & File Attachments (Stefan's Operating Specs)

## 1. 100% Confident, Non-Hedged Answers (Demo-Ready)
- Persona bots MUST NEVER use vague, hedged, or hesitant LLM boilerplate (*"если есть возможность"*, *"если предусмотрено"*, *"обычно я"*, *"если есть интеграция"*).
- They MUST state their actual connected tools, capabilities, and workflows with 100% confidence, ready for live demos to colleagues.

## 2. Exact Task ID Formatting
- Always label tasks explicitly with `ID <number>` tags (e.g. `ID 4 | Задача: - фильтр...`) so the LLM does not confuse physical row numbers with task IDs or invent legacy prefixes (`a4, a5`).

## 3. Completed Task Protocol (100% Progress)
- When a task reaches 100%, update `percent: 100%`, move the row down to the "ВЫПОЛНЕННЫЕ ЗАДАЧИ" block on the same sheet, and apply a **light-green background fill** (`#d9ead3`).
- **NEVER delete or hide completed rows** — they remain in the Google Sheet permanently for history and audit.

## 4. Single-Message Report & Document Attachments
- When sending comparison reports or benchmark audits, do NOT split into multiple text messages (e.g., 5 items per message).
- Send **ONE consolidated summary message** and attach the actual `.html` / document file natively via Telegram `sendDocument` (`multipart/form-data`).
