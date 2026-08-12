# Callum Vance Memory & Tech Directives

- **Role**: Tech Lead & Full-Stack Engineer for Avalanche Agency and Navo24.
- **Hostinger Production / Staging Server**:
  - SSH Host: `82.29.199.155:65002` (user `u473746908`, password `Stefrogovskyi#1`).
  - Production Path: `/home/u473746908/domains/aavalanche.com/public_html/`
  - Staging Path: `/home/u473746908/domains/aavalanche.com/public_html/staging/`
  - Dev Path: `/home/u473746908/domains/aavalanche.com/public_html/dev/`
- **Mailer Configuration**:
  - `send_mail.php` MUST use `$from_email = 'info@aavalanche.com'` and LF (`\n`) line endings for Hostinger sendmail.
- **GitHub Repository**:
  - Repo: `stefrogovskiy/aavalanche-website`
  - Always perform `git commit` & `git push origin main` on all code changes automatically.
