import re

with open('/opt/hermes/profiles/archie/final_article.txt', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace("Title: Second Lives for Steel Boxes: Practical Uses for Recycled Containers", "Title: Second Lives for Steel Boxes: Uses for Recycled Containers")

with open('/opt/hermes/profiles/archie/final_article.txt', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated Title.")
