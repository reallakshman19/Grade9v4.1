import re

with open('nsejs/physics/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

links = re.findall(r'href=["\']([^"\']+)["\']', text)
rec_links = [l for l in links if 'recovery' in l]
print(f'Total recovery links in physics/index.html: {len(rec_links)}')
for l in rec_links:
    print(' ', l)
