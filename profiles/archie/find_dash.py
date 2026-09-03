with open('/opt/hermes/profiles/archie/draft_article.md') as f:
    for i, line in enumerate(f, 1):
        if '—' in line or '--' in line or '–' in line:
            print(f"Line {i}: {line.strip()}")
