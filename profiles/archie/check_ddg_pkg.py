try:
    from duckduckgo_search import DDGS
    results = list(DDGS().text("freight rate management software 2025 2026", max_results=5))
    for r in results:
        print(r['title'], "-", r['body'])
except Exception as e:
    print("DDGS Error:", e)
