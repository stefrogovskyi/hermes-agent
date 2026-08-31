# Hostinger Subdomains, Multi-Environment Deployments & SPA .htaccess Routing

## Architecture on Hostinger Web Hosting
On Hostinger hPanel, creating subdomains (`dev.aavalanche.com`, `staging.aavalanche.com`) under a primary domain (`aavalanche.com`) creates document root directories inside `/public_html/`:
- **Production (`aavalanche.com`):** `/home/<user>/domains/<domain>/public_html/`
- **Dev Environment (`dev.aavalanche.com`):** `/home/<user>/domains/<domain>/public_html/dev/`
- **Staging Environment (`staging.aavalanche.com`):** `/home/<user>/domains/<domain>/public_html/staging/`

### Direct Access vs Subdomain DNS
1. **Subfolder URL (Immediate):** `https://aavalanche.com/dev/` works immediately via Apache file path.
2. **Subdomain URL (`dev.aavalanche.com`):** Requires adding a DNS **A-record** in Hostinger hPanel DNS Zone Editor pointing `dev` to the server IP (`185.170.199.230` or `82.29.199.155`).

---

## Apache `.htaccess` Routing Rules

### 1. Indexing Protection for Dev / Staging
Always inject `X-Robots-Tag` header in `.htaccess` to block search engine indexing on dev and staging:
```apache
<IfModule mod_headers.c>
  Header set X-Robots-Tag "noindex, nofollow"
</IfModule>
```

### 2. Static Page Mapping for Extensionless URLs
When serving standalone HTML pages (`services.html`, `pricing.html`, `about.html`, `contact.html`) alongside a custom `index.html`, map the clean extensionless URLs directly to their static `.html` files FIRST before fallbacks:
```apache
<IfModule mod_rewrite.c>
  RewriteEngine On
  Header set X-Robots-Tag "noindex, nofollow"
  RewriteBase /dev/

  # Direct static page mapping
  RewriteRule ^services/?$ services.html [L,QSA]
  RewriteRule ^pricing/?$ pricing.html [L,QSA]
  RewriteRule ^about/?$ about.html [L,QSA]
  RewriteRule ^contact/?$ contact.html [L,QSA]

  # Allow direct access to existing physical assets (assets/, images/, logo.png)
  RewriteCond %{REQUEST_FILENAME} -f [OR]
  RewriteCond %{REQUEST_FILENAME} -d
  RewriteRule ^ - [L]
</IfModule>
```

### 3. Pure Single-Page Application (React / Vue SPA) Fallback
If the subpages are managed by client-side React Router:
```apache
<IfModule mod_rewrite.c>
  RewriteEngine On
  Header set X-Robots-Tag "noindex, nofollow"

  RewriteCond %{REQUEST_FILENAME} -f [OR]
  RewriteCond %{REQUEST_FILENAME} -d
  RewriteRule ^ - [L]

  # Rewrite all non-asset requests to index.html
  RewriteRule ^ index.html [L]
</IfModule>
```

---

## Modular Layout Architecture
When updating specific pages or blocks:
1. **Shared Layout Components (100% Untouched):**
   - **Header (`header.html`):** Sticky top bar, logo badge, clean menu links (Services, Pricing, About, Contact), vector SVG flags language dropdown.
   - **Footer (`footer.html`):** Dark charcoal footer, logo, address, contact email/phone, social links, copyright.
2. **Page Content Files (Isolated):**
   - Keep page-specific body content (`services_content.html`, `pricing_content.html`, `about_content.html`, `contact_content.html`) separated from shared layout code.
3. **Relative Navigation Links:**
   - Convert all internal links to relative paths (`href="services.html"`, `href="pricing.html"`) so they navigate natively inside the active environment (`dev`, `staging`, or `prod`) without crossing over.

---

## Deployment & Versioning Workflow
- Always report the active Git commit SHA (`📌 ACTIVE GIT COMMIT SHA: <sha>`) in every deployment summary.
- Perform SFTP/SSH uploads over paramiko / scp with error checks.
