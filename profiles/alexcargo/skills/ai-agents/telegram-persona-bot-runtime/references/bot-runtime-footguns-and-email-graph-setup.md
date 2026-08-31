# Bot Runtime Footguns, Voice Keys & MS Graph Email Setup

## 1. Module-Level MODEL Evaluation Before `_load_env()`
If `MODEL = os.environ.get("MODEL", "default")` is declared at module top BEFORE `_load_env()` is called, Python evaluates `MODEL` at import time with unpopulated environment variables.
This causes the bot to attempt dead/missing fallback models (e.g. `tencent/hy3:free`), incurring 15s+ retry delays per request and triggering error fallback stubs (*"Richard here — briefly lost the line to the desk"*).

**Fix Pattern:**
Always call `_load_env()` at the very top of the script before reading environment variables or initializing module-level LLM clients.

```python
def _load_env():
    here = os.path.dirname(os.path.abspath(__file__))
    for envf in (".env", ".env.local"):
        p = os.path.join(here, envf)
        if os.path.exists(p):
            with open(p, encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        os.environ[k.strip()] = v.strip().strip('"').strip("'")

_load_env()  # Run immediately on module import!
```

## 2. OpenAI Key Keyname Mismatch for Whisper & TTS
If `openai_key()` looks strictly for `OPENAI_API_KEY` but the host environment stores the key in `VOICE_TOOLS_OPENAI_KEY`, audio transcription (Whisper) and speech synthesis (TTS) silently fail without raising fatal errors, causing voice messages to be ignored or failing to send voice replies.

**Fix Pattern:**
```python
def openai_key():
    k = os.environ.get("OPENAI_API_KEY", "") or os.environ.get("VOICE_TOOLS_OPENAI_KEY", "")
    if k and not k.startswith("stub-"):
        return k
    env_p = r"C:\Users\Stefan\AppData\Local\hermes\.env"
    if os.path.exists(env_p):
        for line in open(env_p, encoding="utf-8", errors="ignore"):
            line = line.strip()
            if line.startswith("VOICE_TOOLS_OPENAI_KEY=") or line.startswith("OPENAI_API_KEY="):
                val = line.split("=", 1)[1].strip()
                if val and not val.startswith("stub-"):
                    return val
    return ""
```

## 3. Microsoft 365 Exchange Online Basic Auth vs Graph API
Exchange Online rejects legacy IMAP Basic Authentication with `b'AUTHENTICATE failed'` due to Azure AD Security Defaults, even when IMAP is checked in Microsoft 365 Admin Center.

**Fix Pattern (Microsoft Graph API OAuth2):**
Use Microsoft Graph API with Application Permissions (`Mail.Read` / `Mail.ReadWrite`) + Admin Consent:
1. Register Azure App (`App Registrations`).
2. Add `Mail.Read` under **Application permissions** (not Delegated!).
3. Click **Grant admin consent for <Tenant>**.
4. Authenticate via Client Credentials flow:
```python
url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
payload = urllib.parse.urlencode({
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "scope": "https://graph.microsoft.com/.default",
    "grant_type": "client_credentials"
})
```

## 4. Outlook Corporate Signature Rule
When sending via Outlook / Exchange / Microsoft Graph API:
Never append custom/fake text signature footers in the email body (e.g. `Richard Marlowe / Navo24 Sales Engine`).
End the email body with a simple closing (e.g. `Best regards, Richard`), letting Outlook's native pre-configured HTML signature attach automatically.
