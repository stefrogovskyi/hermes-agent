# Hostinger Subdomain Routing, Caching & Multilingual Single Source of Truth Notes

## 1. Subdomain DocumentRoot & `.htaccess` Double-Prefixing Gotcha
On Hostinger hPanel, when a subdomain (e.g. `dev.aavalanche.com`) is mapped to `/public_html/dev/`, the Apache DocumentRoot for `dev.aavalanche.com` IS ALREADY `/home/u473746908/domains/aavalanche.com/public_html/dev/`.

### ⚠️ The Gotcha
Adding `RewriteBase /dev/` inside `/public_html/dev/.htaccess` causes Apache to append `/dev/` TWICE when requested via the subdomain `dev.aavalanche.com/services`:
- Requested: `https://dev.aavalanche.com/services`
- Rewritten: `https://dev.aavalanche.com/dev/services` -> Hostinger 404 (`htdocs_error/page_not_found.svg`).

### ✅ Known-Good Subdomain `.htaccess`
Omit `RewriteBase /dev/` inside `/public_html/dev/.htaccess`:
```apache
<IfModule mod_rewrite.c>
  RewriteEngine On
  Header set X-Robots-Tag "noindex, nofollow"
  Header set Cache-Control "no-cache, no-store, must-revalidate"
  Header set Pragma "no-cache"
  Header set Expires "0"

  # Direct static page mappings for subdomain dev.aavalanche.com
  RewriteRule ^services(\.html)?$ services.html [L,QSA]
  RewriteRule ^pricing(\.html)?$ pricing.html [L,QSA]
  RewriteRule ^about(\.html)?$ about.html [L,QSA]
  RewriteRule ^contact(\.html)?$ contact.html [L,QSA]

  # Allow direct access to physical static files
  RewriteCond %{REQUEST_FILENAME} -f [OR]
  RewriteCond %{REQUEST_FILENAME} -d
  RewriteRule ^ - [L]
</IfModule>
```

---

## 2. Single Source of Truth & 1-to-1 Multilingual Mirroring

### Rule
The English version (`/` root) is the Single Source of Truth for the entire site structure, DOM geometry, component hierarchy, buttons, cards, headers, and footers.

### Workflow
1. Apply and verify any layout or component changes on the English master version (`index.html`, `services.html`, `pricing.html`, `about.html`, `contact.html`).
2. Mirror the EXACT HTML/CSS structure to all 8 language subfolders (`/es/`, `/de/`, `/fr/`, `/it/`, `/uk/`, `/ru/`, `/zh/`, `/ar/`).
3. ONLY translate the text strings (headings, paragraphs, feature lists, button labels).
4. Never add extra buttons, change card geometry, or alter design on language versions — they must remain 100% mirrored clones.
5. On language subfolder pages, ensure logo images point to relative paths (`../avalanche_logo.png`), and the language selector button dynamically displays the active language flag and code (e.g. 🇪🇸 `ES` on `/es/`).

---

## 3. Contact Form Dual Mailer Configuration (`send_mail.php`)

To support testing contact forms on `dev` without breaking client confirmation:
```php
<?php
header('Content-Type: application/json; charset=utf-8');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    echo json_encode(['status' => 'error', 'message' => 'Invalid request method']);
    exit;
}

$name = isset($_POST['name']) ? trim($_POST['name']) : '';
$email = isset($_POST['email']) ? filter_var(trim($_POST['email']), FILTER_VALIDATE_EMAIL) : false;
$message = isset($_POST['message']) ? trim($_POST['message']) : '';

if (empty($name) || !$email || empty($message)) {
    echo json_encode(['status' => 'error', 'message' => 'Please fill in all required fields.']);
    exit;
}

$from_email = 'noreply@aavalanche.com';
$admin_email = 'dr.reenforce@gmail.com';

// 1. Admin Notification
$admin_subject = "[NEW REQUEST] New Inquiry from " . $name . " - Avalanche Agency";
$admin_body = "Hello Admin,\n\nNew inquiry from Dev site:\nName: " . $name . "\nEmail: " . $email . "\nMessage:\n" . $message;
$admin_headers = "From: Avalanche Agency <" . $from_email . ">\r\nReply-To: " . $email;
@mail($admin_email, $admin_subject, $admin_body, $admin_headers);

// 2. User Confirmation
$user_subject = "Your Request to Avalanche Agency";
$user_body = "Dear " . $name . ",\n\nThank you for contacting Avalanche Agency. We have received your request and will get back to you shortly.";
$user_headers = "From: Avalanche Agency <" . $from_email . ">\r\nReply-To: " . $from_email;
@mail($email, $user_subject, $user_body, $user_headers);

echo json_encode(['status' => 'success', 'message' => 'Your request has been sent! Confirmation sent to ' . $email]);
?>
```
