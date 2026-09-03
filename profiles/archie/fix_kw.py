with open("/opt/hermes/profiles/archie/draft_article.md", "r") as f:
    text = f.read()

text = text.replace("Poor drayage coordination happens when shippers", "Poor last-mile drayage coordination happens when shippers")

with open("/opt/hermes/profiles/archie/draft_article.md", "w") as f:
    f.write(text)

print("Restored keyword.")
