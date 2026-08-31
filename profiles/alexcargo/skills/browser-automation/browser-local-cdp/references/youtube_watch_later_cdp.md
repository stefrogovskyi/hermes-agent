# YouTube Watch Later Automation & CDP Workaround

## Key Findings & API Limitations

1. **YouTube Data API v3 Restriction (`playlistId=WL`):**
   - Direct API calls to `playlistId=WL` return `200 OK` but `0 items` due to Google API privacy restrictions introduced in 2020.
   - `channels?mine=true&part=contentDetails` no longer returns `watchLater` in `relatedPlaylists`.
   - API `playlistItems.delete` fails on `WL` item IDs for the same reason.

2. **Automated Dual-Mode Solution via Playwright Chromium + Data API:**
   - **Profile Directory:** `C:\Users\Stefan\AppData\Local\hermes\chrome_youtube_user_data`.
   - **Reading Watch Later:** Open `https://www.youtube.com/playlist?list=WL` via Playwright Chromium with persistent context. Scroll down multiple times (`page.mouse.wheel(0, 2000)`) to load the full DOM.
   - **User Preference (DO NOT TRUNCATE):** Never limit the output to 10 items — display 100% of all videos present in the playlist.
   - **Moving Videos to Target Playlists (`Listen`, `Quick watch`, `Guitar`, etc.):** Use YouTube Data API v3 (`playlistItems.insert`) — 100% fast and reliable.
   - **Deleting Videos from Watch Later (`WL`):** MUST be done via Playwright Browser UI clicks on the active DOM:
     - `container = page.query_selector(f"ytd-playlist-video-renderer:has(a[href*='{vid}'])")`
     - `container.hover()`
     - Click 3-dots action menu button (`yt-icon-button#button`)
     - Click `"Remove from Watch Later"` / `"Удалить из «Смотреть позже»"`
     - This physically deletes the video in Google's cloud profile, syncing across all user devices (including mobile phones!).

3. **Interactive Daily Guardrail (23:00 Evening Review):**
   - At 23:00, generate a complete numbered list of ALL videos (`1`, `2`, `3`...) with durations and channels.
   - Deliver digest to user in Telegram DM.
   - **STRICT RULE:** Never move, delete, or summarize videos without explicit user reply commands (e.g. `"1, 2 in Guitar, 3 summarize, 4 delete"`).
