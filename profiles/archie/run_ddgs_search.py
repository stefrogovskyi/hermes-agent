from duckduckgo_search import DDGS

ddgs = DDGS()

queries = [
    "container tracking API multi carrier logistics 2025",
    "distance and time freight calculator sea air transport",
    "digital freight alliance DFA membership freight forwarding"
]

keywords = []

for q in queries:
    print(f"=== QUERY: {q} ===")
    results = list(ddgs.text(q, max_results=3))
    for r in results:
        print("Title:", r.get('title'))
        print("Snippet:", r.get('body'))
        print()
