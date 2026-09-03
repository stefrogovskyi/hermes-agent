try:
    from duckduckgo_search import DDGS
    results = list(DDGS().text("Transport Logistic Munich 2025 green supply chain", max_results=3))
    for r in results:
        print(r.get('title'), ':', r.get('body'))
except Exception as e:
    print("Error:", e)
