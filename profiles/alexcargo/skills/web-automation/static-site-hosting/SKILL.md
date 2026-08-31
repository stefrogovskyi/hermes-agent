---
name: static-site-hosting
description: Publish static HTML to a free URL, no public GitHub repo.
version: 1.0.0
author: hermes
license: MIT
platforms: [linux, macos, windows]
tags: [hosting, static-site, deploy, surge, neocities, preview-link, no-github]
---

# Static Site Hosting (no public GitHub repo)

Use when the user wants to *view* a built HTML page at a URL ("залей на ссылку",
"give me a link to see it") but does NOT want a public GitHub repository.

## When to use
- "Publish this landing page so I can see it" + "no public GitHub repos".
- Sharing a design artifact (claude-design output, prototype) for review.
- Any one-off static HTML that needs a live URL, not a repo.

## Vercel Deployment (Interactive Apps & Serverless APIs)
Install/run: `npx vercel --prod --yes` (or pass folder path `npx vercel "<path>" --prod --yes --name <subdomain>`).

**Non-interactive deploy:**
```bash
npx vercel "<folder_path>" --prod --yes --name <subdomain-name>
```
- Automatically deploys static HTML, Node.js `/api/` serverless functions, and `vercel.json` routing configuration.
- Provides public HTTPS URL: `https://<subdomain-name>.vercel.app`.
- Ideal for standalone Kanban dashboards, interactive Trello-style boards, and self-contained web apps.

## Surge.sh (primary — zero GitHub, free, CLI)
Install: `npm i -g surge` (needs Node/npm; on this Windows host npm global root
is `C:\Users\Stefan\AppData\Roaming\npm`).

**Token without the user pasting a password:**
Surge has NO separate signup endpoint — `POST /token` with email:password
*creates the account and returns a long-lived token* (valid 3 years). So you
can mint a token yourself:
```
curl -s -X POST https://surge.surge.sh/token -u "user@email.com:AnyPass123!"
# -> {"email":"...","token":"<32-hex>","id":"tok-...",...}
```
Save the token locally (e.g. `scripts/_surge_token.txt`) — do NOT echo it to
chat. The user's email is enough; pick any password, you won't store it.

**Non-interactive deploy:**
```
export SURGE_TOKEN="<token>"
cd <folder-with-index.html-or-page.html>
surge . --domain <name>.surge.sh --token "$SURGE_TOKEN"
```
- `--domain` must be a unique `*.surge.sh` subdomain (e.g. `avalanche-hermes.surge.sh`).
- `surge .` publishes the whole dir; deploy one page at a time into its own
  folder, or use distinct `--domain` per variant for A/B compares.
- Output gives "Production: <name>.surge.sh" — that's the public URL.

Pitfalls:
- `surge whoami` / interactive `surge` prompt for email/password → avoid;
  always pass `--token`. Interactive prompts hang in non-interactive agents.
- Unverified surge accounts have tighter publish rate limits — verify the email
  (`POST /verification`) if deploys start failing.
- If you deployed the wrong folder, `surge teardown <domain>.surge.sh --token …`.
- **404 "page not found" after a successful deploy** = Surge served the folder but
  found no `index.html` (the artifact was named `page.html` / `avalanche_hermes.html`
  etc.). Surge only auto-serves `index.html` at the root. Fix: `cp myfile.html
  index.html` in the deploy folder, or name the artifact `index.html` before
  `surge .`. Always open the public URL and confirm 200, not a 404 walrus page.
- `surge .` is slow/times out on large dirs (e.g. a 170 KB HTML with an embedded
  base64 logo). Run the deploy in the background (`terminal(background=true,
  notify_on_complete=true)`) and poll, rather than blocking on a 60s foreground cap.

## Multi-variant A/B compare (the pattern that actually works)
When the user wants to compare designs (e.g. "Claude's version vs mine", or
"redesign vs current"), do NOT overwrite one URL. Deploy each variant to its OWN
subdomain from its OWN folder:
1. Build each variant as `index.html` inside a separate folder (e.g. `avalanche_claude/`,
   `avalanche_hermes/`, `_deploy_redesign/`).
2. `surge <folder> --domain <name>-claude.surge.sh --token "$TOKEN"`,
   `surge <folder> --domain <name>-hermes.surge.sh --token "$TOKEN"`, etc.
3. Hand Stefan the list of URLs. Each is independently viewable; no cross-contamination.
- This also dodges the 404-from-wrong-folder risk: every deploy folder has its own
  `index.html` at root.

## Embed assets as base64 (or they 404)
`surge .` publishes only what is IN the deploy folder. If your HTML references an
external file like `<img src="../assets/logo.png">` or `src="logo.png"` and that file
is NOT inside the deployed folder, the page renders with a BROKEN image (the 404
walrus, but for the asset, not the page). Two fixes:
- Preferred: inline images as `data:image/png;base64,<...>` directly in the HTML
  (a small Python step: `b64=open('logo.png','rb').read()` → replace `src="logo.png"`
  with `src="data:image/png;base64,"+b64`). Then `surge .` carries the image inside
  the single file. Confirmed this session: a Claude-generated page that linked
  `logo.png` externally showed a broken logo until re-inlined.
- Or copy the `assets/` subfolder INTO the deploy folder so the relative path resolves.
- Always open the public URL and confirm the logo/images actually render, not just
  that the page returns 200.

## Neocities (alternative — free, API token from account settings)
- User creates account at neocities.org, generates API key in Settings.
- `npm i -g neocities` then `neocities push <folder> --api-key <key>`.
- Good when Surge is blocked/unavailable; same "no GitHub" property.

- Netlify Drop (manual fallback)
- netlify.com/drop — drag the HTML folder in a browser. Agent can't push
  programmatically without CLI+token; use only if user will do it themselves.

## Hostinger Subdomains & Multi-Environment Deployments
For Hostinger SSH/SFTP deployments to `dev` / `staging` subdomains, `.htaccess` SPA routing, and modular component isolation, see `references/hostinger-subdomains-spa.md`.

## References
- `references/surge-api.md` — exact token-mint + deploy curl/CLI recipes,
  account/verification notes (condensed from surge.sh docs).
- `references/hostinger-subdomains-spa.md` — Hostinger subdomains, `.htaccess` SPA/static routing rules, and modular layout isolation.
