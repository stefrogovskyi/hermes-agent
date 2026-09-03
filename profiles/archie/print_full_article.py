with open("/opt/hermes/profiles/archie/original_article.txt") as f:
    text = f.read()

# Let's clean out header/navigation/footer if any and extract main content
print("FULL LENGTH:", len(text))
print("--- FULL TEXT ---")
print(text)
