#!/usr/bin/env python3
"""google_reauth.py — переавторизация Google OAuth с полным набором скоупов
(Workspace + YouTube, чтобы не сломать youtube_playlist_sorter).
Использование:
  --auth-url            печатает ссылку для Стефана
  --auth-code "<url>"   обменивает код/redirect-URL на токен
"""
import json, sys
from pathlib import Path

HH = Path("/opt/hermes")
TOKEN = HH / "google_token.json"
SECRET = HH / "google_client_secret.json"
PENDING = HH / "google_oauth_pending_reauth.json"

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/contacts.readonly",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.force-ssl",
]
REDIRECT = "http://localhost:1"

sys.path.insert(0, str(HH / "hermes-agent"))
from google_auth_oauthlib.flow import Flow  # noqa: E402


def make_flow():
    return Flow.from_client_secrets_file(str(SECRET), scopes=SCOPES, redirect_uri=REDIRECT)


def auth_url():
    flow = make_flow()
    url, state = flow.authorization_url(access_type="offline", prompt="consent", include_granted_scopes="true")
    # ВАЖНО: сохраняем PKCE code_verifier — без него обмен кода в новом
    # процессе падает с "Missing code verifier"
    PENDING.write_text(json.dumps({"state": state, "code_verifier": flow.code_verifier}))
    print(url)


def auth_code(raw: str):
    code = raw.strip()
    if "code=" in code:
        from urllib.parse import urlparse, parse_qs
        code = parse_qs(urlparse(code).query)["code"][0]
    flow = make_flow()
    if PENDING.exists():
        pend = json.loads(PENDING.read_text())
        if pend.get("code_verifier"):
            flow.code_verifier = pend["code_verifier"]
    flow.fetch_token(code=code)
    creds = flow.credentials
    data = {
        "token": creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri": creds.token_uri,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "scopes": list(creds.scopes or SCOPES),
        "expiry": creds.expiry.isoformat() + "Z" if creds.expiry else None,
    }
    if TOKEN.exists():
        TOKEN.rename(TOKEN.with_suffix(".json.old"))
    TOKEN.write_text(json.dumps(data, indent=2))
    PENDING.unlink(missing_ok=True)
    print("TOKEN_SAVED refresh_token=", bool(creds.refresh_token), " scopes=", len(data["scopes"]))


if __name__ == "__main__":
    if sys.argv[1] == "--auth-url":
        auth_url()
    elif sys.argv[1] == "--auth-code":
        auth_code(sys.argv[2])
