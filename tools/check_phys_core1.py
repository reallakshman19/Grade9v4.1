import re

with open('nsejs/physics/core1/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

links = re.findall(r'href=["\']([^"\']+)["\']', text)
rec_links = [l for l in links if 'recovery' in l]
print(f'Total recovery links in physics/core1/index.html: {len(rec_links)}')
for l in rec_links:
    print(' ', l)

all_lessons = [l for l in links if 'index.html' in l and l != '../../index.html' and l != '../../../index.html' and l != 'index.html']
print(f'Total lesson links in physics/core1/index.html: {len(all_lessons)}')
for l in all_lessons:
    print(' ', l)
