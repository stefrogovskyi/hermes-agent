try:
    from duckduckgo_search import DDGS
    results = list(DDGS().text("international logistics supply chain technology trends", max_results=5))
    for r in results:
        print(r['title'], "::", r['body'])
except Exception as e:
    print("DDGS Error:", e)
