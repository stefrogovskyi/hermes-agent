---
name: canva-connect-api
description: Integrate Canva Connect API for design generation and OAuth.
category: creative
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [canva, oauth, pkce, api, design, automation]
    related_skills: [popular-web-designs, claude-design]
---

# Canva Connect API Integration

Guide for setting up Canva Connect API applications, handling authentication (OAuth 2.0 PKCE), and managing Canva designs, brand templates, and assets programmatically.

## When to Use

Use this skill when setting up or troubleshooting Canva Connect API applications, configuring OAuth 2.0 PKCE authentication, creating Canva developer integrations, or automating Canva design operations.

## Prerequisites & App Creation Steps

### 1. Developer Portal Access
Apps/integrations are created on the **Canva Developer Portal**:
* **URL**: [https://www.canva.com/developers/integrations](https://www.canva.com/developers/integrations)
* *Note*: Do NOT look in user account settings (`canva.com/settings/your-apps`), as creation buttons do not exist there.

### 2. Multi-Factor Authentication (MFA) Requirement & Common Pitfall
Canva requires **Multi-Factor Authentication (MFA)** to be enabled on the account before creating developer integrations.

#### ⚠️ Critical Pitfall: Missing MFA Section (Google SSO / Passkeys)
* **Issue**: If the account was created or logged in using **Google SSO** or **Passkeys**, Canva hides the MFA setup section under *Account & Security*.
* **Resolution**:
  1. Go to **Settings → Login** and set a direct password via **Update password**.
  2. Log out from all devices (**Sign out of all devices**).
  3. Sign back in manually using **Email + Password** (do NOT click *Continue with Google*).
  4. Return to **Account & Security** → the **Multi-Factor Authentication (MFA)** / **Authenticator app** section will now be visible.
  5. Enable MFA using an Authenticator app (e.g. Google Authenticator, 1Password, Authy).

### 3. Creating the Integration
1. Navigate to `canva.com/developers/integrations` and click **Create an integration**.
2. Select **Public** or **Private** (Enterprise).
3. Under **Credentials**, copy the **Client ID** and click **Generate secret** to save the **Client Secret**.
4. Under **Authentication → Authorized redirects**, add your callback URL (for local dev: `http://127.0.0.1:<port>/callback` — note that `localhost` is not allowed).
5. Under **Scopes**, enable required permissions (e.g. `design:content:read`, `design:content:write`, `asset:read`, `asset:write`, `brandtemplate:read`). Note: All requested scopes in the OAuth authorization URL must match what is enabled in the Developer Portal, otherwise Canva returns `invalid_scope`.

---

## OAuth 2.0 PKCE Authentication Flow

Canva Connect API requires OAuth 2.0 Authorization Code flow with **PKCE (S256)**.

### Authorization URL
```text
https://www.canva.com/api/oauth/authorize?code_challenge=<challenge>&code_challenge_method=s256&scope=<scopes>&response_type=code&client_id=<client_id>&redirect_uri=<redirect_uri>
```

### Python PKCE Helper Code
```python
import base64
import hashlib
import os
import secrets
import urllib.parse

def generate_pkce():
    code_verifier = secrets.token_urlsafe(64)
    code_challenge_bytes = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge_bytes).decode('utf-8').replace('=', '')
    return code_verifier, code_challenge

def get_canva_auth_url(client_id, redirect_uri, scopes):
    code_verifier, code_challenge = generate_pkce()
    params = {
        "code_challenge": code_challenge,
        "code_challenge_method": "s256",
        "scope": " ".join(scopes),
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri
    }
    url = f"https://www.canva.com/api/oauth/authorize?{urllib.parse.urlencode(params)}"
    return url, code_verifier
```

### Token Exchange & Refresh Helper (Python)
```python
import base64
import requests

def exchange_code_for_tokens(client_id, client_secret, code, code_verifier, redirect_uri):
    token_url = "https://api.canva.com/rest/v1/oauth/token"
    auth_str = f"{client_id}:{client_secret}"
    b64_auth = base64.b64encode(auth_str.encode()).decode()
    
    headers = {
        "Authorization": f"Basic {b64_auth}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "authorization_code",
        "code_verifier": code_verifier,
        "code": code,
        "redirect_uri": redirect_uri
    }
    res = requests.post(token_url, headers=headers, data=data)
    res.raise_for_status()
    return res.json()  # Returns {'access_token': ..., 'refresh_token': ..., 'expires_in': 14400, ...}

def refresh_access_token(client_id, client_secret, refresh_token):
    token_url = "https://api.canva.com/rest/v1/oauth/token"
    auth_str = f"{client_id}:{client_secret}"
    b64_auth = base64.b64encode(auth_str.encode()).decode()
    
    headers = {
        "Authorization": f"Basic {b64_auth}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }
    res = requests.post(token_url, headers=headers, data=data)
    res.raise_for_status()
    return res.json()
```

---

## Support References

* For detailed error transcripts and step-by-step troubleshooting, see `references/oauth-troubleshooting.md`.
* For binary asset uploads via Python (`POST /v1/asset-uploads`), see `references/asset-upload.md`.
* For Navo24 v5.52 Brand Book specifications, design system templates, and Hostinger `.htaccess` routing fixes, see `references/navo24-brand-guidelines.md`.

## Asset Uploads API (`POST /v1/asset-uploads`)
To upload local PNG/JPG images directly into user's Canva library:
* **Endpoint**: `POST https://api.canva.com/rest/v1/asset-uploads`
* **Headers**:
  * `Authorization: Bearer <token>`
  * `Content-Type: application/octet-stream`
  * `Asset-Upload-Metadata: {"name_base64": "<base64_title>"}`
* **Polling**: Check upload progress via `GET https://api.canva.com/rest/v1/asset-uploads/{job_id}` until `job.status == "success"`.

## Troubleshooting & Best Practices

1. **`invalid_scope` Error**: `Requested scopes are not allowed for this client.`
   * **Cause**: Scopes requested in the `scope` parameter of the Authorization URL are not enabled/checked in the Canva Developer Portal.
   * **Resolution**: Go to `canva.com/developers/integrations` → Select App → **Scopes** → Check all required checkboxes under **Reading and writing** → Click **Save**.
2. **`invalid_field` on `POST /v1/designs`**: `name must be one of the following: doc, email, presentation, whiteboard`
   * **Note**: `POST /v1/designs` currently accepts `preset` names: `doc`, `email`, `presentation`, `whiteboard`. Preset names like `instagram_post` are not direct preset strings for `POST /v1/designs`. Use asset uploads or brand template autofills for custom social media graphics.
3. **Logo & Brand Compliance (Navo24 v5.52)**:
   * **Official Wordmark**: `navo` lowercase wordmark where letter `o` is **The Disc (7 concentric rings)** (`white` → `gold #FFC42E` → `sun #FF7A1F` → `red #E2231A` → `turquoise #12C2C2` → `cobalt #1F4FE6` → `navy #0C2A5E`). Vector SVG: `https://navo24.com/brand/navo-wordmark-white.svg`.
   * **Dark Ground**: Navy-ink `#0A0E16` or `#0C2A5E` (NEVER pure black `#000000`).
   * **Light Ground**: Canvas Paper `#FCFCFB`, `#FFFFFF` cards with hairline border `#E9E8E3`, Signal Soft `#EEF1FE`.
   * **Typography**: Ranade **Ultralight (200, -0.03em)** for display headlines (never bold display headlines!), Switzer for text, JetBrains Mono for eyebrows/metrics (`● EYEBROW`, tracked `+0.14em`).
   * **One-Liner Rule**: Subheads stretch across full measure in a single line. Trim copy until it fits.
   * **No Machine Em-Dashes**: Spaced em-dash (` — `) is banned from prose. Use colons, periods, or semicolons.
4. **Redirect URI Restrictions**: Canva enforces exact match on redirect URIs. `localhost` is rejected; use `http://127.0.0.1:<port>` for local testing.
5. **Client Secret One-Time Display**: Save the Client Secret immediately upon generation as Canva will not display it again.
6. **Token Expiry**: Access tokens expire in 14,400 seconds (4 hours). Use the `refresh_token` flow to maintain persistent access without user re-authentication.
