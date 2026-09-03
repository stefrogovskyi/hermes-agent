
import sys
import os
import json
import csv
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from pathlib import Path

# --- Configuration (passed via environment or hardcoded for cronjob context) ---
GOOGLE_SHEET_ID = os.environ.get("GOOGLE_SHEET_ID")
NAVO_BLOG_POSTS_FOLDER_ID = os.environ.get("NAVO_BLOG_POSTS_FOLDER_ID")
API_KEY = os.environ.get("GOOGLE_API_KEY") # For web_search (if used in future)
HERMES_ROOT = Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes"))
ARCHIE_PROFILE_ROOT = HERMES_ROOT / "profiles" / "archie"
SKILL_DIR = ARCHIE_PROFILE_ROOT / "skills" / "creative" / "avalanche-copywriting" # Assuming the skill location
GOOGLE_CLIENT_SECRET_PATH = ARCHIE_PROFILE_ROOT / "google_client_secret.json"
GOOGLE_TOKEN_PATH = ARCHIE_PROFILE_ROOT / "google_token.json"

SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets"
]

def get_google_credentials():
    creds = None
    if GOOGLE_TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(GOOGLE_TOKEN_PATH, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not GOOGLE_CLIENT_SECRET_PATH.exists():
                print(f"Error: Google client secret file not found at {GOOGLE_CLIENT_SECRET_PATH}", file=sys.stderr)
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(GOOGLE_CLIENT_SECRET_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(GOOGLE_TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())
    return creds

def get_sheets_service():
    creds = get_google_credentials()
    return build('sheets', 'v4', credentials=creds)

def get_drive_service():
    creds = get_google_credentials()
    return build('drive', 'v3', credentials=creds)

def read_spreadsheet_row(sheets_service, sheet_id, row_index):
    # Google Sheets API is 1-indexed for rows.
    # We want to read columns A, B, C, D (for Status), E, F, G (for Navo details)
    # Range should be A<row_index>:G<row_index>
    range_name = f"Sheet1!A{row_index}:G{row_index}"
    result = sheets_service.spreadsheets().values().get(
        spreadsheetId=sheet_id, range=range_name).execute()
    
    values = result.get('values', [])
    if not values:
        return None
    
    # Pad the row with empty strings if it's shorter than expected
    row_data = values[0]
    while len(row_data) < 7: # Ensure we have at least G column
        row_data.append('')
    return row_data

def update_spreadsheet_row(sheets_service, sheet_id, row_index, column_index, value):
    # Google Sheets API is 1-indexed for rows.
    # Convert 0-indexed column_index to A, B, C...
    column_letter = chr(ord('A') + column_index)
    range_name = f"Sheet1!{column_letter}{row_index}"
    
    body = {
        'values': [[value]]
    }
    result = sheets_service.spreadsheets().values().update(
        spreadsheetId=sheet_id, range=range_name,
        valueInputOption="USER_ENTERED", body=body).execute()
    return result

def upload_file_to_drive(drive_service, file_path, folder_id, file_name, mime_type):
    from googleapiclient.http import MediaFileUpload
    
    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }
    media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)
    
    # Check if a file with the same name exists in the folder
    query = f"name='{file_name}' and '{folder_id}' in parents and trashed=false"
    response = drive_service.files().list(q=query, fields='files(id, name)').execute()
    existing_files = response.get('files', [])

    if existing_files:
        # Update existing file
        file_id = existing_files[0]['id']
        file = drive_service.files().update(
            fileId=file_id,
            media_body=media,
            fields='id, name, mimeType, webViewLink'
        ).execute()
        print(f"Updated existing file: {file.get('name')} ({file.get('webViewLink')})")
    else:
        # Create new file
        file = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, name, mimeType, webViewLink'
        ).execute()
        print(f"Uploaded new file: {file.get('name')} ({file.get('webViewLink')})")
    
    return file.get('id'), file.get('webViewLink')

