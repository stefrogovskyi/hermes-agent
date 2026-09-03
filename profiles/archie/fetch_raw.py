import urllib.request

url = 'https://www.searates.com/blog/post/searates-updates-week-47-2024'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8')

print("HTML length:", len(html))
print(html[:2000])

with open("/opt/hermes/profiles/archie/raw_page.html", "w") as f:
    f.write(html)
