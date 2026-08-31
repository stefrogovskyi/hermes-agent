# Google Doc insertion (steps 3-7 of the publish task)

## Finding the marker + inserting
The task: find line `пунктуационные и фразеологические ошибки неточности`, add a blank line, then insert `Дата: YYYY-MM-DD` + `Файл: <name>` + the generated text. Never delete anything.

### Method A — gws CLI (if available)
`gws` (google-workspace skill) can read/edit Docs. Prefer it; it handles auth.
- Read doc: `gws docs read <docId>`
- The doc URL `.../document/d/<docId>/edit` → `<docId>` is the long string between /d/ and /edit.

### Method B — Drive API REST (service account / OAuth token)
Google Docs API has no "insert at text" — you use `documents.batchUpdate` with `insertText` at a known index, OR append. To insert under a specific line:
1. GET `https://docs.googleapis.com/v1/documents/<docId>` → find the `index` of the marker line's end (use `content` structural elements; the text run's `startIndex`).
2. `POST https://docs.googleapis.com/v1/documents/<docId>:batchUpdate` body:
```json
{ "requests": [
  { "insertText": { "location": { "index": <idx_after_marker> }, "text": "\n\nДата: 2026-07-27\nФайл: Standard recording 1.mp3\n\n<REFLECTION TEXT>\n" } }
] }
```
3. The reflection text must have newlines as `\n` inside the JSON string. Escape quotes.

### Verification (required by user)
Re-GET the document (or `gws docs read`) and confirm the inserted block appears after the marker line and is complete (character count matches the generated file). If the doc shows truncation, re-run batchUpdate with the full text — Docs API can drop very long single inserts if they exceed a size boundary; split into 2-3 insertText requests appended sequentially.

### Failure recording
If anything fails, insert (do not replace): `Обработка не завершилась: <file>, <date>`.
