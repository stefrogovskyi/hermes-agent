---
name: defuddle
description: "Extract clean Markdown from web pages via Defuddle CLI."
version: 1.0.0
author: Steph Ango (@kepano, https://github.com/kepano/defuddle)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [obsidian, markdown, readability, scraping, extraction, web]
    category: note-taking
    homepage: https://github.com/kepano/defuddle
    related_skills: [obsidian, web_extract]
---

# Defuddle: Clean Web-to-Markdown Extraction

Extract clean, article-focused markdown content from web pages using Kepano's Defuddle CLI. Removes clutter, ads, footers, headers, cookie banners, and navigation menus to preserve high signal and minimize token usage.

## When to use this skill

Load this skill whenever:
- You need to extract full articles, documentation, or blog posts from a URL into clean Markdown.
- Saving web pages directly into an Obsidian vault with frontmatter.
- A web page contains too much noisy HTML/navigation for standard extractors.

## Command Reference

CLI binary is globally installed at `/usr/bin/defuddle`.

### 1. Extract clean Markdown to stdout
```bash
defuddle parse <url> --md
```

### 2. Save directly to file (e.g. for Obsidian Vault)
```bash
defuddle parse <url> --md -o note.md
```

### 3. Extract specific metadata properties
```bash
defuddle parse <url> -p title
defuddle parse <url> -p description
defuddle parse <url> -p domain
defuddle parse <url> -p author
```

### 4. JSON output (contains metadata, HTML & Markdown)
```bash
defuddle parse <url> --json
```
