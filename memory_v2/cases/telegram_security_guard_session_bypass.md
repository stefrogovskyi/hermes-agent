# Case: Telegram Security Guard OTP Invalidation & Session File Auth

## Context
When attempting to log into a Telegram userbot (`@stefrogovskiy`) by having the user paste the 5-digit OTP verification code sent by Telegram (777000) directly into Telegram chat, Telegram Security Guard automatically identified the code in message text.

## Root Cause
Telegram System Bot (777000) monitors chat messages for login code strings. If an OTP code appears in plain chat text, Telegram flags it as a compromised credential, immediately invalidates the code, and blocks the new device login attempt from the server IP.

## Resolution
1. Abandoned inline chat OTP code login.
2. Transferred the pre-authenticated Telethon session file (`router_telethon_session.session`) directly from Stefan's local machine via Tailscale / Telegram document upload.
3. Placed session file at `/opt/hermes/stefan_userbot.session`.
4. Successfully initialized userbot connection for "Не повредит, Одесса" channel parser without triggering OTP code generation or Security Guard blocks.
