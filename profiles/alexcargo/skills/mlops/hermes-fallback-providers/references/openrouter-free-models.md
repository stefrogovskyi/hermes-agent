# OpenRouter Free Models — verified 2026-08-28

All models below were liveness-tested against OpenRouter API (`prompt=$0 / completion=$0`).
Context = input context window.

| # | Model (OpenRouter id) | Context | Status | Class / Notes |
|---|---|---|---|---|
| 1 | `nvidia/nemotron-3-super-120b-a12b:free` | 262,144 | 200 (LIVE) | 120B NVIDIA Super Model |
| 2 | `google/gemma-4-31b-it:free` | 262,144 | 200 (LIVE) | Google Gemma 4 31B |
| 3 | `google/gemma-4-26b-a4b-it:free` | 262,144 | 200 (LIVE) | Google Gemma 4 26B MoE |
| 4 | `minimax/minimax-m3:free` | 1,048,576 | 200 (LIVE) | MiniMax M3 (1M context) |
| 5 | `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free` | 256,000 | 200 (LIVE) | NVIDIA 30B Reasoning |
| 6 | `minimax/minimax-m2.7:free` | 196,608 | 200 (LIVE) | MiniMax M2.7 |
| 7 | `poolside/laguna-s-2.1:free` | 262,144 | Rate-limited / 429 | Poolside Coding Model |
| 8 | `z-ai/glm-5.2:free` | 256,000 | Rate-limited / 429 | Z.ai GLM 5.2 |

Excluded from text fallback: `lyria-3*` (music/audio), `nemotron-3.5-content-safety:free` (classifier), `nemotron-nano-12b-v2-vl` (vision only).

Documented account-wide free-tier limits: ~20 requests/min, ~200 requests/day.
