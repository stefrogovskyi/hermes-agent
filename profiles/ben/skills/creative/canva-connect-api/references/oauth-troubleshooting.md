# Canva Connect API OAuth & Setup Troubleshooting

## Error 1: Missing MFA Creation Button in Account Settings
- **Symptom**: User tries to create developer app or enable MFA, but Canva settings (`canva.com/settings/your-apps` or account settings) does not show Multi-Factor Authentication options.
- **Root Cause**: Canva account was authenticated via Google SSO or Passkey. Canva delegates MFA to Google/passkey manager and hides the native MFA section.
- **Fix**:
  1. Open Canva **Settings → Login**.
  2. Click **Update password** and set a direct password for the account email.
  3. Click **Sign out of all devices**.
  4. Log back in manually with **Email + Password** (do NOT click *Continue with Google*).
  5. Return to **Settings → Account and security**. The **Multi-Factor Authentication (MFA)** section will now be visible.
  6. Enable MFA via Authenticator app (TOTP).

## Error 2: `invalid_scope` (Requested scopes are not allowed for this client)
- **Symptom**: User visits authorization URL and gets redirected to `http://127.0.0.1:8000/callback?error=invalid_scope&error_description=Requested%20scopes%20are%20not%20allowed%20for%20this%20client.`
- **Root Cause**: The authorization URL requested scopes that were not explicitly checked/saved in Canva Developer Portal settings.
- **Fix**:
  1. Open `https://www.canva.com/developers/integrations`.
  2. Click on the integration.
  3. In the left menu, click **Scopes**.
  4. Check the boxes for all required scopes (e.g., `design:content:read`, `design:content:write`, `asset:read`, `asset:write`, `brandtemplate:read`, `brandtemplate:content:read`, etc.).
  5. Click **Save**.
  6. Re-generate the authorization URL with those exact scopes.

## Error 3: Token Exchange Failure (400 Bad Request or 401 Unauthorized)
- **Endpoint**: `POST https://api.canva.com/rest/v1/oauth/token`
- **Headers**: `Authorization: Basic base64(client_id:client_secret)` (HTTP Basic Auth) and `Content-Type: application/x-www-form-urlencoded`.
- **Note**: The authorization code is single-use and expires quickly. Pass the exact `code_verifier` generated alongside the `code_challenge` for PKCE validation.
