# Aeon Framework CLI & Telegram Integration Reference

## CLI Quick Reference
```bash
# Inspection
./aeon config show
./aeon skills ls
./aeon skills <name>
./aeon secrets ls
./aeon runs ls
./aeon memory search <query>

# Mutation
./aeon skills enable <name>
./aeon skills disable <name>
./aeon skills run <name>
./aeon secrets set <KEY>
./aeon config set model <name>
./aeon sync
```

## Telegram Webhook Setup (`apps/webhook`)
Deploy the Cloudflare Worker to achieve ~1s message latency:
```bash
cd apps/webhook
npm install
npx wrangler secret put TELEGRAM_BOT_TOKEN
npx wrangler secret put TELEGRAM_CHAT_ID
npx wrangler secret put TELEGRAM_ALLOWED_USER_ID
npx wrangler secret put TELEGRAM_WEBHOOK_SECRET
npx wrangler secret put GITHUB_REPO
npx wrangler secret put GITHUB_TOKEN
npx wrangler deploy
```

Register webhook URL with Telegram:
```bash
curl "https://api.telegram.org/bot<TELEGRAM_BOT_TOKEN>/setWebhook?url=https://<worker-subdomain>.workers.dev&secret_token=<TELEGRAM_WEBHOOK_SECRET>"
```
