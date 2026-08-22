---
name: pdf-inspector
description: "Use when inspecting, classifying, and converting PDFs to MD."
version: 1.0.0
author: Firecrawl & Hermes Agent
license: MIT
metadata:
  tags: [pdf, firecrawl, markdown, tables, classification, ocr-routing, extraction]
---

# PDF Inspector (Firecrawl Fast Engine)

`pdf-inspector` is an ultra-fast Rust-native PDF classification and position-aware text/table extractor created by Firecrawl. It operates in **~10-50ms** per document, converting text-based PDFs into clean, structured Markdown (preserving tables, headings, lists, and code blocks) without relying on slow/expensive OCR unless strictly necessary.

## When to Use

- **Document ingestion:** Parsing inbound invoices, bills of lading (BL), financial statements, contracts, shipping reports, and research papers.
- **Smart routing / Classification:** Checking whether a PDF is `TextBased`, `Scanned`, `ImageBased`, or `Mixed` in ~20ms before deciding whether to call heavy OCR/Vision models.
- **Table extraction:** Extracting aligned financial and logistics tables directly into Markdown.

## CLI Usage

A global command `pdf-inspect` is available on the system:

```bash
# 1. Classify PDF type (scanned vs text)
pdf-inspect classify <file.pdf>

# 2. Extract full position-aware Markdown to terminal or file
pdf-inspect markdown <file.pdf> -o output.md

# 3. Extract plain text
pdf-inspect text <file.pdf>
```

## Python API Usage

```python
import pdf_inspector

# 1. Classification & Smart OCR Routing
classification = pdf_inspector.classify_pdf("document.pdf")
print("PDF Type:", classification.pdf_type) # 'text', 'scanned', 'mixed'
print("Confidence:", classification.confidence)

# 2. Fast Markdown Extraction
res = pdf_inspector.extract_pages_markdown("document.pdf")
for page in res.pages:
    print(f"--- Page {page.page} ---")
    print(page.markdown)
    if page.needs_ocr:
        print("⚠️ This page requires OCR fallback!")

# 3. Extract Structured Elements / Positions
elements = pdf_inspector.extract_structure_elements("document.pdf")
```

## Advantages over Standard Parsers

| Feature | `pdf-inspector` | PyPDF / PyMuPDF |
| :--- | :---: | :---: |
| **Speed (200 docs)** | **~0.47s (Rust core)** | ~17.1s |
| **Markdown Output** | Native (H1-H4, Tables, Lists) | Raw Text / Needs conversion |
| **Table Detection** | Rectangle + Text Alignment | Basic / Fails on borderless |
| **Scanned Detection** | Built-in (Confidence score) | Manual heuristics |
