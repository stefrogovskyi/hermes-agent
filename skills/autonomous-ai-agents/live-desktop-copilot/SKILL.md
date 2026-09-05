---
name: live-desktop-copilot
description: "Live screen-sharing voice copilot with visual grounding."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows, macos, linux]
metadata:
  hermes:
    tags: [screen-sharing, voice-agent, copilot, gemini-live, webrtc, visual-reasoning]
    category: autonomous-ai-agents
    related_skills: [computer-use]
---

# Live Desktop Copilot (Realtime Screen-Sharing + Voice Assistant)

## When to Use
Use when building, deploying, or troubleshooting an interactive screen-sharing voice copilot where an AI agent sees the user's desktop/browser screen, listens to voice queries, and guides the user verbally through software, portals, or workflows.

## Critical Pitfalls & Lessons Learned

### 1. Browser Media Security Constraints (W3C Secure Context)
- `navigator.mediaDevices.getDisplayMedia` and `getUserMedia` require a **Secure Context**.
- They work seamlessly over `http://localhost:<port>` or `https://<ip_or_domain>:<port>`.
- Opening a LAN/Tailscale IP over plain `http://` (e.g. `http://100.79.157.46:8765`) throws:
  ```
  TypeError: Cannot read properties of undefined (reading 'getDisplayMedia')
  ```
- **Rule:** Direct users to `http://localhost:<port>` on the local machine, or install a local SSL certificate (`https://`) when accessing across LAN/Tailscale. See `references/ssl-tailscale-webrtc.md` for the automated Python SAN certificate recipe and aiohttp SSL setup.

### 2. The "Stupid Model" Trap in Speech-to-Speech Endpoints
- Raw low-latency speech-to-speech models (like basic Bidi WebSockets with native audio) prioritize 300ms latency over reasoning.
- In complex or unfamiliar software interfaces, raw speech models lack search grounding: they guess buttons by trial-and-error, hallucinate menus, fail to keep context, and loop repeatedly.
- **Solution:** Use a 2-tier architecture:
  - **Brain:** Flagship multimodal model with deep visual reasoning (`gemini-3.8-flash` or `gemini-2.5-pro`).
  - **Grounding:** Mandatory **Google Search Grounding** (`tools: [{"google_search": {}}]`). When asked about a specific portal (e.g., Stripe, Cloudflare, CRM, 1C), the model pulls exact current documentation before answering.
  - **Context:** Maintain a session history buffer (last 10 turns with image snapshots) so the copilot remembers past actions and does not repeat failed steps.
  - **Voice:** Neural TTS (e.g., Edge-TTS `ru-RU-DmitryNeural`) delivering clean, professional audio back to the client.

### 3. Windows Desktop Capture Boundaries
- `cua-driver` and `ImageGrab`/`pyautogui` run in Session 0 when invoked from headless Windows SSH services, failing screen capture without an interactive console session.
- Browser-based `getDisplayMedia` runs directly in the user's interactive Windows Desktop (Session 1), giving full access to "Entire Screen" across all native applications without OS permission blocks.

### 4. WebSocket Disconnects & Multi-Part Candidate Parsing
- **Heartbeat Requirement:** `aiohttp` and browsers drop idle WebSockets after ~15-30s. The client must emit a periodic JSON ping (e.g. every 10s) with a server pong reply to keep the copilot session alive indefinitely.
- **Thought Signature & Empty Text Bug:** Models like `gemini-3.8-flash` return structured candidate parts including `thoughtSignature` and separate text chunks. Reading only `candidate['content']['parts'][0]['text']` fails when the first part is empty thoughts/search queries, leading to false "Could not recognize screen" errors. Always filter and join all parts: `text_parts = [p.get('text', '') for p in parts if p.get('text')]`.
- **Dual-Port Binding (Localhost vs Tailscale):** To eliminate self-signed certificate SSL mismatch errors (`wss://localhost` refusing connection due to cert hostname), run a dual-listener in `aiohttp`:
  - Port `8766`: Plain HTTP/WS bound to `0.0.0.0` (for zero-config local desktop browser use).
  - Port `8765`: HTTPS/WSS with SAN SSL certificate (for Tailscale / remote LAN access).
  - Starter template ready at `templates/copilot-server-template.py`.
- Automated Telethon user-session group parsing and historical VOC research reference ready at `references/telegram_group_scraping_and_voc_audit.md`.

### 5. Latency & Context Ballooning (The "1-Minute Delay" Trap)
- **Problem:** When transmitting full 1080p/1440p frames on every user turn and keeping them in conversation history, the payload sent to the multimodal API balloons to several megabytes. Compounded by long text generation and TTS, round-trip latency explodes from 2s to 45–60s.
- **Fixes:**
  - **Single Active Image In History:** Strip heavy base64 `inline_data` from all previous turns in `conversation_history` before sending to the model; retain ONLY the image in the current active user turn. Keep preceding turns as text-only context.
  - **Resolution & Compression:** Scale canvas captures to `960x540` at `0.5` JPEG quality (~35 KB vs 400 KB+). UI text and buttons remain crystal clear, but transfer is instantaneous.
  - **Direct Concise Prompting:** Set `maxOutputTokens: 200–300` and instruct the system prompt to give 1–2 crisp, direct sentences.

