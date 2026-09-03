with open('/opt/hermes/profiles/archie/clean_original_article.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Trim after "By investing in these tools, you’ll not only protect your assets but also create a safer and more efficient environment for everyone involved in the supply chain."
end_pos = text.find('By investing in these tools')
if end_pos != -1:
    end_of_para = text.find('\n', end_pos)
    if end_of_para != -1:
        text = text[:end_of_para].strip()

with open('/opt/hermes/profiles/archie/clean_original_article.txt', 'w', encoding='utf-8') as f:
    f.write(text)

print(f"Final clean original length: {len(text)} chars.")
