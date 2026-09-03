try:
    from duckduckgo_search import DDGS
    results = list(DDGS().text('b2b logistics social media marketing strategies freight', max_results=5))
    for r in results:
        print(r['title'], ':', r['body'])
except Exception as e:
    print('Error:', e)
