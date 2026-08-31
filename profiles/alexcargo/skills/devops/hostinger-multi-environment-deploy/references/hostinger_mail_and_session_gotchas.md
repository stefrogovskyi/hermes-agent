# Hostinger Mail & Session Architecture Gotchas

## 1. Hostinger Linux Sendmail Line Endings (\n vs \r\n)
On Hostinger PHP mailers, email headers MUST use **LF (`\n`) line endings**, NOT `\r\n` (CRLF). 
Header strings formatted with `\r\n` cause Hostinger sendmail to reject the headers and return `false`. 
Header strings formatted with `\n` return `true` and deliver reliably.

```php
$client_headers = "From: Avalanche Agency <info@aavalanche.com>\n";
$client_headers .= "Reply-To: info@aavalanche.com\n";
$client_headers .= "MIME-Version: 1.0\n";
$client_headers .= "Content-Type: text/html; charset=UTF-8\n";

$r = mail($email, $subject, $body, $client_headers);
```

## 2. Active Registered Sender Address
The `From:` address in `mail()` MUST be an active registered mailbox on Hostinger (e.g. `From: info@aavalanche.com`), not an unconfigured alias like `noreply@`. Unregistered aliases are dropped by Hostinger's outbound mail filter.

## 3. Persistent Single-Domain Auth Sessions across Language Subfolders
In `auth.php`, configure `ini_set('session.cookie_path', '/')` and `session_set_cookie_params(['path' => '/', 'samesite' => 'Lax'])` before `session_start()`. This guarantees the `PHPSESSID` cookie is valid across all language subfolders (`/uk/`, `/es/`, `/de/`, etc.) so users are NOT logged out when switching site languages.
