---
name: drive-spreadsheets-workflow
description: Google Drive and Sheets workflows and best practices.
version: 1.0.0
author: Archie Wright (Hermes Agent)
license: MIT
metadata:
  hermes:
    tags: [google-drive, google-sheets, file-management, spreadsheets, workflow]
    related_skills: [google-workspace, xlsx, hermes-agent]
---

# Drive & Spreadsheets Workflow

This skill documents best practices and efficient workflows for interacting with Google Drive and Google Sheets, focusing on native format conversions and reliable update procedures. It incorporates lessons learned from common pitfalls in file handling and API interactions.

## When to Use

Use this skill when you need to:

*   Manage spreadsheet files on Google Drive, especially converting between local formats (TSV, CSV, XLSX) and native Google Sheets.
*   Update existing spreadsheet files on Google Drive programmatically.
*   Understand best practices for efficient and reliable Google Drive and Sheets API interactions.
*   Troubleshoot issues related to large file processing or long-running tasks with `execute_code`, `terminal(background=True)`, or `cronjob` orchestration.

## Best Practices for Spreadsheets on Google Drive

When working with spreadsheets on Google Drive, prefer native Google Sheets (converted from XLSX) over TSV/CSV for direct editing and seamless integration. This avoids complex download/upload cycles and enables direct manipulation via Google's UI or Sheets API.

### Workflow to upload an Excel file (XLSX) and convert it to a native Google Sheet:

1.  **Convert your local data (e.g., TSV/CSV) to an XLSX file first.**
    (Refer to the `xlsx` skill for local CSV/TSV to XLSX conversion procedures.)

2.  **Upload the XLSX file directly with the native Google Sheet MIME type:**
    ```bash
    GAPI="python ${HERMES_HOME:-$HOME/.hermes}/skills/productivity/google-workspace/scripts/google_api.py"
    $GAPI drive upload /path/to/your_file.xlsx --name "Your Sheet Name" --mime-type application/vnd.google-apps.spreadsheet
    ```
    This command directly converts and uploads the XLSX as a Google Sheet, provided the XLSX is well-formed and compatible with Google Sheets conversion. This was the command that eventually succeeded in the conversation.

### Workflow to update an existing Google Drive file (e.g., replacing a Google Sheet with new data):

`google_api.py drive upload` creates a *new* file. To replace an existing file (e.g., updating a Google Sheet with new data from a local XLSX/CSV):

1.  **Delete the old file** using its `FILE_ID`:
    ```bash
    GAPI="python ${HERMES_HOME:-$HOME/.hermes}/skills/productivity/google-workspace/scripts/google_api.py"
    $GAPI drive delete FILE_ID
    ```
2.  **Upload the new file** (with the desired name and MIME type for conversion, if applicable):
    ```bash
    GAPI="python ${HERMES_HOME:-$HOME/.hermes}/skills/productivity/google-workspace/scripts/google_api.py"
    $GAPI drive upload /path/to/new_file.xlsx --name "Your Sheet Name" --mime-type application/vnd.google-apps.spreadsheet
    ```
    This will create a new file, effectively replacing the old one with a fresh native Google Sheet.

## Sheet Range & Queue-Processing Pitfalls

These apply whenever a sheet is used as a work queue driven by a script or a recurring cronjob (read a row, process it, write status back).

*   **Never assume the tab is literally named `Sheet1`.** Custom or non-English tab names (e.g. "Блогпосты Сирейтс") are common, especially on sheets built from an uploaded/converted file. `HttpError 400: Unable to parse range` on a range like `Sheet1!A:G` is almost always this, not a shell-quoting bug. Fix: call `spreadsheets().get(spreadsheetId=...)` once, read `sheets[0]['properties']['title']`, and reuse that literal (quoted) name in every subsequent range.

*   **Never hardcode a small row range (e.g. `A1:G100`) in a recurring/cron prompt without first checking the real size of the sheet.** A queue-processing job that reads only the first ~100 rows will silently report "queue almost empty" while thousands of real rows below that point are never touched. Fix: before writing the prompt, call `spreadsheets().get(..., includeGridData=False)` and read `sheets[0]['properties']['gridProperties']['rowCount']`, then use that real row count (or `A2:G<rowCount>`) in the job. If the API balks at reading the whole range in one call, batch it (e.g. 5000 rows at a time) rather than truncating the search window.

*   **Row 1 is always the header.** Any queue-processing job must explicitly start scanning/writing at row 2 and must never let a "find first empty/matching row" search accidentally land on row 1. State this explicitly in the job prompt; a job that overwrites headers is a easy, embarrassing, and avoidable bug.

*   **Check for stray artifacts before automating over a sheet at scale.** Terminal output or other non-data text can end up pasted into a cell (e.g. a `__HERMES_CWD_...` marker from a shell snapshot script) if a prior manual step went wrong. Spot-check a few rows across the full range (start, middle, end) before trusting the sheet as clean automation input, and blank out any garbage rows found.

## OAuth Token Expiry: "Testing" Publishing Status (Google Cloud)

If a Google Workspace/Drive/Sheets OAuth refresh token starts failing with `RefreshError: invalid_grant: Token has been expired or revoked` roughly every 6-7 days despite active use, the root cause is almost always that the Google Cloud OAuth consent screen for that client is still in **Testing** publishing status. Google unconditionally expires refresh tokens after 7 days for apps in Testing, regardless of usage — this is a hard platform rule, not a token/credentials bug to debug further.

Fix: in Google Cloud Console, go to the OAuth consent screen for the project (in the newer UI this is under **APIs & Services → Google Auth Platform → Audience**) and publish the app to **Production**. For an internal/personal-use tool with sensitive-but-not-restricted scopes (Drive, Sheets, Docs, Gmail, Calendar, Contacts.readonly all qualify), this does not require Google's verification review — just click through. Google may still ask for an **App domain** section (homepage URL, privacy policy URL, terms of service URL) before allowing publish; a minimal 3-page static site (home/privacy/terms) deployed anywhere with a stable HTTPS URL satisfies this. After publishing, the user must still re-run the OAuth code exchange one final time — publishing alone does not extend an already-issued Testing-mode token.

## Pitfalls and Considerations for Tool Usage

*   **`execute_code` for large file processing:** Avoid using `execute_code` for extensive file I/O operations (reading/writing very large files or performing long computational tasks). It can hit internal limits on output size or execution time, leading to repeated failures. For such tasks, prefer standalone Python scripts executed via `terminal` (blocking mode) or well-structured `cronjob` tasks.

*   **`terminal(background=True)` for long-running processes within current session:** Using `terminal(background=True)` from the interactive session can be problematic if the background process tries to interact with Hermes' internal gateway or if it is too long-running. For reliable, long-term background tasks or complex multi-step pipelines, always prefer `cronjob`.

*   **Orchestrating complex pipelines with `cronjob`:** For multi-step workflows involving API calls, file manipulations, and skill delegation, a `cronjob` with a detailed `prompt` that directly calls tools (like `delegate_task`) and other scripts is the most robust approach. Python scripts launched by a `cronjob` cannot directly invoke `delegate_task` or other Hermes skills; the *cronjob's prompt* must contain the high-level orchestration logic.

*   **Running Python scripts in `terminal`:** Always explicitly use `python3 /path/to/script.py` when executing Python scripts via the `terminal` tool. Simply calling `/path/to/script.py` (even if executable) can lead to syntax errors if the shell attempts to interpret it as a bash script.