### 6. Speech Sanitization & Echo-Interruption Trap
- **The "Asterisk Asterisk" Annoyance:** Multimodal models format text in Markdown (`**bold**`, `#`, lists). Neural TTS engines read these literally as *"звездочка звездочка"* (asterisk asterisk). Strip markdown syntax via regex (`re.sub(r'[*_#`~>\[\]()\\-]', ' ', raw_reply)`) and strictly instruct the prompt to avoid markdown formatting.
- **Microphone Acoustic Echo Loop (The Mid-Sentence Abort Bug):** If the browser's `SpeechRecognition` remains active while the speaker plays TTS audio, the microphone hears the AI's own voice, interprets it as a new speech input from the user, and triggers `currentAudio.pause()` mid-sentence, cutting off the copilot.
  - **Fix:** Temporarily pause speech recognition while `audio.play()` is active, or track an `isSpeaking` flag and ignore incoming speech transcripts until playback ends. Convert audio base64 to a `Blob URL` (`URL.createObjectURL(blob)`) to guarantee smooth, unclipped hardware playback.
- **Deep Reasoning Requirement:** For complex, custom, or desktop applications, Flash-tier models lack deep visual reasoning and make shallow guesses. Deploy `gemini-2.5-pro` with visual grounding for high-accuracy guidance without trial-and-error hallucinations.

### 7. Full Agent Identity & Long-Term Context Preservation
- **Pitfall (The "Generic Bot Regression"):** When troubleshooting network/audio transport, engineers often strip the system prompt down to a minimal stub ("You are a helpful assistant"). This instantly strips the agent of its identity, domain knowledge, and organizational memory.
- **Rule:** The copilot server's initial system prompt must explicitly embed the agent's full persona, domain memory (e.g. Navo business goals, sub-agent roles, active tech stack), and guidelines. When the user shares their screen showing internal dashboards or codebases, the agent must instantly recognize the project and its context rather than treating it as an unfamiliar generic interface.

### 8. The "Glass Overlay" & Touchpad Lockup Pitfall on Windows (Hardware Driver vs RAM vs Overlays)
- **Symptom:** The user reports a "sheet of glass over the desktop" where Windows and applications stop responding to single/double taps or multi-finger gestures on the Precision Touchpad; only hard mechanical clicks register. Four-finger and swipe gestures fail completely.
- **Root Cause Analysis (Do not blame RAM prematurely):**
  Even under 97–99% RAM load, Windows handles touch taps normally under healthy conditions. The real culprits in order of probability:
  1. **Hardware / Device Driver Freeze (ASUS / Precision Touchpad on I2C HID):** Physical clicks run through the standard mouse pipeline (`HID-compliant mouse`), while taps and gestures run through the manufacturer's Precision Touchpad controller (`ASUS Precision Touchpad [HID\ASUE140D&COL02...]` over `I2C HID [ACPI\ASUE140D...]`). When the touchpad interrupt hangs, tap/gesture reporting halts completely while physical clicks continue to work.
  2. **Invisible Fullscreen Overlays:** `TextInputHost.exe` (Windows Input Experience / Touch Keyboard), `TabTip.exe`, `ShellHost.exe`, or CUA/automation cursor overlays (`Cua.AgentCursorOverlay.default` 2880x1800) create invisible top-level windows intercepting touch events.
- **Proven Recovery Protocol (Run via remote PowerShell/SSH):**
  1. **Kill Overlays:**
     ```cmd
     taskkill /f /im TextInputHost.exe & taskkill /f /im TabTip.exe & taskkill /f /im ShellHost.exe
     ```
  2. **Cycle the Hardware Touchpad Driver (PnP Device Re-initialization):**
     ```powershell
     $tp = Get-PnpDevice -FriendlyName "*Precision Touchpad*" -ErrorAction SilentlyContinue
     if ($tp) {
         Disable-PnpDevice -InstanceId $tp.InstanceId -Confirm:$false
         Start-Sleep -Seconds 1
         Enable-PnpDevice -InstanceId $tp.InstanceId -Confirm:$false
     }
     ```
  3. **Force-Flush Touchpad Registry & Notify Win32 Subsystem:**
     Toggle `TapsEnabled` in registry and broadcast `WM_SETTINGCHANGE` (0x001A) to all top-level windows via `SendMessageTimeout`:
     ```powershell
     $path = "HKCU:\Software\Microsoft\Windows\CurrentVersion\PrecisionTouchPad"
     Set-ItemProperty -Path $path -Name "TapsEnabled" -Value 1
     Set-ItemProperty -Path $path -Name "TwoFingerTapEnabled" -Value 1
     Set-ItemProperty -Path $path -Name "TapAndDrag" -Value 1
     Add-Type @"
     using System; using System.Runtime.InteropServices;
     public class Notifier {
         [DllImport("user32.dll", SetLastError=true, CharSet=CharSet.Auto)]
         public static extern IntPtr SendMessageTimeout(IntPtr hWnd, uint Msg, UIntPtr wParam, string lParam, uint fuFlags, uint uTimeout, out UIntPtr lpdwResult);
     }
     "@
     $res = [UIntPtr]::Zero
     [Notifier]::SendMessageTimeout([IntPtr]0xffff, 0x001A, [UIntPtr]::Zero, "PrecisionTouchPad", 2, 1000, [ref]$res)
     ```
- **CRITICAL WARNING — Do NOT kill `explorer.exe` over headless SSH:**
  Terminating `explorer.exe` from an SSH / Session 0 console kills the user's interactive Windows shell (Taskbar, Desktop icons) in Session 1. Re-launching `explorer.exe` from an SSH service fails to bind back to the interactive Session 1 due to Windows session isolation boundaries. Always target the specific driver and overlay processes.

