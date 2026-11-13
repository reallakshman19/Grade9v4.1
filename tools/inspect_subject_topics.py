import re

with open('nsejs/biology/index.html', 'r', encoding='utf-8') as f:
    bio = f.read()

print("Biology Topic Cards:")
for m in re.finditer(r'<article class="topic-card-tab" id="([^"]+)">[\s\S]*?<h2>([^<]+)</h2>', bio):
    print(f"  ID: {m.group(1)} | Title: {m.group(2)}")

with open('nsejs/chemistry/index.html', 'r', encoding='utf-8') as f:
    chem = f.read()

print("\nChemistry Topic Cards:")
for m in re.finditer(r'<article class="topic-card-tab" id="([^"]+)">[\s\S]*?<h2>([^<]+)</h2>', chem):
    print(f"  ID: {m.group(1)} | Title: {m.group(2)}")
