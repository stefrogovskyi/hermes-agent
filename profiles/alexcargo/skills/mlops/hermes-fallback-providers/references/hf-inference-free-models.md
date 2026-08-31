# Hugging Face — Free Model Reality (verified 2026-07-25)

Context: Stefan asked whether HF serverless API gives free access to "almost 3 million models, even paid ones within limits." Verified with his `HF_TOKEN`.

## Router (serverless) — `router.huggingface.co/v1`
- `GET /v1/models` returns **127 models** (curated integrated providers: together, deepinfra, novita, groq, cerebras, fireworks, featherless-ai, etc.). NOT "3 million" — that is the entire HF Hub (download/finetune), not the serverless API.
- Field `providers[].is_free` is **`false` for ALL 127 models**. Every model is priced (input/output > 0).
- **Conclusion: ZERO free LLMs via HF serverless router.** It is a paid service (billed in HF credits).

## Free Inference API — `api-inference.huggingface.co`
- In Stefan's network this host **does NOT resolve DNS** (`Could not resolve host`; other HF hosts — huggingface.co, router., endpoints. — all 200). Provider-level block on that subdomain. A VPN (WireGuard is installed) would change DNS resolution but still won't yield free chat LLMs.
- Even when reachable, HF free Inference serves **task models, not chat LLMs**: embeddings, sentence-similarity, text-classification, token-classification, translation, summarization, fill-mask, ASR (whisper), TTS, image-classification, object-detection. Chat/text-generation LLM is only via `huggingface.co/chat` web UI, not the API.
- Limits (free HF Inference, documented): ~1 req/s per model, queue, cold start (model unloads after minutes idle → "Model is currently loading"), no SLA, IP-based rate limit. Token quotas unpublished.

## Takeaway for fallback chains
- HF is **NOT** a source of free LLM fallback. Use OpenRouter (see SKILL.md).
- The HF token is still useful as a **paid** provider if HF credits are added (set `HF_TOKEN` + `HF_BASE_URL=https://router.huggingface.co/v1` in `.env`).
