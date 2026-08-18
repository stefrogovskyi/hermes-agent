# AI Copywriting & Human Style Priming Guide

## Why Abstract Rules Produce "90% AI" Text
When an LLM is given an 8-step algorithm or checklist without reference text, it applies the rules using its statistical baseline prose style. This results in "90% AI-sounding" text full of corporate clichés, robotic transitions, and structured bullet points.

## How to Teach an AI Agent a Human Style (Few-Shot Style Priming)

1. **Few-Shot Human Examples (Primary Mechanism):**
   - Provide 2–3 real human articles written by the target author inside `HUMAN_STYLE_GUIDE.md` or the prompt.
   - LLMs learn rhythm, sentence length, tone, humor, and vocabulary from reference text, not from abstract checklists.

2. **Model Choice Matters (Claude Sonnet vs Gemini/GPT):**
   - **Claude 3.5 Sonnet / Claude 3.7 Sonnet** has an exceptionally natural prose baseline with minimal robotic AI-isms.
   - **Gemini Flash / GPT-4o-mini** default to bulleted, structured, corporate phrasing unless constrained with negative prompts and few-shot human text.

3. **Anti-AI Negative Prompting:**
   - Explicitly ban high-frequency AI words: "в современном мире", "ключевой аспект", "погрузимся в", "важно отметить", "трансформация", "экосистема", "подчеркивает", "стоит отметить", "нельзя не упомянуть".
   - Prohibit decorative em dashes, excessive bolding, forced sub-bullets for every sentence, and cliché concluding slogans ("будущее уже наступило").

4. **Two-Pass Generation (Draft -> Anti-AI Polish):**
   - **Pass 1:** Generate initial draft for factual structure and ideas.
   - **Pass 2 (Self-Editing Pass):** Re-read the draft against the human style samples, strip remaining AI tells, and rewrite in active, personal voice.