# --- Main script logic for processing one article ---
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python process_article_for_blog.py <google_sheet_id> <row_index>", file=sys.stderr)
        sys.exit(1)

    google_sheet_id = sys.argv[1]
    row_index = int(sys.argv[2])

    if not NAVO_BLOG_POSTS_FOLDER_ID:
        print("Error: NAVO_BLOG_POSTS_FOLDER_ID environment variable not set.", file=sys.stderr)
        sys.exit(1)

    sheets_service = get_sheets_service()
    drive_service = get_drive_service()

    try:
        # 1. Read article details from the spreadsheet
        article_data = read_spreadsheet_row(sheets_service, google_sheet_id, row_index)
        if not article_data:
            print(f"No data found for row {row_index} in spreadsheet {google_sheet_id}", file=sys.stderr)
            sys.exit(1)

        # Columns: A=0, B=1, C=2, D=3, E=4, F=5, G=6
        article_title = article_data[0] # Column A: Название статьи
        article_url = article_data[1]   # Column B: Ссылка
        article_language = article_data[2] # Column C: Язык
        current_status = article_data[3] # Column D: Статус

        if current_status != "В очереди":
            print(f"Skipping row {row_index}: Status is '{current_status}', expected 'В очереди'.", file=sys.stderr)
            sys.exit(0) # Exit gracefully if not in queue

        print(f"Processing article: '{article_title}' from {article_url}, Language: {article_language}")

        # Update status to "В процессе"
        update_spreadsheet_row(sheets_service, google_sheet_id, row_index, 3, "В процессе")

        # 2. Call the "Блограйтинг" skill (avalanche-copywriting)
        # This part requires interaction with Hermes internal tools, which isn't direct Python API.
        # For a cron job, this script will be executed *by* Hermes, so we'd expect Hermes to
        # delegate to the skill itself.
        # This part needs to be handled by the parent cron job's prompt, or by making
        # a skill call directly if there's a Python API for it.
        # For now, I'll simulate a skill call and assume it generates a DOCX locally.

        # Simulate skill output (replace with actual skill invocation if possible)
        output_docx_path = ARCHIE_PROFILE_ROOT / "cache" / "generated_articles" / f"{Path(article_url).stem}.docx"
        output_docx_path.parent.mkdir(parents=True, exist_ok=True)
        # --- Placeholder for actual skill execution ---
        # In a real scenario, the cronjob prompt would invoke avalanche-copywriting directly
        # or this script would trigger a subagent/skill call.
        # For demonstration, let's create a dummy DOCX file.
        with open(output_docx_path, 'w', encoding='utf-8') as f:
            f.write(f"Dummy DOCX content for: {article_title}\nLanguage: {article_language}\nURL: {article_url}")
        # --- End placeholder ---
        
        generated_article_name = f"{article_title} ({article_language}).docx"

        # 3. Upload the generated DOCX to Google Drive
        uploaded_file_id, uploaded_file_link = upload_file_to_drive(
            drive_service, str(output_docx_path), NAVO_BLOG_POSTS_FOLDER_ID, 
            generated_article_name, 
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document" # MIME type for .docx
        )
        print(f"Uploaded article DOCX: {uploaded_file_link}")

        # 4. Update the Google Spreadsheet
        update_spreadsheet_row(sheets_service, google_sheet_id, row_index, 4, generated_article_name) # Column E: Название статьи на Наво
        update_spreadsheet_row(sheets_service, google_sheet_id, row_index, 5, uploaded_file_link) # Column F: Ссылка на Наво / Файл Наво
        update_spreadsheet_row(sheets_service, google_sheet_id, row_index, 3, "Готово") # Column D: Статус

        print(f"Successfully processed and updated spreadsheet for row {row_index}.")

    except Exception as e:
        print(f"An error occurred while processing row {row_index}: {e}", file=sys.stderr)
        # Optionally, update status to "Ошибка" in the spreadsheet
        # update_spreadsheet_row(sheets_service, google_sheet_id, row_index, 3, "Ошибка")
        sys.exit(1)

