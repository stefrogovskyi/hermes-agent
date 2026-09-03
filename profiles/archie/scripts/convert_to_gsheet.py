
import sys
import os
import json
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from pathlib import Path

# --- Configuration ---
# Correctly building path to profile-specific config files
# ARCHIE_PROFILE_ROOT should be the direct path to the archie profile
ARCHIE_PROFILE_ROOT = Path("/opt/hermes/profiles/archie") # Direct path to archie's profile
GOOGLE_CLIENT_SECRET_PATH = ARCHIE_PROFILE_ROOT / "google_client_secret.json"
GOOGLE_TOKEN_PATH = ARCHIE_PROFILE_ROOT / "google_token.json"

SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets"
]

def get_google_credentials():
    creds = None
    if GOOGLE_TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(GOOGLE_TOKEN_PATH), SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not GOOGLE_CLIENT_SECRET_PATH.exists():
                print(f"Error: Google client secret file not found at {GOOGLE_CLIENT_SECRET_PATH}", file=sys.stderr)
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(str(GOOGLE_CLIENT_SECRET_PATH), SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(GOOGLE_TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())
    return creds

def get_drive_service():
    creds = get_google_credentials()
    return build('drive', 'v3', credentials=creds)

# --- Main script logic ---
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python convert_to_gsheet.py <source_file_id>", file=sys.stderr)
        sys.exit(1)

    source_file_id = sys.argv[1]
    
    drive_service = get_drive_service()

    try:
        # 1. Create a copy of the XLSX file, converting it to Google Sheet format
        file_metadata = {
            'name': 'Блогпосты Сирейтс',
            'mimeType': 'application/vnd.google-apps.spreadsheet'
        }
        copied_file = drive_service.files().copy(
            fileId=source_file_id,
            body=file_metadata,
            fields='id, name, mimeType, webViewLink'
        ).execute()

        new_sheet_id = copied_file.get('id')
        new_sheet_link = copied_file.get('webViewLink')

        print(f"Successfully converted and copied to Google Sheet.")
        print(f"New Google Sheet ID: {new_sheet_id}")
        print(f"New Google Sheet Link: {new_sheet_link}")

        # 2. Delete the original temporary XLSX file
        drive_service.files().delete(fileId=source_file_id).execute()
        print(f"Successfully deleted temporary XLSX file (ID: {source_file_id}).")

    except Exception as e:
        print(f"An error occurred during conversion to Google Sheet: {e}", file=sys.stderr)
        sys.exit(1)
