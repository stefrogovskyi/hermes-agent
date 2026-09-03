try:
    from ddgs import DDGS
    results = list(DDGS().text("freight rate management software trends", max_results=5))
    for r in results:
        print(r['title'], "-", r['body'])
except Exception as e:
    print("DDGS Error:", e)
