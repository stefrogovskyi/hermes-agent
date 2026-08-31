# Surge.sh API recipes (condensed)

Auth forms (HTTP Basic):
- Token: username `token`, password = your API token. Used for everything.
- Email+password: `POST /token` mints a token AND creates the account if email
  is new. Tokens valid 3 years.

## Mint a token (also creates account)
```sh
curl -s -X POST https://surge.surge.sh/token -u "you@example.com:password"
# -> {"email":"...","token":"<32-hex>","id":"tok-...",...}
```
Pick any password; you won't store it. Save token locally, never echo to chat.

## Deploy (non-interactive)
```sh
export SURGE_TOKEN="<token>"
surge . --domain <name>.surge.sh --token "$SURGE_TOKEN"
```
`surge .` publishes cwd. Use a unique `*.surge.sh` subdomain per artifact so
you can host A/B variants side by side.

## Verify email (lifts publish rate limits on new accounts)
```sh
curl -X POST https://surge.surge.sh/verification -u token:<TOKEN>
# 200 {"verified":true} | 201 {"sent":true}
```

## Teardown (remove a bad deploy)
```sh
surge teardown <name>.surge.sh --token "$SURGE_TOKEN"
```

## Notes
- `surge whoami` / bare `surge` prompt interactively — avoid in agents; always
  pass `--token`.
- Install CLI: `npm i -g surge` (Windows npm root:
  `C:\Users\Stefan\AppData\Roaming\npm`).
- Alternative host: Neocities (`npm i -g neocities`, API key from account
  Settings, `neocities push <folder> --api-key <key>`).
