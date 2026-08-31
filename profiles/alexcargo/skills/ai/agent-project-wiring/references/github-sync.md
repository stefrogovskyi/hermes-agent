# GitHub sync — make a PRIVATE repo the agent project's source of truth

## Why
The live agent project folder (often in OneDrive) is the working copy;
a private GitHub repo under the user's account is the authoritative backup +
version history. Hermes linked-references point at the LIVE files, so a push
keeps repo and agent in lockstep.

## Steps (used for richard-marlowe, user stefrogovskyi)
1. In the project folder: `git init -q`
2. Create private repo (gh must be authed):
   `gh repo create <name> --private --description "..."`
   (Do NOT pass `--source` if the folder is not yet a git repo — it errors.)
3. `git remote add origin https://github.com/<user>/<name>.git`
4. Add `.gitignore` BEFORE first commit:
   ```
   __pycache__/
   .env / *.env / .env.*
   *.log
   .idea/ .vscode/ .DS_Store
   ```
   NEVER commit real API keys — use env vars / secret managers.
5. `git add -A && git -c user.name=.. -c user.email=.. commit -m "..."`
6. `git branch -M main && git push -u origin main`

## Verify after push (ad-hoc, no secrets in output)
- `gh repo view <user>/<name> --json visibility` → must be `PRIVATE`.
- `gh api repos/<user>/<name>/contents --jq '.[].name'` → lists pushed files.
- `git status --porcelain` → empty (working tree clean).

## Gotcha
- `gh repo create --source=.` fails with "current directory is not a git repository"
  if you haven't `git init` first. Init, then create without --source.
- CRLF warnings on Windows are harmless; git normalizes line endings.
- After editing any live file, re-run: `git add -A && git commit && git push`
  so the private repo stays the source of truth.