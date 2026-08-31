---
name: youtube-playlist-automation
description: "Automate YouTube Watch Later and playlist sorting."
---

# youtube-playlist-automation

Class-level workflow for automating YouTube Watch Later playlist extraction, video categorization, AI summarization, and interactive daily review.

## When to use
- User asks to automate YouTube Watch Later or playlist sorting.
- Setting up or executing daily interactive YouTube playlist reviews.

## Key Technical Learnings & Workarounds

### 1. YouTube Data API v3 Watch Later Restriction
- **Problem:** Since 2020, Google's YouTube Data API v3 returns 0 items when querying `playlistId=WL` due to third-party privacy restrictions.
- **Workaround:** Use Playwright Chromium with a persistent profile (`chrome_youtube_user_data`). Navigate to `https://www.youtube.com/playlist?list=WL` and extract video elements (`ytd-playlist-video-renderer`) directly from the DOM.

### 2. Interactive Review Guardrails
- **Schedule:** Evening review at 23:00 MSK. **Cron Note:** Cron schedules in UTC require setting `0 20 * * *` to fire at 23:00 MSK local time (UTC+3).
- **Complete List Rule:** NEVER limit video output to 10 or 15 items — list ALL videos present in the playlist (default `limit=500` in helper scripts). When the user asks if there are more videos, re-scan the live DOM directly without cached limits to extract all present items (e.g. 44+ videos).
- **Move = Delete Rule:** "Move" ALWAYS implies deletion from Watch Later ("Move also always means deletion from watch later"). When moving a video to a target playlist (e.g. "2 move to piano"), automatically remove it from Watch Later.
- **Pre-Offered Categorization:** Save channel-to-playlist mappings in `youtube_sorting_preferences.json`. On future daily reviews, pre-offer the learned categorizations for user approval ("1 -> Piano, 2 -> Guitar; approve?") rather than making them type commands from scratch.
- **Strict Real Playlist Constraint:** Recommendations MUST match ONLY from the user's exact real existing YouTube playlists (retrieved via `youtube.playlists().list(mine=True)`: 49 real playlists saved in `stefan_youtube_playlists.json`: `Programming`, `Automations`, `Moneymaking`, `SeaRates`, `Маркетинг`, `Продажи`, `Biz`, `Investments`, `Productivity`, `Languages`, `Guitar`, `Piano`, `Must watch`, `Must listen`, `Favorites`, etc.). NEVER suggest or invent non-existent playlist names.
- **One-Word Approval ("Да / Ок"):** Format the daily 23:00 digest with pre-offered playlist recommendations for every item so the user can accept all with a single "Да" or customize specific items ("1 да, 2 в Музыку, 3 удалить").
- **Preference Pattern Learning:** Permanently save user sorting preferences (e.g. Upwork/Freelance -> `Moneymaking`/`Quick watch`, Guitar/Music -> `Guitar`, News/Illarionov -> Delete) to memory so the 23:00 cron continually improves its recommendations over time.
- **Strict User Confirmation:** NEVER move or delete any video automatically without explicit user commands or approval ("numbers + actions" or "Да/Ок" on pre-offered proposal).

### 3. Deletion & Cloud Sync Protocol
- **Moving to Playlists:** Use YouTube Data API v3 (`playlistItems.insert`) with `playlistId` for fast, reliable additions. Auto-refresh Google OAuth token (`oauth2.googleapis.com/token`) if API returns 401.
- **Removing from Watch Later:** Use Playwright Browser UI automation. **DOM Selector Gotcha:** Avoid `.hover().click()` on action buttons as hidden elements cause 30000ms Playwright timeouts. Use direct JS evaluation: `item.evaluate('el => { const b = el.querySelector("button#button"); if (b) b.click(); }')` to open the 3-dot menu instantly in headless mode.
- **Telegram Chunking & Escaping:** For 30+ video lists, chunk Telegram messages into <=3800 character blocks and escape HTML entities (`html.escape()`) to prevent 400 Bad Request errors.
- **Batch Operations:** Process multi-item batch commands (e.g. 30+ video moves in a single run) by mapping video numbers to exact YouTube video IDs, refreshing Google OAuth tokens, and automating browser UI removals.
