import json

d1 = json.load(open('nsejs/data/independent-core1-recovery.v1.json', encoding='utf-8'))
items = d1.get('items', [])
for c in items:
    subj = c.get('subject')
    title = c.get('title')
    slug = c.get('slug')
    route = c.get('publication_route')
    print(f"{subj:<10} | {slug:<35} | {route}")
