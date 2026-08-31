---
name: sermon-transcribe-publish
description: "Process Sunday sermon audio recordings for Stefan."
---

# sermon-transcribe-publish

Dedicated weekly Sunday Sermon processing pipeline for Stefan Rogovskiy.

## When to use
- Use every Sunday or whenever Stefan provides a Sunday sermon audio recording (`.ogg`, `.mp3`, `.m4a`, `.wav`).
- User asks to transcribe sermon, generate summary, write reflections, and publish to the Sunday prayer Google Doc.

## The 7-Step Protocol

1. **Transcribe to Russian verbatim:**
   - Wait for complete transcription. Deliver the complete `.txt` transcript file to chat (`MEDIA:` path).
   - Generate an immediate concise summary of the sermon and deliver as a separate `.txt` summary file to chat (`MEDIA:` path).

2. **First-Person Reflection (500 words):**
   - Write a 500-word reflection from the first person ("я", "мы") in a free, human, conversational style.
   - Use original Scripture passages and cited Biblical verses.
   - **CRITICAL:** Do NOT use long em-dashes (`—`). Use hyphens `-` or commas/periods instead.
   - Intentionally allow minor punctuation / phrasing informalities to sound completely human and authentic.

3. **Open Target Google Doc:**
   - Document ID: `1EI9fmDJ1yIdHVVgZ6Jqp086yKE1hN-sYeKCF3E-5uso`
   - Document URL: `https://docs.google.com/document/d/1EI9fmDJ1yIdHVVgZ6Jqp086yKE1hN-sYeKCF3E-5uso/edit?tab=t.0`

4. **Locate Marker & Insert:**
   - Find line `пунктуационные и фразеологические ошибки неточности`.
   - Make a line break under it and insert:
     ```
     Дата: YYYY-MM-DD
     Файл: [имя файла]

     <размышления от первого лица (500 слов)>
     ```
   - **Constraint:** NEVER delete anything from the document — ONLY add/insert under that marker.

5. **Format Header:**
   - Prepend `Дата: YYYY-MM-DD` and `Файл: [имя файла]`.

6. **Verify Insertion:**
   - Re-open/read the Google Doc via API and verify the reflection is completely saved and visible.

7. **Error Recording:**
   - If anything fails, record error in document: `Обработка не завершилась: [имя файла], [дата]`.
